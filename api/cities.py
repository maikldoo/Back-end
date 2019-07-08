from nuga.sql import SqlQuery, SqlQueryRow, SqlQueryInsert, SqlQueryUpdate, SqlQueryScalar, SqlQueryDelete

class Cities():
    conn = None
    def __init__(self, conn):
        self.conn = conn

    def IsExists(self, city_id):
        return SqlQueryScalar(self.conn, 'select exists(select * from cities where id=%s)', city_id)

    def Create(self, **data):
        name = data.get("name")
        if not name:
            raise Warning("Введите имя город")
            
        return SqlQueryInsert(self.conn, """ 
            insert into cities (name)
            values( %s )
        """, name)

    def Delete(self, city_id):
        if not city_id:
            raise Warning("Не передан идентификатор")
            
        return SqlQueryDelete(self.conn, 'delete from cities where id = %s', city_id)

    def Read(self, city_id):
        if not city_id:
            raise Warning("Не передан идентификатор")
            
        return SqlQueryRow(self.conn, 'select * from cities where id = %s', city_id)

    def List(self):
        return SqlQuery(self.conn, 'select * from cities')

    def Update(self, city_id, **data):
        if not data.get("name"):
            raise Warning("Введите имя город")
            
        if not city_id:
            raise Warning("Не передан идентификатор")
            
        return SqlQueryUpdate(self.conn, 'cities', ['name'], city_id, data)