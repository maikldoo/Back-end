from nuga.sql import SqlQuery, SqlQueryRow, SqlQueryInsert, SqlQueryUpdate, SqlQueryScalar, SqlQueryDelete
from nuga.api.cities import Cities

class Salons():
    conn = None
    def __init__(self, conn):
        self.conn = conn

    def IsExists(self, salon_id):
        return SqlQueryScalar(self.conn, 'select exists(select 1 from salons where id=%s)', salon_id)

    def IsExistsCode(self, code):
        return SqlQueryScalar(self.conn, 'select exists(select 1 from salons where code=%s)', code)

    def Create(self, **data):
        if not data.get("city_id") or not Cities(self.conn).IsExists(data["city_id"]):
            raise Warning("Выберете существующий город")
        if not data.get("code"):
            raise Warning("Введите код зада")
        if not data.get("name"):
            raise Warning("Введите имя зада")

        if self.IsExistsCode(data.get("code")):
            raise Warning("Такой код зала уже существует!")

        return SqlQueryInsert(self.conn, """ 
            insert into salons (name, city_id, code)
            values( %s, %s, %s)
        """, data.get("name"), data.get("city_id"), data.get("code"))

    def Delete(self, salon_id):
        if not salon_id:
            raise Warning("Не передан идентификатор")
            
        return SqlQueryDelete(self.conn, 'delete from salons where id = %s', salon_id)

    def Read(self, salon_id):
        if not salon_id:
            raise Warning("Не передан идентификатор")
            
        query = self._listQuery()
        return SqlQueryRow(self.conn, query + ' where salons.id = %s', salon_id)

    def List(self):
        query = self._listQuery()
        return SqlQuery(self.conn, query)

    def Update(self, salon_id, **data):
        if not salon_id:
            raise Warning("Не передан идентификатор")
            
        if "city_id" in data and (not data.get("city_id") or not Cities(self.conn).IsExists(data.get("city_id"))):
            raise Warning("Выберете существующий город")
        if "code" in data and not data.get("code"):
            raise Warning("Введите код зада")
        if "name" in data and not data.get("name"):
            raise Warning("Введите имя зада")
            
        return SqlQueryUpdate(self.conn, 'salons', ['name', 'city_id', 'code'], salon_id, data)

    def _listQuery(self):
        return """
            select 
                salons.id, 
                salons.name, 
                salons.city_id,
                salons.code,
                cities.name as city_name
            from 
                salons 
            left join 
                cities on cities.id = salons.city_id
        """