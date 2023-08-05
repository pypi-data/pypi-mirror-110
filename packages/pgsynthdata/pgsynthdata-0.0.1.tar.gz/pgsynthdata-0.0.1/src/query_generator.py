from typing import Dict, Any, List, Optional, Union
import random
from src.generator import generator_utils
import datetime
from src import postgres


def create_insert_query(total_rows: int, insert_query: str, table_name: str,
                        column_names: List[str],
                        table_information, column_information: Dict[str, Dict[str, Any]],
                        insert_dict: Dict) -> Dict:
    # Numerate for columns without frequency
    i = 0
    print(f'Creating insert query for the "{table_name}" table...')

    for _ in range(round(total_rows)):
        column_values = list()
        insert_query += "INSERT INTO {table_name}("
        insert_query += '{0}{1}'.format(', '.join(column_names), ') VALUES (')
        random_frac = random.random()

        for column_info in table_information[table_name]["column_information"].values():
            column_name = column_info.get("column_name")
            data_type = column_info.get("data_type")

            if data_type not in postgres.DataTypes.SUPPORTED_TYPES:
                data_type = 'not_supported'

            max_length = column_info.get("max_length")
            numeric_precision = column_info.get("numeric_precision")
            numeric_precision_radix = column_info.get(
                "numeric_precision_radix")
            numeric_scale = column_info.get("numeric_scale")

            """ The next line messes up the primary key insertion. It forces to diregard 
                the generated_vals and does an auto increment where it is specified as a 
                column_default. 

                This can subsequently lead to insertion errors on foreign keys since primary 
                keys might not be the same in generated database and the ones used to 
                generate foreign key values in the tool. 

            """
            # if column_info.get("column_default"):
            # continue

            generated_vals = None
            generated_freqs: Optional[Union[List[float], bool]] = None
            null_frac = None
            column_stats = None

            if column_name in table_information[table_name]["pg_stats"]:
                column_stats = table_information[table_name]["pg_stats"][column_name]

            if column_stats:
                if "generated_vals" in column_information[column_name] \
                        and column_information[column_name]["generated_vals"]:
                    generated_vals = column_information[column_name]["generated_vals"]
                    generated_freqs = column_information[column_name]["generated_freqs"]
                    null_frac = column_stats["null_frac"]

            def numeric():
                # Columns containing MCV
                if generated_vals and generated_freqs:
                    if null_frac and random_frac <= null_frac:
                        column_values.append("{0}".format('null'))
                    else:
                        column_values.append("{0}".format(
                            generator_utils.random_choices(generated_vals, generated_freqs)))
                # All distinct columns
                elif generated_vals:
                    column_values.append(
                        "{0}".format(generated_vals[i]))
                else:
                    column_values.append(
                        "{0}".format(generator_utils.random_number(numeric_precision,
                                                                   numeric_precision_radix,
                                                                   numeric_scale)))

            def date():
                if generated_vals and generated_freqs:
                    if null_frac and random_frac <= null_frac:
                        column_values.append("{0}".format('NULL'))
                    else:
                        column_values.append("'{0}'".format(
                            generator_utils.random_choices(generated_vals, generated_freqs)))
                # All distinct columns
                elif generated_vals:
                    column_values.append("'{0}'".format(generated_vals[i]))
                else:
                    START_DATE = datetime.date(year=1950, month=1, day=1)
                    END_DATE = datetime.date.today()
                    column_values.append("'{0}'".format(
                        generator_utils.random_date(START_DATE, END_DATE)))

            def boolean():
                column_values.append("{0}".format(
                    generator_utils.random_boolean()))

            def varchar():
                if generated_vals and generated_freqs:
                    if null_frac and random_frac <= null_frac:
                        column_values.append("{0}".format('NULL'))
                    else:
                        column_values.append("'{0}'".format(
                            generator_utils.random_choices(generated_vals, generated_freqs)))
                # All distinct columns
                elif generated_vals:
                    column_values.append("'{0}'".format(generated_vals[i]))
                else:
                    column_values.append("'{0}'".format(
                        generator_utils.random_word(max_length / 2.5)))

            def geometry():
                # Columns containing MCV
                if generated_vals and generated_freqs:
                    if null_frac and random_frac <= null_frac:
                        column_values.append("{0}".format('NULL'))
                    else:
                        column_values.append("'{0}'".format(
                            generator_utils.random_choices(generated_vals, generated_freqs)))
                # All distinct columns
                elif generated_vals:

                    column_values.append(
                        "{0}".format(generated_vals[i]))
                else:
                    column_values.append("{0}".format('NULL'))

            def bytea():
                # Columns containing MCV
                if generated_vals and generated_freqs:
                    if null_frac and random_frac <= null_frac:
                        column_values.append("{0}".format('NULL'))
                    else:
                        column_values.append("'{0}'".format(
                            generator_utils.random_choices(generated_vals, generated_freqs)))
                # All distinct columns
                elif generated_vals:

                    column_values.append(
                        "'{0}'".format(generated_vals[i]))
                else:
                    column_values.append("{0}".format('NULL'))

            def no_type():
                """ print(
                    f'The "{data_type}" data type is not supported. '
                    f'Skipping the table\'s "{table_name}" data generation...') """
                column_values.append("{0}".format('NULL'))

            funcDict = {'text': varchar,
                        'character varying': varchar,
                        'character': varchar,
                        'smallint': numeric,
                        'integer': numeric,
                        'bigint': numeric,
                        'decimal': numeric,
                        'numeric': numeric,
                        'double precision': numeric,
                        'real': numeric,
                        'date': date,
                        'timestamp': date,
                        'timestamp without time zone': date,
                        'boolean': boolean,
                        'bool': boolean,
                        'point': geometry,
                        'line': geometry,
                        'polygon': geometry,
                        'circle': geometry,
                        'box': geometry,
                        'lseg': geometry,
                        'path': geometry,
                        'bytea': bytea,
                        'not_supported': no_type}

            funcDict[data_type]()

        i = i + 1
        insert_query += '{0}{1}'.format(', '.join(column_values), ');')

    insert_dict[table_name] = insert_query

    return insert_dict
