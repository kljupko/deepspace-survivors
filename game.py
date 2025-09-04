import pygame

from ship import Ship

class Game:
    """Class that represents the game object."""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((100, 500), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        # create the player ship
        self.player_ship = Ship(self.screen)
        # TODO: add ship to group, after adding image loading
    
    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()

            # control the framerate and timing
            self.dt = self.clock.tick(60) / 1000
            # TODO: add a settings variable for the framerate,
            #   avoid hardcoding values
        
        pygame.quit()
    
    def _handle_events(self):
        """Handles user input (or window events too?)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # will probably need to find a more elegant solution for
                # controlling the player ship
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player_ship.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.player_ship.moving_right = True
                if event.key == pygame.K_UP:
                    self.player_ship.moving_up = True
                if event.key == pygame.K_DOWN:
                    self.player_ship.moving_down = True
        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player_ship.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.player_ship.moving_right = False
                if event.key == pygame.K_UP:
                    self.player_ship.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.player_ship.moving_down = False
            
            # handle resizing
            elif event.type == pygame.WINDOWSIZECHANGED:
                self.player_ship.handle_resize(self.screen)
                # TODO: recalculate speed of all game entities
                # TODO: move all game entities to appropriate positions
                
    
    def _update(self):
        """Update the game objects."""
        # TODO: use the group to update the ship
        self.player_ship.update(self.dt)
    
    def _draw(self):
        """Draws to the screen."""
        # first, clear the screen/ fill with background color
        self.screen.fill("purple")

        # handle the rest of the drawing
        # TODO: use the group to draw the ship
        self.player_ship.draw()

        # draw everything to the screen
        pygame.display.flip()