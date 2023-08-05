import os
import subprocess
import sys
from subprocess import Popen
from typing import List, Optional, Any
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2._psycopg import cursor
from psycopg2 import sql
from src import postgres
from src import model_generator
from src import utils
import argparse
from argparse import Namespace

__version__ = '2.0'
examples: Optional[str] = '''How to use pgsynthdata.py:

  python pgsynthdata.py test postgres -show
  \t-> Connects to database "test", host="localhost", port="5432", default user with password "postgres"
  \t-> Shows statistics from the tables in database "test"
  
  python pgsynthdata.py db pw1234 -H myHost -p 8070 -U testuser -show
  \t-> Connects to database "db", host="myHost", port="8070", user="testuser" with password "pw1234"
  \t-> Shows statistics from the tables in database "db"
  
  python pgsynthdata.py dbin dbgen pw1234 -H myHost -p 8070 -U testuser -generate
  \t-> Connects to database "dbin", host="myHost", port="8070", user="testuser" with password "pw1234"
  \t-> Creates new database "dbgen" with synthetic data
  
  python pgsynthdata.py dbin dbgen pw1234 -H myHost -p 8070 -U testuser -generate -tables table1,table2
  \t-> Connects to database "dbin", host="myHost", port="8070", user="testuser" with password "pw1234"
  \t-> Creates new database "dbgen" with synthetic data on tables: "table1" and "table2"
  
  python pgsynthdata.py --version
  \t-> Show the version of this program and quit'''

DUMP_FILE_PATH = 'schema.dump'


def main() -> None:
    args = parse_arguments()

    if args.show:
        show(args)
    else:
        if args.DB_NAME_GEN is None:
            sys.exit(
                'When "-generate" argument is given, the following argument is required: DB_NAME_GEN')
        else:
            connection = None
            try:

                connection = psycopg2.connect(dbname=args.DB_NAME_IN,
                                              user=args.user,
                                              host=args.hostname,
                                              port=args.port,
                                              password=args.password)

                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = connection.cursor()
                postgres.analyze_database(cursor, args.DB_NAME_IN)

                generate(connection, cursor, args)
            except psycopg2.DatabaseError:
                sys.exit('''Connection failed because of at least one of the following reasons:
                        Database does not exist
                        User does not exist
                        Wrong password''')
            finally:
                if connection is not None:
                    connection.close()


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(description='Connects to a database and reads statistics',
                                     epilog=examples,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--version', action='version',
                        version=f'pgsynthdata version: {__version__}')
    parser.add_argument('DB_NAME_IN', type=str,
                        help='Name of an existing postgres database')
    parser.add_argument('DB_NAME_GEN', type=str, nargs='?',
                        help='Name of database to be created')  # optional, but not if DB_NAME_GEN is given
    parser.add_argument('password', type=str, help='Required user password')

    # One of the two options in action_group has to be given, but not both
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        '-show', '--show', action='store_true', help='If given, shows config')
    action_group.add_argument('-generate', '--generate', action='store_true',
                              help='If given, generates new synthesized data to database DB_NAMEG_EN')

    parser.add_argument('-mf', '--mf', type=float, default=1.0,
                        help='Multiplication factor (mf) for the generated synthesized data (default: 1.0)')
    parser.add_argument('-tables', '--tables', type=str,
                        help='Only generate data for specific tables, separated by a comma')

    parser.add_argument('-O', '--owner', type=str,
                        help='Owner of the database, default: same as user')
    parser.add_argument('-H', '--hostname', type=str,
                        help='Specifies the host name, default: localhost')
    parser.add_argument('-p', '--port', type=int,
                        help='Specifies the TCP/IP port, default: 5432')
    parser.add_argument('-U', '--user', type=str,
                        help='An existing postgres database user, default: default user')

    return parser.parse_args()


def show(args: Any) -> None:
    connection = None
    try:
        connection = psycopg2.connect(dbname=args.DB_NAME_IN,
                                      user=args.user,
                                      host=args.hostname,
                                      port=args.port,
                                      password=args.password)

        cursor = connection.cursor()

        postgres.show_database_stats(cursor, args.tables)
        cursor.close()

    except psycopg2.DatabaseError:
        sys.exit('''Connection failed because of at least one of the following reasons:
                    Database does not exist
                    User does not exist
                    Wrong password''')
    finally:
        if connection is not None:
            connection.close()


