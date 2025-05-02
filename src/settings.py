import pygame

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
TITLE = "Equation Quest"

# Coordinate system
# Origin is at the center of the screen
ORIGIN_X = WIDTH // 2
ORIGIN_Y = HEIGHT // 2

# Define coordinate ranges
X_MIN = -ORIGIN_X
X_MAX = WIDTH - ORIGIN_X
Y_MIN = -(HEIGHT - ORIGIN_Y)  # Bottom of screen (negative in real coordinates)
Y_MAX = ORIGIN_Y              # Top of screen (positive in real coordinates)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (5, 5, 20)
DARKER_BLUE = (2, 2, 10)
NEON_BLUE = (30, 144, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 255, 102)
NEON_PURPLE = (180, 30, 255)

# Game states
STATE_PLAYING = "playing"
STATE_LEVEL_COMPLETE = "level_complete"
STATE_HELP = "help"

# Ball settings
BALL_RADIUS = 15
BALL_SPEED = 2
GRAVITY = 0.2

# Initial equation - modified for real coordinates
DEFAULT_EQUATION = "0.01*x**2 - 50*sin(0.05*x)"  # Parabola with sine wave, centered around origin

# Default star positions - now in real coordinates with (0,0) at center
DEFAULT_STARS = [(-200, 100), (-100, -150), (0, 200), (150, -100), (250, 150)]

# Improved font loading
def load_font(font_name, size):
    """Attempt to load a font with fallbacks"""
    try:
        # Try system font by name
        available_fonts = pygame.font.get_fonts()
        
        # Common fallback options
        fallbacks = [
            font_name.lower(),
            'arial',
            'freesans',
            'liberationsans',
            'dejavu',
            'ubuntu',
            None  # None will use the default font
        ]
        
        # Try each font name in the fallbacks list
        for font in fallbacks:
            if font is None:
                return pygame.font.Font(None, size)  # Default pygame font
            
            if font.lower() in available_fonts:
                return pygame.font.SysFont(font, size)
        
        # If we get here, use default
        return pygame.font.Font(None, size)
    except:
        # Last resort
        return pygame.font.Font(None, size)

# Load fonts with proper fallback
TITLE_FONT = load_font('Arial', 48)
MAIN_FONT = load_font('Arial', 28)
SMALL_FONT = load_font('Arial', 22)