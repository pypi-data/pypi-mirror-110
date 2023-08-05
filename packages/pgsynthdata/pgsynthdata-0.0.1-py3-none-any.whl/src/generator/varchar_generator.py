from typing import List
from src.generator import generator_utils


def get_varchar_no_constraints(rows_to_gen: int, avg_width: int, list_for_bound: List[str] = None):
    generated_vals = list()

    if list_for_bound is not None:
        value = list_for_bound[0]
    else:
        value = None

    for _ in range(rows_to_gen):
        generated_vals.append(generator_utils.random_word(
            avg_width,
            value=value))

    return generated_vals


def get_varchar_foreign_constraint(rows_to_gen: int, pk_values, ref_table, ref_column):
    generated_vals = list()

    pk_values_list = pk_values[ref_table][ref_column]
    while len(generated_vals) < rows_to_gen:
        for value in pk_values_list:
            if len(generated_vals) < rows_to_gen:
                generated_vals.append(value)

    return generated_vals


def get_varchar_primary_constraints(rows_to_gen: int, avg_width: int, list_for_bound: List[str] = None):
    generated_vals = list()
    for _ in range(rows_to_gen):
        value = generator_utils.random_word(avg_width - 1,
                                            value=list_for_bound[generator_utils.gen_random_number(0, len(list_for_bound) - 1)])
        if value not in generated_vals:
            generated_vals.append(value)

    return generated_vals
