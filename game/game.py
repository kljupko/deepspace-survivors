"""
A module containing the main Game class,
which manages the game as a whole.
"""

import pygame
from pygame import sprite

from .systems import *
from .entities import *
from .input import *
from .ui import menus, trays
from .utils import config, events
from .mechanics import upgrades, rewards

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
        self.settings = Settings(self)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = 0
        self.state = State()
        self._make_upgrades()
        self._make_rewards()
        self.progress = Progress(self)
        self._load_saved_upgrades()
        self._load_saved_rewards()

        self.music_player = MusicPlayer(self)
        self.drop_manager = RandomDropManager(self)

        self._make_menus()

        self.default_ship_class = ships.Ship
        self.ship_class = self.default_ship_class
        # load correct ship class
        for ship_reward in self.toggleable_ships:
            if ship_reward.is_toggled_on:
                # re-toggle to start with the correct ship
                ship_reward.toggle_on()
                break
    
    # region INIT HELPER FUNCTIONS
    # -------------------------------------------------------------------

    def _make_upgrades(self):
        """Set up the upgrades with default values."""

        self.upgrades: dict[str, upgrades.Upgrade] = {
            'hit_points': upgrades.HitPoints(self),
            'thrust': upgrades.Thrust(self),
            'fire_power': upgrades.FirePower(self),
            'fire_rate': upgrades.FireRate(self),
            'active_slots': upgrades.ActiveSlots(self),
            'passive_slots': upgrades.PassiveSlots(self),
            'charge_time': upgrades.ChargeTime(self),
            'luck': upgrades.Luck(self),
        }

    def _make_rewards(self):
        """Set up the rewards with default values."""

        self.rewards: dict[str, rewards.Reward] = {        
            'bakers_dozen': rewards.BakersDozen(self),
            'spear_fish': rewards.SpearFish(self)
        }

        self.toggleable_ships: list[rewards.ToggleableReward] = []
        for reward in self.rewards.values():
            if isinstance(reward, rewards.ToggleableReward):
                self.toggleable_ships.append(reward)

    def _load_saved_upgrades(self):
        """Loads upgrades from self.progress."""

        saved = self.progress.data['upgrades']

        for upgrade in self.upgrades.values():
            if upgrade.name in saved:
                upgrade.level = saved[upgrade.name]['level']

    def _load_saved_rewards(self):
        """Load rewards from self.progress."""

        saved = self.progress.data['rewards']

        for reward in self.rewards.values():
            if reward.name in saved:
                reward.is_unlocked = saved[reward.name]['is_unlocked']
                if isinstance(reward, rewards.ClaimableReward):
                    reward.is_claimed = saved[reward.name]['is_claimed_or_toggled']
                elif isinstance(reward, rewards.ToggleableReward):
                    reward.is_toggled_on = saved[reward.name]['is_claimed_or_toggled']

    def _make_menus(self):
        """Load all the menus."""

        self.menus: menus.MenusDict = {
            'main' : menus.Main(self),
            'upgrade' : menus.Upgrade(self),
            'rewards' : menus.Rewards(self),
            'settings' : menus.Settings(self),
            'remap' : menus.Remap(self),
            'info' : menus.Info(self),
            'pause' : menus.Pause(self),
        }


    # -------------------------------------------------------------------
    # endregion init helper functions
    
    def run(self):
        """Run the game loop."""

        self.menus['main'].open()
        self.music_player.load_sequence("main_menu.json", True)

        while self.game_running:
            self._handle_events()
            self._update()
            self._draw()

            # control the framerate and timing
            self.dt = self.clock.tick(self.settings.data["fps"]) / 1000
            self.fps = int(self.clock.get_fps())
        
        pygame.quit()

    # region GAME FLOW HELPER FUNCTIONS
    # -------------------------------------------------------------------

    def start_session(self):
        """Start the session."""

        self.state = State()
        self.state.session_running = True

        self.play_surf = pygame.Surface((
            self.screen.width, self.screen.height - 28
        ))
        self.play_rect = self.play_surf.get_rect()

        self.ship = self.ship_class(self)
        # TODO: add ship to group, after adding image loading

        self.top_tray = trays.TopTray(self)
        self.top_tray.update()
        self.bot_tray = trays.BottomTray(self)
        self.bot_tray.update()

        self.bullets: sprite.Group[sprite.Sprite] = sprite.Group()
        self.aliens: sprite.Group[sprite.Sprite] = sprite.Group()
        self.powerups: sprite.Group[sprite.Sprite] = sprite.Group()

        self.spawn_manager = SpawnManager(self)

        self.menus['main'].close()
        self.music_player.load_sequence("test.json", True)
    
    def _level_up(self, seconds: int):
        """Increase the level of the game after a period of time."""

        if seconds < 1:
            return False
        
        if seconds % 5 != 0:
            return False
        
        self.state.level += 1
        print("\nLevel:", self.state.level)
        self.spawn_manager.level_up()
        self.spawn_manager.spawn_wave()
    
    def quit_session(self):
        """Quit the session and return to the main menu."""

        self.state.session_running = False
        self.progress.update()

        # check for unlocked rewards
        for reward in self.rewards.values():
            reward.unlock()

        # TODO: clear the game objects ?? (ship can't be None?)
        self.menus['main'].open()
        self.music_player.load_sequence("main_menu.json", True)
    
    def quit(self):
        """Handle quitting the game."""

        # TODO: prepare the game for quitting
        if self.state.session_running:
            self.quit_session()
        
        self.game_running = False
    
    # -------------------------------------------------------------------
    # endregion

    # region DISPLAY HELPER FUNCTIONS
    # -------------------------------------------------------------------

    def _configure_display(self,
                           resolution: tuple[int, int] | None = None
                           ) -> None:
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
    
    def _calculate_render_resolution(self,
                                     ship_width: int = 24
                                     ) -> tuple[int, int]:
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
            
            # ensure integers
            res_x = int(current_resolution[0])
            res_y = int(current_resolution[1])

            if current_resolution[0] > ideal_width:
                max_resolution = (res_x, res_y)
                continue

            if current_resolution[0] <= ideal_width:
                min_resolution = (res_x, res_y)
                break
    
        if max_resolution[0] - ideal_width <= min_resolution[0] - ideal_width:
            return max_resolution
        return min_resolution
    
    # -------------------------------------------------------------------
    # endregion
    
    # region EVENT HANDLING FUNCTIONS
    # -------------------------------------------------------------------

    def _handle_events(self):
        """Handle user input and window events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            
            elif event.type == events.MUSIC_STEP_FINISHED:
                self.music_player.update()

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
            
            elif event.type == pygame.MOUSEWHEEL:
                self._handle_mousewheel_event(event)
            
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mousemove_event(event)
                
    def _handle_keydown_events(self, event: pygame.Event):
        """Handle what happens when certain keys are pressed."""
        
        self.menus['remap'].listen_for_key(event.key)

        if not self.state.session_running:
            return
        
        if event.key == self.settings.data['keybinds']['cancel'].keycode:
            self.menus['pause'].open()

        if event.key == self.settings.data['keybinds']['move_left'].keycode:
            self.ship.moving_left = True
        if event.key == self.settings.data['keybinds']['move_right'].keycode:
            self.ship.moving_right = True
        if event.key == self.settings.data['keybinds']['fire'].keycode:
            self.ship.fire_bullet()
            self.ship.start_ability_charge()

        if event.key == self.settings.data['keybinds']['active_1'].keycode:
            self.ship.ability_slots['active_1'].toggle()
        if event.key == self.settings.data['keybinds']['active_2'].keycode:
            self.ship.ability_slots['active_2'].toggle()
        if event.key == self.settings.data['keybinds']['active_3'].keycode:
            self.ship.ability_slots['active_3'].toggle()
        if event.key == self.settings.data['keybinds']['passive_1'].keycode:
            self.ship.ability_slots['passive_1'].toggle()
        if event.key == self.settings.data['keybinds']['passive_2'].keycode:
            self.ship.ability_slots['passive_2'].toggle()
        if event.key == self.settings.data['keybinds']['passive_3'].keycode:
            self.ship.ability_slots['passive_3'].toggle()
        if event.key == self.settings.data['keybinds']['passive_4'].keycode:
            self.ship.ability_slots['passive_4'].toggle()
                
    def _handle_keyup_events(self, event: pygame.Event):
        """Handle what happens when certain keys are released."""

        if not self.state.session_running:
            return

        if event.key == self.settings.data['keybinds']['move_left'].keycode:
            self.ship.moving_left = False
        if event.key == self.settings.data['keybinds']['move_right'].keycode:
            self.ship.moving_right = False
        if event.key == self.settings.data['keybinds']['fire'].keycode:
            self.ship.stop_ability_charge()
    
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
            if not isinstance(alien, Alien):
                continue
            alien.handle_resize()
    
    def _handle_mousedown_event(self, event: pygame.Event):
        """
        Handle what happens when the user presses the mouse button.
        A touchscreen touch is interpreted as a mouse click.
        """

        # respond only to left mouse button
        if not event.touch and event.button != 1:
            return

        self.touch.register_mousedown_event(event)

        if self.touch.touch_start_ts is None:
            return
        
        if self.touch.current_pos is None:
            return

        for menu in self.menus.values():
            if not isinstance(menu, menus.Menu):
                continue
            menu.start_touch(self.touch.current_pos)
        
        if not self.state.session_running:
            return
        
        self.top_tray.start_touch(self.touch.current_pos)
        self.top_tray.interact()
        
        # TODO: find a better way to organize this; a better place ??
        self.bot_tray.start_touch(self.touch.current_pos)
        self.bot_tray.interact()
        
        # control the ship if nothing else is clicked
        if pygame.Rect.collidepoint(
            self.top_tray.rect, self.touch.current_pos[0],
            self.touch.current_pos[1]
        ):
            return
        if pygame.Rect.collidepoint(
            self.bot_tray.rect, self.touch.current_pos[0],
            self.touch.current_pos[1]
        ):
            return
        self.ship.fire_bullet()
        self.ship.start_ability_charge()
        self.ship.destination = (
            self.touch.current_pos[0] - round(self.ship.rect.width / 2),
            self.ship.y
        )
    
    def _handle_mouseup_event(self, event: pygame.Event):
        """
        Handle what happens when the user releases the mouse button.
        A touchscreen touch is interpreted as a mouse click.
        """

        self.touch.register_mouseup_event()

        for menu in self.menus.values():
            if not isinstance(menu, menus.Menu):
                continue
            menu.interact()
            menu.end_touch()

        if not self.state.session_running:
            return
        
        self.ship.stop_ability_charge()
        self.ship.destination = None
    
    def _handle_mousewheel_event(self, event: pygame.Event):
        """Handles what happens when the user scrolls the mouse wheel."""

        x = event.x * config.mouse_wheel_magnitude
        y = event.y * config.mouse_wheel_magnitude

        for menu in self.menus.values():
            if not isinstance(menu, menus.Menu):
                continue
            menu.scroll((x, y), True)

    def _handle_mousemove_event(self, event: pygame.Event):
        """
        Handle what happens when the user moves the mouse.
        A touchscreen touch is interpreted as a mouse.
        """

        self.touch.register_mousemove_event(event)
        if self.touch.current_pos is None:
            return

        for menu in self.menus.values():
            if not isinstance(menu, menus.Menu):
                continue
            menu.scroll(self.touch.current_pos)

        if self.touch.touch_start_ts is None:
            return
        
        if not self.state.session_running:
            return

        # TODO: make the play area a separate surface to avoid the
        #   nonsense below
        if self.top_tray.rect.collidepoint(self.touch.current_pos):
            # do nothing when moving around the top tray
            return
        if self.bot_tray.rect.collidepoint(self.touch.current_pos):
            # do nothing when moving around the bottom tray
            return

        # move the ship
        self.ship.destination = (
            self.touch.current_pos[0] - round(self.ship.rect.width / 2),
            self.ship.y
        )

    # -------------------------------------------------------------------
    # endregion

    # region UPDATE HELPER FUNCTIONS
    # -------------------------------------------------------------------

    def _update_each_second(self):
        """
        This method handles updates that need to be checked only once
        each second, to improve performance by reducing method calls.
        """

        seconds = self.state.session_duration // 1000
        if seconds <= self.state.last_second_tracked:
            return False
        
        self.top_tray.update()
        self._level_up(seconds)

        self.state.last_second_tracked = seconds

    def _update_session(self):
        """Updates the entities and trays if the session is running."""

        if not self.state.session_running:
            return False
        
        self.state.track_duration()
        self._update_each_second()

        self.spawn_manager.spawn_random()

        # TODO: use an "entity" group to update them
        self.ship.update()
        self.aliens.update()
        self.bullets.update()
        self.powerups.update()
    # -------------------------------------------------------------------
    # endregion

    def _update(self):
        """Update the game objects."""

        if self.touch:
            self.touch.track_touch_duration()

        self._update_session()
    
    # region DRAW HELPER FUNCTIONS
    # -------------------------------------------------------------------

    def _draw_session(self):
        """Draws the play surface and trays if the session is running."""

        if not self.state.session_running:
            return False
        
        # first, clear the play surface by drawing the background
        pygame.draw.rect(self.play_surf, "black", self.play_rect)

        # TODO: use an entities group to draw the entities
        self.ship.draw()
        for bullet in self.bullets:
            if not isinstance(bullet, Bullet):
                continue
            bullet.draw()
        for powerup in self.powerups:
            if not isinstance(powerup, powerups.PowerUp):
                continue
            powerup.draw()
        for alien in self.aliens:
            if not isinstance(alien, Alien):
                continue
            alien.draw()

        # draw the play surface
        self.screen.blit(self.play_surf)

        self.top_tray.needs_redraw = True
        self.bot_tray.needs_redraw = True
        self.top_tray.draw()
        self.bot_tray.draw()

    # -------------------------------------------------------------------
    # endregion

    def _draw(self):
        """Draw to the screen."""

        self._draw_session()     
                
        for menu in self.menus.values():
            if not isinstance(menu, menus.Menu):
                continue
            menu.draw()

        # draw everything to the screen
        pygame.display.flip()

__all__ = ["Game"]
