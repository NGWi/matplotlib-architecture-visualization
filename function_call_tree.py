import ast
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def graph_call_tree(start_function, file_path, max_depth=10):
    """
    Graphs the call tree starting from a specified function in a given file.

    Args:
        start_function (str): The name of the function to start from.
        file_path (str): The path to the Python file containing the code.
        max_depth (int): Maximum depth of the call tree to explore.
    """
    # Create a graph
    call_graph = nx.DiGraph()

    # Parse the entire file
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    # Find all function definitions
    function_defs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_defs[node.name] = node

    def get_calls(func_node):
        calls = []
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
        return calls

    # Use a queue for breadth-first exploration
    queue = deque([(start_function, 0)])  # (function_name, depth)
    visited = set()

    while queue:
        func_name, depth = queue.popleft()
        if func_name in visited or depth > max_depth:
            continue
        
        visited.add(func_name)
        call_graph.add_node(func_name)

        if func_name in function_defs:
            calls = get_calls(function_defs[func_name])
            for called_func in calls:
                call_graph.add_edge(func_name, called_func)
                if called_func not in visited:
                    queue.append((called_func, depth + 1))

    # Draw the call tree
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(call_graph)
    nx.draw(call_graph, pos, with_labels=True, node_color="lightblue", 
            node_size=3000, font_size=8, font_weight="bold", 
            arrows=True, arrowsize=5)
    
    # Add labels to the nodes
    labels = nx.get_node_attributes(call_graph, 'name')
    nx.draw_networkx_labels(call_graph, pos, labels, font_size=8)

    plt.title(f"Call Tree for {start_function} (max depth: {max_depth})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
# Updated code to include class and object tracing
def graph_with_classes(start_function, file_path, max_depth=10):
    call_graph = nx.DiGraph()

    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    function_defs = {}
    class_defs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_defs[node.name] = node
        elif isinstance(node, ast.ClassDef):
            class_defs[node.name] = node

    def get_calls(func_node):
        calls = []
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
        return calls

    queue = deque([(start_function, 0)])
    visited = set()

    while queue:
        func_name, depth = queue.popleft()
        if func_name in visited or depth > max_depth:
            continue
        
        visited.add(func_name)
        call_graph.add_node(func_name)

        if func_name in function_defs:
            calls = get_calls(function_defs[func_name])
            for called_func in calls:
                call_graph.add_edge(func_name, called_func)
                if called_func not in visited:
                    queue.append((called_func, depth + 1))
        elif func_name in class_defs:
            call_graph.add_node(func_name, color='green')  # Class nodes in green
            for method in class_defs[func_name].body:
                if isinstance(method, ast.FunctionDef):
                    call_graph.add_node(method.name)
                    call_graph.add_edge(func_name, method.name)

    # Draw the call tree with class nodes in green
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(call_graph)
    node_colors = ['green' if 'color' in call_graph.nodes[node] and call_graph.nodes[node]['color'] == 'green' else 'lightblue' for node in call_graph.nodes]
    nx.draw(call_graph, pos, with_labels=True, node_color=node_colors, 
            node_size=3000, font_size=8, font_weight="bold", 
            arrows=True, arrowsize=20)

    plt.title(f"Call Tree for {start_function} (max depth: {max_depth})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return {
        "filename": file_path,
        "functions": list(function_defs.keys()),
        "classes": list(class_defs.keys())
    }

# Usage
result = graph_with_classes('sci', '././matplotlib/lib/matplotlib/pyplot.py', max_depth=5)
print(result)

# Usage
# graph_call_tree('sci', './matplotlib/lib/matplotlib/pyplot.py')