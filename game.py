import pygame

class Game:
    """Class that represents the game object."""

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            self._handle_events()

            self.update

            self.draw()
        
        pygame.quit()
    
    def _handle_events(self):
        """Handles user input (or window events too?)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def draw(self):
        """Draws to the screen."""
        # first, clear the screen/ fill with background color
        self.screen.fill("purple")

        # handle the rest of the drawing


        # draw everything to the screen
        pygame.display.flip()

        # control the framerate
        self.clock.tick(60)
        # TODO: add a settings variable for the framerate, avoid hardcode
    
    def update(self):
        """Update the game objects."""
        # TODO: do what needs to be done here...