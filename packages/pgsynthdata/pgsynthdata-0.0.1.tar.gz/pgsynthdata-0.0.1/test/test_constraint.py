import pytest
from src import utils
from src import model_generator


def test_topological_sorting():
    # Sort tables topological
    tables_to_sort = ['atp_players', 'atp_matches', 'atp_rankings']
    constraints_to_consider = [('loser_id', 'atp_matches', 'player_id', 'atp_players', 'FOREIGN KEY', 'atp_matches_loser_id_fkey'),
                               ('player_id', 'atp_rankings', 'player_id', 'atp_players',
                                'FOREIGN KEY', 'atp_rankings_player_id_fkey'),
                               ('ranking_date', 'atp_jury', 'ranking_date', 'atp_rankings', 'FOREIGN KEY', 'atp_jury_ranking_date_fkey')]

    tables_sorted = utils.sort_tables_topological(
        constraints_to_consider, tables_to_sort)
    print(tables_sorted)
    assert tables_sorted == ['atp_players', 'atp_matches', 'atp_rankings']


def test_topological_sorting_cycle_negative():
    # Given tables are not topologically sortable, as they represent a cycle, i.e. interdependence
    # Atp_players is dependent on atp_rankings and vice versa
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tables_to_sort = ['atp_players', 'atp_matches', 'atp_rankings']
        constraints_to_consider = [
            ('loser_id', 'atp_matches', 'player_id', 'atp_players',
             'FOREIGN KEY', 'atp_matches_loser_id_fkey'),
            ('player_id', 'atp_rankings', 'player_id', 'atp_players',
             'FOREIGN KEY', 'atp_rankings_player_id_fkey'),
            ('ranking_date', 'atp_jury', 'ranking_date', 'atp_rankings',
             'FOREIGN KEY', 'atp_jury_ranking_date_fkey'),
            ('player_name', 'atp_players', 'player_id', 'atp_rankings', 'FOREIGN KEY', 'atp_test_key')]

        utils.sort_tables_topological(constraints_to_consider, tables_to_sort)

    assert pytest_wrapped_e.type == SystemExit


def test_constraint_collector():

    tables_to_sort = ['atp_players', 'atp_matches', 'atp_rankings', 'atp_jury']

    db_constraints = [('player_id', 'atp_players', 'player_id', 'atp_players', 'PRIMARY KEY', 'atp_players_pkey'),
                      ('loser_id', 'atp_matches', 'player_id', 'atp_players',
                       'FOREIGN KEY', 'atp_matches_loser_id_fkey'),
                      ('winner_id', 'atp_matches', 'player_id', 'atp_players',
                       'FOREIGN KEY', 'atp_matches_winner_id_fkey'),
                      ('player_id', 'atp_rankings', 'player_id', 'atp_players',
                       'FOREIGN KEY', 'atp_rankings_player_id_fkey'),
                      ('ranking_date', 'atp_rankings', 'ranking_date',
                       'atp_rankings', 'PRIMARY KEY', 'atp_rankings_pkey'),
                      ('ranking_date', 'atp_jury', 'ranking_date', 'atp_rankings',
                       'FOREIGN KEY', 'atp_jury_ranking_date_fkey'),
                      ('jury_name', 'atp_jury', 'jury_name', 'atp_jury', "PRIMARY KEY"    "atp_jury_pkey")]

    constraints_to_consider = utils.check_constraints(
        tables_to_sort, db_constraints, None, None)

    assert constraints_to_consider == [('loser_id', 'atp_matches', 'player_id', 'atp_players', 'FOREIGN KEY', 'atp_matches_loser_id_fkey'),
                                       ('player_id', 'atp_rankings', 'player_id', 'atp_players',
                                        'FOREIGN KEY', 'atp_rankings_player_id_fkey'),
                                       ('ranking_date', 'atp_jury', 'ranking_date', 'atp_rankings', 'FOREIGN KEY', 'atp_jury_ranking_date_fkey')]


def test_determine_constraint_fk():

    table_name = 'atp_matches'
    column_name = 'loser_id'
    tables_sorted = ['atp_players', 'atp_matches']
    db_constraints = [('player_id', 'atp_players', 'player_id', 'atp_players', 'PRIMARY KEY', 'atp_players_pkey'),
                      ('loser_id', 'atp_matches', 'player_id', 'atp_players', 'FOREIGN KEY',
                       'atp_matches_loser_id_fkey'),
                      ('winner_id', 'atp_matches', 'player_id', 'atp_players', 'FOREIGN KEY',
                       'atp_matches_winner_id_fkey')]
    constraint = model_generator.determine_constraint_info(
        table_name, column_name, tables_sorted, db_constraints)
    assert constraint == 'FOREIGN KEY'


def test_determine_constraint_pk():
    table_name = 'atp_players'
    column_name = 'player_id'
    tables_sorted = ['atp_players', 'atp_matches']
    db_constraints = [('player_id', 'atp_players', 'player_id', 'atp_players', 'PRIMARY KEY', 'atp_players_pkey'), ('loser_id', 'atp_matches', 'player_id', 'atp_players',
                                                                                                                    'FOREIGN KEY', 'atp_matches_loser_id_fkey'), ('winner_id', 'atp_matches', 'player_id', 'atp_players', 'FOREIGN KEY', 'atp_matches_winner_id_fkey')]
    constraint = model_generator.determine_constraint_info(
        table_name, column_name, tables_sorted, db_constraints)
    assert constraint == 'PRIMARY KEY'


def test_determine_no_constraint():
    table_name = 'atp_rankings'
    column_name = 'ranking'
    tables_sorted = ['atp_players', 'atp_matches']
    db_constraints = [('player_id', 'atp_players', 'player_id', 'atp_players', 'PRIMARY KEY', 'atp_players_pkey'),
                      ('loser_id', 'atp_matches', 'player_id', 'atp_players',
                       'FOREIGN KEY', 'atp_matches_loser_id_fkey'),
                      ('winner_id', 'atp_matches', 'player_id', 'atp_players', 'FOREIGN KEY', 'atp_matches_winner_id_fkey')]
    constraint = model_generator.determine_constraint_info(
        table_name, column_name, tables_sorted, db_constraints)
    assert constraint is None


def test_determine_tables_to_generate():

    tables_result = [('public', 'atp_jury', '10', '4'),
                     ('public', 'atp_matches', '2781', '2'),
                     ('public', 'atp_players', '54938', '1'),
                     ('public', 'atp_rankings', '47', '3'),
                     ('public', 'atp_sponsor', '3', '5')]

    u_tables = 'atp_matches,atp_rankings,atp_players'

    tables_to_sort = utils.determine_tables_to_generate(
        tables_result, u_tables)

    assert tables_to_sort == ['atp_matches', 'atp_players', 'atp_rankings']
