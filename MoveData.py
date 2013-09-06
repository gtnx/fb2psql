# -*- coding: utf-8 -*-

from Connect import *
#from django.utils.encoding import smart_str, smart_unicode
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
                        elif self.table.fieldsProp[i].charset != 0:
                           #print unicode(row[i]).encode('ascii', 'ignore')
                           rowArray.append(row[i])
                        elif self.table.fieldsProp[i].type == 7 and self.table.fieldsProp[i].name in ["GROUPVIEWMODE", "TYPEFORMVIEW", "VIEWMODE", "SUBDICTIONARYVIEWMODE", "OBJECTTYPE", "STRINGSUBTYPE", "MULTILINK", "CACHEPOSITION", "ORDERDIR"]:
                           rowArray.append(row[i])

                        elif self.table.fieldsProp[i].type == 7 or (self.table.fieldsProp[i].type == 8 and self.table.fieldsProp[i].name in ["ISGROUPBY"]):
                           if str(row[i]) == "1":
                              rowArray.append("true")
                           else:
                              rowArray.append("false")   
                        else:
                           #print row[i]
                           rowArray.append(row[i])
                        insert += u", %s"
                        
                     # выполняем запрос
                     insert += u")"
                     curPSQL.execute(insert, rowArray)
                conPSQL.commit()
            except psycopg2.IntegrityError :
                 pass
            #except:
            #     print "error"
            finally:
              curFB.close()
              curPSQL.close()
              conFB.close()
              conPSQL.close()
        else:
            print u"Нет данных для: " + table.name

        