def generate(connection, cursor: cursor, args) -> None:

    print(
        f'Preparing the generation of synthetic data into the "{args.DB_NAME_GEN}" database...\n')

    # Build up new Database based on source database DB_NAME_IN
    postgres.create_database(connection, cursor, args.DB_NAME_GEN, args.owner)
    copy_database_structure(args)
    cursor.close()

    # Connect to source and target database
    connection_src, cursor_src = postgres.get_db_cursor(
        args.DB_NAME_IN, args.user, args.hostname, args.port, args.password)
    connection_target, cursor_target = postgres.get_db_cursor(
        args.DB_NAME_GEN, args.user, args.hostname, args.port, args.password)

    # Collect all constraints
    db_constraints = postgres.get_constr_information(cursor_src)

    # Collect all table names from source database
    table_results = postgres.get_tables(cursor_src)

    # Arrange tables based on constraints
    tables_to_sort = utils.determine_tables_to_generate(
        table_results, args.tables)

    constraints_to_consider = utils.check_constraints(tables_to_sort, db_constraints,
                                                      cursor_target, connection_target)

    tables_sorted = utils.sort_tables_topological(
        constraints_to_consider, tables_to_sort)

    insert_column_settings(cursor_target, connection_target, tables_sorted)

    for table_name in tables_sorted:
        # Generate data model and data based on input data
        insert_dict = model_generator.generate_model(cursor_src=cursor_src,
                                                     table_name=table_name,
                                                     tables_sorted=tables_sorted,
                                                     db_constraints=db_constraints,
                                                     mf=args.mf)

        # Insert table data into targe database DB_NAME_GEN
        insert_data(cursor_target, connection_target, insert_dict)

    cursor_src.close()
    cursor_target.close()
    sys.stdout.write(
        f'Successfully generated the synthetic data into the "{args.DB_NAME_GEN}" database.')


def copy_database_structure(args) -> None:
    print(f'Copying the "{args.DB_NAME_GEN}" database structure...\n')

    try:
        process = Popen(['pg_dump',
                         '--dbname=postgresql://{}:{}@{}:{}/{}'.format(args.user,
                                                                       args.password,
                                                                       'localhost',
                                                                       '5432',
                                                                       args.DB_NAME_IN),
                         '-s',
                         '-Fc',
                         '-f', DUMP_FILE_PATH
                         ],
                        stdout=subprocess.PIPE)

        process.communicate()[0]

        process = Popen(['pg_restore',
                         '--dbname=postgresql://{}:{}@{}:{}/{}'.format(args.user,
                                                                       args.password,
                                                                       'localhost',
                                                                       '5432',
                                                                       args.DB_NAME_GEN),
                         DUMP_FILE_PATH],
                        stdout=subprocess.PIPE
                        )

        process.communicate()[0]
    except Exception as error:
        sys.exit('Database structure could not be copied. Error: {}'.format(error))
    finally:
        if os.path.exists(DUMP_FILE_PATH):
            os.remove(DUMP_FILE_PATH)


def insert_data(cursor_target: cursor, connection_target, insert_dict) -> None:
    for table_name, insert_query in insert_dict.items():
        print(f'Inserting synthetic data into the "{table_name}" table...\n')
        try:
            if insert_query:
                cursor_target.execute(sql.SQL(insert_query).format(
                    table_name=sql.Identifier(table_name)))
                connection_target.commit()

        except psycopg2.DatabaseError as db_error:
            sys.stdout.write(
                f'An error occurred while inserting data into the "{table_name}" table.'
                f' Error description: {db_error}.\n')
            connection_target.rollback()


def insert_column_settings(cursor_target: cursor, connection_target, tables: List[any]) -> None:
    print(f'Gathering and inserting information_schema for sorted tables')
    string_list = '('
    counter = 0
    for table in tables:
        counter += 1
        string_list += '\''
        string_list += table
        string_list += '\''
        if counter != len(tables):
            string_list += ','
    string_list += ')'

    tab_var_setting = 'tab_var_setting'
    insert_query = f'select * into {tab_var_setting} from information_schema.columns where true and table_name in {string_list} order by ordinal_position'

    try:
        cursor_target.execute(sql.SQL(insert_query).format(
            table_name=sql.Identifier(tab_var_setting)))
        connection_target.commit()
    except psycopg2.DatabaseError as db_error:
        sys.stdout.write(
            f'An error occurred while inserting data into the "{tab_var_setting}" table.'
            f' Error description: {db_error}.\n')
        connection_target.rollback()


if __name__ == '__main__':
    main()
