"""
Retro Graphics Engine for Space Quest style adventure game
Renders pixel art graphics, UI, and handles game interaction
"""

import pygame
import sys
import math
import random
from enum import Enum

# Game window size
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Retro game area (320x200 scaled 2x)
GAME_WIDTH = 320
GAME_HEIGHT = 200
SCALE = 2

# VGA Color Palette (classic Sierra colors)
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_BLUE = (0, 0, 170)
    LIGHT_BLUE = (85, 85, 255)
    DARK_GREEN = (0, 170, 0)
    LIGHT_GREEN = (85, 255, 85)
    CYAN = (85, 255, 255)
    RED = (170, 0, 0)
    MAGENTA = (170, 85, 255)
    YELLOW = (255, 255, 85)
    GRAY = (170, 170, 170)
    DARK_GRAY = (85, 85, 85)
    BROWN = (170, 85, 0)
    LIGHT_MAGENTA = (255, 85, 255)
    STARFIELD = (0, 0, 50)

class Verb(Enum):
    WALK = 0
    LOOK = 1
    TAKE = 2
    USE = 3
    TALK = 4
    GIVE = 5
    OPEN = 6
    CLOSE = 7
    PUSH = 8
    PULL = 9

VERBS = [Verb.WALK, Verb.LOOK, Verb.TAKE, Verb.USE, Verb.TALK, Verb.GIVE, 
         Verb.OPEN, Verb.CLOSE, Verb.PUSH, Verb.PULL]
VERB_NAMES = ["Walk", "Look", "Take", "Use", "Talk", "Give", "Open", "Close", "Push", "Pull"]

