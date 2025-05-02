import pygame
import pygame.gfxdraw
import numpy as np
from src.settings import *
from src.utils import real_to_screen, screen_to_real

def draw_text(screen, text, position, color=NEON_GREEN, font_to_use=MAIN_FONT, glow_effect=False):
    """Draw text with optional glow effect"""
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

def draw_panel(screen, rect, border_color=NEON_BLUE, fill_color=DARKER_BLUE, alpha=180):
    """Draw a modern UI panel with glowing borders"""
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

def draw_path(screen, path_func, color=NEON_BLUE):
    """Draw the equation path with neon glow effect - updated for real coordinates"""
    # Generate x values across the real coordinate space
    x_vals = np.linspace(X_MIN, X_MAX, 400)
    
    try:
        # Calculate y values using the equation function
        y_vals = [path_func(x) for x in x_vals]
        
        # Convert real coordinates to screen coordinates for drawing
        screen_points = [real_to_screen(x_vals[i], y_vals[i]) for i in range(len(x_vals))]
        
        # Draw glow effect (wider line underneath)
        for i in range(len(screen_points) - 1):
            screen_x1, screen_y1 = screen_points[i]
            screen_x2, screen_y2 = screen_points[i + 1]
            
            # Check if points are within screen bounds before drawing
            if (0 <= screen_x1 < WIDTH and 0 <= screen_y1 < HEIGHT and
                0 <= screen_x2 < WIDTH and 0 <= screen_y2 < HEIGHT):
                # Draw glow (thick line)
                pygame.draw.line(screen, (*color[:3], 100), 
                                (int(screen_x1), int(screen_y1)), 
                                (int(screen_x2), int(screen_y2)), 8)
        
        # Draw main line (thin bright line)
        for i in range(len(screen_points) - 1):
            screen_x1, screen_y1 = screen_points[i]
            screen_x2, screen_y2 = screen_points[i + 1]
            
            if (0 <= screen_x1 < WIDTH and 0 <= screen_y1 < HEIGHT and
                0 <= screen_x2 < WIDTH and 0 <= screen_y2 < HEIGHT):
                pygame.draw.line(screen, color, 
                                (int(screen_x1), int(screen_y1)), 
                                (int(screen_x2), int(screen_y2)), 2)
    except Exception as e:
        print(f"Error drawing path: {e}")

def draw_stars(screen, stars):
    """Draw stars with neon glow effect - updated for real coordinates"""
    for star in stars:  # stars are now in real coordinates
        # Convert from real to screen coordinates
        screen_x, screen_y = real_to_screen(star[0], star[1])
        
        # Draw glow
        for radius in range(15, 5, -3):
            alpha = 50 if radius > 10 else 100
            glow_color = (*NEON_YELLOW[:3], alpha)
            pygame.gfxdraw.filled_circle(screen, int(screen_x), int(screen_y), radius, glow_color)
        
        # Draw main star
        pygame.draw.circle(screen, NEON_YELLOW, (int(screen_x), int(screen_y)), 8)

def draw_ball(screen, ball_pos, ball_radius=BALL_RADIUS):
    """Draw the ball with neon glow effect - updated for real coordinates"""
    # Convert from real to screen coordinates
    screen_x, screen_y = real_to_screen(ball_pos[0], ball_pos[1])
    
    # Draw glow
    for radius in range(ball_radius + 12, ball_radius, -3):
        alpha = 30 if radius > ball_radius + 6 else 80
        glow_color = (*NEON_PINK[:3], alpha)
        pygame.gfxdraw.filled_circle(screen, int(screen_x), int(screen_y), radius, glow_color)
    
    # Draw main ball
    pygame.draw.circle(screen, NEON_PINK, (int(screen_x), int(screen_y)), ball_radius)

def draw_game_ui(screen, collected_stars, total_stars, current_equation, input_active, input_text):
    """Draw the main game UI elements"""
    # Draw top panel for game info
    top_panel = (10, 10, WIDTH - 20, 50)
    draw_panel(screen, top_panel, NEON_PURPLE)
    
    # Draw game title - with glow effect
    draw_text(screen, "EQUATION QUEST", (20, 20), NEON_PURPLE, TITLE_FONT, glow_effect=True)
    
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
    draw_text(screen, f"{collected_stars}/{total_stars}", (WIDTH - 120, 20), NEON_YELLOW)

    # Draw equation panel at the bottom
    equation_panel = (10, HEIGHT - 60, WIDTH - 20, 50)
    draw_panel(screen, equation_panel)
    
    if input_active:
        # Draw fancy input box
        input_box = (20, HEIGHT - 50, WIDTH - 40, 30)
        draw_panel(screen, input_box, NEON_GREEN)
        # No glow for equation text - needs to be very readable
        draw_text(screen, "f(x) = " + input_text, (30, HEIGHT - 45), NEON_GREEN)
    else:
        # No glow for equation text
        draw_text(screen, "Current equation:  f(x) = " + current_equation, (20, HEIGHT - 45), NEON_BLUE)

    # Draw controls helper
    controls_panel = (WIDTH - 200, 75, 190, 120)
    draw_panel(screen, controls_panel, NEON_GREEN)
    # Header with glow, controls without
    draw_text(screen, "CONTROLS", (WIDTH - 180, 80), NEON_GREEN, MAIN_FONT, glow_effect=True)
    # Updated to use Ctrl for all controls
    draw_text(screen, "Ctrl+E - Edit equation", (WIDTH - 190, 110), NEON_GREEN, SMALL_FONT)
    draw_text(screen, "Ctrl+R - Reset level", (WIDTH - 190, 130), NEON_GREEN, SMALL_FONT)
    draw_text(screen, "Ctrl+H - Help screen", (WIDTH - 190, 150), NEON_GREEN, SMALL_FONT)
    draw_text(screen, "Ctrl+ESC - Quit game", (WIDTH - 190, 170), NEON_GREEN, SMALL_FONT)

