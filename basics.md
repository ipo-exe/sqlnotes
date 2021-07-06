#SQL basics
by Ipo
by Ipo
Here are some notes to use PostgreSQL both from `psql` and `pgAdmin4`.

A great ref: https://www.postgresqltutorial.com/


## Databases

### Create a new database
Syntax:
```
CREATE DATABASE database_name

-- optional clauses:
WITH
   [OWNER =  role_name]
   [TEMPLATE = template]
   [ENCODING = encoding]
   [LC_COLLATE = collate]
   [LC_CTYPE = ctype]
   [TABLESPACE = tablespace_name]
   [ALLOW_CONNECTIONS = true | false]
   [CONNECTION LIMIT = max_concurrent_connection]
   [IS_TEMPLATE = true | false ]
;
```
### Rename a database
First, disconnect from the database that you want to rename and connect to another database e.g., `postgres`.
Next, terminate all the connections to the database that you want to rename by using the following statement:
```
SELECT pg_terminate_backend (pid)
FROM pg_stat_activity
WHERE datname = 'database_name'
;
```
After that, rename the database using the `ALTER DATABASE RENAME TO` statement as follows:
```
ALTER DATABASE database_name RENAME TO new_database_name
;
```
### Delete an existing database
Terminate the active connections by issuing the following query:
```
SELECT pg_terminate_backend (pid)
FROM pg_stat_activity
WHERE datname = 'database_name'
;
```
Then use the `DROP` statement:
```
DROP DATABASE [IF EXISTS] database_name
;
```

## Schemas
There are some scenarios that you want to use schemas:
* Schemas allow you to organize database objects e.g., tables into logical groups to make them more manageable.
* Schemas enable multiple users to use one database without interfering with each other.

### Create new schema
Syntax:
```
CREATE SCHEMA [IF NOT EXISTS] schema_name
;
```
### Rename schema
Syntax:
```
ALTER SCHEMA schema_name 
RENAME TO new_name
;
```
### Remove schema (and all contents)
Syntax:
```
DROP SCHEMA [IF EXISTS] schema_name1 [,schema_name2,...] 
[CASCADE | RESTRICT]  -- Cascate in case of schema usages elsewhere in the DB
;
```

## Tables

### Creating a table
General syntax to create a table:


```
CREATE TABLE [IF NOT EXISTS] table_name ( -- use the `if not exists` clause to prevent error)
   column1 datatype(length) column_contraint,
   column2 datatype(length) column_contraint,
   column3 datatype(length) column_contraint,
   table_constraints
);
```

There are many datatypes and possible constrains. Check on PostgreSQL docs: https://www.postgresql.org/docs/9.5/datatype.html. 

A good example:
```
CREATE TABLE user_accounts (

    "user_id" SERIAL PRIMARY KEY,  -- automated serial number and primary key of table
    
    "user_name" VARCHAR(100) UNIQUE NOT NULL, -- varying characters w/ max of 100. unique values and not null constrains
    
    "user_cpf" CHAR(11) UNIQUE NOT NULL, -- fixed 11 characters 
    
    "user_descrip" TEXT, -- characters of variable unlimited length
    
    "user_birthdate" DATE, -- date in 'YYYY-MM-DD' format
    
    "user_n_houses" SMALLINT, 
    
    "user_height" REAL, --  6 decimal digits precision
    
    "user_total_bank" NUMERIC(10, 2), -- 10 digits w/ 2 decimal digits precision   
    
    "entry_tstamp" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP -- time stamp type auto populated by default 
);
```
### Inserting new records
Insert manually a single new record into the table with the following syntax:
```
INSERT INTO table_name(column1, column2, …)
VALUES (value1, value2, … 
;
```
In our example:
```
INSERT INTO user_accounts("user_name", "user_cpf")
VALUES ('Fulano de Tal', '83733533000')
;
```
### Updating records
To edit existing records (i.e., updating the record) use the following syntax:
```
UPDATE table_name
SET 
    column1 = value1,
    column2 = value2,
    ...
WHERE condition
;
```
In our example:
```
UPDATE user_accounts
SET 
    "user_descrip" = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vestibulum, lectus ac ultrices dignissim, ex leo sollicitudin risus, nec mattis metus ipsum sed diam. Sed nec dolor nisi.',
    "user_total_bank" = 10000.0
WHERE user_name = 'Fulano de Tal'
;
```

### Removing a record

The syntax:
```
DELETE FROM table_name
WHERE condition
RETURNING (select_list | *) -- optional clause to return the removed rows
;
```
Example:
```
DELETE FROM user_accounts
WHERE 
    user_id = 7 OR
    user_name = 'Fulano de Tal2'
RETURNING *
;
```


### Adding new column to table

The syntax:
```
ALTER TABLE table_name
    ADD COLUMN column_name1 data_type constraint,
    ADD COLUMN column_name2 data_type constraint,
    ...
    ADD COLUMN column_namen data_type constraint
;
```
Example:
```
ALTER TABLE user_accounts
    ADD COLUMN "user_email" VARCHAR(100),
    ADD COLUMN "user_address" VARCHAR(100)
;
```

### Edit all column values

The syntax is the same of record editing, but without the `WHERE` clause.
Example:
```
UPDATE user_accounts
SET 
    "user_n_houses" = 1
;
```

### Removing a column

The syntax:
```
ALTER TABLE table_name 
    DROP COLUMN [IF EXISTS] column_name [CASCADE]; -- use the `cascade` clause if the column is used elsewhere in the database
;
```
Example:
```
ALTER TABLE user_accounts
    DROP COLUMN "user_address" CASCADE
;
```

### Conditional editing with `CASE` statement

