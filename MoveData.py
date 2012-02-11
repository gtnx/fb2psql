# -*- coding: utf-8 -*-

from Util import *
import exceptions

class MoveData:
    table = None
    #TableProperty
    def __init__(self,  table):    
        self.table = table
    
    def run(self):
        if len(self.table.fieldsProp) > 0:
            conFB, curFB = openFB()
            conPSQL, curPSQL = openPSQL()
            try:
                 # получам данные
                map = {"tableName":self.table.name}
                sql = "SELECT * FROM %(tableName)s" % map
                curFB.execute(sql)
                rows = curFB.fetchall()
                print u"count row: ",  len(rows)
                for row in rows:
                     # формируем запрос
                     insert = u"INSERT INTO " + self.table.name +  u" VALUES (%s"
                     count = len(self.table.fieldsProp)
                     rowArray = [row[0]] 
                     for i in range(1,  count):                       
                        if self.table.fieldsProp[i].type == 261 and self.table.fieldsProp[i].subType == 0 and row[i] is not None:
                           rowArray.append(psycopg2.Binary(row[i]))
                           #print u"error then copy row: " + unicode(row[0]) + u", table: " + self.table.name
                        else:
                           rowArray.append(row[i])
                        insert += u", %s"
                        
                     # выполняем запрос
                     insert += u")"
                     curPSQL.execute(insert, rowArray)
                conPSQL.commit()
            except psycopg2.IntegrityError :
                 pass
            finally:
              curFB.close()
              curPSQL.close()
              conFB.close()
              conPSQL.close()
        else:
            print u"Нет данных для: " + table.name

        
