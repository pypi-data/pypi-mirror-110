import datetime
import numpy
from src import data_generator
from src import postgres
from src import utils
from src import query_generator
from psycopg2._psycopg import cursor
from typing import List, Dict, Tuple, Any, Optional


DEFAULT_NUMBER_OF_ROWS = 100
RANDOM_WORD_LENGTH = 15

# TODO: eliminate global variables
table_information: Dict = {}
pk_values: Dict = {}
fk_ref_info: Dict = {}


def generate_model(cursor_src, table_name, tables_sorted, db_constraints, mf=None) -> Dict:

    # TODO: Create more functions!
    print(f'Generating synthetic data for the "{table_name}" table...')
    insert_query = ""

    # Determine number of rows in source table
    cursor_src.execute(f"SELECT COUNT(*) FROM {table_name};")
    number_of_rows = cursor_src.fetchone()[0]
    if number_of_rows is None:
        number_of_rows = DEFAULT_NUMBER_OF_ROWS

    # Consider multiplication factor
    total_rows = (int(number_of_rows * mf))

    # Fill dict with general and statistical table information
    collect_meta_data(cursor_src, table_name)

    # Get tables column names
    column_names = list()

    for column_name, column_info in table_information.get(table_name)["column_information"].items():
        """ The next line messes up the primary key insertion. It forces to diregard 
                the generated_vals and does an auto increment where it is specified as a 
                column_default. 

                This can subsequently lead to insertion errors on foreign keys since primary 
                keys might not be the same in generated database and the ones used to 
                generate foreign key values in the tool. 

            """
        # if not column_info.get("column_default"):
        column_names.append(column_name)

    if not column_names:
        print(f'No columns found to generate data into. ' f'Skipping the'
              f' table\'s "{table_name}" data generation...')

    # Retrieve column general information
    column_information: Dict = {}
    for column_info in table_information[table_name]["column_information"].values():
        column_name = column_info.get("column_name")
        data_type = column_info.get("data_type")
        numeric_precision = column_info.get("numeric_precision")
        numeric_precision_radix = column_info.get("numeric_precision_radix")
        numeric_scale = column_info.get("numeric_scale")
        column_information[column_name] = {}

        if data_type not in postgres.DataTypes.SUPPORTED_TYPES:
            data_type = 'not_supported'

        # Retrieve column statistical information
        if column_name in table_information[table_name]["pg_stats"]:
            column_stats: Dict = table_information[table_name]["pg_stats"][column_name]
            most_common_values = column_stats["most_common_vals"]
            most_common_freqs = column_stats["most_common_freqs"]
            avg_width = column_stats["avg_width"]
            n_distinct = column_stats["n_distinct"]
            histogram_bounds = column_stats["histogram_bounds"]

            # Determine_frequency
            generated_freqs, rows_to_gen = determine_frequency(number_of_rows,
                                                               total_rows,
                                                               most_common_values,
                                                               most_common_freqs,
                                                               n_distinct)

            # Determine_boundaries
            min_bound, max_bound, list_for_bound = determine_boundaries(cursor_src, table_name,
                                                                        column_name, data_type,
                                                                        most_common_values,
                                                                        histogram_bounds)

            # Determine whether column is constraint
            constraint = determine_constraint_info(
                table_name, column_name, tables_sorted, db_constraints)
            if constraint == "FOREIGN KEY":
                generated_vals = data_generator.generate_fk(data_type, rows_to_gen, table_name,
                                                            column_name, pk_values,
                                                            fk_ref_info, min_bound, max_bound, histogram_bounds)

            elif constraint == "PRIMARY KEY":
                generated_vals = data_generator.generate_pk(data_type, rows_to_gen, avg_width, table_name,
                                                            min_bound, max_bound, list_for_bound, histogram_bounds)

                pk_values[table_name][column_name] = generated_vals

            else:
                generated_vals = data_generator.generate_no_constraint(data_type, rows_to_gen, avg_width,
                                                                       table_name, numeric_precision,
                                                                       numeric_precision_radix, numeric_scale,
                                                                       min_bound, max_bound, list_for_bound, histogram_bounds)

            column_information[column_name]["generated_vals"] = generated_vals
            column_information[column_name]["generated_freqs"] = generated_freqs

    insert_dict: Dict = {}
    insert_dict = query_generator.create_insert_query(total_rows, insert_query, table_name, column_names,
                                                      table_information, column_information,
                                                      insert_dict)

    return insert_dict


def collect_meta_data(cursor_src, table_name: str) -> None:

    # Initialize dict per table
    table_information[table_name] = {}
    table_information[table_name]["column_information"] = {}
    table_information[table_name]["pg_stats"] = {}

    # Retrieve general column information and fill into dict
    fill_columns_dict(cursor_src, table_name)

    # Retrieve statistical column information and fill into dict
    fill_stats_dict(cursor_src, table_name)


def fill_columns_dict(cursor_src, table_name: str) -> None:

    column_results = postgres.get_column_information(cursor_src, table_name)

    for column_entry in column_results:
        columns_dict = dict()
        columns_dict["column_name"] = column_entry[0]
        columns_dict["data_type"] = column_entry[1]
        columns_dict["max_length"] = column_entry[2]
        if column_entry[3]:
            columns_dict["column_default"] = column_entry[3]
        if column_entry[4]:
            columns_dict["numeric_precision"] = column_entry[4]
        if column_entry[5]:
            columns_dict["numeric_precision_radix"] = column_entry[5]
        if column_entry[6]:
            columns_dict["numeric_scale"] = column_entry[6]

        table_information[table_name]["column_information"][column_entry[0]] = columns_dict