The `CASE` statement has the following syntax:
```
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    . . . 
    WHEN conditionN THEN resultN
    ELSE result
END
;
```
Example of embedding the `CASE` statement in `SET` expression:

```
UPDATE user_accounts
SET 
    "user_n_houses" = 
        CASE
            WHEN "user_id" < 4 THEN 0
            WHEN "user_id" >= 4 AND "user_id" < 6 THEN 1
            ELSE 2
        END 
;
```

### Move table to another schema

Syntax:
```
ALTER TABLE table_name
    SET SCHEMA another_schema
;
```


### Import data from a CSV file
Files may be in `.csv` or `.txt` extension.
The syntax:
```
COPY table_name("column1", "column2", ... , "columnn") -- or just `table_name` to load all fields
    FROM 'C:\bin\data.txt'  -- string filepath 
    DELIMITER ';'  -- specify delimiter
    CSV -- format 
    HEADER -- contains headers
;
```
The example data (copy and paste to a `.txt` file):
```
user name;user email;data;cpf
user A;usera@a.com;2000-01-02;44061890635
user B;userb@b.com;2000-01-03;60301570331
user C;userc@c.com;2000-01-04;59449305705
user D;userd@d.com;2000-01-05;55157126904
```

The example code:
```
COPY user_accounts("user_name", "user_email", "user_birthdate", "user_cpf")
    FROM 'C:\bin\data.txt'  -- string filepath
    DELIMITER ';'  -- specify delimiter
    CSV -- format 
    HEADER -- contains headers
;
```

### Export table to a CSV file
Files may be in `.csv` or `.txt` extension.
The syntax:
```
COPY table_name("column1", "column2", ... , "columnn") -- or just `table_name` to export all fields
    TO 'C:\bin\output.txt'  -- string filepath 
    DELIMITER ';' -- specify delimiter
    CSV -- specify format
    HEADER -- include headers
;
```
In the example:
```
COPY user_accounts("user_name", "user_email", "user_cpf")
    TO 'C:\bin\output.txt'  -- string filepath 
    DELIMITER ';' -- specify delimiter
    CSV -- specify format
    HEADER -- include headers to file
;
```

##Queries and Views

###Query data with the`SELECT` statement
Basic syntax of a `SELECT` statement:
```
SELECT * | column1, column2, ... columnN -- * means ALL
    FROM table_name 
    [WHERE] condition_expression
    [ORDER BY] column_name ASC | DESC
    [LIMIT] n -- subset of n rows
;
```
Example:
```
SELECT "user_id", "user_name", "user_email"
    FROM user_accounts
    ORDER BY "user_name" ASC
;
```

###Save a query in a View
Syntax of view creation:
```
CREATE VIEW view_name AS query
;
```
Example:
```
CREATE VIEW user_emails AS 
    SELECT "user_id", "user_name", "user_email"
        FROM user_accounts
        ORDER BY "user_name" ASC
;
```
###Rename view
Syntax:
```
ALTER VIEW old_name RENAME TO new_name
;
```
###Export query or view to CSV file
Just like in tables, use the `COPY` statement to export the output dataframe to file.
Syntax:
```
COPY query_expression | view_name | view_name("column1", ...)
    TO 'C:\bin\output.txt'  -- string filepath 
    DELIMITER ';' -- specify delimiter
    CSV -- specify format
    HEADER -- include headers to file
;
```

##Data aggregation
A special clause in the `SELECT` statement is the `GROUP BY` for data aggregation.
Syntax:
```
SELECT 
   column_1, 
   column_2,
   ...,
   aggregate_function(column_3) -- call and agg function on a column
FROM 
   table_name
GROUP BY 
   column_1, -- incremental priority of aggregation
   column_2,
   ...
;
```
Some standard agg functions available:
* AVG() – return the average value.
* COUNT() – return the number of values.
* MAX() – return the maximum value. 
* MIN() – return the minimum value. 
* SUM() – return the sum of all or distinct values.

## Joining data
Great ref: https://www.postgresqltutorial.com/postgresql-joins/

Dataframes, such as tables, views and on-the-fly queries can be joined **side-by-side** in four ways:
* `INNER JOIN`, which is the intersection of both dataframes, only matching rows;
* `LEFT JOIN`, which keeps all rows from the left dataframe;
* `RIGHT JOIN`, which keeps all rows from the right dataframe, and;
* `FULL JOIN`, which keeps all rows from both dataframes.

Apllying the `WHERE` clause to the joins leads to variations. 

Syntax:
```
SELECT
    table_a.column1,
    table_a.key,
    table_b.column1,
    table_b.key
FROM
    table_a -- left dataframe
INNER JOIN | LEFT JOIN | RIGHT JOIN | FULL JOIN
    table_b  -- right dataframe
    ON 
    table_a.key = table_b.key;
[WHERE] -- optional conditioning
    table_a.key IS NULL | table_b.key IS NULL | table_a.key IS NULL OR table_b.key IS NULL
;
```



## Automating SQL commands with `python`
Good reference to use python to automate postgreSQL database commands:

https://www.dataquest.io/blog/loading-data-into-postgres/

Typical python script to control a postgreSQL database:
```python
import getpass  # to get the password from the prompt
import psycopg2  # library to control postgreSQL

# ask for the password:
p = getpass.getpass('>> Password:')
# database connection:
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password={}".format(p))
# instanciate a cursor:
cur = conn.cursor()
# define the sql command in a string:
s = """UPDATE user_accounts 
        SET 
        "user_descrip" = 'Lorem ipsum dolor',
        "user_total_bank" = 777.0
        WHERE "user_name" = 'Fulano de Tal' 
    ;"""
# execute SQL command
cur.execute(s)
# commit the changes:
conn.commit()
```







