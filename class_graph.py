import ast
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

class FunctionClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()

    def visit_ClassDef(self, node):
        class_name = node.name
        self.graph.add_node(class_name, type='class')
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                function_name = f"{class_name}.{item.name}"
                self.graph.add_node(function_name, type='function')
                self.graph.add_edge(class_name, function_name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        function_name = node.name
        self.graph.add_node(function_name, type='function')
        self.generic_visit(node)

def analyze_directory(directory):
    visitor = FunctionClassVisitor()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=file)
                    visitor.visit(tree)
    return visitor.graph

def save_graph(graph, filename):
    # Save the graph as a list of edges
    edges = list(graph.edges())
    with open(filename, 'w') as f:
        json.dump(edges, f)

def load_graph(filename):
    # Load the graph from a JSON file
    with open(filename, 'r') as f:
        edges = json.load(f)
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    return graph

# Specify the path to the Matplotlib source code
matplotlib_path = './matplotlib/lib'  # Change this to the actual path
graph_data_filename = 'matplotlib_graph_data.json'

# Analyze the codebase and save the graph
if not os.path.exists(graph_data_filename):
    graph = analyze_directory(matplotlib_path)
    save_graph(graph, graph_data_filename)
else:
    graph = load_graph(graph_data_filename)

# Draw the graph with thinner and pale arrows
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='lightblue', 
        font_size=10, font_weight='bold', arrows=True, 
        arrowstyle='-|>', linewidths=0.5, edge_color='lightgray', alpha=0.5)

plt.title("Graph of Matplotlib Classes and Functions Relationships")
plt.show()