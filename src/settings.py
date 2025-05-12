import pygame
from src.levels import get_default_equation, get_default_stars

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Window settings
WIDTH, HEIGHT = 1200, 675
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
STATE_MENU = "menu"
STATE_LEVEL_SELECT = "level_select"
STATE_PLAYING = "playing"
STATE_LEVEL_COMPLETE = "level_complete"
STATE_HELP = "help"

# Ball settings
BALL_RADIUS = 15
BALL_SPEED = 3
GRAVITY = 0.0

# Set initial level equation and stars (backwards compatibility)
DEFAULT_EQUATION = get_default_equation()
DEFAULT_STARS = get_default_stars()

# Sound settings
SOUND_ENABLED = True
SOUND_VOLUME = 0.5  # 0.0 to 1.0
UI_SOUND_PATH = "assets/sfx/ui click.mp3"
STAR_SOUND_PATH = "assets/sfx/star collect.mp3"

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