import pygame

from ships import Ship
from aliens import Alien
from touch import Touch
from config import Config
from settings import Settings, Controls
from state import State
from ui import TopTray, BottomTray, MainMenu

class Game:
    """Class that represents the game object."""

    def __init__(self):
        """Initialize the core game object."""
        
        pygame.init()

        self.game_running = True

        # --- use in the final version ---
        """ self.native_resolution = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h
        ) """
        # ---

        # --- used for testing ---
        self.native_resolution = (1080, 2340)
        # ---

        self._configure_display()

        self.touch = Touch()
        self.config = Config()
        self.settings = Settings()
        self.controls = Controls()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.state = State()

        self.main_menu = MainMenu(self)
    
    def run(self):
        """Run the game loop."""

        while self.game_running:
            self._handle_events()
            self._update()
            self._draw()

            # control the framerate and timing
            self.dt = self.clock.tick(self.settings.fps) / 1000
        
        pygame.quit()
    
    def start_session(self):
        """Start the session."""

        # TODO: reset the state
        self.state.session_running = True
        self.top_tray = TopTray(self, self.screen.width, 23)
        self.bottom_tray = BottomTray(self, self.screen.width, 50)

        self.play_surf = pygame.Surface((
            self.screen.width,
            self.screen.height - self.bottom_tray.rect.height + 11
        ))
        self.play_rect = self.play_surf.get_rect()

        # create the player ship
        self.ship = Ship(self)
        # TODO: add ship to group, after adding image loading

        # finish setting up the trays
        self.top_tray.complete_init()
        self.top_tray.draw()
        self.bottom_tray.complete_init()
        self.bottom_tray.draw()

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens.add(Alien(self))
        self.powerups = pygame.sprite.Group()

        self.main_menu.hide()
    
    def quit_session(self):
        """Quit the session and return to the main menu."""

        self.state.session_running = False
        # TODO: clear the game objects
        self.main_menu.show()

    # region DISPLAY HELPER FUNCTIONS
    # -------------------------------------------------------------------

    def _configure_display(self, resolution=None):
        """Scale the display to fit the screen."""

        if resolution is None:
            resolution = self._calculate_render_resolution()

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
        """Handle user input and window events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # TODO: prepare the game for quitting
                self.game_running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._handle_keyup_events(event)

            elif event.type == pygame.WINDOWSIZECHANGED:
                self._handle_resize_event()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown_event(event)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouseup_event(event)
            
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mousemove_event(event)
                
    def _handle_keydown_events(self, event):
        """Handle what happens when certain keys are pressed."""

        if event.key == pygame.K_ESCAPE:
            self.quit_session()

        if not self.state.session_running:
            return False

        if event.key == self.controls.move_left:
            self.ship.moving_left = True
        if event.key == self.controls.move_right:
            self.ship.moving_right = True
        if event.key == self.controls.fire:
            self.ship.fire_bullet()
            self.ship.start_ability_charge()

        if event.key == self.controls.active_1:
            self.ship.active_abilities[0].toggle()
        if event.key == self.controls.active_2:
            self.ship.active_abilities[1].toggle()
        if event.key == self.controls.active_3:
            self.ship.active_abilities[2].toggle()
        if event.key == self.controls.passive_1:
            self.ship.passive_abilities[0].toggle()
        if event.key == self.controls.passive_2:
            self.ship.passive_abilities[1].toggle()
        if event.key == self.controls.passive_3:
            self.ship.passive_abilities[2].toggle()
        if event.key == self.controls.passive_4:
            self.ship.passive_abilities[3].toggle()
                
    def _handle_keyup_events(self, event):
        """Handle what happens when certain keys are released."""

        if not self.state.session_running:
            return False

        if event.key == self.controls.move_left:
            self.ship.moving_left = False
        if event.key == self.controls.move_right:
            self.ship.moving_right = False
        if event.key == self.controls.fire:
            self.ship.cancel_ability_charge()
    
    def _handle_resize_event(self):
        """Handle what happens when the window is resized."""

        new_res = self._calculate_render_resolution()
        if self.screen.size != new_res:
            self._configure_display(new_res)
        
        if not self.state.session_running:
            return False
        # TODO: recalculate speed of all game entities
        # TODO: move all game entities to appropriate positions
        self.ship.handle_resize()
        for alien in self.aliens:
            alien.handle_resize()
    
    def _handle_mousedown_event(self, event):
        """
        Handle what happens when the user presses the mouse button.
        A touchscreen touch is interpreted as a mouse click.
        """

        self.touch.register_mousedown_event(event)
        pos = self.touch.current_pos

        if self.touch.touch_start_ts is None:
            return False
        
        if self.main_menu.visible and self.main_menu.focused:
            done = False
            for element in self.main_menu.elements.values():
                if element.rect.collidepoint(pos):
                    element.trigger()
                    done = True
                    break
            return done
        
        if not self.state.session_running:
            return False
        
        if self.top_tray.rect.collidepoint(pos):
            # do nothing when clicking the top tray
            return False
        
        # TODO: find a better way to organize this; a better place
        if self.bottom_tray.rect.collidepoint(pos):
            inner_pos = (
                pos[0],
                pos[1] - self.screen.height + self.bottom_tray.rect.height
            )
            done = False
            for element in self.bottom_tray.elements.values():
                if element.rect.collidepoint(inner_pos):
                    element.trigger()
                    self.bottom_tray.draw() # update
                    done = True
                    break
            return done
        
        # control the ship if nothing else is clicked
        self.ship.fire_bullet()
        self.ship.start_ability_charge()
        self.ship.destination = (
            self.touch.current_pos[0] - self.ship.rect.width/2,
            self.ship.y
        )
    
    def _handle_mouseup_event(self, event):
        """
        Handle what happens when the user releases the mouse button.
        A touchscreen touch is interpreted as a mouse click.
        """

        self.touch.register_mouseup_event()

        if not self.state.session_running:
            return False
        
        self.ship.cancel_ability_charge()
        self.ship.destination = None

    def _handle_mousemove_event(self, event):
        """
        Handle what happens when the user moves the mouse.
        A touchscreen touch is interpreted as a mouse.
        """

        self.touch.register_mousemove_event(event)
        pos = self.touch.current_pos

        if self.touch.touch_start_ts is None:
            return False
        
        if not self.state.session_running:
            return False

        # TODO: make the play area a separate surface to avoid the
        #   nonsense below
        if self.top_tray.rect.collidepoint(pos):
            # do nothing when moving around the top tray
            return False
        if self.bottom_tray.rect.collidepoint(pos):
            # do nothing when moving around the bottom tray
            return False

        # move the ship
        self.ship.destination = (
            pos[0] - self.ship.rect.width/2,
            self.ship.y
        )

    # -------------------------------------------------------------------
    # endregion

    def _update(self):
        """Update the game objects."""

        if self.touch:
            self.touch.track_touch_duration()

        if not self.state.session_running:
            return False
        
        # TODO: move this sessio update logic to a better place (func?)
        self.state.track_duration()
        # TODO: find a better place for the code below?...
        mins, secs = divmod(self.state.session_duration // 1000, 60)
        hours, mins = divmod(mins, 60)
        time = f"{mins:02d}:{secs:02d}"
        if hours > 0:
            time = f"{hours:02d}:" + time
        if self.state.last_second_tracked < self.state.session_duration // 1000:
            self.top_tray.elements["session_duration"].update(time)
            self.state.last_second_tracked = self.state.session_duration // 1000
            self.top_tray.draw()

        # TODO: use the group to update the ship maybe
        self.ship.update(self.dt)
        self.bullets.update(self.dt)
        self.powerups.update(self.dt)
        self.aliens.update(self.dt)
    
    def _draw(self):
        """Draw to the screen."""

        # TODO: organize the session drawing better (func?)
        if self.state.session_running:        
            # first, clear the play surface by drawing the background
            pygame.draw.rect(self.play_surf, "black", self.play_rect)

            # TODO: use an entities group to draw the entities
            self.ship.draw()
            for bullet in self.bullets:
                bullet.draw()
            for powerup in self.powerups:
                powerup.draw()
            for alien in self.aliens:
                alien.draw()
            
            # draw the top and part of bottom tray to the play surface
            self.play_surf.blit(self.top_tray.surface, self.top_tray.rect)
            self.play_surf.blit(self.bottom_tray.surface, (
                0, self.play_rect.height - 11,
                self.bottom_tray.rect.width, self.bottom_tray.rect.height
            ))

            # draw the play surface
            self.screen.blit(self.play_surf)

        self.main_menu.draw()

        # draw everything to the screen
        pygame.display.flip()