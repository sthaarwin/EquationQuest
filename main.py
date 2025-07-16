import pygame
from src.settings import *
from src.utils import safe_eval, screen_to_real
from src.game import Game
from src.levels import LEVELS, is_free_level  # Import is_free_level
from src.ui import (
    draw_text, 
    draw_panel, 
    draw_path, 
    draw_stars, 
    draw_ball,
    draw_game_ui, 
    draw_level_complete, 
    draw_help_screen, 
    draw_starfield_background,
    draw_coordinate_system,
    draw_main_menu,
    draw_level_select,
    draw_point_coordinates  # Import new function
)

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Create game instance
    game = Game()
    
    # Backspace handling variables
    backspace_held = False
    backspace_delay = 500  # Initial delay in ms before rapid deletion starts
    backspace_rate = 50    # Time between deletions in ms during rapid deletion
    backspace_timer = 0
    
    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if in free exploration mode and playing state
                if game.is_free_mode and game.game_state == STATE_PLAYING and event.button == 1:
                    # Add a point at the clicked position
                    game.add_point(mouse_pos)
                
            if event.type == pygame.KEYDOWN:
                # Handle different input based on game state
                if game.game_state == STATE_MENU:
                    if event.key == pygame.K_UP:
                        game.move_menu_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        game.move_menu_selection(1)
                    elif event.key == pygame.K_RETURN:
                        running = game.select_menu_item()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        
                elif game.game_state == STATE_LEVEL_SELECT:
                    if event.key == pygame.K_UP:
                        game.move_menu_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        game.move_menu_selection(1)
                    elif event.key == pygame.K_RETURN:
                        game.select_menu_item()
                    elif event.key == pygame.K_ESCAPE:
                        game.game_state = STATE_MENU
                        
                elif game.game_state == STATE_LEVEL_COMPLETE:
                    if event.key == pygame.K_RETURN:
                        game.next_level()
                    elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        game.reset_level()
                    elif event.key == pygame.K_ESCAPE:
                        game.game_state = STATE_LEVEL_SELECT
                
                elif game.game_state == STATE_PLAYING:
                    # Check for free mode specific keys first
                    if game.handle_free_mode_keys(event):
                        # Key was handled by free mode
                        continue
                        
                    # Normal game controls
                    if event.key == pygame.K_ESCAPE and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        game.game_state = STATE_MENU
                    elif event.key == pygame.K_RETURN and game.input_active:
                        game.submit_equation()
                    elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        game.toggle_input()
                    elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Only allow reset if not attempted yet in challenge mode
                        if not game.has_attempted or game.is_free_mode:
                            game.reset_level()
                    elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        game.show_help()  # Use the show_help function to properly remember the previous state
                    elif event.key == pygame.K_t and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Toggle hint display
                        game.toggle_hint()
                    elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Toggle answer display
                        game.toggle_answer()
                    elif game.input_active:
                        if event.key == pygame.K_BACKSPACE:
                            game.handle_backspace()
                            backspace_held = True
                            backspace_timer = current_time + backspace_delay
                        else:
                            game.add_character(event.unicode)
                
                elif game.game_state == STATE_HELP:
                    # Return to the previous state (menu or playing)
                    game.exit_help()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    backspace_held = False
    
        # Handle continuous backspace when held down
        if backspace_held and game.input_active:
            if current_time >= backspace_timer:
                game.handle_backspace()
                backspace_timer = current_time + backspace_rate
    
        # Update game state
        game.update()
    
        # Draw everything
        screen.fill(DARK_BLUE)
        
        # Draw starfield background
        draw_starfield_background(screen)
        
        # Draw game elements based on state
        if game.game_state == STATE_MENU:
            draw_main_menu(screen, game.selected_menu_item, game.menu_items)
            
        elif game.game_state == STATE_LEVEL_SELECT:
            draw_level_select(screen, game.selected_level, game.unlocked_levels, game.level_stats)
            
        elif game.game_state == STATE_PLAYING:
            # Draw coordinate system
            draw_coordinate_system(screen)
            
            # Draw path, stars and ball
            draw_path(screen, lambda x: game.path(x))  # Pass as a lambda function
            draw_stars(screen, game.stars)
            if not game.is_free_mode:
                draw_ball(screen, game.ball_pos)
            
            # Draw UI elements with free mode indication
            draw_game_ui(screen, game.collected_stars, game.total_stars, 
                        game.current_equation, game.input_active, game.input_text,
                        is_free_mode=game.is_free_mode, game=game)
            
            # In free mode, show the real coordinates near the mouse cursor
            if game.is_free_mode:
                draw_point_coordinates(screen, mouse_pos)
                         
        elif game.game_state == STATE_LEVEL_COMPLETE:
            # Check if there are more levels available
            next_level_available = game.current_level + 1 < len(LEVELS)
            draw_level_complete(screen, game.collected_stars, next_level_available)
            
        elif game.game_state == STATE_HELP:
            draw_help_screen(screen)
    
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
