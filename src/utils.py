import numpy as np
from src.settings import HEIGHT

def safe_eval(expr, x):
    """Evaluate mathematical expression safely"""
    # Replace common math functions with their numpy equivalents
    expr = expr.replace('sin', 'np.sin')
    expr = expr.replace('cos', 'np.cos')
    expr = expr.replace('tan', 'np.tan')
    expr = expr.replace('sqrt', 'np.sqrt')
    expr = expr.replace('abs', 'np.abs')
    expr = expr.replace('^', '**')
    
    try:
        # Create a dictionary with only the allowed variables and functions
        safe_dict = {
            'x': x,
            'np': np,
            'pi': np.pi,
            'e': np.e
        }
        return eval(expr, {"__builtins__": {}}, safe_dict)
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return HEIGHT // 2  # Default value if evaluation fails