import numpy as np
from typing import List, Any
from src.generator import generator_utils


data_type_dict = {
    'smallint': int,
    'integer': int,
    'bigint': int,
    'decimal': int,
    'real': float,
    'double precision': float,
    'numeric': float
}


def get_numeric_vals_no_constraints(data_type, rows_to_gen, min_bound, max_bound,
                                    numeric_precision, numeric_precision_radix,
                                    numeric_scale, histogram):
    generated_vals = list()
    if generator_utils.fulfill_histogram_properties(histogram, rows_to_gen, data_type_dict[data_type]):

        while len(generated_vals) < rows_to_gen:
            # pick random number from buckets since all have same size
            random_pick = np.random.randint(0, len(histogram)-1)

            # get local bound min + max
            local_min = data_type_dict[data_type](histogram[random_pick])
            local_max = data_type_dict[data_type](histogram[random_pick+1])
            try:

                partial_generated_vals = generator_utils.random_number(numeric_precision,
                                                                       numeric_precision_radix,
                                                                       numeric_scale, min_value=local_min,
                                                                       max_value=local_max)

                generated_vals.append(partial_generated_vals)

            except ValueError:
                print('Sample size exceeded population size.')
    else:
        for _ in range(rows_to_gen):
            generated_vals.append(
                generator_utils.random_number(numeric_precision,
                                              numeric_precision_radix,
                                              numeric_scale,
                                              min_value=min_bound, max_value=max_bound))

    return generated_vals


def get_numeric_vals_foreign_constraint(data_type, rows_to_gen: int,
                                        pk_values, ref_table, ref_column,
                                        min_bound: Any = None,
                                        max_bound: Any = None,
                                        histogram: List[any] = None):

    error_count = 0
    generated_vals = list()
    pk_values_list = pk_values[ref_table][ref_column]

    if generator_utils.fulfill_histogram_properties(histogram, rows_to_gen,
                                                    data_type_dict[data_type]):
        # sort pks such we can use bisect
        pk_values_list.sort()
        while len(generated_vals) < rows_to_gen:
            # pick random number from histogram buckets
            random_pick = np.random.randint(0, len(histogram)-1)
            # get local bound min + max
            local_min = int(histogram[random_pick])
            local_max = int(histogram[random_pick+1])
            try:
                # check if local histogram bounds of original attribute is in pk.
                # if not take the closest value from pk_list
                if local_min in pk_values_list:
                    min_index = pk_values_list.index(local_min)
                else:
                    min_index = pk_values_list.index(
                        generator_utils.take_closest(pk_values_list, local_min))
                if local_max in pk_values_list:
                    max_index = pk_values_list.index(local_max)
                else:
                    max_index = pk_values_list.index(
                        generator_utils.take_closest(pk_values_list, local_max))
                pk_values_boundaries_list = pk_values_list[min_index:max_index]
                partial_generated_vals = generator_utils.random.choice(
                    pk_values_boundaries_list)
                generated_vals.append(partial_generated_vals)
            except ValueError:
                error_count += 1
    else:
        counter = 0
        if rows_to_gen <= len(pk_values_list):
            while len(generated_vals) < rows_to_gen:
                for value in pk_values_list:
                    if len(generated_vals) < rows_to_gen:
                        if counter < len(pk_values_list):
                            counter = counter + 1
                            if (min_bound <= value <= max_bound
                                    and value in pk_values_list):
                                generated_vals.append(value)
                        else:
                            l_min_bound = min(pk_values_list)
                            l_max_bound = max(pk_values_list)
                            if (l_min_bound <= value <= l_max_bound
                                    and value in pk_values_list):
                                generated_vals.append(value)

    return generated_vals


def get_numeric_vals_primary_constraint(data_type, rows_to_gen: int, min_value: Any = None,
                                        max_value: Any = None, histogram: List[any] = None):

    generated_vals = list()

    if generator_utils.fulfill_histogram_properties(histogram, rows_to_gen,
                                                    data_type_dict[data_type]):
        while len(generated_vals) < rows_to_gen:
            # pick random number from buckets since all have same size
            random_pick = np.random.randint(0, len(histogram)-1)
            # get local bound min + max
            local_min = int(histogram[random_pick])
            local_max = int(histogram[random_pick+1])
            try:
                # get random number from of the local bounds
                partial_generated_vals = np.random.randint(
                    local_min, local_max)
                if partial_generated_vals not in generated_vals:
                    generated_vals.append(partial_generated_vals)
            except ValueError:
                print('Sample size exceeded population size.')
    else:
        if rows_to_gen > (max_value - min_value):
            max_value = min_value + rows_to_gen
        try:
            generated_vals = generator_utils.random.sample(
                range(min_value, max_value), int(rows_to_gen))
        except ValueError:
            print('Sample size exceeded population size.')
    return generated_vals
