import pygame
import pygame.gfxdraw
import numpy as np
import math 
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
                                (int(screen_x2), int(screen_y2)), 4)
        
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
    
    # Check if ball is off-screen to avoid overflow errors
    if (screen_x < -100 or screen_x > WIDTH + 100 or 
        screen_y < -100 or screen_y > HEIGHT + 100):
        return  # Don't try to draw the ball if it's far off-screen
    
    # Draw glow using safer pygame.draw.circle
    for radius in range(ball_radius + 12, ball_radius, -3):
        alpha = 30 if radius > ball_radius + 6 else 80
        # Use regular circle drawing which is more robust
        pygame.draw.circle(screen, (*NEON_PINK[:3], alpha), (int(screen_x), int(screen_y)), radius)
    
    # Draw main ball
    pygame.draw.circle(screen, NEON_PINK, (int(screen_x), int(screen_y)), ball_radius)

def draw_game_ui(screen, collected_stars, total_stars, current_equation, input_active, input_text, is_free_mode=False, game=None):
    """Draw the main game UI elements"""
    # Draw top panel for game info
    top_panel = (10, 10, WIDTH - 20, 50)
    draw_panel(screen, top_panel, NEON_PURPLE)
    
    # Draw game title - with glow effect
    draw_text(screen, "EQUATION QUEST", (20, 20), NEON_PURPLE, TITLE_FONT, glow_effect=True)
    
    # For free mode, show "Free Exploration" instead of stars
    if is_free_mode:
        # Draw mode name instead of star counter
        draw_text(screen, "FREE EXPLORATION", (WIDTH - 240, 20), NEON_YELLOW, MAIN_FONT)
    else:
        # Draw star counter with cool icon for normal levels
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

    # Draw controls helper - different for free mode
    if is_free_mode and game:
        # Draw free mode specific UI elements
        draw_free_exploration_ui(screen, game.user_points, game.selected_method, 
                                game.polynomial_degree, game.rootfinding_methods)
    else:
        # Draw challenge mode UI with hint/answer options
        draw_challenge_mode_ui(screen, game)

def draw_free_exploration_ui(screen, user_points, selected_method, polynomial_degree, method_names):
    """Draw UI specific to the free exploration mode"""
    # Draw free mode info panel
    info_panel = (10, 75, 270, 200)
    draw_panel(screen, info_panel, NEON_PURPLE)
    
    # Draw title
    draw_text(screen, "FREE EXPLORATION MODE", (20, 85), NEON_PURPLE, MAIN_FONT, glow_effect=True)
    
    # Draw point counter
    draw_text(screen, f"Points: {len(user_points)}", (20, 120), NEON_YELLOW, SMALL_FONT)
    
    # Draw current method
    method_color = NEON_GREEN
    draw_text(screen, "Fitting Method:", (20, 150), WHITE, SMALL_FONT)
    draw_text(screen, method_names[selected_method], (150, 150), method_color, SMALL_FONT)
    
    # Draw polynomial degree if using least squares
    if selected_method == 0:  # Least Squares
        draw_text(screen, f"Polynomial Degree: {polynomial_degree}", (20, 180), WHITE, SMALL_FONT)
        draw_text(screen, "UP/DOWN to change degree", (20, 200), NEON_BLUE, SMALL_FONT)
    
    # Draw free mode controls panel
    controls_panel = (10, 285, 270, 170)
    draw_panel(screen, controls_panel, NEON_GREEN)
    
    # Draw controls
    draw_text(screen, "FREE MODE CONTROLS", (20, 295), NEON_GREEN, MAIN_FONT, glow_effect=True)
    draw_text(screen, "CLICK - Add point", (20, 330), NEON_GREEN, SMALL_FONT)
    draw_text(screen, "Ctrl+Z - Remove last point", (20, 355), NEON_GREEN, SMALL_FONT)
    draw_text(screen, "Ctrl+C - Clear all points", (20, 380), NEON_GREEN, SMALL_FONT)
    draw_text(screen, "Ctrl+M - Change fitting method", (20, 405), NEON_GREEN, SMALL_FONT)
    draw_text(screen, "Ctrl+E - Custom equation", (20, 430), NEON_GREEN, SMALL_FONT)

