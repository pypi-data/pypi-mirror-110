import numpy as np
from typing import Any


def get_geometry_no_constraints(data_type: str, rows_to_gen: int, max_bound: Any = None):
    generated_vals = list()

    if max_bound is None:
        max_bound = 1000

    if data_type == 'point':
        for _ in range(rows_to_gen):
            generated_vals.append(
                f'point({np.random.randint(1,max_bound)},{np.random.randint(1,max_bound)})')

    if data_type == 'line':
        for _ in range(rows_to_gen):
            value = f'line( point \'({np.random.randint(1,max_bound)}, \
            {np.random.randint(1,max_bound)})\',\'({np.random.randint(1,max_bound)}, \
            {np.random.randint(1,max_bound)})\')'
            generated_vals.append(value)

    if data_type == 'polygon':
        for _ in range(rows_to_gen):
            start_0 = np.random.randint(1, max_bound)
            start_1 = np.random.randint(1, max_bound)
            generated_vals.append(
                f' polygon \'({start_0,start_1},({np.random.randint(1,max_bound)}, \
                {np.random.randint(1,max_bound)}),{start_0,start_1})\'')

    if data_type == 'circle':
        for _ in range(rows_to_gen):
            generated_vals.append(
                f'circle \'<({np.random.randint(1,max_bound)}, \
                {np.random.randint(1,max_bound)}),{np.random.randint(1,10)}>\'')

    if data_type == 'box':
        for _ in range(rows_to_gen):
            generated_vals.append(
                'box \'(({0},{1}),({2},{3}))\''.format(
                    np.random.randint(1, max_bound),
                    np.random.randint(1, max_bound),
                    np.random.randint(1, max_bound),
                    np.random.randint(1, max_bound)))

    if data_type == 'lseg':
        for _ in range(rows_to_gen):
            generated_vals.append(
                'lseg \'(({0},{1}),({2},{3}))\''.format(
                    np.random.randint(1, max_bound),
                    np.random.randint(1, max_bound),
                    np.random.randint(1, max_bound),
                    np.random.randint(1, max_bound)))

    if data_type == 'path':
        for _ in range(rows_to_gen):
            start_0 = np.random.randint(1, max_bound)
            start_1 = np.random.randint(1, max_bound)
            generated_vals.append(
                f' path \'({start_0,start_1},({np.random.randint(1,max_bound)},\
                {np.random.randint(1,max_bound)}),  \
                {start_0,start_1})\'')

    return generated_vals
