# fb2sql

This project provide python tools to convert [firebird](http://www.firebirdsql.org/ "Firebird") databases to [postgresql](http://www.postgresql.org/ "PostGreSQL").

This was orginally a fork from https://code.google.com/p/fb2psql/ but the project has been completely modified since

*This is an alpha version and some conversion feature are not yet implemented. DO NOT USE IT IN PRODUCTION.*

## Quick install

   $> virtualenv env
   $> source env/bin/activate
   $> pip install -r requirements.txt
   $> python main.py --help
   $> python main.py


## Requirements

* fdb
* psycopg2

Use of kinterbasdb has been dropped since it's not on pypi global repository (seriously guys?) and fdb implements Python Database API 2.0 compliant support.

## Features

Supported features
* Copy table schema
* Copy table data
* Copy table index 

Unsupported features
* No handling of foreign keys
* No handling of triggers
* No handling of procedures 

## Contribution

Please feel free to contribute