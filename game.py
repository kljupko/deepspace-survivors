import pygame

from ship import Ship
from entity import Entity

class Game:
    """Class that represents the game object."""

    def __init__(self):
        """Initialize the core game object."""
        
        pygame.init()

        # --- use in the final version ---
        """ self.native_resolution = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h
        ) """
        # ---

        # --- used for testing ---
        self.native_resolution = (1080, 2340)
        #self.native_resolution = (640, 480)
        # ---

        self._configure_display()

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        # create the player ship
        self.ship = Ship(self.screen)
        # TODO: add ship to group, after adding image loading
    
    def run(self):
        """Run the game loop."""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()

            # control the framerate and timing
            self.dt = self.clock.tick(60) / 1000
            # TODO: add a settings variable for the framerate,
            #   avoid hardcoding values
        
        pygame.quit()
    
    # region DISPLAY HELPER FUNCTIONS
    # -------------------------------------------------------------------

    def _configure_display(self, resolution=None):
        """Scale the display to fit the screen."""

        if resolution is None:
            resolution = self._calculate_render_resolution()

        print(resolution)
        # --- use in the final version ---
        """ 
        self.screen = pygame.display.set_mode(
            resolution,
            pygame.FULLSCREEN | pygame.SCALED
        )
        """
        # ---

        # --- used for testing ---
        self.screen = pygame.display.set_mode(
            resolution,
            pygame.SCALED
        )
        # ---
    
    def _calculate_render_resolution(self, ship_width=24):
        """
        Calculate the resolution that the game will be rendered at.
        Ideal width: 6x width of the player ship (in pixels).
        """

        ideal_width = 6 * ship_width
        min_width = 5 * ship_width

        max_resolution = self.native_resolution
        min_resolution = self.native_resolution

        scale_factor = 1
        while True:
            # search for resolutions close to ideal

            scale_factor += 1
            current_resolution = (
                self.native_resolution[0] / scale_factor,
                self.native_resolution[1] / scale_factor
            )

            if current_resolution[0] < min_width:
                # looped through all possibilities
                    # couldn't find other valid resolutions
                break

            if (not current_resolution[0].is_integer() or
                not current_resolution[1].is_integer()):
                # current resolution not valid
                continue
            
            if current_resolution[0] > ideal_width:
                max_resolution = current_resolution
                continue

            if current_resolution[0] <= ideal_width:
                min_resolution = current_resolution
                break
    
        if max_resolution[0] - ideal_width <= min_resolution[0] - ideal_width:
            return max_resolution
        return min_resolution
    
    # -------------------------------------------------------------------
    # endregion
    
    # region EVENT HANDLING
    # -------------------------------------------------------------------

    def _handle_events(self):
        """Handle user input (or window events too?)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)

            elif event.type == pygame.WINDOWSIZECHANGED:
                self._handle_resize_event()
                
    def _handle_keydown_events(self, event):
        """Handle what happens when certain keys are pressed."""

        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
                
    def _handle_keyup_events(self, event):
        """Handle what happens when certain keys are released."""

        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
    
    def _handle_resize_event(self):
        """Handle what happens when the window is resized."""

        new_res = self._calculate_render_resolution()
        if self.screen.size != new_res:
            self._configure_display(new_res)
        
        # TODO: recalculate speed of all game entities
        # TODO: move all game entities to appropriate positions
        self.ship.handle_resize(self.screen)

    # -------------------------------------------------------------------
    # endregion

    def _update(self):
        """Update the game objects."""
        # TODO: use the group to update the ship
        self.ship.update(self.dt)
    
    def _draw(self):
        """Draw to the screen."""
        # first, clear the screen/ fill with background color
        self.screen.fill("black")

        # handle the rest of the drawing
        # TODO: use the group to draw the ship
        self.ship.draw()

        # draw everything to the screen
        pygame.display.flip()