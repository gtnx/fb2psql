# -*- coding: utf-8 -*-

#
# psycopg2 - для соединения с postgresql
# kinterbasdb - для соединения с firebird
# apt-get install python-kinterbasdb
# apt-get install python-psycopg2
#


import ConfigParser
import psycopg2
import kinterbasdb


# return cursor
def openPSQL():
  config = ConfigParser.ConfigParser()
  config.read('config.cfg')

  prop = {}
  for key, value in config.items('psql'):
    prop[key] = value
  connectionString = 'dbname=%(dbname)s user=%(user)s host=%(host)s password=%(password)s' % prop
  conPSQL = psycopg2.connect(connectionString);
  return conPSQL, conPSQL.cursor()

def openFB():
  config = ConfigParser.ConfigParser()
  config.read('config.cfg')

  conFB = kinterbasdb.connect(dsn=config.get('fb', 'host')+':'+config.get('fb', 'dbname'), \
                user=config.get('fb','user'), \
                password=config.get('fb', 'password'), \
                charset=config.get('fb', 'charset'), \
                dialect=config.getint('fb', 'dialect'))
  return conFB, conFB.cursor()

def createTable(table,  relationName,  curFB,  curPSQL):
     table.name = relationName
     # получить все индексы для таблици relationName
     sql = """
             select 
                        i_s.RDB$INDEX_NAME as "index name", 
                        i_s.RDB$FIELD_NAME as "field name",
                       rc.RDB$CONSTRAINT_TYPE as "type"
             from 
                     rdb$index_segments i_s 
                     join rdb$indices i 
                     on i.RDB$INDEX_NAME = i_s.RDB$INDEX_NAME
                     left join rdb$relation_constraints rc
                     on rc.RDB$INDEX_NAME = i.RDB$INDEX_NAME
                     and rc.RDB$RELATION_NAME = i.RDB$RELATION_NAME
             where 
                 i.RDB$RELATION_NAME = '%(tableName)s'
             order by 
                 i_s.RDB$INDEX_NAME, 
                 RDB$FIELD_POSITION
     """ % {"tableName":relationName}
     curFB.execute(sql)
     indexis = curFB.fetchall()
     # мап обычных индексов.
     # ключ - имя индекса, значение - массив полей
     newIndexis = {}
     # мап уникальных индексов.
     # ключ - имя индекса, значение - массив полей
     newUniqueIndexis = {}
     for index in indexis:
         key = unicode(index[0]).strip()
         value = unicode(index[1]).strip()
         if unicode(index[2]).strip()== u"UNIQUE":
             if key in newUniqueIndexis.keys():
                 newUniqueIndexis[key].append(value)
             else :
                 newUniqueIndexis[key] = [value]
         elif  unicode(index[2]).strip()== u"PRIMARY KEY":
             # PRIMARY KEY - создается в месте с таблицей
             table.primaryKey.append(value)
         else :
             if key in newIndexis.keys():
                 newIndexis[key].append(value)
             else :
                 newIndexis[key] = [value]
     try :
     #if True:
         # создаем таблицу
         print table
         curPSQL.execute(unicode(table))
         # добавляем индексы
         for  indexName in newIndexis:
             listField = newIndexis[indexName]
             sqlCreateIndex = u"CREATE INDEX " + indexName + u" ON " + relationName + u"(" + ",".join(listField)  + u")"
             print sqlCreateIndex
             curPSQL.execute(unicode(sqlCreateIndex))
         # добавляем уникальные индексы
         for  indexName in newUniqueIndexis:
             listField = newUniqueIndexis[indexName]
             sqlCreateIndex = u"CREATE UNIQUE INDEX " + indexName + u" ON " + relationName + u"(" + ",".join(listField)  + u")"
             print sqlCreateIndex
             curPSQL.execute(unicode(sqlCreateIndex))
     except  psycopg2.ProgrammingError:
         print  u"tableName= " + relationName  + u" is Exists"
