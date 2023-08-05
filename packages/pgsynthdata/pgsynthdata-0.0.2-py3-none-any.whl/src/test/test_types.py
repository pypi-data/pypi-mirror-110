
from src import data_generator

# Geometry types


def test_generate_no_constraints_point():
    data_type = 'point'
    rows_to_gen = 20
    avg_width = None
    table_name = 'geom_types'
    min_bound = 1
    max_bound = 21
    numeric_precision = 32

    values = data_generator.generate_no_constraint(data_type=data_type,
                                                   rows_to_gen=rows_to_gen,
                                                   avg_width=avg_width,
                                                   table_name=table_name,
                                                   numeric_precision=numeric_precision,
                                                   min_bound=min_bound,
                                                   max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 20
    #assert values[0] == '(0,0)'


def test_generate_no_constraints_line():
    data_type = 'line'
    rows_to_gen = 20
    avg_width = None
    table_name = 'geom_types'
    min_bound = 1
    max_bound = 21
    numeric_precision = 32

    values = data_generator.generate_no_constraint(data_type=data_type,
                                                   rows_to_gen=rows_to_gen,
                                                   avg_width=avg_width,
                                                   table_name=table_name,
                                                   numeric_precision=numeric_precision,
                                                   min_bound=min_bound,
                                                   max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 20
    #assert values[0] == '{1,2,3}'


def test_generate_no_constraints_polygon():
    data_type = 'polygon'
    rows_to_gen = 20
    avg_width = None
    table_name = 'geom_types'
    min_bound = 1
    max_bound = 21
    numeric_precision = 32

    values = data_generator.generate_no_constraint(data_type=data_type,
                                                   rows_to_gen=rows_to_gen,
                                                   avg_width=avg_width,
                                                   table_name=table_name,
                                                   numeric_precision=numeric_precision,
                                                   min_bound=min_bound,
                                                   max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 20
    #assert values[0] == '((0,0),(1,1),(0,0))'


def test_generate_no_constraints_circle():
    data_type = 'circle'
    rows_to_gen = 20
    avg_width = None
    table_name = 'geom_types'
    min_bound = 1
    max_bound = 21
    numeric_precision = 32

    values = data_generator.generate_no_constraint(data_type=data_type,
                                                   rows_to_gen=rows_to_gen,
                                                   avg_width=avg_width,
                                                   table_name=table_name,
                                                   numeric_precision=numeric_precision,
                                                   min_bound=min_bound,
                                                   max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 20
    #assert values[0] == '<(0,0),1>'


def test_generate_no_constraints_box():
    data_type = 'box'
    rows_to_gen = 20
    avg_width = None
    table_name = 'geom_types'
    min_bound = 1
    max_bound = 21
    numeric_precision = 32

    values = data_generator.generate_no_constraint(data_type=data_type,
                                                   rows_to_gen=rows_to_gen,
                                                   avg_width=avg_width,
                                                   table_name=table_name,
                                                   numeric_precision=numeric_precision,
                                                   min_bound=min_bound,
                                                   max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 20
    #assert values[0] == '((0,1),(1,0))'


def test_generate_no_constraints_lseg():
    data_type = 'lseg'
    rows_to_gen = 20
    avg_width = None
    table_name = 'geom_types'
    min_bound = 1
    max_bound = 21
    numeric_precision = 32

    values = data_generator.generate_no_constraint(data_type=data_type,
                                                   rows_to_gen=rows_to_gen,
                                                   avg_width=avg_width,
                                                   table_name=table_name,
                                                   numeric_precision=numeric_precision,
                                                   min_bound=min_bound,
                                                   max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 20
    #assert values[0] == '((0,1),(2,2))'


# binary types
def test_generate_no_constraints_bytea():
    data_type = 'bytea'
    rows_to_gen = 20
    avg_width = None
    table_name = 'geom_types'
    min_bound = 1
    max_bound = 21
    numeric_precision = 32

    values = data_generator.generate_no_constraint(data_type=data_type,
                                                   rows_to_gen=rows_to_gen,
                                                   avg_width=avg_width,
                                                   table_name=table_name,
                                                   numeric_precision=numeric_precision,
                                                   min_bound=min_bound,
                                                   max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    print(values)

    assert values
    assert len(values) == 20
