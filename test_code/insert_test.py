import datetime
from model.dbsecurity.dbconn import DbConnection

instance_dbconn = DbConnection(database="petfeeder_db")

sql = (
    'INSERT INTO petfeeder_db.tbldrinklog (millilitres_left, timestamp, dog_id) '
    'VALUES ( %(millilitres_left)s, %(timestamp)s,  %(dog_id)s );'
)
params = {
    'millilitres_left': 3550,
    'timestamp': datetime.datetime.now(),
    'dog_id': 1,
}

result = instance_dbconn.execute(sql, params)