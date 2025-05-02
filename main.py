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
    
    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                elif event.key == pygame.K_RETURN and game.input_active:
                    game.submit_equation()
                    
                elif event.key == pygame.K_e and game.game_state == STATE_PLAYING:
                    game.toggle_input()
                    
                elif event.key == pygame.K_r:
                    game.reset_level()
                    
                elif event.key == pygame.K_h and game.game_state == STATE_PLAYING:
                    game.game_state = STATE_HELP
                    
                elif game.game_state == STATE_HELP:
                    # Any key returns from help screen
                    game.game_state = STATE_PLAYING
                    
                elif game.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        game.handle_backspace()
                    else:
                        game.add_character(event.unicode)
    
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
