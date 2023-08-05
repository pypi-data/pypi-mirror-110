import sys
import psycopg2
from psycopg2 import sql
from psycopg2._psycopg import cursor


class DataTypes:
    VARCHAR_TYPES = [
        'text',
        'character varying',
        'character'
    ]

    NUMERIC_TYPES = [
        'smallint',
        'integer',
        'bigint',
        'decimal',
        'numeric',
        'real',
        'double precision'
    ]

    DATE_TYPES = [
        'date',
        'timestamp',
        'timestamp without time zone'
    ]

    BOOLEAN_TYPES = [
        'boolean',
        'bool'
    ]

    GEOMETRY_TYPES = [
        'point',
        'circle',
        'lseg',
        'polygon',
        'box',
        'line',
        'path'
    ]

    BINARY_TYPES = [
        'bytea'
    ]

    SUPPORTED_TYPES = VARCHAR_TYPES + NUMERIC_TYPES + \
        DATE_TYPES + BOOLEAN_TYPES + GEOMETRY_TYPES + BINARY_TYPES


def get_db_cursor(DB_NAME: str, user: str, hostname: str, port: str, password: str):

    try:
        connection = psycopg2.connect(dbname=DB_NAME,
                                      user=user,
                                      host=hostname,
                                      port=port,
                                      password=password)
    except psycopg2.DatabaseError as error:
        sys.exit('Could not connect to the "{0}" database. Error description: {1}'.format(
            DB_NAME, error))

    cursor = connection.cursor()
    return connection, cursor


def delete_constraint(constraints_to_delete, cursor_target: cursor, connection_target):

    for constraint_name, table_name in constraints_to_delete.items():
        query = sql.SQL("ALTER TABLE {table} DROP CONSTRAINT {constraint_name}").format(
            table=sql.Identifier(table_name),
            constraint_name=sql.Identifier(constraint_name))
        try:
            cursor_target.execute(query)
            connection_target.commit()
        except psycopg2.DatabaseError as error:
            sys.exit('Could not delete constraint.')


def create_database(connection, cursor: cursor, db_name: str, owner_name: str):
    print(f'Creating the "{db_name}" database...')

    cursor.execute(
        f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()

    if not exists:
        try:
            if owner_name is not None:
                cursor.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(db_name),
                    sql.Identifier(owner_name)))
            else:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(db_name)))

            connection.commit()
        except psycopg2.DatabaseError as error:
            sys.exit('Database "{0}" could not be created. Error: {1}'.format(
                db_name, error))
    else:
        sys.exit(
            f'The database you tried to create "{db_name}" already exists. Please specify a new database name.')


def analyze_database(cursor: cursor, db_name: str) -> None:
    try:
        print('Retrieving statistics from the "{0}" database.'.format(db_name))
        cursor.execute("VACUUM ANALYZE;")
    except psycopg2.DatabaseError as error:
        sys.exit('Database "{0}" could not be analyzed. Error: {1}'.format(
            db_name, error))


def show_database_stats(cursor: cursor, tables_arg: str):
    tables = get_tables(cursor)

    tables_list = None
    if tables_arg:
        tables_list = tables_arg.split(",")
        tables_list = [table.strip(' ') for table in tables_list]

    for table_info in tables:
        table_name = table_info[1]

        if tables_list:
            if table_name not in tables_list:
                continue
        sub_result = get_table_stats(cursor, table_name)

        print(f'\n -- {table_name} -- \n')
        print(sub_result)


def get_tables(cursor: cursor):
    try:
        cursor.execute("""
        SELECT 
            nspname AS schemaname,relname as tablename, reltuples::bigint as rowcount,rank() over(order by reltuples desc)
        FROM pg_class C
        LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
        WHERE 
            nspname NOT IN ('pg_catalog', 'information_schema') AND
            relkind='r' 
        ORDER BY tablename;""")

        return cursor.fetchall()
    except psycopg2.DatabaseError as error:
        sys.exit(
            'Could not retrieve the database\'s table information. Error description: {0}'.format(error))


def get_table_stats(cursor: cursor, table_name: str):
    try:
        cursor.execute(f"""
           select 
            attname, null_frac, avg_width, n_distinct, 
            most_common_vals, most_common_freqs, histogram_bounds, 
            correlation 
           from pg_stats 
          where schemaname not in ('pg_catalog') 
            and tablename = '{table_name}'
            and inherited = false;""")

        return cursor.fetchall()
    except psycopg2.DatabaseError as error:
        sys.exit('Could not get statistics for the "{0}" table. Error description: {1}'.format(
            table_name, error))


def get_column_information(cursor: cursor, table_name: str):
    try:
        cursor.execute(f"""
            SELECT 
                column_name, data_type, character_maximum_length,
                column_default,
                numeric_precision, numeric_precision_radix, numeric_scale
            FROM   information_schema.columns
            WHERE  table_name = '{table_name}'
            ORDER  BY ordinal_position;
            """)

        return cursor.fetchall()
    except psycopg2.DatabaseError as error:
        sys.exit('Could not get columns for the "{0}" table. Error description: {1}'.format(
            table_name, error))


def get_constr_information(cursor: cursor):
    try:
        cursor.execute(f"""
                    SELECT kcu.column_name AS foreign_column,
                            tc.table_name AS foreign_table,   
                            ccu.column_name "referenced primary_column",
                            ccu.table_name AS "referenced primary_table",
                            tc.constraint_type,
                            kcu.constraint_name		
                      FROM information_schema.table_constraints AS tc 
                      JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                       AND tc.table_schema = kcu.table_schema
                      JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                       AND ccu.table_schema = tc.table_schema;""")

        return cursor.fetchall()
    except psycopg2.DatabaseError as error:
        sys.exit('Could not constraint information')
