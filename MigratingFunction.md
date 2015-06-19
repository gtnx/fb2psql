Can not be migrating function from database firebird to database postgresql because function syntax not compatible.
Some features can be converted ( example `gen_id(<gen_name>, 1)` or `gen_id(<gen_name>, 0)` ), and some do not (example 'if')
Due to the fact that not all functions migrate, some triggers can not be converted.

In current version gen\_id converted to nextval,
Example:

Firebird:
```
AS
BEGIN
  IF (NEW.ID IS NULL) THEN
    NEW.ID = GEN_ID(GEN_NAME,1);
END
```

Convert to postgresql:

```
CREATE FUNCTION TABLE_BI() RETURNS trigger AS $$ 
BEGIN
  IF (NEW.ID IS NULL) THEN
    NEW.ID = nextval('GEN_NAME');
END 
$$ LANGUAGE plpgsql;
```

Correct pastgresql:
```
CREATE FUNCTION TABLE_BI() RETURNS trigger AS $$ 
BEGIN
  IF (NEW.ID IS NULL) THEN
    NEW.ID = nextval('GEN_NAME');
  END IF;
END 
$$ LANGUAGE plpgsql;
```
