import numpy as np
import hygese as hgs
from scipy.spatial import distance_matrix

def hgs_solve(coords, demands, capacity, subset=None, time_limit=5):
    """
    Args:
        coords: a numpy array of coordinates, where each row represents the x and y coordinates of a node
        demands: a numpy array of demands, where index 0 represents the demand of the depot (0)
        capacity: integer, capacity of all vehicles
        subset: a subset of node IDs that we want to solve for
        time_limit: integer, maximum time limit for the solver in seconds
    
    Returns:
        result: a RoutingSolution from Python package Hygese with the following attributes:
            - cost: the total cost of the solution
            - time: the time taken to solve the problem
            - n_routes: the number of routes in the solution
            - routes: a list of routes, where each route is a list of node IDs, excluding the depots.
    """

    if subset != None:
        subset = sorted(subset)
        coords = coords[subset]
        demands = demands[subset]
        index_to_node = {i: node for i, node in enumerate(subset)}

    n = len(coords)
    x = coords[:, 0]
    y = coords[:, 1]

    # Solver initialization
    ap = hgs.AlgorithmParameters(timeLimit=time_limit)
    hgs_solver = hgs.Solver(parameters=ap, verbose=False)

    # Data preparation
    data = dict()
    data['x_coordinates'] = x
    data['y_coordinates'] = y
    data['distance_matrix'] = distance_matrix(coords, coords)
    data['service_times'] = np.zeros(n)
    data['demands'] = demands
    data['vehicle_capacity'] = capacity
    data['num_vehicles'] = 100  # Update with the appropriate number of vehicles
    data['depot'] = 0

    result = hgs_solver.solve_cvrp(data)
    if subset != None:
        result.routes = [[index_to_node[i] for i in route] for route in result.routes]
    return result

def hgs_solve_subproblems(coords, demands, capacity, subsets, time_limit=5):
    """
    Args:
        coords: a numpy array of coordinates, where each row represents the x and y coordinates of a node
        demands: a numpy array of demands, where index 0 represents the demand of the depot (0)
        capacity: integer, capacity of all vehicles
        subsets: a list of subsets of node IDs that we want to solve for
        time_limit: integer, maximum time limit for the solver in seconds

    Returns:
        cost: the total cost of the solution
        time: the time taken to solve the problem
        n_routes: the number of routes in the solution
        routes: a list of routes, where each route is a list of node IDs, excluding the depots.
    """
    cost, time, n_routes = 0, 0, 0
    routes = []
    for subset in subsets:
        result = hgs_solve(coords, demands, capacity, subset, time_limit)
        cost += result.cost
        time += result.time
        n_routes += result.n_routes
        routes.extend(result.routes)
    return cost, time, n_routes, routes
