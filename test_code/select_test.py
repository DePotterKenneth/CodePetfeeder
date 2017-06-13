import datetime
from model.dbsecurity.dbconn import DbConnection

instance_dbconn = DbConnection(database="petfeeder_db")

sql = 'SELECT millilitres_left, timestamp, dog_id FROM tbldrinklog where drink_id > %(size_id)s;'
params = {
    'size_id': 0,
}
result = instance_dbconn.query(sql, params, True)

print(result)