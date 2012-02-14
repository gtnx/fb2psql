#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# psycopg2 - для соединения с postgresql
# kinterbasdb - для соединения с firebird
# apt-get install python-kinterbasdb
# apt-get install python-psycopg2
#
import FieldProperty
import TableProperty
import MoveData
import MoveGenerators
import MoveTriggers

from Connect import *


conFB, curFB = openFB()
conPSQL, curPSQL = openPSQL()

try:
     # получаем структуру таблиц
     curFB.execute("""
     select 
            R.RDB$RELATION_NAME AS "TABLENAME", 
            F.RDB$FIELD_TYPE AS "TYPE", 
            F.RDB$CHARACTER_LENGTH AS "LENGTH",
            F.RDB$FIELD_SCALE AS "SCALE", 
            F.RDB$FIELD_SUB_TYPE AS "SUB_TYPE",
            F.RDB$FIELD_PRECISION AS "PRECISION", 
            R.RDB$FIELD_NAME AS "NAME",
            R.RDB$DEFAULT_SOURCE AS "DEFAULT_VALUE",
            R.RDB$NULL_FLAG                    
     from 
              RDB$FIELDS F, 
              RDB$RELATION_FIELDS R 
     where 
                 F.RDB$FIELD_NAME = R.RDB$FIELD_SOURCE 
                 and R.RDB$SYSTEM_FLAG = 0 
     order by 
                 R.RDB$RELATION_NAME, 
                 R.RDB$FIELD_POSITION
     """)
     rows = curFB.fetchall()
     relationName = None 
     table = TableProperty.TableProperty()
     print u"all fields count: ", len(rows)
     count = 0
     for row in rows:              
         if relationName is not None  and relationName != unicode(row[0].strip()):             
             createTable(table,  relationName,  curFB,  curPSQL)
             conPSQL.commit()             
             MoveData.MoveData(table).run()              
             table = TableProperty.TableProperty()
             del table.fields[:]
             del table.fieldsProp[:]
             del table.primaryKey[:]
             
         relationName = unicode(row[0].strip())
         fp = FieldProperty.FieldProperty()
         fp.type = row[1]
         fp.length = row[2]
         fp.scale = row[3]
         fp.subType = row[4]
         fp.precision = row[5]
         fp.name = row[6].strip()
         fp.defaultValue = row[7]
         fp.nullFlag = row[8]
         table.fields.append(unicode(fp))
         table.fieldsProp.append(fp)
         count += 1
         if count % 1000 == 0:
             print "using ", count, "fields, remain: " , (len(rows) - count)
         
     createTable(table,  relationName,  curFB,  curPSQL)    
     conPSQL.commit()
     MoveData.MoveData(table).run()
     MoveTriggers.MoveTriggers().run()
finally:
  curFB.close()
  curPSQL.close()
  conFB.close()
  conPSQL.close()
# переносим имеющиеся генераторы
MoveGenerators.MoveGenerators().run()

