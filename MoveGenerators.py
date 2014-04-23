# -*- coding: utf-8 -*-

from Connect import *

class MoveGenerators:
    
    def run(self):
        conFB, curFB = openFB()
        conPSQL, curPSQL = openPSQL()
        try:
            # получам спсок генератов
            sql = """
                        SELECT 
                             RDB$GENERATOR_NAME
                        FROM 
                             RDB$GENERATORS
                         WHERE 
                             RDB$SYSTEM_FLAG = 0
                    """ 
            curFB.execute(sql)
            rows = curFB.fetchall()
            print "count gen: ",  len(rows)
            for row in rows:
                # получаем значение генератора
                curFB.execute("""SELECT GEN_ID( %(renName)s, 1 ) FROM RDB$DATABASE;""" % {"renName":unicode(row[0])})
                value = curFB.fetchone()[0]
                # формируем запрос
                if value > 0:
                    create = u"CREATE SEQUENCE " + unicode(row[0]) + u" START " + unicode(value)
                else :
                    create = u"CREATE SEQUENCE " + unicode(row[0]) 
                curPSQL.execute(create)
            conPSQL.commit()
        finally:
            curFB.close()
            curPSQL.close()
            conFB.close()
            conPSQL.close()


