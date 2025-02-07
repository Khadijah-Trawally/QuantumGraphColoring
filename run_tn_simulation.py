# -*- coding: utf-8 -*-
import os
import math
import json
import matplotlib.pyplot as plt
from tn_simulation import QUBOSimulation


def save_plot(folder, filename):
    """
    Save the current plot to a specified folder and filename.

    :param folder: Folder where the plot will be saved.
    :param filename: Name of the file (including extension, e.g., "plot.png").
    """
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    plt.savefig(filepath)
    print(f"Plot saved to {filepath}")

def main():
    # Parameters
    n_range =   [8] #[4, 8, 16]  
    max_bond_dimensions =  [8] #[4, 8, 16]  
    transverse_field_ratios = [1e9] # [1e9, 1e7, 1e5]  
    probability = 0.5
    output_folder = "plots"
    output_file = "results.json"

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Initialize QUBOSimulation instance
    simulation = QUBOSimulation(probability=probability)

    # Generate graph instances
    simulation.generate_graph_instance()

    # Results container (try loading existing results if any)
    output_path = os.path.join(output_folder, output_file)
    if os.path.exists(output_path):
        with open(output_path, "r") as file:
            results = json.load(file)
    else:
        results = {'max_bond_dimension': {}, 'transverse_field_ratio': {}}

    # Vary max_bond_dimension
    for max_bond_dimension in max_bond_dimensions:
        if max_bond_dimension not in results['max_bond_dimension']:
            results['max_bond_dimension'][max_bond_dimension] = {'chromatic_numbers': [], 'costs': []}

        for n in n_range:
            c = math.ceil(0.5 * n) + 2  # Upper bound on colors
            try:
                # Load graph instance
                _, _, edges = simulation.load_graph_instance(n, c, instance_index=0)

                # Run QUBO simulation
                cost, chromatic_number, _ = simulation.run_simulation(
                    n, c, edges, max_bond_dimension, transverse_field_ratio=1e9
                )
                results['max_bond_dimension'][max_bond_dimension]['chromatic_numbers'].append(chromatic_number)
                results['max_bond_dimension'][max_bond_dimension]['costs'].append(cost)

                # Save results after each iteration
                with open(output_path, "w") as file:
                    json.dump(results, file, indent=4)

            except FileNotFoundError:
                print(f"Graph instance for n={n}, c={c} not found. Skipping.")

    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
