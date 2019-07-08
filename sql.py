import nuga.config as config
import pymysql.cursors

class DB:
    connect = None
    def Connect(self, host=config.host, user=config.user, password=config.password, db=config.db):
        self.connect = pymysql.connect(
            host=host,
            user=user,
            password=password, 
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return self.connect
    
    def CloseConnect(self):
        if self.connect:
            self.connect.commit()
            self.connect.close()
            self.connect = None
    
    
def SqlQuery(conn, query, *data):
    cursor = conn.cursor()
    cursor.execute(query, data)
    res = cursor.fetchall()
    cursor.close()
    return res

def SqlQueryInsert(conn, query, *data):
    cursor = conn.cursor()
    cursor.execute(query, data)
    res = cursor.lastrowid
    cursor.close()
    conn.commit()
    return res
    
def SqlQueryRow(conn, query, *data):
    result = SqlQuery(conn, query, *data)
    return result[0] if result else None 
    
def SqlQueryScalar(conn, query, *data):
    result = SqlQueryRow(conn, query, *data)
    if result:
        result = list(result.values())
        if result:
            result = result[0]
    return result
    
def SqlQueryDelete(conn, query, *data):
    result = SqlQuery(conn, query, *data)
    conn.commit()
    return result
    
def SqlQueryUpdate(conn, table_name, columns, id, data, id_name='id'):
    for key in list(data):
        if key not in columns:
            del data[key]
    query = """ update {} set """.format(table_name)
    sql_set = []
    params = []
    for pair in data.items():
        sql_set.append("{}= %s".format(pair[0]))
        params.append(pair[1])
    query += ', '.join(sql_set)
    query += """ where {} = %s """.format(id_name)
    params.append(id)
    res = SqlQuery(conn, query, *params)    
    conn.commit()
    return res
    