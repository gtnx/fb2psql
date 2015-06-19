WARN: FOREIGN KEY no support (ticket: [Migration foreign key](http://code.google.com/p/fb2psql/issues/detail?id=10))!

List of index received sql-query:
```
select 
      i_s.RDB$INDEX_NAME as "index name", 
      i_s.RDB$FIELD_NAME as "field name",
      rc.RDB$CONSTRAINT_TYPE as "type"
from 
      rdb$index_segments i_s 
      join rdb$indices i 
      on i.RDB$INDEX_NAME = i_s.RDB$INDEX_NAME
      left join rdb$relation_constraints rc
      on rc.RDB$INDEX_NAME = i.RDB$INDEX_NAME
      and rc.RDB$RELATION_NAME = i.RDB$RELATION_NAME
where 
      i.RDB$RELATION_NAME = '%(tableName)s'
order by 
      i_s.RDB$INDEX_NAME, 
      RDB$FIELD_POSITION
```

type:
<li>UNIQUE  - for unique field<br>
<li>PRIMARY KEY - for primary key<br>
<li>Null - for others index<br>
<br>
The keys are organized into named.<br>
Example:<br>
<br>
<table><thead><th> index1 </th><th> FIELD1 </th><th> Null </th></thead><tbody>
<tr><td> index1 </td><td> FIELD2 </td><td> Null </td></tr>
<tr><td> pk_id  </td><td> ID     </td><td> PRIMARY KEY </td></tr>
<tr><td> uq_field </td><td> FIELD3 </td><td> UNIQUE </td></tr></tbody></table>

result:<br>
<li>primary key - id,<br>
<li>unique field - FIELD3<br>
<li>complex index, index1 - FIELD1, FIELD2