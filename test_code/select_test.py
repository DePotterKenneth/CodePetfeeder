import datetime
from model.dbsecurity.dbconn import DbConnection

instance_dbconn = DbConnection(database="petfeeder_db")

sql = 'SELECT millilitres_left, timestamp, dog_id FROM tbldrinklog where drink_id > %(size_id)s;'
params = {
    'size_id': 0,
}
result = instance_dbconn.query(sql, params, True)

print(result)

sql2 = 'SELECT led_alarm_enabeld, sound_alarm_enabled, email_alarm_enabled, sms_alarm_enabled, food_alarm_enabled, drink_alarm_enabled, provision_alarm_enabled, food_alarm_threshold, drink_alarm_threshold, provision_alarm_threshold, alarm_interval, email, phone_number FROM tblsettings;'

result2 = instance_dbconn.query(sql2, dictionary = True)

print(result2[0])