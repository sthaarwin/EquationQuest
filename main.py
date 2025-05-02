import pygame
from src.settings import *
from src.utils import safe_eval
from src.game import Game
from src.ui import (
    draw_text, 
    draw_panel, 
    draw_path, 
    draw_stars, 
    draw_ball,
    draw_game_ui, 
    draw_level_complete, 
    draw_help_screen, 
    draw_starfield_background
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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                # Changed: All commands now use Ctrl modifier
                if event.key == pygame.K_ESCAPE and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    running = False
                    
                elif event.key == pygame.K_RETURN and game.input_active:
                    game.submit_equation()
                    
                elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_CTRL and game.game_state == STATE_PLAYING:
                    game.toggle_input()
                    
                elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    game.reset_level()
                    
                elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_CTRL and game.game_state == STATE_PLAYING:
                    game.game_state = STATE_HELP
                    
                elif game.game_state == STATE_HELP:
                    # Any key returns from help screen
                    game.game_state = STATE_PLAYING
                    
                elif game.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        game.handle_backspace()
                        backspace_held = True
                        backspace_timer = current_time + backspace_delay
                    else:
                        game.add_character(event.unicode)
            
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
        if game.game_state == STATE_PLAYING:
            draw_path(screen, game.path)
            draw_stars(screen, game.stars)
            draw_ball(screen, game.ball_pos)
            draw_game_ui(screen, game.collected_stars, game.total_stars, 
                         game.current_equation, game.input_active, game.input_text)
                         
        elif game.game_state == STATE_LEVEL_COMPLETE:
            draw_level_complete(screen, game.total_stars)
            
        elif game.game_state == STATE_HELP:
            draw_help_screen(screen)
    
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
