# -*- coding: utf-8 -*-

import FBError
# свойства полей
class FieldProperty :
    
    type = -1
    length = None
    scale = 0
    subType = 0
    precision = None
    name = ''
    defaultValue = None
    nullFlag = 0
    uniq = None
    
    def getType(self):
         if self.type == 7:
             return u"smallint"
         elif self.type == 261 and self.subType == 1:
             return u"text"
         elif self.type == 261 and (self.subType == 0 or self.subType == 2):
             return u"bytea"
         elif self.type == 14:
             return u"char (" + unicode(self.length) + u")"
         elif self.type == 37 :
             return u"varchar (" + unicode(self.length) + u")"
         elif self.type == 12 :
             return u"date"
         elif self.type == 16 and self.subType == 2:
              return u"decimal (" + unicode(self.precision) + u"," + unicode(-1*self.scale)  + u")"
         elif self.type == 27:
              return u"double precision"
         elif self.type == 10:
              return u"real"
         elif self.type == 16 and self.subType == 0:
              return u"bigint"
         elif self.type == 8:
              return u"integer"
         elif self.type == 16 and self.subType  == 1:
              return u"numeric (" + unicode(self.precision) + u"," + unicode(-1*self.scale)  + u")"
         elif self.type == 13:
              return u"time"
         elif self.type == 35:
              return u"timestamp"
         raise FBError('type is unknown: ' + self.type)
    
    def __str__(self):
        notNull = u"" 
        if self.nullFlag is not None and self.nullFlag == 1:
            notNull = u" NOT NULL "
        defaultValue = u""
        if self.defaultValue is not None :
            defaultValue = unicode(self.defaultValue)
        return (" ".join([unicode(self.name), self.getType(), defaultValue, notNull])).strip()