def draw_coordinate_system(screen):
    """Draw coordinate axes to visualize the real coordinate system"""
    # Draw x-axis
    pygame.draw.line(screen, WHITE, (0, ORIGIN_Y), (WIDTH, ORIGIN_Y), 1)
    # Draw y-axis
    pygame.draw.line(screen, WHITE, (ORIGIN_X, 0), (ORIGIN_X, HEIGHT), 1)
    
    # Draw origin point
    pygame.draw.circle(screen, NEON_GREEN, (ORIGIN_X, ORIGIN_Y), 3)
    
    # Draw tick marks and labels
    # X-axis ticks
    for x in range(-300, 301, 100):
        tick_x, tick_y = real_to_screen(x, 0)
        # Draw tick mark
        pygame.draw.line(screen, WHITE, (tick_x, tick_y - 5), (tick_x, tick_y + 5), 1)
        # Draw label
        if x != 0:  # Skip zero to avoid cluttering the origin
            label = SMALL_FONT.render(str(x), True, WHITE)
            screen.blit(label, (tick_x - label.get_width()//2, tick_y + 10))
    
    # Y-axis ticks
    for y in range(-200, 201, 100):
        tick_x, tick_y = real_to_screen(0, y)
        # Draw tick mark
        pygame.draw.line(screen, WHITE, (tick_x - 5, tick_y), (tick_x + 5, tick_y), 1)
        # Draw label
        if y != 0:  # Skip zero to avoid cluttering the origin
            label = SMALL_FONT.render(str(y), True, WHITE)
            screen.blit(label, (tick_x + 10, tick_y - label.get_height()//2))

def draw_level_complete(screen, total_stars):
    """Draw level complete screen"""
    panel = (WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2)
    draw_panel(screen, panel, NEON_GREEN)
    
    # Title with glow, other text without
    draw_text(screen, "LEVEL COMPLETE!", (WIDTH//4 + 50, HEIGHT//4 + 40), NEON_GREEN, TITLE_FONT, glow_effect=True)
    draw_text(screen, f"You collected all {total_stars} stars!", (WIDTH//4 + 60, HEIGHT//4 + 100), NEON_YELLOW)
    
    draw_text(screen, "Press R to restart level", (WIDTH//4 + 70, HEIGHT//4 + 180), NEON_BLUE)
    draw_text(screen, "Press ESC to quit", (WIDTH//4 + 90, HEIGHT//4 + 220), NEON_BLUE)

def draw_help_screen(screen):
    """Draw help screen with instructions - updated for real coordinates"""
    panel = (WIDTH//6, HEIGHT//6, WIDTH*2//3, HEIGHT*2//3)
    draw_panel(screen, panel, NEON_PURPLE)
    
    # Title with glow, help text without
    draw_text(screen, "HOW TO PLAY", (WIDTH//6 + 100, HEIGHT//6 + 20), NEON_PURPLE, TITLE_FONT, glow_effect=True)
    
    help_texts = [
        "Guide the glowing ball to collect all stars using math!",
        "Type custom equations to create paths for the ball.",
        "",
        "The coordinate system uses real mathematical coordinates:",
        "- (0,0) is at the center of the screen",
        "- y increases upward, decreases downward",
        "- x increases rightward, decreases leftward",
        "",
        "Example equations to try:",
        "- Line: 2*x",
        "- Parabola: 0.01*x^2",
        "- Sine wave: 50*sin(0.05*x)",
        "- Complex: 0.01*x^2 + 30*sin(0.1*x)"
    ]
    
    y_pos = HEIGHT//6 + 80
    for text in help_texts:
        # No glow for instruction text - must be readable
        draw_text(screen, text, (WIDTH//6 + 40, y_pos), WHITE, SMALL_FONT)
        y_pos += 30
    
    draw_text(screen, "Press any key to return to game", (WIDTH//6 + 80, HEIGHT*5//6 - 40), NEON_BLUE)

def draw_starfield_background(screen, stars_count=100):
    """Draw a starfield background with random stars"""
    for i in range(stars_count):
        x = np.random.randint(0, WIDTH)
        y = np.random.randint(0, HEIGHT)
        size = np.random.randint(1, 3)
        brightness = np.random.randint(50, 150)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)