class GraphicsEngine:
    """Main graphics engine for retro adventure game"""
    
    def __init__(self):
        """Initialize the graphics engine"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Quest 4: The Retro Adventure")
        self.clock = pygame.time.Clock()
        
        # Create retro surface (320x200)
        self.retro_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        
        # Game state
        self.player_x = GAME_WIDTH // 2
        self.player_y = GAME_HEIGHT - 50
        self.selected_verb = Verb.WALK
        self.inventory = ["Rubber Chicken", "Decoder Ring"]
        self.current_message = ""
        self.message_timer = 0
        self.animation_frame = 0
        
        # Stars for starfield
        self.stars = [(random.randint(0, GAME_WIDTH), random.randint(0, GAME_HEIGHT)) 
                     for _ in range(50)]
        
        # Humorous messages
        self.messages = [
            "You die horribly!",
            "The laws of physics are not negotiable.",
            "You performed an illegal action.",
            "Press any key to continue.",
            "What are you trying to do?",
            "That doesn't make sense.",
            "I don't understand that.",
            "You can't do that here.",
            "Nothing happens.",
            "You see nothing special.",
            "You have no idea how to use that.",
            "The Sequel Police are after you!",
            "Look behind you! A Three-Toed Sloth!",
            "Ever notice how you're never quite sure?",
            "Good grief!"
        ]
        
    def draw_starfield(self):
        """Draw animated starfield background"""
        self.retro_surface.fill(Color.STARFIELD)
        
        # Draw stars
        for i, (x, y) in enumerate(self.stars):
            brightness = 100 + int(50 * math.sin(self.animation_frame * 0.02 + i))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.retro_surface, color, (x, y), 1)
    
    def draw_player(self):
        """Draw pixel art player character"""
        x, y = self.player_x, self.player_y
        
        # Animation frame (walk cycle)
        frame = (self.animation_frame // 4) % 2
        
        # Draw simple pixel art character (head, body, legs)
        # Head
        pygame.draw.circle(self.retro_surface, Color.YELLOW, (x, y - 8), 3)
        
        # Body
        pygame.draw.line(self.retro_surface, Color.CYAN, (x, y - 5), (x, y + 3), 2)
        
        # Arms (animated)
        if frame == 0:
            pygame.draw.line(self.retro_surface, Color.YELLOW, (x, y - 2), (x - 4, y - 1), 2)
            pygame.draw.line(self.retro_surface, Color.YELLOW, (x, y - 2), (x + 4, y + 1), 2)
        else:
            pygame.draw.line(self.retro_surface, Color.YELLOW, (x, y - 2), (x - 4, y + 1), 2)
            pygame.draw.line(self.retro_surface, Color.YELLOW, (x, y - 2), (x + 4, y - 1), 2)
        
        # Legs (animated)
        if frame == 0:
            pygame.draw.line(self.retro_surface, Color.RED, (x, y + 3), (x - 2, y + 8), 2)
            pygame.draw.line(self.retro_surface, Color.RED, (x, y + 3), (x + 2, y + 8), 2)
        else:
            pygame.draw.line(self.retro_surface, Color.RED, (x, y + 3), (x + 2, y + 8), 2)
            pygame.draw.line(self.retro_surface, Color.RED, (x, y + 3), (x - 2, y + 8), 2)
    
    def draw_ui(self):
        """Draw UI elements (verb panel, inventory)"""
        # Verb panel background
        pygame.draw.rect(self.retro_surface, Color.DARK_BLUE, 
                        (0, GAME_HEIGHT - 30, GAME_WIDTH, 30))
        
        # Draw verbs
        verb_width = GAME_WIDTH // len(VERBS)
        for i, verb in enumerate(VERBS):
            x = i * verb_width
            
            # Highlight selected verb
            if verb == self.selected_verb:
                pygame.draw.rect(self.retro_surface, Color.LIGHT_BLUE, 
                               (x, GAME_HEIGHT - 30, verb_width, 30))
            
            # Draw verb name (simple text rendering)
            verb_text = VERB_NAMES[i]
            # Simplified text - just draw a small indicator
            pygame.draw.rect(self.retro_surface, Color.YELLOW, 
                           (x + 2, GAME_HEIGHT - 28, 3, 3))
        
        # Inventory panel
        pygame.draw.rect(self.retro_surface, Color.DARK_GRAY, 
                        (0, 0, GAME_WIDTH, 15))
        
        # Draw inventory items count
        inv_text = f"Items: {len(self.inventory)}"
        # Simple indicator
        for j in range(len(self.inventory)):
            pygame.draw.circle(self.retro_surface, Color.YELLOW, (j * 10 + 10, 8), 2)
    
    def draw_message(self):
        """Draw current message on screen"""
        if self.message_timer > 0:
            # Draw message box
            msg_width = min(len(self.current_message) * 4 + 10, GAME_WIDTH - 20)
            msg_height = 20
            msg_x = (GAME_WIDTH - msg_width) // 2
            msg_y = 50
            
            pygame.draw.rect(self.retro_surface, Color.BLACK, 
                           (msg_x, msg_y, msg_width, msg_height))
            pygame.draw.rect(self.retro_surface, Color.YELLOW, 
                           (msg_x, msg_y, msg_width, msg_height), 1)
            
            # Draw simple text representation
            for i, char in enumerate(self.current_message[:30]):
                pygame.draw.circle(self.retro_surface, Color.YELLOW, 
                                 (msg_x + 5 + i * 4, msg_y + 10), 1)
    
    def draw_crosshair(self, mouse_x, mouse_y):
        """Draw retro crosshair cursor"""
        # Convert mouse coordinates to retro surface coordinates
        retro_x = mouse_x // SCALE
        retro_y = mouse_y // SCALE
        
        if 0 <= retro_x < GAME_WIDTH and 0 <= retro_y < GAME_HEIGHT:
            # Draw crosshair
            pygame.draw.line(self.retro_surface, Color.LIGHT_GREEN, 
                           (retro_x - 3, retro_y), (retro_x + 3, retro_y), 1)
            pygame.draw.line(self.retro_surface, Color.LIGHT_GREEN, 
                           (retro_x, retro_y - 3), (retro_x, retro_y + 3), 1)
    
    def render(self):
        """Render the game"""
        # Draw game elements
        self.draw_starfield()
        self.draw_player()
        self.draw_ui()
        self.draw_message()
        
        # Get mouse position for crosshair
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.draw_crosshair(mouse_x, mouse_y)
        
        # Scale retro surface to window
        scaled_surface = pygame.transform.scale(self.retro_surface, 
                                               (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))
        
        pygame.display.flip()
    
    def handle_input(self):
        """Handle player input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_UP:
                    self.player_y = max(self.player_y - 3, 10)
                elif event.key == pygame.K_DOWN:
                    self.player_y = min(self.player_y + 3, GAME_HEIGHT - 35)
                elif event.key == pygame.K_LEFT:
                    self.player_x = max(self.player_x - 3, 10)
                elif event.key == pygame.K_RIGHT:
                    self.player_x = min(self.player_x + 3, GAME_WIDTH - 10)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                self.handle_mouse_click(mouse_x, mouse_y)
        
        return True
    
    def handle_mouse_click(self, mouse_x, mouse_y):
        """Handle mouse clicks"""
        # Convert to retro coordinates
        retro_x = mouse_x // SCALE
        retro_y = mouse_y // SCALE
        
        # Check if click is in verb panel
        verb_height = 30
        verb_y_start = GAME_HEIGHT - verb_height
        
        if retro_y >= verb_y_start:
            # Calculate which verb was clicked
            verb_width = GAME_WIDTH // len(VERBS)
            verb_index = retro_x // verb_width
            
            if 0 <= verb_index < len(VERBS):
                self.selected_verb = VERBS[verb_index]
                self.show_message(f">>> {VERB_NAMES[verb_index]}")
        
        # Check if click is in game area
        elif retro_y < GAME_HEIGHT - verb_height:
            self.show_message(random.choice(self.messages))
    
    def show_message(self, message):
        """Display a message"""
        self.current_message = message
        self.message_timer = 60  # Show for 60 frames
    
    def update(self):
        """Update game state"""
        self.animation_frame += 1
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_input()
            self.update()
            self.render()
            self.clock.tick(30)  # 30 FPS for retro feel
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    engine = GraphicsEngine()
    engine.run()
