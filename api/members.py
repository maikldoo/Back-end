import nuga.sql as sql
from nuga.api.cities import Cities
from nuga.api.salons import Salons

class Members():
    conn = None
    def __init__(self, conn):
        self.conn = conn

    def IsExists(self, member_id):
        return sql.SqlQueryScalar(self.conn, 'select exists(select * from members where id=%s)', member_id)

    def IsExistsCoupon(self, coupon):
        return sql.SqlQueryScalar(self.conn, 'select exists(select * from members where coupon=%s)', coupon)

    def Create(self, **data):
        name = data.get("name")
        phone = data.get("phone")
        city_id = data.get("city_id")
        salon_id = data.get("salon_id")
        coupon = data.get("coupon")
        date = data.get("date")
        coupon_got = data.get("coupon_got")
        winner = data.get("winner") or False
        
        if not name:
            raise Warning("Введите имя")
        if not phone:
            raise Warning("Введите телефон")
        if not city_id or not Cities(self.conn).IsExists(city_id):
            raise Warning("Выберете город")
        if not salon_id or not Salons(self.conn).IsExists(salon_id):
            raise Warning("Выберете зал")
        if not coupon:
            raise Warning("Введите купон")
        if self.IsExistsCoupon(coupon):
            raise Warning("Купон уже зарегистрирован!")  
        if not date:
            raise Warning("Введите дату получения купона")
        if not coupon_got:
            raise Warning("Выберете за что полуен купон")
            
        return sql.SqlQueryInsert(self.conn, """ 
            insert into members (name, coupon, phone, city_id, salon_id, coupon_got, date, winner)
            values( %s, %s, %s, %s, %s, %s, %s, %s )
        """, name, coupon, phone, city_id, salon_id, coupon_got, date, winner)

    def Delete(self, member_id):
        return sql.SqlQueryDelete(self.conn, 'delete from members where id = %s', member_id)

    def Read(self, member_id):
        query = self._listQuery()
        return sql.SqlQueryRow(self.conn, query + 'where members.id = %s', member_id)

    def List(self):
        query = self._listQuery()
        return sql.SqlQuery(self.conn, query)

    def Update(self, member_id, **params):
        if not member_id:
            raise Warning("Не передан идентификатор")
            
        data = {}
        if params.get("name"):
            data["name"] = params.get("name")
        if params.get("coupon"):
            data["coupon"] = params.get("coupon")
        if params.get("city_id"):
            data["city_id"] = params.get("city_id")
        if params.get("salon_id"):
            data["salon_id"] = params.get("salon_id")
        if params.get("coupon_got"):
            data["coupon_got"] = params.get("coupon_got")
        if params.get("date"):
            data["date"] = params.get("date")
        if params.get("phone"):
            data["phone"] = params.get("phone")
        if "winner" in params:
            data["winner"] = params.get("winner")
            
        if data:
            return sql.SqlQueryUpdate(
                self.conn, 
                'members',
                ['name', 'phone', 'city_id', 'salon_id', 'code', 'winner', 'date', 'coupon', 'coupon_got'], 
                member_id, 
                data
            )

    def _listQuery(self):
        return """
            select 
                members.id, 
                members.name, 
                members.phone, 
                members.city_id, 
                members.coupon, 
                members.salon_id, 
                members.coupon_got, 
                members.winner, 
                members.date, 
                salons.code as salon_code,
                cities.name as city_name, 
                salons.name as salon_name
            from 
                members 
            left join 
                cities on cities.id = members.city_id 
            left join 
                salons on salons.id = members.salon_id 
        """