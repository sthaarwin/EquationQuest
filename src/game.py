import numpy as np
import pygame
from src.settings import *
from src.levels import LEVELS, is_free_level
from src.utils import safe_eval, real_to_screen, screen_to_real
from src.rootfinding import find_best_fit

class Game:
    def __init__(self):
        """Initialize game state and objects"""
        # Game state
        self.game_state = STATE_MENU
        self.previous_state = STATE_MENU  # Track where we came from (for help screen)
        self.current_level = 0
        self.unlocked_levels = 1  # Start with only first level unlocked
        
        # Challenge mode settings
        self.one_try_mode = True  # Enable challenging one-try mode
        self.has_attempted = False  # Track if player has made an attempt
        self.show_answer = False  # Whether to show the solution
        self.show_hint = False   # Whether to show hint
        
        # Menu navigation
        self.selected_menu_item = 0
        self.menu_items = ["Play", "Explore", "Level Select", "Help", "Quit"]
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
        
        # Free exploration mode
        self.is_free_mode = False
        self.user_points = []
        self.fit_method = "least_squares"  # Default fitting method
        self.polynomial_degree = 2  # Default polynomial degree
        self.rootfinding_methods = ["Least Squares", "Lagrange", "Custom"]
        self.selected_method = 0
        
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
            
            # Reset challenge mode flags
            self.has_attempted = False
            self.show_answer = False
            self.show_hint = False
            
            # Check if this is a free exploration level
            self.is_free_mode = is_free_level(LEVELS[level_index])
            if self.is_free_mode:
                self.user_points = []  # Reset user points when entering free mode
                self.selected_method = 0  # Reset to default method
    
    def add_point(self, screen_pos):
        """Add a point at the given screen position (for free exploration mode)"""
        if not self.is_free_mode:
            return
            
        # Convert screen position to real coordinates
        real_x, real_y = screen_to_real(screen_pos[0], screen_pos[1])
        
        # Add to user points
        self.user_points.append((real_x, real_y))
        
        # Sort points by x coordinate for better interpolation
        self.user_points.sort(key=lambda p: p[0])
        
        # Update stars to visualize points
        self.stars = self.user_points.copy()
        
        # Generate equation if we have enough points
        self.generate_equation_from_points()
        
    def remove_last_point(self):
        """Remove the last added point (for free exploration mode)"""
        if not self.is_free_mode or not self.user_points:
            return
            
        self.user_points.pop()
        self.stars = self.user_points.copy()
        
        # Regenerate equation
        self.generate_equation_from_points()
        
    def clear_points(self):
        """Clear all points (for free exploration mode)"""
        if not self.is_free_mode:
            return
            
        self.user_points = []
        self.stars = []
        self.current_equation = "0"  # Reset to flat line
        self.reset_ball = True
        
    def generate_equation_from_points(self):
        """Generate an equation that fits the user points"""
        if len(self.user_points) < 2:
            # Need at least 2 points to generate an equation
            self.current_equation = "0"
            return
        
        try:
            # Get selected method
            method = "least_squares" if self.selected_method == 0 else "lagrange"
            
            # Generate the fitting function
            fit_func = find_best_fit(
                self.user_points, 
                method=method,
                degree=self.polynomial_degree
            )
            
            # Test the function with some values to check it works
            test_x = self.user_points[0][0]
            test_y = fit_func(test_x)
            
            # Create a function string representation for the equation
            if method == "least_squares":
                # For least squares, we can get the polynomial coefficients and format them
                x_vals = np.array([p[0] for p in self.user_points])
                y_vals = np.array([p[1] for p in self.user_points])
                coeffs = np.polyfit(x_vals, y_vals, self.polynomial_degree)
                
                # Format the polynomial equation
                terms = []
                for i, c in enumerate(coeffs):
                    power = len(coeffs) - i - 1
                    if abs(c) < 1e-10:  # Skip near-zero coefficients
                        continue
                    if power == 0:
                        terms.append(f"{c:.6f}".rstrip('0').rstrip('.'))
                    elif power == 1:
                        terms.append(f"{c:.6f}".rstrip('0').rstrip('.') + "*x")
                    else:
                        terms.append(f"{c:.6f}".rstrip('0').rstrip('.') + f"*x^{power}")
                
                self.current_equation = " + ".join(terms).replace("+ -", "- ")
            else:
                # For Lagrange, just show it's a Lagrange polynomial
                point_str = ", ".join([f"({x:.1f},{y:.1f})" for x, y in self.user_points])
                self.current_equation = f"Lagrange polynomial through {point_str}"
            
            # Update the input text in case the user wants to edit
            self.input_text = self.current_equation
            self.reset_ball = True
            
        except Exception as e:
            print(f"Error generating equation: {e}")
            self.current_equation = "0"  # Fallback to a flat line
    
    def cycle_fitting_method(self):
        """Cycle through available fitting methods"""
        if not self.is_free_mode:
            return
            
        self.selected_method = (self.selected_method + 1) % len(self.rootfinding_methods)
        self.play_ui_sound()
        
        # If custom method, enable equation input
        if self.selected_method == 2:  # Custom
            self.toggle_input()
        else:
            # Regenerate equation with new method
            self.generate_equation_from_points()
            
    def change_polynomial_degree(self, change):
        """Change the polynomial degree for least squares fitting"""
        if not self.is_free_mode or self.selected_method != 0:
            return
            
        # Ensure degree is between 1 and 10
        new_degree = max(1, min(10, self.polynomial_degree + change))
        if new_degree != self.polynomial_degree:
            self.polynomial_degree = new_degree
            self.play_ui_sound()
            self.generate_equation_from_points()
    
    def handle_free_mode_keys(self, event):
        """Handle key presses specific to free exploration mode"""
        if not self.is_free_mode:
            return False
            
        if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
            # Clear all points
            self.clear_points()
            return True
            
        elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
            # Remove last point
            self.remove_last_point()
            return True
            
        elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:
            # Cycle through fitting methods
            self.cycle_fitting_method()
            return True
            
        elif event.key == pygame.K_UP:
            # Increase polynomial degree
            self.change_polynomial_degree(1)
            return True
            
        elif event.key == pygame.K_DOWN:
            # Decrease polynomial degree
            self.change_polynomial_degree(-1)
            return True
            
        return False
    
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
            elif self.selected_menu_item == 1:  # Explore
                self.is_free_mode = True
                self.clear_points()  # Clear any existing points
                self.current_equation = "0"  # Reset to flat line
                self.reset_ball = True
                self.game_state = STATE_PLAYING
            elif self.selected_menu_item == 2:  # Level Select
                self.game_state = STATE_LEVEL_SELECT
            elif self.selected_menu_item == 3:  # Help
                self.show_help()  # Show help and remember we came from menu
            elif self.selected_menu_item == 4:  # Quit
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
        
        # Mark that player has attempted in one-try mode
        if self.one_try_mode and not self.is_free_mode:
            self.has_attempted = True
    
    def toggle_hint(self):
        """Toggle hint display"""
        if not self.is_free_mode and self.current_level < len(LEVELS):
            self.show_hint = not self.show_hint
            self.play_ui_sound()
    
    def toggle_answer(self):
        """Toggle answer display"""
        if not self.is_free_mode and self.current_level < len(LEVELS):
            self.show_answer = not self.show_answer
            self.play_ui_sound()
    
    def get_current_hint(self):
        """Get hint for current level"""
        if self.current_level < len(LEVELS) and "hint" in LEVELS[self.current_level]:
            return LEVELS[self.current_level]["hint"]
        return "No hint available"
    
    def get_current_solution(self):
        """Get solution for current level"""
        if self.current_level < len(LEVELS) and "solution" in LEVELS[self.current_level]:
            return LEVELS[self.current_level]["solution"]
        return "No solution available"
    
    def path(self, x):
        """Calculate the y-coordinate for a given x based on the current equation"""
        try:
            return safe_eval(self.current_equation, x)
        except Exception as e:
            # If there's an error, return 0 (flat line)
            print(f"Error evaluating path: {e}")
            return 0
    
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
                
        # Check if all stars are collected (but not in free mode)
        if not self.is_free_mode and self.collected_stars == self.total_stars and self.total_stars > 0:
            self.game_state = STATE_LEVEL_COMPLETE
    
    def handle_backspace(self):
        """Handle backspace key in equation input"""
        if self.input_active:
            self.input_text = self.input_text[:-1]
            
    def add_character(self, char):
        """Add character to equation input"""
        if self.input_active:
            self.input_text += char
