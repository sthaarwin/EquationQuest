import numpy as np
from src.settings import *
from src.utils import safe_eval, real_to_screen, screen_to_real

class Game:
    def __init__(self):
        """Initialize game state and objects"""
        # Ball settings - now using real coordinates with (0,0) at center
        self.ball_pos = [-350, 0]  # Start position left side in real coordinates
        self.ball_speed = BALL_SPEED
        self.on_path = False
        self.reset_ball = True
        
        # Game state
        self.collected_stars = 0
        self.stars = DEFAULT_STARS.copy()  # Stars are now in real coordinates
        self.total_stars = len(self.stars)
        self.game_state = STATE_PLAYING
        
        # Equation handling
        self.current_equation = DEFAULT_EQUATION
        self.input_active = False
        self.input_text = self.current_equation
    
    def path(self, x):
        """Calculate the ball's y position based on the current equation"""
        return safe_eval(self.current_equation, x)
    
    def reset_level(self):
        """Reset the game level to initial state"""
        self.reset_ball = True
        self.stars = DEFAULT_STARS.copy()
        self.total_stars = len(self.stars)
        self.collected_stars = 0
        self.game_state = STATE_PLAYING
        
    def toggle_input(self):
        """Toggle equation input mode"""
        self.input_active = not self.input_active
        self.input_text = self.current_equation
        
    def submit_equation(self):
        """Submit the current input text as the new equation"""
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
                self.ball_pos = [start_x, self.path(start_x)]
                self.ball_speed = BALL_SPEED
                self.on_path = True
                self.reset_ball = False
            except Exception as e:
                print(f"Error resetting ball: {e}")
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
                
        # Check if all stars are collected
        if self.collected_stars == self.total_stars and self.total_stars > 0:
            self.game_state = STATE_LEVEL_COMPLETE