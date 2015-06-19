# How to use to fb2psql #

## Depends ##
python version 2.6 and more.

Modules python connect to firebird and postgresql:
[python-kinterbasdb](http://kinterbasdb.sourceforge.net/) and [python-psycopg2](http://initd.org/psycopg/)

For debian/ubuntu install:
```
apt-get install python
apt-get install python-kinterbasdb
apt-get install python-psycopg2
```

## Install ##
downloads last version from [downloads](http://code.google.com/p/fb2psql/downloads/list).

extract archive:
```
   tar -xzf fb2psql.<current version>.tar.gz 
```

or download source code.
Get the source code on your local drive using [mercurial](http://mercurial.selenic.com/).

```
   hg clone https://code.google.com/p/fb2psql/ 
```


## Setting and run ##
In file 'config.cfg' specify the connection settings.

To make an executable file main.py and run it
```
  chmod +x main.py
  ./main.py > run.log
```
or run as
```
  python main.py > run.log
```

It is better to redirect the output to a file (recomend).

After completion of the file 'noCreateTriggers.sql' contains no triggers created.