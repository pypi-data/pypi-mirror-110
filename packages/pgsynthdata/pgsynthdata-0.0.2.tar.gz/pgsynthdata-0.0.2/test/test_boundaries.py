from src import utils
from src import model_generator
import datetime


def test_number_bound_mvc():
    # Testing requirement MM-3
    cursor_src = None
    table_name = 'atp_players'
    column_name = 'player_id'
    data_type = 'integer'
    most_common_values = [2, 3, 4, 5, 6, 6, 7, 5, 34, 2, 34, 2, 33, 4]
    histogram_bounds = [11, 22, 33, 44, 55, 66, 77, 88, 99, 12, 23]

    min_bound, max_bound, list_for_bound = model_generator.determine_boundaries(cursor_src, table_name,
                                                                                column_name, data_type,
                                                                                most_common_values,
                                                                                histogram_bounds)
    assert min_bound == 2
    assert max_bound == 34
    assert list_for_bound == [2, 3, 4, 5, 6, 6, 7, 5, 34, 2, 34, 2, 33, 4]


def test_number_bound_hist():
    # MM-4
    cursor_src = None
    table_name = 'atp_players'
    column_name = 'player_id'
    data_type = 'integer'
    most_common_values = None
    histogram_bounds = [11, 22, 33, 44, 55, 66, 77, 88, 99, 12, 23]

    min_bound, max_bound, list_for_bound = model_generator.determine_boundaries(cursor_src, table_name,
                                                                                column_name, data_type,
                                                                                most_common_values,
                                                                                histogram_bounds)
    assert min_bound == 11
    assert max_bound == 99
    assert list_for_bound == [11, 22, 33, 44, 55, 66, 77, 88, 99, 12, 23]


def test_date_bound_mcv():

    cursor_src = None
    table_name = 'atp_players'
    column_name = 'player_id'
    data_type = 'date'
    most_common_values = ['2025-04-01',
                          '2010-03-02', '2011-1-03', '2020-03-18']
    histogram_bounds = ['2034-01-12', '1919-04-22',
                        '2028-12-01', '2030-08-08', '1999-01-01']

    min_bound, max_bound, list_for_bound = model_generator.determine_boundaries(cursor_src, table_name,
                                                                                column_name, data_type,
                                                                                most_common_values,
                                                                                histogram_bounds)
    assert min_bound == datetime.date(year=2010, month=3, day=2)
    assert max_bound == datetime.date(year=2025, month=4, day=1)
    assert list_for_bound == ['2025-04-01',
                              '2010-03-02', '2011-1-03', '2020-03-18']


def test_date_bound_hist():

    cursor_src = None
    table_name = 'atp_players'
    column_name = 'player_id'
    data_type = 'date'
    most_common_values = None
    histogram_bounds = ['2025-04-01', '2010-03-02', '2011-1-03', '2020-03-18']

    min_bound, max_bound, list_for_bound = model_generator.determine_boundaries(cursor_src, table_name,
                                                                                column_name, data_type,
                                                                                most_common_values,
                                                                                histogram_bounds)
    assert min_bound == datetime.date(year=2010, month=3, day=2)
    assert max_bound == datetime.date(year=2025, month=4, day=1)
    assert list_for_bound == ['2025-04-01',
                              '2010-03-02', '2011-1-03', '2020-03-18']


def test_date_bound_no_list():
    # MM-6
    cursor_src = None
    table_name = 'atp_players'
    column_name = 'player_id'
    data_type = 'date'
    most_common_values = None
    histogram_bounds = None

    min_bound, max_bound, list_for_bound = model_generator.determine_boundaries(cursor_src, table_name,
                                                                                column_name, data_type,
                                                                                most_common_values,
                                                                                histogram_bounds)
    assert min_bound == datetime.date(year=1950, month=1, day=1)
    assert max_bound == datetime.date.today()
    assert list_for_bound is None


def test_get_date_boundaries():
    # helper function in utils
    mcv = ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04']
    min = utils.get_date_bound(mcv, 'start')
    max = utils.get_date_bound(mcv, 'end')
    assert min == datetime.date(year=2020, month=1, day=1)
    assert max == datetime.date(year=2020, month=1, day=4)
