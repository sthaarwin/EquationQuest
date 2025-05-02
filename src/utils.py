import numpy as np
from src.settings import HEIGHT, ORIGIN_X, ORIGIN_Y

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

def real_to_screen(x, y):
    """Convert real coordinates to screen coordinates
    In real coordinates: 
    - Origin (0,0) is at center
    - y increases upward
    - x increases rightward
    
    In screen coordinates:
    - Origin (0,0) is top left
    - y increases downward
    - x increases rightward
    """
    screen_x = x + ORIGIN_X
    screen_y = ORIGIN_Y - y  # Flip y-axis
    return screen_x, screen_y

def screen_to_real(screen_x, screen_y):
    """Convert screen coordinates to real coordinates"""
    x = screen_x - ORIGIN_X
    y = ORIGIN_Y - screen_y  # Flip y-axis
    return x, y