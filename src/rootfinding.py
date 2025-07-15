import numpy as np
from typing import Callable, List, Tuple

def bisection_method(f: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> Tuple[float, int, List[float]]:
    """
    Find the root of a function using the bisection method.
    
    Args:
        f: The function to find the root of
        a: Lower bound of the interval
        b: Upper bound of the interval
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        
    Returns:
        Tuple containing (root approximation, number of iterations, list of approximations)
    """
    if f(a) * f(b) > 0:
        raise ValueError("Function must have opposite signs at interval endpoints")
    
    iterations = 0
    approximations = []
    
    while (b - a) / 2 > tol and iterations < max_iter:
        c = (a + b) / 2
        approximations.append(c)
        
        if f(c) == 0:
            return c, iterations, approximations
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
            
        iterations += 1
    
    root = (a + b) / 2
    approximations.append(root)
    return root, iterations, approximations

def newton_raphson(f: Callable[[float], float], df: Callable[[float], float], x0: float, 
                  tol: float = 1e-6, max_iter: int = 100) -> Tuple[float, int, List[float]]:
    """
    Find the root of a function using the Newton-Raphson method.
    
    Args:
        f: The function to find the root of
        df: The derivative of the function
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        
    Returns:
        Tuple containing (root approximation, number of iterations, list of approximations)
    """
    x = x0
    iterations = 0
    approximations = [x0]
    
    while iterations < max_iter:
        # Avoid division by zero
        if abs(df(x)) < 1e-10:
            raise ValueError("Derivative too close to zero")
            
        x_new = x - f(x) / df(x)
        approximations.append(x_new)
        
        if abs(x_new - x) < tol:
            return x_new, iterations, approximations
            
        x = x_new
        iterations += 1
    
    return x, iterations, approximations

def secant_method(f: Callable[[float], float], x0: float, x1: float, 
                 tol: float = 1e-6, max_iter: int = 100) -> Tuple[float, int, List[float]]:
    """
    Find the root of a function using the secant method.
    
    Args:
        f: The function to find the root of
        x0: First initial guess
        x1: Second initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        
    Returns:
        Tuple containing (root approximation, number of iterations, list of approximations)
    """
    iterations = 0
    approximations = [x0, x1]
    
    while iterations < max_iter:
        f_x0 = f(x0)
        f_x1 = f(x1)
        
        # Avoid division by (almost) zero
        if abs(f_x1 - f_x0) < 1e-10:
            raise ValueError("Function values too close, cannot continue secant method")
            
        x_new = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        approximations.append(x_new)
        
        if abs(x_new - x1) < tol:
            return x_new, iterations, approximations
            
        x0 = x1
        x1 = x_new
        iterations += 1
    
    return x1, iterations, approximations

def polynomial_from_points(points: List[Tuple[float, float]]) -> Callable[[float], float]:
    """
    Create a polynomial function that passes through the given points.
    Uses Lagrange interpolation.
    
    Args:
        points: List of (x, y) coordinate pairs
        
    Returns:
        A function representing the polynomial that passes through the points
    """
    def lagrange_polynomial(x):
        n = len(points)
        result = 0.0
        
        for i in range(n):
            xi, yi = points[i]
            term = yi
            
            for j in range(n):
                if i != j:
                    xj, _ = points[j]
                    term *= (x - xj) / (xi - xj)
            
            result += term
        
        return result
    
    return lagrange_polynomial

def find_best_fit(points: List[Tuple[float, float]], method: str = "least_squares", degree: int = 2) -> Callable[[float], float]:
    """
    Find the best fitting curve for the given points.
    
    Args:
        points: List of (x, y) coordinate pairs
        method: Method to use ('least_squares' or 'lagrange')
        degree: Polynomial degree for least squares method
        
    Returns:
        A function representing the best fit curve
    """
    if len(points) < 2:
        raise ValueError("Need at least 2 points to fit a curve")
    
    x_vals = np.array([p[0] for p in points])
    y_vals = np.array([p[1] for p in points])
    
    if method == "lagrange":
        return polynomial_from_points(points)
    else:  # Default to least squares
        # Polynomial fit using least squares
        coefficients = np.polyfit(x_vals, y_vals, degree)
        
        def polynomial(x):
            return np.polyval(coefficients, x)
        
        return polynomial