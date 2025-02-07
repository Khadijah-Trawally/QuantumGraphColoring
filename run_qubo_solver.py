

from qubo_solver import QUBOMatrix, QUBOValidator
from tn_simulation import QUBOSimulation
import math
import os

def main():
    """Generate all graphs first, then load and run QUBO simulation."""

    # Initialize QUBOSimulation
    simulation = QUBOSimulation(lambda1 = 1.5,lambda2 = 2,lambda3 = 1.5, graph_dir="graph_instances")

    # Generate all graphs if they don't exist
    if not os.path.exists("graph_instances") or not os.listdir("graph_instances"):
        print("No graph instances found. Generating all graphs...")
        simulation.generate_graph_instance()
        print("Graph generation complete.")

        # Check if graphs were successfully generated
        if not os.listdir("graph_instances"):
            print("Error: Graphs were not generated correctly. Please check your graph generator.")
            return
    else:
        print("Graph instances already exist. Skipping generation.")
    # Define the single graph instance to load (modify as needed)
    n = 10  # Number of nodes
    c = 5   # Number of colors
    instance_index = 1  # Specific instance index

    try:
        # Load the specified graph instance
        print(f"Loading graph instance: n={n}, c={c}, instance={instance_index}...")
        graph_data = simulation.load_graph_instance(n, c, instance_index)

        # Unpack the graph data
        n, c, edges = graph_data

        # Run the QUBO simulation
        print("Running QUBO simulation on the selected graph...")
        cost, chromatic_number, _ = simulation.run_simulation(
            n=n, c=c, edges=edges, 
            max_bond_dimension=8, transverse_field_ratio=1e9
        )

        # Display results
        print("\nSimulation Result:")
        print(f"n={n}, c={c} → Cost: {cost}, Chromatic Number: {chromatic_number}")

    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


