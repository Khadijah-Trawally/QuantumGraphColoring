# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
from tn_simulation import QUBOSimulation
import math 



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
    n_range = [10]
    max_bond_dimensions = [ 8]
    transverse_field_ratios = [1e9]
    probability = 0.5
    output_folder = "plots"

    # Initialize QUBOSimulation instance
    simulation = QUBOSimulation(probability=probability)

    # Results container
    results = {'max_bond_dimension': {}, 'transverse_field_ratio': {}}

    # Vary max_bond_dimension
    for max_bond_dimension in max_bond_dimensions:
        chromatic_numbers = []
        costs = []
        for n in n_range:
            edges = simulation.generate_graph(n)
            cost, chromatic_number, _ = simulation.run_simulation(
                n, n, edges, max_bond_dimension, transverse_field_ratio=1e9
            )
            chromatic_numbers.append(chromatic_number)
            costs.append(cost)
        results['max_bond_dimension'][max_bond_dimension] = {'chromatic_numbers': chromatic_numbers, 'costs': costs}

    # # Vary transverse_field_ratio
    # for transverse_field_ratio in transverse_field_ratios:
    #     chromatic_numbers = []
    #     costs = []
    #     for n in n_range:
    #         edges = simulation.generate_graph(n)
    #         cost, chromatic_number, _ = simulation.run_simulation(
    #             n, n, edges, max_bond_dimension=8, transverse_field_ratio=transverse_field_ratio
    #         )
    #         chromatic_numbers.append(chromatic_number)
    #         costs.append(cost)
    #     results['transverse_field_ratio'][transverse_field_ratio] = {'chromatic_numbers': chromatic_numbers, 'costs': costs}

    # 1. Bar charts for chromatic numbers vs number of qubits (varying max_bond_dimension)
    fig1, axs1 = plt.subplots(2, 2, figsize=(14, 10))
    fig1.suptitle("Chromatic Numbers vs Number of Qubits (Varying Max Bond Dimension)")
    axs1 = axs1.flatten()

    for i, (value, metrics) in enumerate(results['max_bond_dimension'].items()):
        axs1[i].bar(n_range, metrics['chromatic_numbers'], label=f"Max Bond Dim: {value}")
        axs1[i].set_title(f"Max Bond Dimension: {value}")
        axs1[i].set_xlabel("Number of Qubits")
        axs1[i].set_ylabel("Chromatic Numbers")
        axs1[i].legend()
    save_plot(output_folder, "chromatic_numbers_bar_max_bond_dimension.png")
    plt.close(fig1)

    # # 2. Bar charts for chromatic numbers vs number of qubits (varying transverse_field_ratio)
    # fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
    # fig2.suptitle("Chromatic Numbers vs Number of Qubits (Varying Transverse Field Ratio)")
    # axs2 = axs2.flatten()

    # for i, (value, metrics) in enumerate(results['transverse_field_ratio'].items()):
    #     axs2[i].bar(n_range, metrics['chromatic_numbers'], label=f"TFR: {value:.1e}")
    #     axs2[i].set_title(f"Transverse Field Ratio: {value:.1e}")
    #     axs2[i].set_xlabel("Number of Qubits")
    #     axs2[i].set_ylabel("Chromatic Numbers")
    #     axs2[i].legend()
    # save_plot(output_folder, "chromatic_numbers_bar_transverse_field_ratio.png")
    # plt.close(fig2)

    # 3. Line plot for chromatic number vs cost (varying max_bond_dimension)
    fig3, axs3 = plt.subplots(2, 2, figsize=(14, 10))
    fig3.suptitle("Chromatic Numbers vs Cost (Varying Max Bond Dimension)")
    axs3 = axs3.flatten()

    for i, (value, metrics) in enumerate(results['max_bond_dimension'].items()):
        axs3[i].plot(metrics['costs'], metrics['chromatic_numbers'], label=f"Max Bond Dim: {value}", marker='o')
        axs3[i].set_title(f"Max Bond Dimension: {value}")
        axs3[i].set_xlabel("Cost")
        axs3[i].set_ylabel("Chromatic Numbers")
        axs3[i].legend()
    save_plot(output_folder, "chromatic_numbers_vs_cost_max_bond_dimension.png")
    plt.close(fig3)

    # # 4. Line plot for chromatic number vs cost (varying transverse_field_ratio)
    # fig4, axs4 = plt.subplots(2, 2, figsize=(14, 10))
    # fig4.suptitle("Chromatic Numbers vs Cost (Varying Transverse Field Ratio)")
    # axs4 = axs4.flatten()

    # for i, (value, metrics) in enumerate(results['transverse_field_ratio'].items()):
    #     axs4[i].plot(metrics['costs'], metrics['chromatic_numbers'], label=f"TFR: {value:.1e}", marker='o')
    #     axs4[i].set_title(f"TFR: {value:.1e}")
    #     axs4[i].set_xlabel("Cost")
    #     axs4[i].set_ylabel("Chromatic Numbers")
    #     axs4[i].legend()
    # save_plot(output_folder, "chromatic_numbers_vs_cost_transverse_field_ratio.png")
    # plt.close(fig4)

if __name__ == "__main__":
    main()
