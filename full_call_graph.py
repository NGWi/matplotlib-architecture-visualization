import ast
import os
import networkx as nx
import matplotlib.pyplot as plt
import chardet
import pickle

class FunctionCallGraphVisitor(ast.NodeVisitor):
    def __init__(self, graph):
        self.graph = graph
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.graph.add_node(self.current_function)  # Add function as a node
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and self.current_function:
            called_function = node.func.id
            self.graph.add_node(called_function)  # Ensure the called function is a node
            self.graph.add_edge(self.current_function, called_function)  # Create an edge
        self.generic_visit(node)

def find_function_calls_in_file(filepath):
    graph = nx.DiGraph()  # Create a directed graph
    try:
        with open(filepath, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        
        with open(filepath, 'r', encoding=encoding) as file:
            tree = ast.parse(file.read(), filename=filepath)
            visitor = FunctionCallGraphVisitor(graph)
            visitor.visit(tree)
    except (UnicodeDecodeError, SyntaxError, Exception) as e:
        print(f"Error reading {filepath}: {e}")
    
    return graph

def find_calls_in_directory(directory):
    overall_graph = nx.DiGraph()
    for root, dirs, files in os.walk(directory):
        # Ignore .venv directories
        dirs[:] = [d for d in dirs if '.venv' not in d]
        
        for file in files:
            if file.endswith('.py'):  # Ensure only Python files are processed
                filepath = os.path.join(root, file)
                file_graph = find_function_calls_in_file(filepath)
                overall_graph = nx.compose(overall_graph, file_graph)  # Combine graphs
    return overall_graph



# Save the graph to a file
def save_graph(graph, filename):
    with open(filename, 'wb') as f:
        pickle.dump(graph, f)

# Load the graph from a file
def load_graph(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Usage
directory_path = '././matplotlib/lib'
graph_data_filename = 'function_call_data.pkl'

# Check if the graph already exists
if os.path.exists(graph_data_filename):
    call_graph = load_graph(graph_data_filename)
    print("Loaded call graph from file.")
else:
  call_graph = find_calls_in_directory(directory_path)
  save_graph(call_graph, graph_data_filename)
  print("Saved call graph to file.")

# Visualizations:
def visualize_call_graph(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)  # Positions for all nodes
    nx.draw(graph, pos, with_labels=True, arrows=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.title("Function Call Graph")
    plt.show()


def draw_function_call_tree(graph):
    # Create a mapping of layers to nodes
    layers = {}
    for node in graph.nodes():
        # Calculate the depth of each node based on its predecessors
        layer = len(list(graph.predecessors(node)))
        if layer not in layers:
            layers[layer] = []
        layers[layer].append(node)  # Add the node to its corresponding layer

    # Use the layers dictionary as the subset_key
    pos = nx.multipartite_layout(graph, subset_key=layers)

    # Draw the graph
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, arrows=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.title("Function Call Tree")
    plt.show()

def draw_function_call_spring(graph):
    plt.figure(figsize=(12, 8))
    
    # Use a spring layout for better spacing
    pos = nx.spring_layout(graph, k=0.5, iterations=50)
    
    # Draw nodes with different colors based on their degree
    node_color = ['lightblue' if graph.degree(node) < 3 else 'lightcoral' for node in graph.nodes()]
    
    nx.draw(graph, pos, with_labels=True, arrows=True, node_size=2000, node_color=node_color, font_size=10, font_weight='bold')
    
    plt.title("Function Call Tree")
    plt.axis('off')  # Hide the axes
    plt.show()
  
# visualize_call_graph(call_graph)
# draw_function_call_tree(call_graph)
draw_function_call_spring(call_graph)