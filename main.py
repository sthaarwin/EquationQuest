import pygame
import pygame.gfxdraw
import numpy as np
from math import sin, cos, tan, pi
import re
import os

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Equation Quest")

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
title_font = load_font('Arial', 48)
main_font = load_font('Arial', 28)
small_font = load_font('Arial', 22)

# Ball settings
ball_radius = 15
ball_pos = [50, 100]  # Start position left side
ball_speed = 2
gravity = 0.2
on_path = False
collected_stars = 0
total_stars = 0

# Path parameters
current_equation = "0.001*x**2 + 0.1*sin(0.1*x) + 200"
input_active = False
input_text = current_equation

# Stars
stars = [(200, 400), (400, 450), (600, 350), (300, 250), (500, 200)]
total_stars = len(stars)

# Game state
game_state = "playing"  # "playing", "level_complete", "help"

# Function to evaluate mathematical expression safely
def safe_eval(expr, x):
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

# Function to calculate the ball's y position on the path
def path(x):
    return safe_eval(current_equation, x)

# Function to draw the path with neon glow effect
def draw_path():
    x_vals = np.linspace(0, WIDTH, 400)
    
    try:
        y_vals = [path(x) for x in x_vals]
        
        # Draw glow effect (wider line underneath)
        for i in range(len(x_vals) - 1):
            x1, y1 = x_vals[i], y_vals[i]
            x2, y2 = x_vals[i + 1], y_vals[i + 1]
            
            # Convert to pixel coordinates
            screen_x1 = int(x1)
            screen_y1 = int(y1)
            screen_x2 = int(x2)
            screen_y2 = int(y2)
            
            # Draw glow (thick line)
            pygame.draw.line(screen, (*NEON_BLUE[:3], 100), (screen_x1, screen_y1), (screen_x2, screen_y2), 8)
        
        # Draw main line (thin bright line)
        for i in range(len(x_vals) - 1):
            x1, y1 = x_vals[i], y_vals[i]
            x2, y2 = x_vals[i + 1], y_vals[i + 1]
            
            screen_x1 = int(x1)
            screen_y1 = int(y1)
            screen_x2 = int(x2)
            screen_y2 = int(y2)
            
            pygame.draw.line(screen, NEON_BLUE, (screen_x1, screen_y1), (screen_x2, screen_y2), 2)
    except Exception as e:
        print(f"Error drawing path: {e}")

# Function to draw stars with neon glow effect
def draw_stars():
    for star in stars:
        # Draw glow
        for radius in range(15, 5, -3):
            alpha = 50 if radius > 10 else 100
            glow_color = (*NEON_YELLOW[:3], alpha)
            pygame.gfxdraw.filled_circle(screen, star[0], star[1], radius, glow_color)
        
        # Draw main star
        pygame.draw.circle(screen, NEON_YELLOW, star, 8)

