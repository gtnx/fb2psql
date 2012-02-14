# -*- coding: utf-8 -*-

from Connect import *
import re

class MoveTriggers:
    
    def run(self):
        conFB, curFB = openFB()
        conPSQL, curPSQL = openPSQL()
        try:
            # получам спсок генератов
            sql = """
                        SELECT 
                            RDB$TRIGGER_NAME AS "Trigger name",
                            CASE RDB$TRIGGER_TYPE
                                WHEN   1 THEN 'BEFORE INSERT'
                                WHEN   2 THEN 'AFTER INSERT'
                                WHEN   3 THEN 'BEFORE UPDATE'
                                WHEN   4 THEN 'AFTER UPDATE'
                                WHEN   5 THEN 'BEFORE DELETE'
                                WHEN   6 THEN 'AFTER DELETE'
                                WHEN  17 THEN 'BEFORE INSERT OR UPDATE'
                                WHEN  18 THEN 'AFTER INSERT OR UPDATE'
                                WHEN  25 THEN 'BEFORE INSERT OR DELETE'
                                WHEN  26 THEN 'AFTER INSERT OR DELETE'
                                WHEN  27 THEN 'BEFORE UPDATE OR DELETE'
                                WHEN  28 THEN 'AFTER UPDATE OR DELETE'
                                WHEN 113 THEN 'BEFORE INSERT OR UPDATE OR DELETE'
                                WHEN 114 THEN 'AFTER INSERT OR UPDATE OR DELETE'
                             END AS "Trigger type",
                             RDB$RELATION_NAME AS "Table name",
                             RDB$TRIGGER_SOURCE AS "Source"
                        FROM 
                             RDB$TRIGGERS
                         WHERE 
                             RDB$SYSTEM_FLAG = 0
                    """ 
            curFB.execute(sql)
            rows = curFB.fetchall()
            print "count triggers: ",  len(rows)
            p = re.compile(r"""gen_id\(([\w_\d]*)\s*,\s*1\s*\)""",  re.I|re.U)
            p1 = re.compile(r"""gen_id\(([\w_\d]*)\s*,\s*0\s*\)""",  re.I|re.U)
            isCreated = False            
            badtriggers = []
            for row in rows:
                triggerCode = unicode(row[3]).strip()
                triggerCode = triggerCode[3: len(triggerCode)]
                # заменяем gen_id(gen_name, 1) на nextval('gen_name')
                m = p.search(triggerCode)
                if m:
                    genId = m.group(1)
                    triggerCode = p.sub(u"nextval('" + genId + u"')",  triggerCode)
                # заменяем gen_id(gen_name, 0) на curval('gen_name')
                m1 = p1.search(triggerCode)
                if m1:
                    genId = m1.group(1)
                    triggerCode = p1.sub(u"curlval('" + genId + u"')",  triggerCode)
                # создаем скрипты создания тригера    
                createFunction = u"CREATE FUNCTION " + unicode(row[0]).strip() + u"() RETURNS trigger AS $$ " + triggerCode + u" $$ LANGUAGE plpgsql;"
                create = u"CREATE TRIGGER " + unicode(row[0]).strip() + u" " + unicode(row[1]).strip() + u" ON " + unicode(row[2]).strip() + u" EXECUTE PROCEDURE " + unicode(row[0]).strip() + u"();"
                try :
                    print createFunction
                    curPSQL.execute(createFunction)
                    print create
                    curPSQL.execute(create)
                    isCreated = True
                except :
                    badtriggers.append("-- create function: \n")
                    badtriggers.append(createFunction)
                    badtriggers.append("\n-- create trigger: \n")
                    badtriggers.append(create)
                    print "Can not create trigger"
            if isCreated:
                conPSQL.commit()
            
            # запишем в файл, те функции которые не удалось создать
            filename = "noCreateTriggers.txt"
            FILE = open(filename,"w")
            try :
                FILE.writelines(badtriggers)
            finally:
                FILE.close()

        finally:
            curFB.close()
            curPSQL.close()
            conFB.close()
            conPSQL.close()


