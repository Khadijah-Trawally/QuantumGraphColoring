# -*- coding: utf-8 -*-
# graph_generator.py
import os
import pickle
import networkx as nx

class ErdosRenyiGraphGenerator:
    '''
    A class to generate, store, and load Erdos-Renyi random graphs.
    '''
    def __init__(self, main_dir='graph_instances', n_range=None, c_range=None, instances=20, p=0.5):
        '''
        Initializes the generator and creates the main directory.
        '''
        self.main_dir = main_dir
        self.n_range = n_range
        self.c_range = c_range
        self.instances = instances
        self.p = p
        os.makedirs(self.main_dir, exist_ok=True)

    def generate_graph(self, n):
        '''
        Generates an Erdos-Renyi random graph.
        '''
        G = nx.erdos_renyi_graph(n, self.p)
        return list(G.edges)

    def generate_and_store_graphs(self):
        '''
        Generates and stores Erdos-Renyi random graphs for different values of n and c.
        '''
        for n in range(self.n_range[0], self.n_range[1] + 1):
            n_dir = os.path.join(self.main_dir, f'n_{n}')
            os.makedirs(n_dir, exist_ok=True)

            c_min = self.c_range[0] if self.c_range else 2
            c_max = self.c_range[1] if self.c_range else n

            for c in range(c_min, c_max + 1):
                c_dir = os.path.join(n_dir, f'c_{c}')
                os.makedirs(c_dir, exist_ok=True)

                for ii in range(self.instances):
                    edges = self.generate_graph(n)
                    graph_data = {'n': n, 'c': c, 'edges': edges}
                    file_name = f'n_{n}_c_{c}_{ii}.pkl'
                    file_path = os.path.join(c_dir, file_name)

                    with open(file_path, 'wb') as f:
                        pickle.dump(graph_data, f)

    def load_graph(self, file_path):
        '''
        Loads a stored graph instance from a pickle file.
        '''
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'The file {file_path} does not exist.')

        with open(file_path, 'rb') as f:
            try:
                graph_data = pickle.load(f)
            except pickle.UnpicklingError:
                raise ValueError(f'The file {file_path} is not a valid pickle file.')

        if not isinstance(graph_data, dict) or 'n' not in graph_data or 'c' not in graph_data or 'edges' not in graph_data:
            raise ValueError(f'The file {file_path} does not contain valid graph data.')

        return graph_data
