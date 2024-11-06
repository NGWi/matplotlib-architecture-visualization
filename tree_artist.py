import json
import os
from graphviz import Source

def create_dot_file(file_path, relationships):
    # Start the DOT file content with a specified size
    dot_content = "digraph G {\n"
    dot_content += '    size="20,20";\n'  # Set the size attribute for the graph
    
    # Iterate over the relationships to create edges
    for parent, child in relationships:
        dot_content += f'    "{parent}" -> "{child}";\n'

    # Close the DOT file
    dot_content += "}\n"
    
    # Write the content to the specified file
    with open(file_path, 'w') as file:
        file.write(dot_content)

def read_relationships_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            relationships = json.load(json_file)
            return relationships
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []

def parse_dot_file(file_path):
    edges = []
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return edges
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                # Check for valid edge format
                if line and '->' in line:
                    parts = line.split('->')
                    if len(parts) == 2:  # Ensure there are exactly two parts
                        parent = parts[0].strip().strip('"')
                        child = parts[1].strip().strip('";')
                        edges.append((parent, child))
                    else:
                        print(f"Invalid edge format: {line}")
    except Exception as e:
        print(f"Error reading file: {e}")

    return edges

def process_edges(edges):
    if edges:  # Check if the list is not empty
        for parent, child in edges:
            print(f"Processing edge from {parent} to {child}")
    else:
        print("No edges to process.")

def visualize_dot_file(dot_file_path):
    # Visualize the DOT file
    try:
        with open(dot_file_path, 'r') as file:
            dot_content = file.read()
            source = Source(dot_content)
            # Render as SVG
            source.render('relationships', format='svg', cleanup=True, engine='dot')  # Generates relationships.svg
            print("Graph visualized and saved as 'relationships.svg'")
    except Exception as e:
        print(f"Error visualizing DOT file: {e}")

def main():
    # Specify the path to your DOT file
    dot_file_path = 'relationships.dot'  # Change the file name as needed

    # Parse the DOT file to get edges
    edges = parse_dot_file(dot_file_path)

    # Print the number of edges found
    print(f"Number of edges found: {len(edges)}")

    # Process the edges
    process_edges(edges)

    # Visualize the DOT file
    visualize_dot_file(dot_file_path)

if __name__ == "__main__":
    # Specify the path for the JSON file containing relationships
    json_file_path = 'matplotlib_graph_data.json'  # Change the file name as needed
    relationships = read_relationships_from_json(json_file_path)

    # Specify the path for the DOT file
    dot_file_path = 'relationships.dot'  # Change the file name as needed
    create_dot_file(dot_file_path, relationships)
    print(f"DOT file created: {dot_file_path}")
    main()
    
# To draw the graph using graphviz layout for a vertical tree
        # plt.figure(figsize=(10, 8))  # Set the figure size
        # pos = nx.nx_agraph.graphviz_layout(G, prog='dot')  # Use 'dot' for hierarchical layout