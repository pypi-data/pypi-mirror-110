from collections import defaultdict
import datetime
from src import postgres
import sys
from psycopg2._psycopg import cursor
from typing import Any, List, Optional, Tuple, Dict


def get_date_bound(most_common_values: List[str], bound: str) -> datetime.date:

    most_common_dates = [old_format.replace(
        "-", '') for old_format in most_common_values]

    if bound == "start":
        date = min(most_common_dates)
    elif bound == "end":
        date = max(most_common_dates)

    if date is not None:
        date_y = int(date[:4])
        date_m = int(date[4:6])
        date_d = int(date[6:8])

        if bound == "start":
            START_DATE = datetime.date(year=date_y, month=date_m, day=date_d)
            return START_DATE

        elif bound == "end":
            END_DATE = datetime.date(year=date_y, month=date_m, day=date_d)
            return END_DATE

    else:
        if bound == "start":
            START_DATE = datetime.date(year=1950, month=1, day=1)
            return START_DATE
        elif bound == "end":
            END_DATE = datetime.date.today()
            return END_DATE


def days_between(date1: Any, date2: Any) -> int:
    return (date2 - date1).days


def determine_tables_to_generate(table_results, u_tables) -> List[str]:
    # Save all database tables in list db_tables
    db_tables = list()
    for table_entry in table_results:
        db_tables.append(table_entry[1])

    # Arrange user specified table into user_tables
    user_tables = list()

    if u_tables is not None:
        user_tables = u_tables.split(",")
        user_tables = [table.strip(' ') for table in user_tables]

    # If given from user, then only user tables should be consider
    tables_to_gen = list()
    if user_tables:
        for table_name in db_tables:
            if table_name in user_tables:
                tables_to_gen.append(table_name)
    else:
        tables_to_gen = db_tables

    return tables_to_gen


def check_constraints(tables_to_sort: List[str], db_constraints: Optional[List[Tuple[str]]] = None,
                      cursor_target: cursor = None, connection_target=None):

    # Only constraint relation of given tables should be considered
    constraints: List[Tuple[str]] = list()
    constraints_to_delete: Dict = {}
    referenced_pk_table: Dict = {}
    for constraint in db_constraints:
        append = True
        if constraint[1] in tables_to_sort and constraint[3] in tables_to_sort \
                and constraint[4] == "FOREIGN KEY":
            # Avoid duplicate entries due to multiple relation between tables
            for duplicate in constraints:
                if constraint[1] != duplicate[1] or constraint[3] != duplicate[3]:
                    continue
                append = False
            if append:
                constraints.append(constraint)
        # Get constraint name to delete in target database
        elif constraint[1] in tables_to_sort and constraint[3] not in tables_to_sort \
                and constraint[4] == "FOREIGN KEY":
            constraints_to_delete[constraint[5]] = constraint[1]
            referenced_pk_table[constraint[5]] = constraint[3]

    if bool(constraints_to_delete):
        print(f"Attention!\n"
              f"The tables you want to synthesize contain foreign key dependencies"
              " to other tables that were not specified.\n"
              "Following constraints are affected and would have to be deleted"
              " in order to generate the data into the specified tables:\n")
        for constraint, table in constraints_to_delete.items():
            print(
                f"""  > constraints_name: {constraint}  - corresponding table: {table}""")

        proceed = str(input("\nDo you wish to proceed with deleting these constraints?"
                            " (YES or NO) ")).upper()
        if proceed == 'YES':
            postgres.delete_constraint(
                constraints_to_delete, cursor_target, connection_target)
            print("\n")
        else:
            sys.exit(
                f"\nPlease specify all dependent tables or remove the corresponding constraints.")

    return constraints


def sort_tables_topological(constraints: List[Tuple[str, str, str, str, str, str]], tables_to_sort: List[str]) -> List[str]:
    # If constraints, then generate a graph to get the tables sorted topologically
    if constraints:
        vertices = len(constraints)
        g = Graph(vertices)
        tables_sorted = g.sort_list(constraints, tables_to_sort)
    else:
        tables_sorted = tables_to_sort

    return tables_sorted


class Graph:
    def __init__(self, vertices: int):
        self.graph = defaultdict(list)  # Dictionary containing adjacency list
        self.V = vertices  # No. of vertices

    def sort_list(self, constraint_list: List[str], tables_to_sort: List[str]) -> List[str]:
        for vertices in constraint_list:
            if "FOREIGN KEY" == vertices[4]:
                u = vertices[1]  # FK
                v = vertices[3]  # Related PK
                # For u, v in constraint_list:
                self.addEdge(u, v)
        sorted_list = self.topological_sort(tables_to_sort)
        return sorted_list

    def addEdge(self, u: str, v: str):
        self.graph[u].append(v)

    def topological_sort(self, tables_to_sort: List[str]) -> List[str]:
        sorted_list = list()
        pk_generated = None
        counter = 0
        # Add tables which are not referenced (independent)
        for table in tables_to_sort:
            counter = counter + 1
            if table not in self.graph.keys():
                if table not in sorted_list:
                    sorted_list.insert(0, table)

        # Add tables which are referenced (dependent)
        while len(sorted_list) < len(tables_to_sort):
            pre_counter = len(sorted_list)
            for table in tables_to_sort:
                for child in self.graph.keys():  # Referencing table (child table)
                    if table == child:
                        pk_generated = True
                        # Referenced tables (parent tables)
                        for parent in self.graph[child]:
                            if parent in sorted_list:
                                continue
                            pk_generated = False  # Referenced table not in list yet

                if pk_generated and table not in sorted_list:
                    sorted_list.insert(0, table)
            # Check if sorted list increased
            if pre_counter == len(sorted_list) and len(sorted_list) < len(tables_to_sort):
                sys.exit("""The specified tables are not topologically sortable as they contain interdependencies.
                            Please remove the necessary dependencies between the tables
                            so that the relations (constraints) do not represent a cycle..""")

        return sorted_list[::-1]
