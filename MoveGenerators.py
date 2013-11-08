# -*- coding: utf-8 -*-

from Connect import *

class MoveGenerators:
    
    def run(self):
        conFB, curFB, dataCharsetFB = openFB()
        conPSQL, curPSQL = openPSQL()
        try:
            # получам спсок генератов
            sql = """
                        SELECT 
                             RDB$GENERATOR_NAME
                        FROM 
                             RDB$GENERATORS
                         WHERE 
                             RDB$SYSTEM_FLAG = 0 and RDB$GENERATOR_NAME not like 'IBE$%'
                    """ 
            curFB.execute(sql)
            rows = curFB.fetchall()
            print "count gen: ",  len(rows)
            for row in rows:
                genName = unicode(row[0].strip())
                # получаем значение генератора
                curFB.execute("""SELECT GEN_ID( %(renName)s, 0 ) FROM RDB$DATABASE;""" % {"renName":genName})
                value = curFB.fetchone()[0]
                # формируем запрос
                if value > 0:
                    create = u"CREATE SEQUENCE " + genName + u" START " + unicode(value)
                else:
                    create = u"CREATE SEQUENCE " + genName
                print create
                try:
                    curPSQL.execute(create)
                except:
                    print  u"sequence= " + unicode(row[0])  + u" is Exists"
            conPSQL.commit()
        finally:
            curFB.close()
            curPSQL.close()
            conFB.close()
            conPSQL.close()


