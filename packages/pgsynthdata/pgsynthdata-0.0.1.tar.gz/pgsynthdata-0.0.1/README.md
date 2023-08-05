# Pure Synthetic Data Generation with a PostgreSQL and Python-based Tool

Description
------
A lightweight tool written in Python that teams up with PostgreSQL and it's *pg_stats* view in order to generate fully synthetic data that seem as realistic as possible.

It generates the synthetic data by reading the *pg_stats* view of PostgreSQL (*pg_statistic* catalog), more explicitly by reading the most common values, their frequencies in the dataset, 
the average width of the column values, the number of distinct values etc. The algorithm combines all these values and properties in order to generate fully synthetic data
that contain no actual values or fragments of the "real" data at all, but are very similar in the context of the "shape" and the properties of them.

Constrains
------
**Types** 

There are some rules on the supported datatypes. 
1) To genereate data which do not have any external constraints all the postgres types are supported
2) Data with primary key constraints can only be of numeric, text or date type (and its subtypes and variations)
3) Data with foreign key constraints can only be of numeric, text or date type (and its subtypes and variations)

Data Import
------
**Prerequisite:**

Make sure the  database *tennis_atp_2020* is present on your Postgres instance such that the import.bat does not throw any errors: 

  ```
  psql -U postgres
  postgres=# CREATE DATABASE tennis_atp_2020; 
  ``` 

**Importing Test dataset for the tool:**
The "Tennis_ATP" test dataset can be found inside *resources/* and can be set-up very easily using the *import.bat* file (if on Windows) or by importing the *.csv* files directly into Postgres (which should be pretty straight-forward).


Installation
------
* Clone the repository into your desired directory.
* Inside the cloned directory: 
 ``` 
 pip install -r requirements.txt 
 ``` 
 to install all the required libraries/dependencies
* Run the tool using the terminal shell while having the PostgreSQL server up and running

Usage
------
Tool arguments:
*  **DBNAMEGEN** - Name of the database to be created
*  **-show/--show** - Shows database stats (default)
*  **-generate/--generate** - Generates new synthesized data to database DBNAMEGEN
*  **-mf/--mf** - Multiplication factor for the generated synthetic data (default: 1.0)
*  **-tables/--tables** - Name(s) of table(s) to be filled, separated with ',', ignoring other tables (default: fill all tables)
*  **-O/--owner** - Owner of new database (default: same as user)
*  **-v/--version** - Show version information, then quit
*  **-h/--help** - Show tool help, then quit


Connection options:
*  **DBNAMEIN** - Name of the existing database to connect to
*  **-H/--hostname** - Name of the PostgreSQL server (default: localhost)
*  **-P/--port** - Port of the PostgreSQL server (default: 5432)
*  **-U/--user** - PostgreSQL server username


Some usage examples:
*  **python pgsynthdata.py test postgres -show**
   * Connects to database *test*, host=*localhost*, port=*5432*, default user with
password *postgres*
   * Shows statistics of the database *test*
* **python pgsynthdata.py dbin dbgen pw1234 -H myHost -p 8070 -U testuser -generate**
  * Connects to database *dbin*, host=*myHost*, port=*8070*, user=*testuser* with
password *pw1234*
  * Create new database *dbgen* and generates synthetic data into it
* **python pgsynthdata.py dbin dbgencreate pw123 -U myUser -generate -tables myTable1, myTable2**
  * Connects to database *dbin*, host=*localhost*, port=*5432*, user=*myUser* with
password *pw123*
  * Creates new database *dbgencreate* with synthetic data on tables: *table1* and *table2*
* **python pgsynthdata.py --help**
  * Show the help information of the tool

Contributions
------

Contributions are welcomed, please check the [issues](https://gitlab.com/kevinost/pgsynthdata/-/issues) list for future ideas.

Author
------
Documentation & Adjustments made by [Etienne Baumgartner](https://gitlab.com/EPB1996)

Tool is written by [Kevin Ammann](https://gitlab.com/kevinost) based on preliminary work by [Labian Gashi](https://gitlab.com/labiangashi).


Feedback is welcome.
