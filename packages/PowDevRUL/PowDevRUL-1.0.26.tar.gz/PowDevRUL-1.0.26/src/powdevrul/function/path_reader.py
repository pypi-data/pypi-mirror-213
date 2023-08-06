import importlib.util

def import_variables(file_path):
    """
    Import the variables module from a Python file.

    Parameters:
    file_path (str): The path to the Python file.

    Returns:
    module: The imported variables module.
    """
    spec = importlib.util.spec_from_file_location("variables", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



