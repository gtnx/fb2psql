# -*- coding: utf-8 -*-

class TableProperty:
   fields = []
   fieldsProp = []
   # имена полей в primaryKey
   primaryKey = []
   name = u""
   def __str__(self):
         result = u""
         if len(self.fields) > 0:
             result = u"CREATE TABLE " + self.name + u" ("
             result += u", ".join(self.fields)
             if len(self.primaryKey) > 0:
                 result += u","
                 result += u"PRIMARY KEY( " + u",".join(self.primaryKey) + ")"
             result += ")"    
         return result