# Function to draw the ball with neon glow effect
def draw_ball():
    # Draw glow
    for radius in range(ball_radius + 12, ball_radius, -3):
        alpha = 30 if radius > ball_radius + 6 else 80
        glow_color = (*NEON_PINK[:3], alpha)
        pygame.gfxdraw.filled_circle(screen, int(ball_pos[0]), int(ball_pos[1]), radius, glow_color)
    
    # Draw main ball
    pygame.draw.circle(screen, NEON_PINK, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

# Function to draw text with better readability
def draw_text(text, position, color=NEON_GREEN, font_to_use=main_font, glow_effect=False):
    # Create the main text surface with anti-aliasing
    text_surface = font_to_use.render(text, True, color)
    
    # Only apply glow effect if explicitly requested
    if glow_effect:
        # Single subtle glow with low alpha
        glow_offset = 1
        glow_alpha = 30
        glow_surface = font_to_use.render(text, True, (*color[:3], glow_alpha))
        screen.blit(glow_surface, (position[0] - glow_offset, position[1] - glow_offset))
        screen.blit(glow_surface, (position[0] + glow_offset, position[1] - glow_offset))
        screen.blit(glow_surface, (position[0] - glow_offset, position[1] + glow_offset))
        screen.blit(glow_surface, (position[0] + glow_offset, position[1] + glow_offset))
    
    # Draw the main text for maximum readability
    screen.blit(text_surface, position)
    return text_surface

# Function to draw a modern UI panel
def draw_panel(rect, border_color=NEON_BLUE, fill_color=DARKER_BLUE, alpha=180):
    # Draw semi-transparent background
    s = pygame.Surface((rect[2], rect[3]))
    s.set_alpha(alpha)
    s.fill(fill_color)
    screen.blit(s, (rect[0], rect[1]))
    
    # Draw glowing border
    for i in range(3, 0, -1):
        alpha = 100 if i == 1 else 50
        border_rect = (rect[0] - i, rect[1] - i, rect[2] + i*2, rect[3] + i*2)
        pygame.draw.rect(screen, (*border_color[:3], alpha), border_rect, 1)
    
    # Draw main border
    pygame.draw.rect(screen, border_color, rect, 2)
    
# Draw game UI
def draw_game_ui():
    # Draw top panel for game info
    top_panel = (10, 10, WIDTH - 20, 50)
    draw_panel(top_panel, NEON_PURPLE)
    
    # Draw game title - with glow effect
    draw_text("EQUATION QUEST", (20, 20), NEON_PURPLE, title_font, glow_effect=True)
    
    # Draw star counter with cool icon
    star_icon_pos = (WIDTH - 150, 25)
    pygame.draw.polygon(screen, NEON_YELLOW,
                      [(star_icon_pos[0], star_icon_pos[1] - 10),
                       (star_icon_pos[0] + 3, star_icon_pos[1] - 3),
                       (star_icon_pos[0] + 10, star_icon_pos[1] - 3),
                       (star_icon_pos[0] + 5, star_icon_pos[1] + 3),
                       (star_icon_pos[0] + 7, star_icon_pos[1] + 10),
                       (star_icon_pos[0], star_icon_pos[1] + 6),
                       (star_icon_pos[0] - 7, star_icon_pos[1] + 10),
                       (star_icon_pos[0] - 5, star_icon_pos[1] + 3),
                       (star_icon_pos[0] - 10, star_icon_pos[1] - 3),
                       (star_icon_pos[0] - 3, star_icon_pos[1] - 3)])
    
    # No glow for counters - need to be readable
    draw_text(f"{collected_stars}/{total_stars}", (WIDTH - 120, 20), NEON_YELLOW)

    # Draw equation panel at the bottom
    equation_panel = (10, HEIGHT - 60, WIDTH - 20, 50)
    draw_panel(equation_panel)
    
    if input_active:
        # Draw fancy input box
        input_box = (20, HEIGHT - 50, WIDTH - 40, 30)
        draw_panel(input_box, NEON_GREEN)
        # No glow for equation text - needs to be very readable
        draw_text("f(x) = " + input_text, (30, HEIGHT - 45), NEON_GREEN)
    else:
        # No glow for equation text
        draw_text("Current equation:  f(x) = " + current_equation, (20, HEIGHT - 45), NEON_BLUE)

    # Draw controls helper
    controls_panel = (WIDTH - 200, 75, 190, 120)
    draw_panel(controls_panel, NEON_GREEN)
    # Header with glow, controls without
    draw_text("CONTROLS", (WIDTH - 180, 80), NEON_GREEN, main_font, glow_effect=True)
    draw_text("E - Edit equation", (WIDTH - 190, 110), NEON_GREEN, small_font)
    draw_text("R - Reset level", (WIDTH - 190, 130), NEON_GREEN, small_font)
    draw_text("H - Help screen", (WIDTH - 190, 150), NEON_GREEN, small_font)
    draw_text("ESC - Quit game", (WIDTH - 190, 170), NEON_GREEN, small_font)

# Draw level complete screen
def draw_level_complete():
    panel = (WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2)
    draw_panel(panel, NEON_GREEN)
    
    # Title with glow, other text without
    draw_text("LEVEL COMPLETE!", (WIDTH//4 + 50, HEIGHT//4 + 40), NEON_GREEN, title_font, glow_effect=True)
    draw_text(f"You collected all {total_stars} stars!", (WIDTH//4 + 60, HEIGHT//4 + 100), NEON_YELLOW)
    
    draw_text("Press R to restart level", (WIDTH//4 + 70, HEIGHT//4 + 180), NEON_BLUE)
    draw_text("Press ESC to quit", (WIDTH//4 + 90, HEIGHT//4 + 220), NEON_BLUE)

# Draw help screen
def draw_help_screen():
    panel = (WIDTH//6, HEIGHT//6, WIDTH*2//3, HEIGHT*2//3)
    draw_panel(panel, NEON_PURPLE)
    
    # Title with glow, help text without
    draw_text("HOW TO PLAY", (WIDTH//6 + 100, HEIGHT//6 + 20), NEON_PURPLE, title_font, glow_effect=True)
    
    help_texts = [
        "Guide the glowing ball to collect all stars using math!",
        "Type custom equations to create paths for the ball.",
        "",
        "Example equations to try:",
        "- Simple line: 0.5*x + 100",
        "- Parabola: 0.001*x^2 + 200",
        "- Sine wave: 100*sin(0.01*x) + 300",
        "- Complex: 0.0005*x^2 + 50*sin(0.02*x) + 250"
    ]
    
    y_pos = HEIGHT//6 + 80
    for text in help_texts:
        # No glow for instruction text - must be readable
        draw_text(text, (WIDTH//6 + 40, y_pos), WHITE, small_font)
        y_pos += 30
    
    draw_text("Press any key to return to game", (WIDTH//6 + 80, HEIGHT*5//6 - 40), NEON_BLUE)

# Main loop
running = True
clock = pygame.time.Clock()
reset_ball = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
            elif event.key == pygame.K_RETURN and input_active:
                current_equation = input_text
                input_active = False
                reset_ball = True
                
            elif event.key == pygame.K_e and game_state == "playing":
                input_active = not input_active
                input_text = current_equation
                
            elif event.key == pygame.K_r:
                reset_ball = True
                stars = [(200, 400), (400, 450), (600, 350), (300, 250), (500, 200)]
                total_stars = len(stars)
                collected_stars = 0
                game_state = "playing"
                
            elif event.key == pygame.K_h and game_state == "playing":
                game_state = "help"
                
            elif game_state == "help":
                # Any key returns from help screen
                game_state = "playing"
                
            elif input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Game logic - only update when in playing state
    if game_state == "playing":
        # Reset ball position if needed
        if reset_ball:
            ball_pos = [50, path(50)]
            ball_speed = 2
            on_path = True
            reset_ball = False

        # Update ball position
        if on_path:
            ball_pos[0] += ball_speed
            try:
                target_y = path(ball_pos[0])
                # Apply some "gravity" effect to make the ball follow the path smoothly
                ball_pos[1] += (target_y - ball_pos[1]) * 0.1
            except:
                # If there's an error evaluating the path, let the ball fall
                ball_pos[1] += gravity
                
            # Check if the ball is out of bounds
            if ball_pos[0] > WIDTH or ball_pos[1] > HEIGHT:
                reset_ball = True

        # Check if the ball collides with any star
        for star in stars[:]:
            if np.sqrt((ball_pos[0] - star[0])**2 + (ball_pos[1] - star[1])**2) < ball_radius + 8:
                stars.remove(star)  # Remove star if collected
                collected_stars += 1
                
        # Check if all stars are collected
        if collected_stars == total_stars and total_stars > 0:
            game_state = "level_complete"

    # Draw everything
    screen.fill(DARK_BLUE)
    
    # Draw starfield background
    for i in range(100):
        x = np.random.randint(0, WIDTH)
        y = np.random.randint(0, HEIGHT)
        size = np.random.randint(1, 3)
        brightness = np.random.randint(50, 150)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
    
    # Draw game elements
    if game_state == "playing":
        draw_path()
        draw_stars()
        draw_ball()
        draw_game_ui()
    elif game_state == "level_complete":
        draw_level_complete()
    elif game_state == "help":
        draw_help_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