def fill_stats_dict(cursor_src, table_name: str) -> None:

    table_stats = postgres.get_table_stats(cursor_src, table_name)
    for stats_entry in table_stats:
        stats_dict = dict()
        stats_dict["column_name"] = stats_entry[0]
        stats_dict["null_frac"] = stats_entry[1]
        stats_dict["avg_width"] = stats_entry[2]
        stats_dict["n_distinct"] = stats_entry[3]

        most_common_values = stats_entry[4]
        if most_common_values is not None:
            most_common_values = most_common_values.strip("{}").split(",")
            most_common_values = [value.strip('"').replace(
                "'", "''") for value in most_common_values]
            most_common_values = [
                value for value in most_common_values if value.strip()]

        stats_dict["most_common_vals"] = most_common_values
        stats_dict["most_common_freqs"] = stats_entry[5]

        histogram_bounds = stats_entry[6]
        if histogram_bounds is not None:
            histogram_bounds = histogram_bounds.strip("{}").split(",")
            histogram_bounds = [bound.strip('"').replace(
                "'", "''") for bound in histogram_bounds]
            histogram_bounds = [
                bound for bound in histogram_bounds if bound.strip()]

        stats_dict["histogram_bounds"] = histogram_bounds
        stats_dict["correlation"] = stats_entry[7]
        table_information[table_name]["pg_stats"][stats_entry[0]] = stats_dict


def determine_frequency(number_of_rows: int, total_rows: int, most_common_values: List[str] = None,
                        most_common_freqs: List[float] = None, n_distinct: float = None) -> Tuple[float, int]:

    if most_common_values and most_common_freqs:

        if n_distinct > 0:
            distinct_no = n_distinct
        else:
            distinct_no = -n_distinct * number_of_rows
        distinct_no = round(distinct_no)
        leftover_freq = 1 - sum(most_common_freqs)
        generated_freqs = most_common_freqs

        # The dirichlet function that generates random floating numbers to fill
        # The left-over frequencies
        # Generated_freqs indicates the probability for a value to get picked
        generated_freqs += (numpy.random.dirichlet(numpy.ones(distinct_no - len(most_common_freqs)))
                            * leftover_freq).tolist()

        # Rows_to_gen has to be equal as distinct values
        rows_to_gen = len(generated_freqs)

    # No mcv means that no values seem to be more common than any others (all unique)
    else:
        # Rows_to_gen has to be equal as rows_to_gen since all unique
        generated_freqs = False
        rows_to_gen = total_rows

    return generated_freqs, rows_to_gen


def determine_boundaries(cursor_src: cursor, table_name: str, column_name: str, data_type: str,
                         most_common_values: Optional[List[any]] = None,
                         histogram_bounds: Optional[List[any]] = None) -> Tuple[Any, Any, Optional[List[any]]]:

    list_for_bound: Optional[List[any]
                             ] = most_common_values or histogram_bounds or None

    def numeric():
        if list_for_bound:
            if data_type in ('decimal', 'numeric'):
                min_value = float(min(list_for_bound))
                max_value = float(max(list_for_bound))
            else:
                list_for_bound_int = list()
                for max_str in list_for_bound:
                    max_int = int(max_str)
                    list_for_bound_int.append(max_int)
                min_value = min(list_for_bound_int)
                max_value = max(list_for_bound_int)

        else:
            min_value = None
            cursor_src.execute(f"SELECT MIN({column_name}) FROM {table_name}")
            result = cursor_src.fetchone()
            if result:
                min_value = result[0]
            max_value = None
            cursor_src.execute(f"SELECT MAX({column_name}) FROM {table_name}")
            result = cursor_src.fetchone()
            if result:
                max_value = result[0]

        return min_value, max_value

    def date():
        if list_for_bound:
            START_DATE = utils.get_date_bound(list_for_bound, "start")
            END_DATE = utils.get_date_bound(list_for_bound, "end")
        else:
            START_DATE = datetime.date(year=1950, month=1, day=1)
            END_DATE = datetime.date.today()

        return START_DATE, END_DATE

    def geometry():
        min_value = max_value = 1000
        return min_value, max_value

    def bytea():
        min_value = max_value = 8
        return min_value, max_value

    def no_type():
        # Data type not supported or boundaries not necessary
        min_value = max_value = None
        return min_value, max_value

    funcDict = {
        'smallint': numeric,
        'integer': numeric,
        'bigint': numeric,
        'decimal': numeric,
        'numeric': numeric,
        'date': date,
        'timestamp': date,
        'timestamp without time zone': date,
        'point': geometry,
        'line': geometry,
        'polygon': geometry,
        'circle': geometry,
        'box': geometry,
        'lseg': geometry,
        'path': geometry,
        'bytea': bytea,
        'not_supported': no_type}

    if data_type in funcDict.keys():
        min_bound, max_bound = funcDict[data_type]()
    else:
        min_bound, max_bound = no_type()

    return min_bound, max_bound, list_for_bound


def determine_constraint_info(table_name: str, column_name: str, tables_sorted: List[str],
                              db_constraints: List[Tuple[str]]) -> str:

    # Retrieve column constraint information
    for key in db_constraints:
        if column_name == key[0] and table_name == key[1] and "FOREIGN KEY" == key[4] \
                and key[3] in tables_sorted:
            constraint = "FOREIGN KEY"
            fk_ref_info[column_name] = dict()
            fk_ref_info[column_name]['ref_column'] = key[2]
            fk_ref_info[column_name]['ref_table'] = key[3]

            return constraint

        elif column_name == key[0] and table_name == key[1] and "PRIMARY KEY" == key[4]:
            constraint = "PRIMARY KEY"
            pk_values[table_name] = {}
            pk_values[table_name][column_name] = dict()

            return constraint
