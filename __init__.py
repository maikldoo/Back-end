from flask import Flask, jsonify, request, render_template, redirect, session, Response, send_file
from nuga.sql import DB 
from nuga.api.members import Members
from nuga.api.cities import Cities
from nuga.api.salons import Salons
from nuga.api.auth import Auth
import nuga.excel

app = Flask(__name__, template_folder="view", static_folder='static')

@app.route('/index3')
def main():
    conn = DB().Connect()
    c = Cities(conn).List()
    s = Salons(conn).List()
    return render_template('index.html', cities = c, salons = s, landing=True)   
    
@app.route('/manager/members/')
@app.route('/manager/')
def manager():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    members = Members(conn).List()
    salons = Salons(conn).List()
    cities = Cities(conn).List()
    return render_template('/admin/members.html', members=members, currentPage = "members", cities=cities, salons=salons)  
    

@app.route('/manager/members/create/')
def members_create():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    salons = Salons(conn).List()
    cities = Cities(conn).List()
    return render_template('/admin/members_create.html', currentPage = "members", cities=cities, salons=salons)  
    

@app.route('/manager/members/update/')
def members_update():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    id = request.args.get('id')
    if not id:
        return redirect("/manager/members/", code=302)
    member = Members(conn).Read(id)
    salons = Salons(conn).List()
    cities = Cities(conn).List()
    return render_template('/admin/members_create.html', currentPage = "members", cities=cities, salons=salons, member=member)    

    
@app.route('/manager/cities/')
def manager_cities():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    cities = Cities(conn).List()
    return render_template('/admin/cities.html', cities=cities, currentPage = "cities")  

@app.route('/manager/cities/create/')
def cities_create():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    
    return render_template('/admin/cities_update.html', currentPage = "cities")
 
@app.route('/manager/cities/update/')
def cities_update():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    id = request.args.get('id')
    if not id:
        return redirect("/manager/cities/", code=302)
    city = Cities(conn).Read(id)
    
    if not city:
        return redirect("/manager/cities/", code=302)
    return render_template('/admin/cities_update.html', currentPage = "cities", city=city)  
    
@app.route('/manager/salons/')
def manager_salons():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    salons = Salons(conn).List()
    cities = Cities(conn).List()
    return render_template('/admin/salons.html', salons=salons, cities=cities, currentPage = "salons")    
 
@app.route('/manager/salons/create/')
def salons_create():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    cities = Cities(conn).List()    
    return render_template('/admin/salons_update.html', currentPage = "salons", cities=cities)
 
@app.route('/manager/salons/update/')
def salons_update():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    id = request.args.get('id')
    if not id:
        return redirect("/manager/salons/", code=302)
    salon = Salons(conn).Read(id)
    
    if not salon:
        return redirect("/manager/salons/", code=302)
    cities = Cities(conn).List()    
    return render_template('/admin/salons_update.html', currentPage = "salons", salon=salon, cities=cities)
 
@app.route('/create')
def create():
    conn = DB().Connect()
    if not Auth(conn).IsAuth():
        return redirect("/auth/", code=302)
    members = Members(conn).List()
    path = excel.create(members)
    
    return send_file("../" + path, as_attachment=True)
    
@app.route('/auth/')
def auth(): 
    return render_template('/admin/login.html')  
    
@app.route('/api/', methods=['POST'])
def api_post():
    try:
        if not request.is_json:
            raise Warning("no")
        body = request.get_json()
        conn = DB().Connect()
        method = body["method"]
        params = body["params"]
        result = None
        
        if method == "auth.login":
            login = params.get("login")
            password = params.get("password")
            return Auth(conn).Login(login, password)
            
        elif method == "auth.exit":
            return Auth(conn).Exit()
            
        elif method == "auth.createuser":
             Auth(conn).CreateUser(params.get("login"), params.get("password"))
        elif method == "members.create":
            result = Members(conn).Create(**params)
        else:
            if not Auth(conn).IsAuth():
                return jsonify(error = "not auth"), 401
               
            if method == "members.delete":
                result = Members(conn).Delete(params.get("id"))
            elif method == "members.import":
                members = Members(conn).List()
                path = excel.create(members)
                return send_file("../" + path, as_attachment=True)
            elif method == "members.update":
                result = Members(conn).Update(params.get("id"), **params)
                
            elif method == "cities.create":
                result = Cities(conn).Create(**params) 
            elif method == "cities.delete":
                result = Cities(conn).Delete(params.get("id"))
            elif method == "cities.update":
                result = Cities(conn).Update(params.get("id"), **params)
            
            elif method == "salons.create":
                result = Salons(conn).Create(**params) 
            elif method == "salons.delete":
                result = Salons(conn).Delete(params.get("id"))
            elif method == "salons.update":
                result = Salons(conn).Update(params.get("id"), **params)
         
        return jsonify(result = result)
    except Exception as ex:
        return jsonify(error = str(ex)), 500
    
if __name__ == '__main__':
    app.run(debug=False)