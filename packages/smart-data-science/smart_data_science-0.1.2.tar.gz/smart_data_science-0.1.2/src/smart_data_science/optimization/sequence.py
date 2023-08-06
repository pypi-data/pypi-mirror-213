"""
- Title:            Sequence Optimizar minimizing cost. Basic Wrapper on Google's ortools
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           Basic Module

- Source:      https://developers.google.com/optimization/routing
"""

import sys
from time import time

import pandas as pd
from ortools.sat.python import cp_model  # poetry add ortools (not yet in package)

from smart_data_science import logger

log = logger.get_logger(__name__)


MAX_NODES = 50  # Max number of nodes to optimize. This is a limitation to avoid excessive computing in OR-Tools library


# TODO: Add force end node


def execute(  # pylint: disable=too-many-statements
    df: pd.DataFrame,
    start_node: str = None,
) -> tuple[list, float, float]:
    """Execute the sequence optimizer (SP)
    Args:
        df (pd.DataFrame): Dataframe with the transition times between nodes (cost matrix)
        start_node (str, optional): Node to start the sequence. Defaults to None.
    Returns:
        tuple[list, float, float]: Sequence of nodes, total cost and execution time

    Note: The cost matrix is modified in this function with toy node "0" if required and 0 costs returning to start node
    """

    assert not df.empty, "Cost matrix must not be empty"

    assert set(df.columns) == set(df.index), "Cost matrix must be square"

    start_time = time()
    # Prepare data
    if start_node is None:
        start_node = "0"  # Toy start node with cost 0 to all nodes to allow searching for the best start node
        df.loc[start_node] = 0  # Toy start node with cost 0 to all nodes to allow searching for the best start node

    df.loc[:, start_node] = 0  # Remove the limitation of returning to the start node

    assert start_node in df.index and start_node in df.columns, "The Start node must be in the cost matrix"

    sorted_nodes = [start_node] + sorted(list(set(df.index) - {start_node}))

    df = df.reindex(sorted_nodes)
    df = df.reindex(sorted_nodes, axis=1)

    all_nodes_str = list(df.index)
    cost_matrix = df.values

    num_nodes = len(cost_matrix)

    if num_nodes > MAX_NODES + 1:
        log.critical(f"Too many nodes to optimize: {num_nodes}. Please select a smaller cost matrix")
        sys.exit(1)

    all_nodes = range(num_nodes)
    # print(all_nodes)
    log.info(f"{num_nodes} Nodes")

    # Model.
    model = cp_model.CpModel()

    obj_vars = []
    obj_coeffs = []

    # Create the circuit constraint.
    arcs = []
    arc_literals = {}
    for i in all_nodes:
        for j in all_nodes:
            if i == j:
                continue

            lit = model.NewBoolVar(f"{i} follows {j}")
            arcs.append([i, j, lit])
            arc_literals[i, j] = lit

            obj_vars.append(lit)
            obj_coeffs.append(cost_matrix[i][j])

    model.AddCircuit(arcs)

    # Minimize weighted sum of arcs. Because this s
    model.Minimize(sum(obj_vars[i] * obj_coeffs[i] for i in range(len(obj_vars))))

    # Solve and print out the solution.
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    # To benefit from the linearization of the circuit constraint.
    solver.parameters.linearization_level = 2

    solver.Solve(
        model,
    )
    # log.debug(solver.ResponseStats())

    current_node = 0
    optimal_sequence = []

    optimal_sequence.append(all_nodes_str[current_node])
    str_route = all_nodes_str[current_node]
    route_is_finished = False
    total_cost = 0
    while not route_is_finished:
        for i in all_nodes:
            if i == current_node:
                continue
            if solver.BooleanValue(arc_literals[current_node, i]):
                optimal_sequence.append(all_nodes_str[i])
                str_route += f" -> {all_nodes_str[i]}"
                total_cost += cost_matrix[current_node][i]
                current_node = i
                if current_node == 0:
                    route_is_finished = True
                break

    total_cost = round(total_cost, 2)
    log.info(f"Sequence: {str_route}")
    log.info(f"Total Transition Time (h): {total_cost}")

    # remove '0' from the sequence
    optimal_sequence = [i for i in optimal_sequence if i != "0"]

    if start_node != "0":
        # Remove the redundant start node at the end of the sequence
        optimal_sequence = optimal_sequence[:-1]

    stop_time = time()

    time_required = round(stop_time - start_time, 2)

    return optimal_sequence, total_cost, time_required
