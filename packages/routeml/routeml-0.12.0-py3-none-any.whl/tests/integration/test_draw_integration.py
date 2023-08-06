import unittest
import numpy as np
import matplotlib.pyplot as plt
from routeml.utils import get_cvrp_problem, routes_to_solution, add_depot_to_routes
from routeml.draw import plot_routes, plot_embeddings, concatenate_images
from routeml.solvers import hgs_solve, hgs_solve_subproblems
import random

class CVRPIntegrationTest(unittest.TestCase):
    def test_solve_and_plot_cvrp(self):
        random.seed(0)

        # Generate a CVRP problem
        num_nodes = 100
        node_coords, demands = get_cvrp_problem(num_nodes)

        # Solve the problem using HGS or any other solver
        result = hgs_solve(node_coords, demands, 50, time_limit=2)
        self.assertTrue(hasattr(result, "cost"))
        self.assertTrue(hasattr(result, "time"))
        self.assertTrue(hasattr(result, "n_routes"))
        self.assertTrue(hasattr(result, "routes"))

        # Obtain the solution routes
        routes = result.routes

        # Plot and save the solution as a PNG file
        fig1_path = plot_routes(routes, node_coords, save_path="test_output/solution.png")

        embeddings = np.random.rand(num_nodes + 1, 20)
        fig2_path = plot_embeddings(routes, embeddings, save_path="test_output/embeddings.png")

        concat_path = concatenate_images([fig1_path, fig2_path], [1, 2], save_path="test_output/concat.png")

        plot_routes(routes, node_coords, save_path="test_output/solution-nolinehaul.png", draw_linehauls=False)
        plot_routes(routes, node_coords, save_path="test_output/solution-onlynodes.png", draw_lines=False)

    def test_solve_and_plot_cvrp_subset(self):
        random.seed(0)

        # Generate a CVRP problem
        num_nodes = 100
        node_coords, demands = get_cvrp_problem(num_nodes)
        self.assertTrue(len(node_coords) == num_nodes + 1)

        subset = [i for i in range(50)]
        result = hgs_solve(node_coords, demands, 50, subset=subset, time_limit=2)

        subset2 = [0] + [i for i in range(50, 101)]
        result2 = hgs_solve(node_coords, demands, 50, subset=subset2, time_limit=2)

        routes = result.routes + result2.routes
        routes = add_depot_to_routes(routes)
        sol = routes_to_solution(routes)
        self.assertTrue(set(sol) == set(range(101)))
        plot_routes(routes, node_coords, save_path="test_output/subset_solution.png")

    def test_solve_and_plot_cvrp_subproblems(self):
        random.seed(0)

        # Generate a CVRP problem
        num_nodes = 100
        node_coords, demands = get_cvrp_problem(num_nodes)

        subset = [i for i in range(50)]
        subset2 = [0] + [i for i in range(50, 101)]

        cost, time, n_routes, routes = hgs_solve_subproblems(node_coords, demands, 50, [subset, subset2], time_limit=1)
        routes = add_depot_to_routes(routes)
        sol = routes_to_solution(routes)
        self.assertTrue(set(sol) == set(range(101)))
        plot_routes(routes, node_coords, save_path="test_output/subset_solution2.png")

if __name__ == '__main__':
    unittest.main()