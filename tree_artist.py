import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
    """
    Main function to draw the tree visualization.
    """
    try:
        # Load JSON data from the file
        with open('./matplotlib_graph_data.json') as f:
            data = json.load(f)  # Load JSON data directly from the file

        # Create a directed graph
        G = nx.DiGraph()

        # Add edges based on the relationships
        for relationship in data:
            if len(relationship) == 2:  # Ensure there are exactly two elements
                parent, child = relationship
                G.add_edge(parent, child)

        # Draw the graph
        plt.figure(figsize=(8, 6))  # Set the figure size
        pos = nx.spring_layout(G)  # positions for all nodes
        nx.draw(G, pos, with_labels=True, arrows=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
        plt.title("Tree Visualization")
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()