def draw_point_coordinates(screen, mouse_pos):
    """Draw the coordinates of the mouse position for precise point placement"""
    # Convert screen coordinates to real coordinates
    real_x, real_y = screen_to_real(mouse_pos[0], mouse_pos[1])
    
    # Format coordinates as text
    coord_text = f"({real_x:.1f}, {real_y:.1f})"
    
    # Draw small panel near mouse cursor
    text_width = SMALL_FONT.size(coord_text)[0]
    panel_rect = (mouse_pos[0] + 15, mouse_pos[1] - 25, text_width + 20, 25)
    draw_panel(screen, panel_rect, NEON_BLUE)
    
    # Draw coordinate text
    draw_text(screen, coord_text, (mouse_pos[0] + 25, mouse_pos[1] - 20), NEON_BLUE, SMALL_FONT)

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
    for x in range(-600, 601, 100):
        tick_x, tick_y = real_to_screen(x, 0)
        # Draw tick mark
        pygame.draw.line(screen, WHITE, (tick_x, tick_y - 5), (tick_x, tick_y + 5), 1)
        # Draw label
        if x != 0:  # Skip zero to avoid cluttering the origin
            label = SMALL_FONT.render(str(x), True, WHITE)
            screen.blit(label, (tick_x - label.get_width()//2, tick_y + 10))
    
    # Y-axis ticks
    for y in range(-400, 400, 100):
        tick_x, tick_y = real_to_screen(0, y)
        # Draw tick mark
        pygame.draw.line(screen, WHITE, (tick_x - 5, tick_y), (tick_x + 5, tick_y), 1)
        # Draw label
        if y != 0:  # Skip zero to avoid cluttering the origin
            label = SMALL_FONT.render(str(y), True, WHITE)
            screen.blit(label, (tick_x + 10, tick_y - label.get_height()//2))

def draw_level_complete(screen, total_stars, next_level_available=True):
    """Draw level complete screen"""
    panel = (WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2)
    draw_panel(screen, panel, NEON_GREEN)
    
    # Title with glow, other text without
    draw_text(screen, "LEVEL COMPLETE!", (WIDTH//4 + 50, HEIGHT//4 + 40), NEON_GREEN, TITLE_FONT, glow_effect=True)
    draw_text(screen, f"You collected all {total_stars} stars!", (WIDTH//4 + 60, HEIGHT//4 + 100), NEON_YELLOW)
    
    # Different options based on whether there's a next level
    if next_level_available:
        draw_text(screen, "Press ENTER for next level", (WIDTH//4 + 70, HEIGHT//4 + 150), NEON_BLUE)
    
    draw_text(screen, "Press Ctrl + R to restart level", (WIDTH//4 + 70, HEIGHT//4 + 190), NEON_BLUE)
    draw_text(screen, "Press ESC for level selection", (WIDTH//4 + 70, HEIGHT//4 + 230), NEON_BLUE)

def draw_level_failed(screen, collected_stars, total_stars):
    """Draw level failed screen similar to level complete screen"""
    panel = (WIDTH//4, HEIGHT//4, WIDTH//2, HEIGHT//2)
    draw_panel(screen, panel, NEON_RED)
    
    # Title with glow, other text without
    draw_text(screen, "LEVEL FAILED!", (WIDTH//4 + 70, HEIGHT//4 + 40), NEON_RED, TITLE_FONT, glow_effect=True)
    draw_text(screen, f"You collected {collected_stars} of {total_stars} stars", (WIDTH//4 + 60, HEIGHT//4 + 100), NEON_YELLOW)
    
    # Options for the player
    draw_text(screen, "Press Ctrl + R to restart level", (WIDTH//4 + 70, HEIGHT//4 + 150), NEON_BLUE)
    draw_text(screen, "Press ESC for level selection", (WIDTH//4 + 70, HEIGHT//4 + 190), NEON_BLUE)
    draw_text(screen, "Try a different equation next time!", (WIDTH//4 + 70, HEIGHT//4 + 230), NEON_GREEN)

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

def draw_main_menu(screen, selected_item, menu_items):
    """Draw the main menu with selection based exactly on the provided screenshot"""
    # Draw title panel with exact dimensions from screenshot
    title_panel = (290, 110, 620, 150)  # Exact position and size to match screenshot
    draw_panel(screen, title_panel, NEON_PURPLE)
    
    # Draw the title text centered in the panel
    title_text = "EQUATION QUEST"
    title_width = TITLE_FONT.size(title_text)[0]
    draw_text(screen, title_text, (600 - title_width//2, 170), NEON_PURPLE, TITLE_FONT)
    
    # Simple decorative line below the title
    line_y = 220
    pygame.draw.line(screen, NEON_PINK, (350, line_y), (850, line_y), 2)
    
    # Draw menu panel with exact dimensions from screenshot - adjusted for 5 menu items
    menu_panel = (290, 300, 620, 280)  # Increased height to accommodate 5 menu items
    draw_panel(screen, menu_panel, NEON_BLUE)
    
    # Menu item positions - adjusted for 5 menu items with proper spacing
    menu_positions = [
        (590, 330),  # Play
        (590, 380),  # Explore (new item)
        (590, 430),  # Level Select
        (590, 480),  # Help
        (590, 530)   # Quit (moved down)
    ]
    
    # Draw each menu item
    for i, item in enumerate(menu_items):
        # Set color based on selection
        color = NEON_GREEN if i == selected_item else WHITE
        
        # Get the exact position from our list
        x_pos, y_pos = menu_positions[i]
        
        # Calculate centered position
        text_width = MAIN_FONT.size(item)[0]
        text_height = MAIN_FONT.size(item)[1]
        centered_x = x_pos - text_width//2
        
        # Draw selection indicator for currently selected item
        if i == selected_item:
            # Draw triangle pointer to the left of the text - PROPERLY CENTERED with text
            # Calculate vertical center of text for arrow positioning
            text_center_y = y_pos + text_height//2
            
            pygame.draw.polygon(screen, NEON_GREEN, 
                              [(centered_x - 30, text_center_y - 8),  # Top point
                               (centered_x - 30, text_center_y + 8),  # Bottom point
                               (centered_x - 10, text_center_y)])     # Right point (pointed end)
            
            # Draw the text without glow for better readability
            draw_text(screen, item, (centered_x, y_pos), color, MAIN_FONT)
        else:
            # Draw normal text
            draw_text(screen, item, (centered_x, y_pos), color, MAIN_FONT)
    
    # Draw controls hint with exact position from screenshot - adjusted for larger menu panel
    controls_panel = (290, 595, 620, 40)  # Moved down to account for taller menu panel
    draw_panel(screen, controls_panel, NEON_BLUE)
    
    # Controls text positioned exactly like screenshot - adjusted for new position
    controls_text = "Use UP/DOWN arrows and ENTER to navigate"
    text_width = SMALL_FONT.size(controls_text)[0]
    draw_text(screen, controls_text, (WIDTH//2 - text_width//2, 608), NEON_BLUE, SMALL_FONT)

def draw_level_select(screen, selected_level, unlocked_levels, level_stats):
    """Draw the level selection screen with proper spacing to avoid overlaps"""
    # Import LEVELS here to avoid circular imports
    from src.levels import LEVELS
    
    # Draw title panel at the top
    title_panel = (WIDTH//4, 50, WIDTH//2, 70)
    draw_panel(screen, title_panel, NEON_GREEN)
    
    # Draw title with glow effect
    title_x = WIDTH//2 - TITLE_FONT.size("SELECT LEVEL")[0]//2  # Center the title
    draw_text(screen, "SELECT LEVEL", (title_x, 65), 
             NEON_GREEN, TITLE_FONT, glow_effect=True)
    
    # Calculate proper spacing for level items
    visible_levels = min(unlocked_levels, len(level_stats))
    item_height = 50  # Height for each level item
    panel_height = visible_levels * item_height + 30  # Add padding
    
    # Draw level selection panel
    level_panel = (WIDTH//4, 140, WIDTH//2, panel_height)
    draw_panel(screen, level_panel, NEON_BLUE)
    
    # Draw level items with proper spacing
    for i in range(visible_levels):
        # Determine color based on selection and completion
        if i == selected_level:
            color = NEON_GREEN  # Selected level but with reduced glow effect
            # Draw softer highlight background for selected level
            highlight_rect = (WIDTH//4 + 5, 150 + i * item_height, WIDTH//2 - 10, item_height - 5)
            s = pygame.Surface((highlight_rect[2], highlight_rect[3]))
            s.set_alpha(40)  # Very subtle highlight
            s.fill(NEON_GREEN)
            screen.blit(s, (highlight_rect[0], highlight_rect[1]))
        elif level_stats[i]["completed"]:
            color = NEON_YELLOW  # Completed level
        else:
            color = WHITE  # Unlocked but not completed
            
        # Calculate vertical position with proper spacing
        y_pos = 155 + i * item_height
        
        # Draw level number and name
        level_text = f"Level {i+1}: {LEVELS[i]['name']}"
        draw_text(screen, level_text, (WIDTH//4 + 25, y_pos), color, MAIN_FONT, 
                 glow_effect=False)  # No glow effect for better readability
        
        # Draw stars if level has been completed
        if level_stats[i]["completed"]:
            stars_text = f"{level_stats[i]['stars']} ★"
            stars_x = WIDTH//4 + WIDTH//2 - 80  # Right-align stars
            draw_text(screen, stars_text, (stars_x, y_pos), NEON_YELLOW, MAIN_FONT)
    
    # Calculate position for locked levels panel
    locked_panel_y = level_panel[1] + level_panel[3] + 20
    
    # Only show locked levels if there are any
    if unlocked_levels < len(level_stats):
        # Calculate height for locked levels panel
        locked_count = min(3, len(level_stats) - unlocked_levels)  # Show up to 3 locked levels
        locked_panel_height = locked_count * 40 + 20
        
        # Draw locked levels panel
        locked_panel = (WIDTH//4, locked_panel_y, WIDTH//2, locked_panel_height)
        draw_panel(screen, locked_panel, (50, 50, 80))  # Darker color for locked panel
        
        # Draw locked level items
        for i in range(unlocked_levels, min(len(level_stats), unlocked_levels + 3)):
            y_pos = locked_panel_y + 20 + (i - unlocked_levels) * 40
            draw_text(screen, f"Level {i+1} (Locked)", (WIDTH//4 + 25, y_pos), 
                     (150, 150, 150), MAIN_FONT)
        
        # Update y-position for back button
        back_y = locked_panel[1] + locked_panel[3] + 20
    else:
        # No locked levels, position back button directly after level panel
        back_y = locked_panel_y
    
    # Draw back button
    back_panel = (WIDTH//4, back_y, WIDTH//2, 60)
    draw_panel(screen, back_panel, NEON_PINK)
    
    # Center back button text
    back_text = "ESC - Return to Main Menu"
    back_x = WIDTH//2 - MAIN_FONT.size(back_text)[0]//2
    draw_text(screen, back_text, (back_x, back_y + 20), NEON_PINK, MAIN_FONT)

def draw_challenge_mode_ui(screen, game):
    """Draw UI specific to challenge mode with hints and answers"""
    if not game:
        return
    
    # Calculate dynamic panel height based on content
    base_height = 140
    hint_height = 0
    answer_height = 0
    
    # Calculate additional height needed for hint
    if game.show_hint:
        hint_text = game.get_current_hint()
        # Better hint text handling for proper wrapping
        max_chars = 30  # Reduced for better fit
        if len(hint_text) > max_chars:
            # If hint needs multiple lines, allocate more space
            hint_lines = [hint_text[i:i+max_chars] for i in range(0, len(hint_text), max_chars)]
            hint_height = min(len(hint_lines), 3) * 20  # Support up to 3 lines
        else:
            hint_height = 20  # 1 line
    
    # Calculate additional height needed for answer
    if game.show_answer:
        answer_height = 20
    
    # Draw challenge mode info panel with dynamic height
    panel_height = base_height + hint_height + answer_height
    info_panel = (10, 75, 280, panel_height)
    draw_panel(screen, info_panel, NEON_PURPLE)
    
    # Draw title
    draw_text(screen, "CHALLENGE MODE", (20, 85), NEON_PURPLE, MAIN_FONT, glow_effect=True)
    
    current_y = 115

    # Only show attempt status if not in level complete/failed state
    # Do not show LEVEL FAILED if all stars are collected
    if game.has_attempted:
        if (
            game.collected_stars < game.total_stars
            and not game.is_free_mode
            and getattr(game, 'game_state', None) not in ('level_complete', 'level_failed', 'LEVEL_COMPLETE', 'LEVEL_FAILED')
        ):
            draw_text(screen, "LEVEL FAILED!", (20, current_y), NEON_RED, SMALL_FONT)
        elif game.collected_stars == game.total_stars:
            draw_text(screen, "Level Complete!", (20, current_y), NEON_GREEN, SMALL_FONT)
        else:
            draw_text(screen, "Attempt Used - One Try Only!", (20, current_y), NEON_RED, SMALL_FONT)
    else:
        draw_text(screen, "One Try Only - Make it count!", (20, current_y), NEON_YELLOW, SMALL_FONT)
    
    current_y += 25
    
    # Show hint if enabled - properly contained within panel
    if game.show_hint:
        hint_text = game.get_current_hint()
        # Improved wrapping for hints to fit within panel width
        max_chars = 30  # Reduced for better fit
        if len(hint_text) > max_chars:
            hint_lines = [hint_text[i:i+max_chars] for i in range(0, len(hint_text), max_chars)]
            for i, line in enumerate(hint_lines[:3]):  # Support up to 3 lines
                prefix = "Hint: " if i == 0 else "      "
                draw_text(screen, f"{prefix}{line}", (20, current_y + i*20), NEON_BLUE, SMALL_FONT)
            current_y += min(len(hint_lines), 3) * 20
        else:
            draw_text(screen, f"Hint: {hint_text}", (20, current_y), NEON_BLUE, SMALL_FONT)
            current_y += 20
    
    # Show answer if enabled - properly contained within panel
    if game.show_answer:
        answer_text = game.get_current_solution()
        # Truncate answer if too long to fit
        max_answer_chars = 25  # Reduced to ensure it fits
        if len(answer_text) > max_answer_chars:
            answer_text = answer_text[:max_answer_chars] + "..."
        draw_text(screen, f"Answer: {answer_text}", (20, current_y), NEON_GREEN, SMALL_FONT)
        current_y += 20
    
    # Draw controls panel - positioned below info panel with gap
    controls_y = info_panel[1] + info_panel[3] + 10
    controls_panel = (10, controls_y, 280, 200)
    draw_panel(screen, controls_panel, NEON_GREEN)
    
    # Draw controls
    control_y = controls_y + 10
    draw_text(screen, "CONTROLS", (20, control_y), NEON_GREEN, MAIN_FONT, glow_effect=True)
    control_y += 30
    draw_text(screen, "Ctrl+E - Edit equation", (20, control_y), NEON_GREEN, SMALL_FONT)
    control_y += 20
    
    # Only show reset if not attempted yet or in free mode
    if not game.has_attempted or game.is_free_mode:
        draw_text(screen, "Ctrl+R - Reset level", (20, control_y), NEON_GREEN, SMALL_FONT)
    else:
        draw_text(screen, "Ctrl+R - Disabled (Used try)", (20, control_y), (100, 100, 100), SMALL_FONT)
    
    control_y += 20
    draw_text(screen, "Ctrl+H - Help screen", (20, control_y), NEON_GREEN, SMALL_FONT)
    control_y += 20
    draw_text(screen, "Ctrl+T - Toggle hint", (20, control_y), NEON_BLUE, SMALL_FONT)
    control_y += 20
    draw_text(screen, "Ctrl+A - Show answer", (20, control_y), NEON_YELLOW, SMALL_FONT)
    control_y += 20
    draw_text(screen, "Ctrl+ESC - Quit game", (20, control_y), NEON_GREEN, SMALL_FONT)
    
    # Add attempt indicator at bottom if used
    if game.has_attempted:
        control_y += 20
        draw_text(screen, "ATTEMPT USED", (20, control_y), NEON_RED, SMALL_FONT)