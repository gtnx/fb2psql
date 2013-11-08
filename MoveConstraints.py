# -*- coding: utf-8 -*-

from Connect import *

class MoveConstraints:
    
    def run(self):
        conFB, curFB, dataCharsetFB = openFB()
        conPSQL, curPSQL = openPSQL()
        try:
            # получаем список FK
            sql = """
                    SELECT
                        CAST(
                            'ALTER TABLE ' || TRIM(RC1.RDB$RELATION_NAME) || ' ADD CONSTRAINT ' || TRIM(RC1.RDB$CONSTRAINT_NAME)
                            || ' ' || RC1.RDB$CONSTRAINT_TYPE || ' (' || TRIM(I1.RDB$FIELD_NAME) || ') REFERENCES '
                            || TRIM(RC2.RDB$RELATION_NAME) || ' (' || TRIM(I2.RDB$FIELD_NAME) || ')'
                            || ';'
                            AS VARCHAR(1000))
                    FROM
                        RDB$RELATION_CONSTRAINTS RC1,
                        RDB$RELATION_CONSTRAINTS RC2, 
                        RDB$REF_CONSTRAINTS RF,
                        RDB$INDEX_SEGMENTS I1,
                        RDB$INDEX_SEGMENTS I2,
                        RDB$RELATION_FIELDS F
                    WHERE
                        RC1.RDB$CONSTRAINT_TYPE = 'FOREIGN KEY' and
                        RC2.RDB$CONSTRAINT_TYPE = 'PRIMARY KEY' and
                        RC1.RDB$CONSTRAINT_NAME = RF.RDB$CONSTRAINT_NAME and
                        RC2.RDB$CONSTRAINT_NAME = RF.RDB$CONST_NAME_UQ and
                        RC1.RDB$INDEX_NAME = I1.RDB$INDEX_NAME and
                        RC2.RDB$INDEX_NAME = I2.RDB$INDEX_NAME and
                        F.RDB$RELATION_NAME = RC1.RDB$RELATION_NAME and
                        F.RDB$FIELD_NAME = I1.RDB$FIELD_NAME
                    ORDER BY
                        RC1.RDB$RELATION_NAME, F.RDB$FIELD_POSITION
                    """ 
            curFB.execute(sql)
            rows = curFB.fetchall()
            print "count FK: ",  len(rows)
            for row in rows:  
                try:
                    curPSQL.execute(row[0])
                except:
                    print  u"FK= " + row[0]  + u" is Exists"
            conPSQL.commit()
            
            # получаем список UNIQUE
            sql = """
                    SELECT
                        RC1.RDB$RELATION_NAME as table_name,
                        RC1.RDB$CONSTRAINT_NAME as unique_name,
                        LIST(TRIM(I1.RDB$FIELD_NAME)) as fields
                    FROM
                        RDB$RELATION_CONSTRAINTS RC1,
                        RDB$INDEX_SEGMENTS I1,
                        RDB$RELATION_FIELDS F
                    WHERE
                        RC1.RDB$CONSTRAINT_TYPE = 'UNIQUE' and
                        F.RDB$RELATION_NAME = RC1.RDB$RELATION_NAME and
                        RC1.RDB$INDEX_NAME = I1.RDB$INDEX_NAME and
                        F.RDB$FIELD_NAME = I1.RDB$FIELD_NAME
                    GROUP BY
                        RC1.RDB$RELATION_NAME,
                        RC1.RDB$CONSTRAINT_NAME
                    """ 
            curFB.execute(sql)
            rows = curFB.fetchall()
            print "count UNIQUE: ",  len(rows)
            for row in rows:  
                try:
                    create = u"ALTER TABLE " + row[0].strip() + u" ADD CONSTRAINT " + row[1].strip() + u" UNIQUE (" +  row[2] + u");"
                    curPSQL.execute(create)
                except:
                    print  u"UNIQUE= " + row[0]  + u" is Exists"
            conPSQL.commit()
        finally:
            curFB.close()
            curPSQL.close()
            conFB.close()
            conPSQL.close()


