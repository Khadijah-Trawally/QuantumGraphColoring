# -*- coding: utf-8 -*-

import random
import numpy as np
import time
import os



class QUBOMatrix:
    def __init__(self, n, c, edges, lambda1=4.0, lambda2=10.0, lambda3=10.0):
        """
        Initialize the QUBOMatrix class with problem parameters.
        :param n: Number of nodes
        :param c: Number of colors
        :param edges: List of edges in the graph, where each edge is a tuple (i, j)
        :param lambda1: Penalty for cost function constraints (default: 1.0)
        :param lambda2: Penalty for coloring constraints (default: 10.0)
        :param lambda3: Penalty for adjacency constraints (default: 10.0)
        """
        self.n = n
        self.c = c
        self.edges = edges
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.Q = self.generate_qubo_matrix()

    def generate_qubo_matrix(self):
        """
        Create the symmetric Q matrix for the QUBO formulation of the graph coloring problem.
        :return: Q matrix
        """
        # Initialize the Q matrix
        Q = np.zeros((self.n * self.c + self.c, self.n * self.c + self.c))

        # Minimize chromatic number: Add diagonal entries for y_k
        for k in range(self.c):
            idx_yk = self.n * self.c + k
            Q[idx_yk, idx_yk] += 1.0  # Coefficient to minimize y_k

        # Constraint 1: Ensure y_k >= x_ik
        for i in range(self.n):
            for k in range(self.c):
                idx = i * self.c + k
                idx_yk = self.n * self.c + k
                Q[idx, idx] += self.lambda1  # x_ik^2 term
                Q[idx, idx_yk] -= self.lambda1  # x_ik * y_k cross term
                Q[idx_yk, idx] -= self.lambda1  # Symmetry for cross term

        # Constraint 2: Each node must have exactly one color
        for i in range(self.n):
            for k in range(self.c):
                idx = i * self.c + k
                Q[idx, idx] -= self.lambda2  # Penalty for x_ik
                for k_prime in range(k + 1, self.c):
                    idx_prime = i * self.c + k_prime
                    Q[idx, idx_prime] += self.lambda2  # Cross penalty
                    Q[idx_prime, idx] += self.lambda2  # Symmetry for cross term

        # Constraint 3: Adjacent nodes must have different colors
        for (i, j) in self.edges:
            for k in range(self.c):
                idx_i = i * self.c + k
                idx_j = j * self.c + k
                Q[idx_i, idx_j] += self.lambda3  # Penalty for adjacent nodes
                Q[idx_j, idx_i] += self.lambda3  # Symmetry for cross term

        return Q




class QUBOValidator:
    def __init__(self, n, c, edges, solution):
        """
        Initialize the QUBOValidator class with the solution and graph parameters.
        :param n: Number of nodes
        :param c: Number of colors
        :param edges: List of edges in the graph
        :param solution: Solution vector (binary variables x and y from solver)
        """
        self.n = n
        self.c = c
        self.edges = edges
        self.solution = solution
        self.x = solution[:n * c]  # Extract x_ik variables
        self.y = solution[n * c:]  # Extract y_k variables
        

    def validate_constraints(self):
        """
        Validate the constraints of the QUBO solution.
        :return: True if all constraints are satisfied, otherwise False
        """
        tot_cons = 0
        tot_sat= 0   
        
        # Check Constraint 1: y_k >= x_ik
        for i in range(self.n):
            for k in range(self.c):
                #tot_cons += 1
                idx = i * self.c + k
                if self.x[idx] == 1 and self.y[k] == 0:
                    print(f"Constraint 1 violated: y[{k}] < x[{i},{k}]")
                # else:
                #     #tot_sat += 1
                    return False

        # Check Constraint 2: Each node must have exactly one color
        for i in range(self.n):
            color_sum = sum(self.x[i * self.c + k] for k in range(self.c))
            if color_sum != 1:
                print(f"Constraint 2 violated: Node {i} has {color_sum} colors assigned.")
                return False

        # Check Constraint 3: Adjacent nodes must have different colors
        for (i, j) in self.edges:
            for k in range(self.c):
                idx_i = i * self.c + k
                idx_j = j * self.c + k
                if self.x[idx_i] == 1 and self.x[idx_j] == 1:
                    print(f"Constraint 3 violated: Nodes {i} and {j} share color {k}.")
                    return False

        print("All constraints satisfied.")
        
        return True

    def compute_chromatic_number(self, strict_validation=True):
        """
        Compute the chromatic number from the solution.
        :param strict_validation: If True, enforce that constraints must be satisfied to compute chromatic number.
        :return: Chromatic number if valid, otherwise None
        """
        if strict_validation:
            if not self.validate_constraints():
                print("Chromatic number cannot be computed because constraints are not satisfied.")
                return None
        else:
            # Optionally print violated constraints without enforcing them
            if not self.validate_constraints():
                print("Warning: Constraints are violated, but chromatic number will still be computed.")

        # Compute the chromatic number
        chromatic_number = sum(self.y)
        if not strict_validation:
            print("Warning: Chromatic number computed without strict constraint validation.")

        print(f"Chromatic Number: {chromatic_number}")
        
        return chromatic_number
