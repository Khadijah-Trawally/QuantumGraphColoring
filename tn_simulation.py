# -*- coding: utf-8 -*-
# qubo_simulation.py
import os
import numpy as np
from qtealeaves.optimization import QUBOSolver, QUBOConvergenceParameter
from qtealeaves.tensors import TensorBackend
from qubo_solver import QUBOMatrix, QUBOValidator
from graph_generator import ErdosRenyiGraphGenerator

class QUBOSimulation:
    def __init__(self, lambda1=2, lambda2=2, lambda3=2, probability=0.5, graph_dir='graph_instances'):
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.probability = probability
        self.graph_dir = graph_dir
        self.graph_generator = ErdosRenyiGraphGenerator(
            main_dir=graph_dir, n_range=(4, 50), c_range=None, instances=20, p=probability
        )

    def generate_graph_instance(self):
        '''
        Generates and stores graph instances.
        '''
        print("Generating graph instances...")
        self.graph_generator.generate_and_store_graphs()
        print("All graph instances generated successfully!")

    def load_graph_instance(self, n, c, instance_index=0):
        '''
        Loads a single graph instance.
        '''
        file_path = os.path.join(self.graph_dir, f'n_{n}', f'c_{c}', f'n_{n}_c_{c}_{instance_index}.pkl')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Graph instance {file_path} does not exist.')

        graph_data = self.graph_generator.load_graph(file_path)
        return graph_data['n'], graph_data['c'], graph_data['edges']

    def load_multiple_graphs(self, n_values, c_values, instance_indices=0):
        '''
        Loads multiple stored graph instances.
        '''
        if isinstance(n_values, int):
            n_values = [n_values]
        if isinstance(c_values, int):
            c_values = [c_values]
        if isinstance(instance_indices, int):
            instance_indices = [instance_indices]

        loaded_graphs = []
        for n in n_values:
            for c in c_values:
                for instance_index in instance_indices:
                    try:
                        graph_data = self.load_graph_instance(n, c, instance_index)
                        loaded_graphs.append(graph_data)
                    except FileNotFoundError:
                        print(f'Skipping missing file: n_{n}_c_{c}_{instance_index}.pkl')

        return loaded_graphs

    def run_simulation(self, n, c, edges, max_bond_dimension, transverse_field_ratio):
        """
        Run the QUBO simulation for the given parameters.

        :param n: Number of nodes in the graph.
        :param c: Number of colors (upper bound).
        :param edges: List of edges in the graph.
        :param max_bond_dimension: Maximum bond dimension for the solver.
        :param transverse_field_ratio: Transverse field ratio for the solver.
        :return: Tuple (cost, chromatic_number, time_to_solution).
        """
        # Set lambda values dynamically based on the number of nodes
        self.lambda1 = 0.5 * n
        self.lambda2 = n
        self.lambda3 = 0.5 * n

        # Generate QUBO matrix
        qubo_matrix_obj = QUBOMatrix(n, c, edges, self.lambda1, self.lambda2, self.lambda3)
        qubo_matrix = qubo_matrix_obj.Q

        

        # Initialize solver
        my_solver = QUBOSolver(qubo_matrix)
        
        
        print('Solving the QUBO problem . . . ')

        # Define convergence parameters
        conv_params = QUBOConvergenceParameter(
            max_bond_dimension=max_bond_dimension,
            max_iter=30,
            enable_spacelink_expansion=True,
            transverse_field_ratio=transverse_field_ratio,
            data_type="D",
            optimization_level=3,
            device="cpu",
        )

        # Define tensor backend
        tn_backend = TensorBackend(device="cpu", dtype=np.float64)

        # Solve the QUBO
        my_solver.solve(tn_convergence_parameters=conv_params, tensor_backend=tn_backend)

        # Extract results
        min_cost_idx = my_solver.cost.index(min(my_solver.cost))
        tnn_config = my_solver.solution[min_cost_idx]
        tnn_cost = my_solver.cost[min_cost_idx]
        print(tnn_cost)
        print(tnn_config)
        
        time_to_solution = my_solver.time_to_solution
        print(f' tn solution found in {my_solver.time_to_solution} s')

        # Validate and compute chromatic number
        validator = QUBOValidator(n, c, edges, tnn_config)
        
        chromatic_number = validator.compute_chromatic_number(strict_validation = False)

        return tnn_cost if tnn_cost else None, chromatic_number, time_to_solution


