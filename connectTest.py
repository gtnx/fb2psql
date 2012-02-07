#!/usr/bin/python
#
# psycopg2 - для соединения с postgresql
# kinterbasdb - для соединения с firebird
# apt-get install python-kinterbasdb
# apt-get install python-psycopg2
#
import psycopg2
import kinterbasdb
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

# return cursor
def openPSQL(config):
  
  prop = {}
  for key, value in config.items('psql'):
    prop[key] = value
  connectionString = 'dbname=%(dbname)s user=%(user)s host=%(host)s password=%(password)s' % prop
  conPSQL = psycopg2.connect(connectionString);
  return conPSQL, conPSQL.cursor()

def openFB(config):
  conFB = kinterbasdb.connect(dsn=config.get('fb', 'host')+':'+config.get('fb', 'dbname'), \
                user=config.get('fb','user'), \
                password=config.get('fb', 'password'), \
                charset=config.get('fb', 'charset'), \
                dialect=config.getint('fb', 'dialect'))
  return conFB, conFB.cursor()


conFB, curFB = openFB(config)
conPSQL, curPSQL = openPSQL(config)

try:
  curFB.execute("""
  select R.RDB$RELATION_NAME, R.RDB$FIELD_POSITION, R.RDB$FIELD_NAME, 
  F.RDB$FIELD_LENGTH, F.RDB$FIELD_TYPE, F.RDB$FIELD_SCALE, F.RDB$FIELD_SUB_TYPE 
  from RDB$FIELDS F, RDB$RELATION_FIELDS R 
  where F.RDB$FIELD_NAME = R.RDB$FIELD_SOURCE and R.RDB$SYSTEM_FLAG = 0 
  order by R.RDB$RELATION_NAME, R.RDB$FIELD_POSITION
  """)
  rows = curFB.fetchall()
  curPSQL.execute(""" drop table if exists fieldsInFB""")
  curPSQL.execute("""
          create table fieldsInFB(
                 name varchar(250), 
                 field_position int, 
				 field_name varchar(250), 
				 field_lingth int, 
				 field_type int, 
				 field_scale int, 
				 field_sub_type int
		  )""")
  for row in rows:     
     map = {}
     num = 1
     for value in row:
        if num == 1 or num == 3:
           map['k' + str(num)] = str(value).strip()
        else:
           map['k' + str(num)] = value
        num += 1
     insert= "INSERT INTO fieldsInFB VALUES ('%(k1)s', %(k2)d, '%(k3)s', %(k4)d, %(k5)d, %(k6)d, %(k7)d )" % map
     
     curPSQL.execute(insert)
  conPSQL.commit()
finally:
  curFB.close()
  curPSQL.close()
  conFB.close()
  conPSQL.close()

