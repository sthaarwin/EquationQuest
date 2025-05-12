"""
Level definitions for Equation Quest
"""

# Level definitions - each level has an equation and star positions
LEVELS = [
    # Level 1: Simple sine wave
    {
        "name": "Sine Wave",
        "equation": "sin(x*0.01)*100",
        "stars": [(-200, 100), (-100, -150), (0, 200), (150, -100), (250, 150)]
    },
    # Level 2: Parabola
    {
        "name": "Parabola",
        "equation": "0.005*x*x",
        "stars": [(-250, 50), (-150, 100), (0, 150), (150, 100), (250, 50)]
    },
    # Level 3: Cubic function
    {
        "name": "Cubic Function",
        "equation": "0.00002*x*x*x",
        "stars": [(-300, -100), (-150, 50), (0, 0), (150, -150), (300, 200)]
    },
    # Level 4: Cosine wave
    {
        "name": "Cosine Wave",
        "equation": "cos(x*0.02)*120",
        "stars": [(-280, 100), (-140, -100), (0, 100), (140, -100), (280, 100)]
    },
    # Level 5: Combined trig
    {
        "name": "Trig Combination",
        "equation": "sin(x*0.01)*100 + cos(x*0.03)*50",
        "stars": [(-250, 0), (-125, 100), (0, -50), (125, 100), (250, -100)]
    }
]

def get_default_equation():
    """Get the default equation from the first level"""
    return LEVELS[0]["equation"]

def get_default_stars():
    """Get the default stars from the first level"""
    return LEVELS[0]["stars"].copy()