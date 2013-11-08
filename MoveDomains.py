# -*- coding: utf-8 -*-

from Connect import *

class MoveDomains:
    
    def run(self):
        conFB, curFB, dataCharsetFB = openFB()
        conPSQL, curPSQL = openPSQL()
        try:
            # получам список доменов
            sql = """
                    SELECT
                        CAST(
                          'CREATE DOMAIN '||TRIM(RDB$FIELD_NAME)||' as '||
                            CASE RDB$FIELD_TYPE
                                WHEN 7 THEN 'SMALLINT'
                                WHEN 8 THEN 'INTEGER'
                                WHEN 12 THEN 'DATE'
                                WHEN 13 THEN 'TIME'
                                WHEN 14 THEN 'CHAR('||rdb$field_length||')'
                                WHEN 16 THEN
                                  iif(rdb$field_sub_type = 0,'BIGINT', 'NUMERIC('||RDB$FIELD_PRECISION||','||(-1*rdb$field_scale)||')')
                                WHEN 35 THEN 'TIMESTAMP'
                                WHEN 37 THEN 'VARCHAR('||rdb$field_length||')'
                                WHEN 261 THEN
                                    iif (rdb$field_sub_type in (0, 2), 'BYTEA', 'TEXT')
                                ELSE CAST(RDB$FIELD_TYPE AS VARCHAR(10))
                            END
                            ||TRIM(iif(RDB$NULL_FLAG = 1,' NOT NULL ',' ')
                              ||COALESCE(' '||RDB$DEFAULT_SOURCE,'')
                              ||COALESCE(' '||rdb$validation_SOURCE,''))
                            ||';'
                        AS VARCHAR(1000))
                    FROM RDB$FIELDS WHERE (NOT (RDB$FIELD_NAME starting WITH 'RDB$')) AND RDB$SYSTEM_FLAG = 0
                    ORDER BY RDB$FIELD_NAME
                    """ 
            curFB.execute(sql)
            rows = curFB.fetchall()
            print "count domen: ",  len(rows)
            for row in rows:  
                try:
                    curPSQL.execute(row[0])
                except:
                    print  u"domain= " + row[0]  + u" is Exists"
            conPSQL.commit()
        finally:
            curFB.close()
            curPSQL.close()
            conFB.close()
            conPSQL.close()


