"""
Level definitions for Equation Quest
"""

# Level definitions - each level has an equation and star positions
LEVELS = [
    # Level 1: Simple linear function - stars align perfectly on y = 0.5*x
    {
        "name": "Linear Challenge",
        "equation": "0",  # Start with flat line, solution is 0.5*x
        "stars": [(-400, -200), (-200, -100), (0, 0), (200, 100), (400, 200)],
        "solution": "0.5*x",
        "hint": "Try a simple linear equation: y = mx + b"
    },
    # Level 2: Parabola - stars align on y = 0.002*x^2 - 50
    {
        "name": "Parabolic Path",
        "equation": "x*0.001",  # Start with gentle slope, solution is parabola
        "stars": [(-300, 130), (-150, -5), (0, -50), (150, -5), (300, 130)],
        "solution": "0.002*x^2 - 50",
        "hint": "A parabola opening upward: y = ax² + c"
    },
    # Level 3: Sine wave - stars align perfectly on sin wave
    {
        "name": "Sine Wave Master",
        "equation": "50",  # Start with horizontal line, solution is sine wave
        "stars": [(-314, 0), (-157, 100), (0, 0), (157, -100), (314, 0)],
        "solution": "100*sin(x*0.01)",
        "hint": "A trigonometric function: y = A*sin(B*x)"
    },
    # Level 4: Exponential decay - more challenging
    {
        "name": "Exponential Curve",
        "equation": "200 - x*0.1",  # Start with declining line, solution is exponential
        "stars": [(-300, 370), (-150, 240), (0, 150), (150, 93), (300, 58)],
        "solution": "150*exp(-x*0.003)",
        "hint": "An exponential function: y = A*exp(B*x)"
    },
    # Level 5: Complex combination - very challenging
    {
        "name": "Ultimate Challenge",
        "equation": "100 + 0.0005*x*x",  # Start with simple parabola, solution is complex
        "stars": [(-400, 190), (-200, 90), (0, 50), (200, 90), (400, 210)],
        "solution": "0.001*x^2 + 50*sin(x*0.02)",
        "hint": "Combine polynomial and trigonometric: y = ax² + B*sin(C*x)"
    },
    # Level 6: Free Exploration
    {
        "name": "Free Exploration",
        "equation": "0",  # Default equation, will be replaced by user's points
        "stars": [],      # Empty stars, user will add points
        "type": "free"    # Special level type for free exploration
    }
]

def get_default_equation():
    """Get the default equation from the first level"""
    return LEVELS[0]["equation"]

def get_default_stars():
    """Get the default stars from the first level"""
    return LEVELS[0]["stars"].copy()

def is_free_level(level_data):
    """Check if the level is a free exploration level"""
    return level_data.get("type") == "free"