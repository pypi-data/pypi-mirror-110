from typing import List, Any
from src.generator import numeric_generator, geometry_generator, bytea_generator, date_generator, varchar_generator


def generate_no_constraint(data_type: str, rows_to_gen: int, avg_width: int,
                           table_name: str, numeric_precision: int = None,
                           numeric_precision_radix: int = None, numeric_scale: int = None,
                           min_bound: Any = None, max_bound: Any = None,
                           list_for_bound: List[str] = None, histogram: List[any] = None) -> List[str]:

    generated_vals = list()

    def numeric():
        nonlocal generated_vals
        generated_vals = numeric_generator.get_numeric_vals_no_constraints(data_type, rows_to_gen,
                                                                           min_bound, max_bound,
                                                                           numeric_precision, numeric_precision_radix, numeric_scale,
                                                                           histogram)

    def date():
        nonlocal generated_vals
        generated_vals = date_generator.get_data_no_constraints(
            data_type, rows_to_gen, min_bound, max_bound)

    def varchar():
        nonlocal generated_vals
        generated_vals = varchar_generator.get_varchar_no_constraints(
            rows_to_gen, avg_width, list_for_bound)

    def geometry():
        nonlocal generated_vals
        generated_vals = geometry_generator.get_geometry_no_constraints(
            data_type, rows_to_gen, max_bound)

    def bytea():
        nonlocal generated_vals
        generated_vals = bytea_generator.get_bytea_no_constraints(rows_to_gen)

    def boolean():
        return

    def no_type():
        print(
            f'The "{data_type}" data type is not supported. '
            f'Skipping the table\'s "{table_name}" data generation...')
        return

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
                'point': geometry,
                'line': geometry,
                'polygon': geometry,
                'circle': geometry,
                'box': geometry,
                'lseg': geometry,
                'path': geometry,
                'bytea': bytea,
                'boolean': boolean,
                'not_supported': no_type}

    funcDict[data_type]()

    return generated_vals


def generate_fk(data_type: str, rows_to_gen: int, table_name: str, column_name: str,
                pk_values, fk_ref_info, min_bound: Any = None,
                max_bound: Any = None, histogram: List[any] = None) -> List[Any]:

    def numeric():
        nonlocal generated_vals
        generated_vals = numeric_generator.get_numeric_vals_foreign_constraint(data_type,
            rows_to_gen, pk_values, ref_table, ref_column, min_bound, max_bound, histogram)

    def date():
        nonlocal generated_vals
        generated_vals = date_generator.get_data_foreign_constraint(
            rows_to_gen, pk_values, ref_table, ref_column, min_bound, max_bound)

    def varchar():
        nonlocal generated_vals
        generated_vals = varchar_generator.get_varchar_foreign_constraint(
            rows_to_gen, pk_values, ref_table, ref_column)

    def no_type():
        print(
            f'The "{data_type}" data type is not supported. '
            f'Skipping the table\'s "{table_name}" data generation...')
        return

    generated_vals = list()

    ref_table = fk_ref_info[column_name]['ref_table']
    ref_column = fk_ref_info[column_name]['ref_column']

    funcDict = {'text': varchar,
                'character varying': varchar,
                'character': varchar,
                'smallint': numeric,
                'integer': numeric,
                'bigint': numeric,
                'decimal': numeric,
                'numeric': numeric,
                'date': date,
                'timestamp': date,
                'timestamp without time zone': date,
                'not_supported': no_type}

    funcDict[data_type]()

    return generated_vals


def generate_pk(data_type: str, rows_to_gen: int, avg_width: int, table_name: str,
                min_value: Any = None, max_value: Any = None,
                list_for_bound: List[str] = None, histogram: List[any] = None
                ) -> List[Any]:

    generated_vals = list()

    def numeric():
        nonlocal generated_vals
        generated_vals = numeric_generator.get_numeric_vals_primary_constraint(data_type,
            rows_to_gen, min_value, max_value, histogram)

    def date():
        nonlocal generated_vals
        generated_vals = date_generator.get_date_primary_constraints(
            data_type, rows_to_gen, min_value, max_value)

    def varchar():
        nonlocal generated_vals
        generated_vals = varchar_generator.get_varchar_primary_constraints(
            rows_to_gen, avg_width, list_for_bound)

    def no_type():
        """ print(
            f'The "{data_type}" data type is not supported. '
            f'Skipping the table\'s "{table_name}" data generation...') """
        return

    funcDict = {'text': varchar,
                'character varying': varchar,
                'character': varchar,
                'smallint': numeric,
                'integer': numeric,
                'bigint': numeric,
                'decimal': numeric,
                'numeric': numeric,
                'date': date,
                'timestamp': date,
                'timestamp without time zone': date,
                'not_supported': no_type}

    funcDict[data_type]()

    return generated_vals
