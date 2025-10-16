import pygame

from ships import Ship
from aliens import Alien
from touch import Touch
from config import Config
from settings import Settings
from state import State
from progress import Progress
import ui

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
        self.settings = Settings(self)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = 0
        self.state = State()
        self.progress = Progress(self)

        self.menus = {}
        self.menus['main'] = ui.MainMenu(self)
        self.menus['settings'] = ui.SettingsMenu(self)
        self.menus['remap'] = ui.RemapKeyMenu(self)
        self.menus['pause'] = ui.PauseMenu(self)
        
    
    def run(self):
        """Run the game loop."""

        self.menus['main'].open()

        while self.game_running:
            self._handle_events()
            self._update()
            self._draw()

            # control the framerate and timing
            self.dt = self.clock.tick(self.settings.data["fps"]) / 1000
            self.fps = int(self.clock.get_fps())
        
        pygame.quit()
    
    def start_session(self):
        """Start the session."""

        self.state = State()
        self.state.session_running = True
        self.top_tray = ui.TopTray(self, "top_tray", self.screen.width, 23)
        self.bot_tray = ui.BottomTray(self, "bot_tray", self.screen.width, 50)

        self.play_surf = pygame.Surface((
            self.screen.width,
            self.screen.height - self.bot_tray.rect.height + 11
        ))
        self.play_rect = self.play_surf.get_rect()

        # create the player ship
        self.ship = Ship(self)
        # TODO: add ship to group, after adding image loading

        # finish setting up the trays
        self.top_tray.update()
        self.top_tray.draw()
        self.bot_tray.update()
        self.bot_tray.draw()

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens.add(Alien(self))
        self.powerups = pygame.sprite.Group()

        self.menus["main"].close()
    
    def quit_session(self):
        """Quit the session and return to the main menu."""

        self.state.session_running = False

        # update the progress
        self.progress.data['credits'] += self.state.credits_earned
        if self.progress.data['credits'] > self.progress.data['max_credits_owned']:
            self.progress.data['max_credits_owned'] = self.progress.data['credits']
        if self.state.credits_earned > self.progress.data['max_credits_session']:
            self.progress.data['max_credits_session'] = self.state.credits_earned
        self.progress.data['num_of_sessions'] += 1
        if self.state.session_duration > self.progress.data['longest_session']:
            self.progress.data['longest_session'] = self.state.session_duration
        self.progress.data['total_session_duration'] += self.state.session_duration
        self.progress.save_data()

        # TODO: clear the game objects
        self.menus["main"].open()
    
    def quit(self):
        """Handle quitting the game."""

        # TODO: prepare the game for quitting
        if self.state.session_running:
            self.quit_session()
        
        self.game_running = False

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
                self.quit()

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
        
        self.menus['remap'].listen_for_key(event.key)

        if not self.state.session_running:
            return False
        
        if event.key == self.settings.data["key_cancel"]:
            self.menus['pause'].open()

        if event.key == self.settings.data["key_move_left"]:
            self.ship.moving_left = True
        if event.key == self.settings.data["key_move_right"]:
            self.ship.moving_right = True
        if event.key == self.settings.data["key_fire"]:
            self.ship.fire_bullet()
            self.ship.start_ability_charge()

        if event.key == self.settings.data["key_active_1"]:
            self.ship.active_abilities[0].toggle()
        if event.key == self.settings.data["key_active_2"]:
            self.ship.active_abilities[1].toggle()
        if event.key == self.settings.data["key_active_3"]:
            self.ship.active_abilities[2].toggle()
        if event.key == self.settings.data["key_passive_1"]:
            self.ship.passive_abilities[0].toggle()
        if event.key == self.settings.data["key_passive_2"]:
            self.ship.passive_abilities[1].toggle()
        if event.key == self.settings.data["key_passive_3"]:
            self.ship.passive_abilities[2].toggle()
        if event.key == self.settings.data["key_passive_4"]:
            self.ship.passive_abilities[3].toggle()
                
    def _handle_keyup_events(self, event):
        """Handle what happens when certain keys are released."""

        if not self.state.session_running:
            return False

        if event.key == self.settings.data["key_move_left"]:
            self.ship.moving_left = False
        if event.key == self.settings.data["key_move_right"]:
            self.ship.moving_right = False
        if event.key == self.settings.data["key_fire"]:
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

        if self.touch.touch_start_ts is None:
            return False
        
        pos = self.touch.current_pos

        for menu in self.menus.values():
            menu.start_touch(pos)
        
        if not self.state.session_running:
            return False
        
        self.top_tray.start_touch(pos)
        self.top_tray.interact()
        
        # TODO: find a better way to organize this; a better place
        self.bot_tray.start_touch(pos)
        self.bot_tray.interact()
        
        # control the ship if nothing else is clicked
        if pygame.Rect.collidepoint(self.top_tray.rect, pos[0], pos[1]):
            return
        if pygame.Rect.collidepoint(self.bot_tray.rect, pos[0], pos[1]):
            return
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

        for menu in self.menus.values():
            menu.interact()
            menu.end_touch()

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

        for menu in self.menus.values():
            menu.scroll(pos)

        if self.touch.touch_start_ts is None:
            return False
        
        if not self.state.session_running:
            return False

        # TODO: make the play area a separate surface to avoid the
        #   nonsense below
        if self.top_tray.rect.collidepoint(pos):
            # do nothing when moving around the top tray
            return False
        if self.bot_tray.rect.collidepoint(pos):
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
        
        self.state.track_duration()
       
        # update top tray each second
        if self.state.session_duration // 1000 > self.state.last_second_tracked:
            self.top_tray.update()
            self.state.last_second_tracked = self.state.session_duration // 1000

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
            self.play_surf.blit(self.bot_tray.surface, (
                0, self.play_rect.height - 11,
                self.bot_tray.rect.width, self.bot_tray.rect.height
            ))

            # draw the play surface
            self.screen.blit(self.play_surf)

        # draw everything to the screen
        pygame.display.flip()