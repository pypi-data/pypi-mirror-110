from src.generator import generator_utils
from typing import Any
import datetime


def get_data_no_constraints(data_type: str, rows_to_gen: int, min_bound: Any = None, max_bound: Any = None):

    generated_vals = list()
    for index in range(rows_to_gen):
        if data_type in ('timestamp', 'timestamp without time zone'):
            generated_vals.append(generator_utils.random_date(
                min_bound, max_bound, time=True))
        else:
            generated_vals.append(
                generator_utils.random_date(min_bound, max_bound))

    return generated_vals


def get_data_foreign_constraint(rows_to_gen: int,
                                pk_values, ref_table, ref_column, min_bound: Any = None,
                                max_bound: Any = None):

    generated_vals = list()
    counter = 0
    pk_values_list = pk_values[ref_table][ref_column]
    while len(generated_vals) < rows_to_gen:  # ensure that all values are created
        for value in pk_values_list:
            # ensure not to exceed values during for loop
            if len(generated_vals) < rows_to_gen:
                # consider every value in PK_values once
                if counter < len(pk_values_list):
                    counter = counter + 1
                    if min_bound <= value <= max_bound and value not in generated_vals:
                        generated_vals.append(value)
                else:  # if pk_values does not contain enough values then extend boundaries
                    l_min_bound = min(pk_values_list)
                    l_max_bound = max(pk_values_list)
                    if l_min_bound <= value <= l_max_bound and value not in generated_vals:
                        generated_vals.append(value)

    return generated_vals


def get_date_primary_constraints(data_type, rows_to_gen: int, min_value: Any = None, max_value: Any = None):
    generated_vals = list()
    # ensure that enough dates btw. start and end are available
    days_between = generator_utils.days_between(min_value, max_value)
    if rows_to_gen > days_between:
        max_value = min_value + datetime.timedelta(days=rows_to_gen)
    while len(generated_vals) < rows_to_gen:
        for index in range(rows_to_gen):
            if data_type in ('timestamp', 'timestamp without time zone'):
                value = generator_utils.random_date(
                    min_value, max_value, time=True)
                if value not in generated_vals:
                    generated_vals.append(value)
            else:
                value = generator_utils.random_date(min_value, max_value)
                if value not in generated_vals:
                    generated_vals.append(value)

    return generated_vals
