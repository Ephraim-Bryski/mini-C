import ast
import subprocess
from collections import defaultdict

# --- Hardcoded filename of the Python source file to analyze ---
SOURCE_FILE = "compiler.py"
DOT_FILE = "call_graph.dot"
PNG_FILE = "call_graph.png"

exclude_func_names = ["push","pop","sizeof","flatten","get_size"]

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.current_function = None
        self.call_graph = defaultdict(set)
        self.defined_functions = set()

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.defined_functions.add(node.name)
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        # Only log function calls inside defined functions
        if self.current_function:
            # Handle direct function calls
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                # Only record if it's a function (not class constructor) defined in this file
                
                if func_name in self.defined_functions and func_name not in exclude_func_names:
                    self.call_graph[self.current_function].add(func_name)
        self.generic_visit(node)

def generate_dot(call_graph):
    lines = ["digraph CallGraph {", "    rankdir=LR;"]
    for caller, callees in call_graph.items():
        for callee in callees:
            lines.append(f'    "{caller}" -> "{callee}";')
    lines.append("}")
    return "\n".join(lines)

def main():
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=SOURCE_FILE)

    visitor = CallGraphVisitor()
    visitor.visit(tree)

    dot_output = generate_dot(visitor.call_graph)
    with open(DOT_FILE, "w", encoding="utf-8") as f:
        f.write(dot_output)

    # Automatically generate PNG using dot
    try:
        subprocess.run(["dot", "-Tpng", DOT_FILE, "-o", PNG_FILE], check=True)
        print(f"Call graph image generated: {PNG_FILE}")
    except FileNotFoundError:
        print("Graphviz 'dot' not found. Please install Graphviz and ensure 'dot' is in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error running dot: {e}")

if __name__ == "__main__":
    main()
