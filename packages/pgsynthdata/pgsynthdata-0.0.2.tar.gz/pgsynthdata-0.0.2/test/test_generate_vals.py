import collections
from src import data_generator


def test_generate_no_constraint():
    data_type = 'integer'
    rows_to_gen = 20
    avg_width = None
    table_name = 'atp_players'
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
    assert min_value >= 1
    assert max_value <= 21


def test_generate_primary_key_number():

    data_type = 'integer'
    rows_to_gen = 30
    avg_width = None
    table_name = 'atp_players'
    min_bound = 1
    max_bound = 40

    values = data_generator.generate_pk(data_type=data_type,
                                        rows_to_gen=rows_to_gen,
                                        avg_width=avg_width,
                                        table_name=table_name,
                                        min_value=min_bound,
                                        max_value=max_bound,)

    max_value = max(values)
    min_value = min(values)
    duplicate = [item for item, count in collections.Counter(
        values).items() if count > 1]

    assert values
    assert len(values) == 30
    assert min_value >= 1
    assert max_value <= 40
    # no duplicated values expected for primary key
    assert len(duplicate) is 0


def test_generate_pk_mf():
    # Amount of values to generate is greater than range between min_bound and max_bound

    data_type = 'integer'
    rows_to_gen = 800
    avg_width = None
    table_name = 'atp_players'
    min_bound = 1
    max_bound = 40

    values = data_generator.generate_pk(data_type=data_type,
                                        rows_to_gen=rows_to_gen,
                                        avg_width=avg_width,
                                        table_name=table_name,
                                        min_value=min_bound,
                                        max_value=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 800
    assert min_value >= 1
    assert max_value >= 40
    assert max_value <= 800


def test_generate_foreign_key():
    data_type = 'integer'
    rows_to_gen = 30
    avg_width = None
    table_name = 'atp_rankings'
    column_name = 'loser_id'
    min_bound = 1
    max_bound = 78
    column_information = {'loser_id': {}}

    ref_values = {1, 2, 3, 5, 7, 9, 11, 13, 14, 15, 16, 17, 18, 29, 30, 35, 36, 37, 38, 39, 40,
                  41, 42, 43, 44, 54, 55, 66, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 81, 80}

    pk_values = dict()
    pk_values['atp_players'] = dict()
    pk_values['atp_players']['player_id'] = ref_values

    fk_ref_info = dict()
    fk_ref_info['loser_id'] = dict()
    fk_ref_info['loser_id']['ref_column'] = 'player_id'
    fk_ref_info['loser_id']['ref_table'] = 'atp_players'

    values = data_generator.generate_fk(data_type=data_type,
                                        rows_to_gen=rows_to_gen,
                                        table_name=table_name,
                                        column_name=column_name,
                                        pk_values=pk_values,
                                        fk_ref_info=fk_ref_info,
                                        min_bound=min_bound,
                                        max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)
    ref_available = True
    for fk in values:
        if fk not in pk_values['atp_players'].get('player_id'):

            ref_available = False
        continue

    assert values
    assert len(values) == 30
    assert min_value >= 1
    assert max_value <= 78
    # foreign key has to be available in provided pk_values
    assert ref_available is True


def test_generate_fk_extended():
    # amount of values to generate is higher than amount of possible values between boundaries
    data_type = 'integer'
    rows_to_gen = 40
    table_name = 'atp_rankings'
    column_name = 'loser_id'
    min_bound = 2
    max_bound = 8

    ref_values = {1, 2, 3, 5, 7, 9, 11, 13, 14, 15, 16, 17, 18, 29, 30, 35, 36, 37, 38, 39, 40,
                  41, 42, 43, 44, 54, 55, 66, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 81, 80}

    pk_values = dict()
    pk_values['atp_players'] = {}
    pk_values['atp_players']['player_id'] = ref_values

    fk_ref_info = dict()
    fk_ref_info['loser_id'] = dict()
    fk_ref_info['loser_id']['ref_column'] = 'player_id'
    fk_ref_info['loser_id']['ref_table'] = 'atp_players'

    values = data_generator.generate_fk(data_type=data_type,
                                        rows_to_gen=rows_to_gen,
                                        table_name=table_name,
                                        column_name=column_name,
                                        pk_values=pk_values,
                                        fk_ref_info=fk_ref_info,
                                        min_bound=min_bound,
                                        max_bound=max_bound)

    max_value = max(values)
    min_value = min(values)

    assert values
    assert len(values) == 40
    assert min_value >= 1
    assert max_value <= 80
