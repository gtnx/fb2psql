List of fields received sql-query:
```
select 
   R.RDB$RELATION_NAME AS "TABLENAME", 
   F.RDB$FIELD_TYPE AS "TYPE", 
   F.RDB$CHARACTER_LENGTH AS "LENGTH",
   F.RDB$FIELD_SCALE AS "SCALE", 
   F.RDB$FIELD_SUB_TYPE AS "SUB_TYPE",
   F.RDB$FIELD_PRECISION AS "PRECISION", 
   R.RDB$FIELD_NAME AS "NAME",
   R.RDB$DEFAULT_SOURCE AS "DEFAULT_VALUE",
   R.RDB$NULL_FLAG AS "NULL_FLAG"                   
from 
   RDB$FIELDS F, 
   RDB$RELATION_FIELDS R 
where 
   F.RDB$FIELD_NAME = R.RDB$FIELD_SOURCE 
   and R.RDB$SYSTEM_FLAG = 0 
order by 
   R.RDB$RELATION_NAME, 
   R.RDB$FIELD_POSITION
```

Analysis of results:

<li> TABLENAME - Table Name<br>
<li> NAME - Name field<br>
<li> DEFAULT_VALUE - source default (example: default 1)<br>
<li> NULL_FLAG - if 1 then field not null<br>
<br>
Check type:<br>
<table><thead><th> TYPE </th><th> LENGTH </th><th> SCALE </th><th> SUB_TYPE </th><th> PRECISION </th><th> Type in postgresql </th></thead><tbody>
<tr><td> 7    </td><td>        </td><td> 0     </td><td> 0        </td><td> 0         </td><td> smallint           </td></tr>
<tr><td> 261  </td><td>        </td><td> 0     </td><td> 1        </td><td>           </td><td> text               </td></tr>
<tr><td> 261  </td><td>        </td><td> 0     </td><td> 0        </td><td>           </td><td> bytea              </td></tr>
<tr><td> 14   </td><td> n      </td><td> 0     </td><td> 0        </td><td>           </td><td> char (n)           </td></tr>
<tr><td> 37   </td><td> n      </td><td> 0     </td><td> 0        </td><td>           </td><td> varchar (n)        </td></tr>
<tr><td> 12   </td><td>        </td><td> 0     </td><td>          </td><td>           </td><td> data               </td></tr>
<tr><td> 16   </td><td>        </td><td> s     </td><td> 2        </td><td> p         </td><td> decimal (p, -s)    </td></tr>
<tr><td> 27   </td><td>        </td><td> 0     </td><td>          </td><td>           </td><td> double precision   </td></tr>
<tr><td> 10   </td><td>        </td><td> 0     </td><td>          </td><td>           </td><td> float              </td></tr>
<tr><td> 16   </td><td>        </td><td> 0     </td><td> 0        </td><td> 0         </td><td> bigint             </td></tr>
<tr><td> 8    </td><td>        </td><td> 0     </td><td> 0        </td><td> 0         </td><td> integer            </td></tr>
<tr><td> 16   </td><td>        </td><td> s     </td><td> 1        </td><td> p         </td><td> numeric (p, -s)    </td></tr>
<tr><td> 13   </td><td>        </td><td> 0     </td><td>          </td><td>           </td><td> time               </td></tr>
<tr><td> 35   </td><td>        </td><td> 0     </td><td>          </td><td>           </td><td> timestamp          </td></tr>