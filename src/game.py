import numpy as np
import pygame
from src.settings import *
from src.levels import LEVELS
from src.utils import safe_eval, real_to_screen, screen_to_real

class Game:
    def __init__(self):
        """Initialize game state and objects"""
        # Game state
        self.game_state = STATE_MENU
        self.previous_state = STATE_MENU  # Track where we came from (for help screen)
        self.current_level = 0
        self.unlocked_levels = 1  # Start with only first level unlocked
        
        # Menu navigation
        self.selected_menu_item = 0
        self.menu_items = ["Play", "Level Select", "Help", "Quit"]
        self.selected_level = 0
        
        # Ball settings - now using real coordinates with (0,0) at center
        self.ball_pos = [-350, 0]  # Start position left side in real coordinates
        self.ball_speed = BALL_SPEED
        self.on_path = False
        self.reset_ball = True
        
        # Stars tracking
        self.collected_stars = 0
        self.stars = []
        self.total_stars = 0
        self.level_stats = [{"completed": False, "stars": 0} for _ in LEVELS]
        
        # Equation handling
        self.current_equation = ""
        self.input_active = False
        self.input_text = ""
        
        # Load sounds
        self.load_sounds()
        
        # Load the first level
        self.load_level(0)
    
    def load_sounds(self):
        """Load game sound effects"""
        self.ui_sound = pygame.mixer.Sound(UI_SOUND_PATH)
        self.star_sound = pygame.mixer.Sound(STAR_SOUND_PATH)
        
        # Set volume based on settings
        self.ui_sound.set_volume(SOUND_VOLUME)
        self.star_sound.set_volume(SOUND_VOLUME)
    
    def play_ui_sound(self):
        """Play UI interaction sound"""
        if SOUND_ENABLED:
            self.ui_sound.play()
    
    def play_star_sound(self):
        """Play star collection sound"""
        if SOUND_ENABLED:
            self.star_sound.play()
            
    def show_help(self):
        """Enter help screen and remember where we came from"""
        self.previous_state = self.game_state
        self.game_state = STATE_HELP
        self.play_ui_sound()
    
    def exit_help(self):
        """Return from help screen to previous state"""
        self.game_state = self.previous_state
        self.play_ui_sound()
    
    def load_level(self, level_index):
        """Load a specific level"""
        if 0 <= level_index < len(LEVELS):
            self.current_level = level_index
            self.current_equation = LEVELS[level_index]["equation"]
            self.stars = LEVELS[level_index]["stars"].copy()
            self.total_stars = len(self.stars)
            self.collected_stars = 0
            self.input_text = self.current_equation
            self.reset_ball = True
            
    def path(self, x):
        """Calculate the ball's y position based on the current equation"""
        return safe_eval(self.current_equation, x)
    
    def reset_level(self):
        """Reset the current level to initial state"""
        self.load_level(self.current_level)
        self.game_state = STATE_PLAYING
        self.play_ui_sound()
        
    def next_level(self):
        """Advance to the next level if available"""
        self.play_ui_sound()
        
        if self.current_level + 1 < len(LEVELS):
            # Update level stats first
            self.level_stats[self.current_level]["completed"] = True
            self.level_stats[self.current_level]["stars"] = max(
                self.level_stats[self.current_level]["stars"], 
                self.collected_stars
            )
            
            # Unlock next level if it's not already unlocked
            if self.current_level + 1 >= self.unlocked_levels:
                self.unlocked_levels = self.current_level + 2
            
            # Load the next level
            self.load_level(self.current_level + 1)
            self.game_state = STATE_PLAYING
        else:
            # Return to level select if no more levels
            self.level_stats[self.current_level]["completed"] = True
            self.level_stats[self.current_level]["stars"] = max(
                self.level_stats[self.current_level]["stars"], 
                self.collected_stars
            )
            self.game_state = STATE_LEVEL_SELECT
    
    def move_menu_selection(self, direction):
        """Move the menu selection up or down"""
        self.play_ui_sound()
        
        if self.game_state == STATE_MENU:
            self.selected_menu_item = (self.selected_menu_item + direction) % len(self.menu_items)
        elif self.game_state == STATE_LEVEL_SELECT:
            max_level = min(self.unlocked_levels, len(LEVELS))
            self.selected_level = (self.selected_level + direction) % max_level
    
    def select_menu_item(self):
        """Handle selection in menu"""
        self.play_ui_sound()
        
        if self.game_state == STATE_MENU:
            if self.selected_menu_item == 0:  # Play
                self.load_level(self.current_level)
                self.game_state = STATE_PLAYING
            elif self.selected_menu_item == 1:  # Level Select
                self.game_state = STATE_LEVEL_SELECT
            elif self.selected_menu_item == 2:  # Help
                self.show_help()  # Show help and remember we came from menu
            elif self.selected_menu_item == 3:  # Quit
                return False  # Signal to quit the game
        elif self.game_state == STATE_LEVEL_SELECT:
            self.load_level(self.selected_level)
            self.game_state = STATE_PLAYING
        
        return True  # Continue running the game
        
    def toggle_input(self):
        """Toggle equation input mode"""
        self.play_ui_sound()
        self.input_active = not self.input_active
        self.input_text = self.current_equation
        
    def submit_equation(self):
        """Submit the current input text as the new equation"""
        self.play_ui_sound()
        self.current_equation = self.input_text
        self.input_active = False
        self.reset_ball = True
        
    def handle_backspace(self):
        """Handle backspace key in equation input"""
        if self.input_active:
            self.input_text = self.input_text[:-1]
            
    def add_character(self, char):
        """Add character to equation input"""
        if self.input_active:
            self.input_text += char
    
    def update(self):
        """Update game state - call once per frame"""
        if self.game_state != STATE_PLAYING:
            return
            
        # Reset ball position if needed
        if self.reset_ball:
            try:
                # Start at left side of screen with x = X_MIN + 50
                start_x = X_MIN + 50  # Real x-coordinate for ball start position
                start_y = self.path(start_x)
                self.ball_pos = [start_x, start_y]
                self.ball_speed = BALL_SPEED
                self.on_path = True
                self.reset_ball = False
            except Exception as e:
                self.ball_pos = [X_MIN + 50, 0]  # Default to center height
                self.on_path = True
                self.reset_ball = False

        # Update ball position in real coordinates
        if self.on_path:
            self.ball_pos[0] += self.ball_speed
            try:
                target_y = self.path(self.ball_pos[0])
                # Apply some "gravity" effect to make the ball follow the path smoothly
                self.ball_pos[1] += (target_y - self.ball_pos[1]) * 0.1
            except:
                # If there's an error evaluating the path, let the ball fall
                self.ball_pos[1] -= GRAVITY  # In real coordinates, gravity decreases y
                
            # Check if the ball is out of bounds (in real coordinates)
            if self.ball_pos[0] > X_MAX or self.ball_pos[0] < X_MIN or self.ball_pos[1] > Y_MAX or self.ball_pos[1] < Y_MIN:
                self.reset_ball = True

        # Check if the ball collides with any star (all in real coordinates)
        for star in self.stars[:]:
            if np.sqrt((self.ball_pos[0] - star[0])**2 + (self.ball_pos[1] - star[1])**2) < BALL_RADIUS + 8:
                self.stars.remove(star)  # Remove star if collected
                self.collected_stars += 1
                self.play_star_sound()  # Play star collection sound
                
        # Check if all stars are collected
        if self.collected_stars == self.total_stars and self.total_stars > 0:
            self.game_state = STATE_LEVEL_COMPLETE