import pygame

from ship import Ship

class Game:
    """Class that represents the game object."""

    def __init__(self):
        """Initialize the core game object."""
        pygame.init()

        self.screen = pygame.display.set_mode((968, 2376), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        # create the player ship
        self.player_ship = Ship(self.screen)
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
    
    def _handle_events(self):
        """Handle user input (or window events too?)."""
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
                if event.key == pygame.K_SPACE:
                    print("UNFOLDING")
                    # simulating a foldable opening
                    self.screen = pygame.display.set_mode((2160, 1856))
                    new_res = self._calculate_render_resolution()
                    self.screen = pygame.display.set_mode(
                        new_res,
                        pygame.SCALED
                    )
        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player_ship.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.player_ship.moving_right = False
                if event.key == pygame.K_UP:
                    self.player_ship.moving_up = False
                if event.key == pygame.K_DOWN:
                    self.player_ship.moving_down = False
                if event.key == pygame.K_RETURN:
                    print("FOLDING")
                    # simulating a foldable closing
                    self.screen = pygame.display.set_mode((968, 2376))
                    new_res = self._calculate_render_resolution()
                    self.screen = pygame.display.set_mode(
                        new_res,
                        pygame.SCALED
                    )
            
            # handle resizing
            elif event.type == pygame.WINDOWSIZECHANGED:
                new_res = self._calculate_render_resolution()
                if self.screen.size != new_res:
                    self.screen = pygame.display.set_mode(
                        new_res,
                        pygame.SCALED
                    )
                self.player_ship.handle_resize(self.screen)
                # TODO: recalculate speed of all game entities
                # TODO: move all game entities to appropriate positions
                
    def _calculate_render_resolution(self, player_ship_width=24):
        """
        Calculate the resolution that the game will be rendered at.
        Ideal width: 6x width of the player ship (in pixels).
        """
        info = pygame.display.Info()
        native_resolution = info.current_w, info.current_h

        ideal_width = 6 * player_ship_width
        min_width = 5 * player_ship_width

        max_resolution = native_resolution
        min_resolution = native_resolution

        scale_factor = 1
        while True:
            # search for resolutions close to ideal

            scale_factor += 1
            current_resolution = (
                native_resolution[0] / scale_factor,
                native_resolution[1] / scale_factor
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


    def _update(self):
        """Update the game objects."""
        # TODO: use the group to update the ship
        self.player_ship.update(self.dt)
    
    def _draw(self):
        """Draw to the screen."""
        # first, clear the screen/ fill with background color
        self.screen.fill("purple")

        # handle the rest of the drawing
        # TODO: use the group to draw the ship
        self.player_ship.draw()

        # draw everything to the screen
        pygame.display.flip()