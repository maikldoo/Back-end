from nuga import sql
from datetime import datetime, timedelta
from flask import jsonify, request
from passlib.utils.pbkdf2 import pbkdf2
import uuid

class SessionStorage():
    conn = None
    def __init__(self, conn):
        self.conn = conn
        
    def SetSid(self, user_id):
        user_hex = "0000000" + hex(user_id)[2:]
        sid = user_hex[-8:] + "-" + str(uuid.uuid4())
        
        sql.SqlQueryInsert(self.conn, """
            insert into session_storage (sid, user_id, create_date) 
            values (%s, %s, %s)
        """, sid, user_id, datetime.now())
        
        return sid

    def GetUserBySid(self, sid):
        return sql.SqlQueryScalar(self.conn, """
            select user_id from session_storage where sid = %s
        """, sid)
    def Delete(self, sid):
        sql.SqlQueryDelete(self.conn, """
            delete from session_storage where sid = %s
        """, sid)
    
class Auth: 
    password_salt = 'abcdefghijklmnopqrstuvwxyz'
    password_size_key = 64
    password_iterations = 1000
    
    conn = None
    def __init__(self, conn):
        self.conn = conn
    
    def Login(self, login, password):
        if not login or not password:
            raise Warning("Проверьте правильность ввода логина и пароля.")
            
        password = self.GetPasswordHash(password)
        user_id = sql.SqlQueryScalar(self.conn, """
            select id from users where login = %s and password = %s
        """, login, password)
        
        if not user_id:
            raise Warning("Проверьте правильность ввода логина и пароля.")
        
        sid = SessionStorage(self.conn).SetSid(user_id)
        response = jsonify( result = sid )
        
        expire_date = datetime.now() + timedelta(days=365)
        response.set_cookie('sid', sid, expires=expire_date, secure=True)
        
        return response
    
    def IsAuth(self):
        if not request.cookies.get("sid"):
            return False
        user_id = SessionStorage(self.conn).GetUserBySid(request.cookies.get("sid"))
        return True if user_id else False
        
    def Exit(self):
        response = jsonify( result = True )
        response.set_cookie('sid', '', expires=0)
        
        if request.cookies.get("sid"):
            SessionStorage(self.conn).Delete(request.cookies.get("sid"))
        return response
        
    def CreateUser(self, login, password):
        password = self.GetPasswordHash(password)
        sql.SqlQueryInsert(self.conn, 'insert into users (login, password) values (%s, %s)', login, password)
        
    def GetPasswordHash(self, password):
        password = password.strip().encode( 'utf-8' )
        salt = self.password_salt.strip().encode( 'utf-8' )
        hashBytes = pbkdf2( password, salt, self.password_iterations, self.password_size_key, prf='hmac-sha1')
        hash =  ''.join( '%02x' % item for item in hashBytes )
        return hash
        