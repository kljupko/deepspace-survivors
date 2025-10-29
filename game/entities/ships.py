"""
A module containing all the playable ships.
"""

import pygame
from .entity import Entity
from .bullet import Bullet
from ..mechanics import abilities, stats
from ..utils import config, helper_funcs

class Ship(Entity):
    """Base class that manages the player ship."""

    def __init__(self, game, image=None, base_stats=None, base_abils=None):
        """Initialize the ship."""
        
        super().__init__(game, image)

        if image is None:
            image = helper_funcs.load_image(None, 'green')
        self.image = image
        self.rect = self.image.get_rect()

        if base_stats is None:
            base_stats = {
                'Hit Points': 3,
                'Thrust': 3,
                'Fire Power': 1,
                'Fire Rate': 3
            }
        self.base_stats = base_stats

        # overwrite Entity's center position
        self.rect.midtop = self.game.play_rect.centerx, self.bounds["bottom"]
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # ship stats
        self.load_stats()

        self.bullet_delay_ms = 1000 * 3
        self.bullet_cooldown_ms = self.bullet_delay_ms

        self.moving_left = False
        self.moving_right = False

        # abilities
        self.charging_ability = False
        self.load_req_charge_time()
        self.charge_time = 0
        if base_abils is None:
            base_abils = {
                'active': [
                    abilities.Blank,
                    abilities.Locked,
                    abilities.Locked
                ],
                'passive': [
                    abilities.Blank,
                    abilities.Locked,
                    abilities.Locked,
                    abilities.Locked
                ]
            }
        self.base_abils = base_abils
        self.load_abilities()
    
    def load_stats(self):
        """Load stats with upgrades."""

        self.stats = {
            'Hit Points': stats.HitPoints(
                self, self.base_stats['Hit Points'] + self.game.upgrades['hp'].level
            ),
            'Thrust': stats.Thrust(
                self, self.base_stats['Thrust'] + self.game.upgrades['thrust'].level
            ),
            'Fire Power': stats.FirePower(
                self, self.base_stats['Fire Power'] + self.game.upgrades['fp'].level
            ),
            'Fire Rate': stats.FireRate(
                self, self.base_stats['Fire Rate'] + self.game.upgrades['fr'].level
            )
        }

    def load_abilities(self):
        """
        Loads the ability slots, along with ones unlocked by upgrades.
        """

        active_unlocked = self.game.upgrades['active'].level # max. 2
        passive_unlocked = self.game.upgrades['passive'].level # max. 3

        self.active_abilities = [
            self.base_abils['active'][0](self.game)
        ]
        self.passive_abilities = [
            self.base_abils['passive'][0](self.game)
        ]

        for i in range(1, 3):
            if i <= active_unlocked:
                self.active_abilities.append(abilities.Blank(self.game))
            else:
                self.active_abilities.append(abilities.Locked(self.game))

        for i in range(1, 4):
            if i <= passive_unlocked:
                self.passive_abilities.append(abilities.Blank(self.game))
            else:
                self.passive_abilities.append(abilities.Locked(self.game))

    def load_req_charge_time(self):
        """
        Loads the time required to charge an active ability, with
        applied upgrades.
        """

        base_time = config.required_ability_charge
        upgrade_level = self.game.upgrades['charge_time'].level
        self.req_charge_time = base_time * 0.9**upgrade_level

    # override Entity update method
    def update(self):
        """Update the ship."""

        self.bullet_cooldown_ms += self.game.dt * 1000
        self._steer()
        # TODO: use thrust for speed
        self._move()
        self._charge_abilities()
        self._fire_passive_abilities()
        self._check_powerup_collisions()
        self._check_alien_collisions()
    
    def _steer(self):
        """Steer the ship left or right."""
        
        if self.game.touch and self.game.touch.touch_start_ts:
            return False
        
        if self.moving_left and self.moving_right:
            self.destination = None
        elif not self.moving_left and not self.moving_right:
            self.destination = None
        elif self.moving_left:
            self.destination = (self.bounds["left"], self.y)
        elif self.moving_right:
            self.destination = (self.bounds["right"], self.y)
    
    def take_damage(self, damage):
        """
        Reduces the ship's HP by the given damage.
        Ends the session at 0 HP.
        """

        self.stats['Hit Points'].modify_stat(-damage)
        self.game.bot_tray.update()

        if self.stats['Hit Points'].value <= 0:
            # TODO: replace this with a 'lose_session' menu
            self.game.quit_session()

    # region COLLISION CHECKING
    # -------------------------------------------------------------------

    def _check_alien_collisions(self):
        """Check if the ship is colliding with any aliens."""

        collisions = pygame.sprite.spritecollide(self, self.game.aliens, False)
        if not collisions:
            return False
        
        for alien in collisions:
            self.take_damage(alien.damage)
            alien.destroy()
        
        return True
    
    def _check_powerup_collisions(self):
        """Check if the ship is colliding with any powerups."""

        collisions = pygame.sprite.spritecollide(
                self, self.game.powerups, False
            )
        if not collisions:
            return False
        
        for powerup in collisions:
            powerup.apply()
        
        # TODO: figure out a way to change ui on powerup pickup
        #   probably in the powerup.apply method
        
        return True
    
    # -------------------------------------------------------------------
    # endregion

    def fire_bullet(self, fire_rate_bonus = 0):
        """Fire a bullet."""

        fire_rate = self.stats['Fire Rate'].value + fire_rate_bonus
        if self.bullet_cooldown_ms < self.bullet_delay_ms / fire_rate:
            return False

        self.game.bullets.add(Bullet(self.game))
        self.bullet_cooldown_ms = 0
        return True
    
    # region ACTIVE ABILITIES
    # -------------------------------------------------------------------

    def add_active_ability(self, new_ability):
        """
        Add an active ability to the ship if there are free slots.
        The method returns True if the ability is added.
        """
        
        abils = self.active_abilities

        for ability in abils:
            idx = abils.index(ability)
            if type(ability) == abilities.Blank:
                abils[idx] = new_ability
                self.game.bot_tray.update()
                print(f"Placed {abils[idx].name} into a blank slot.")
                return True
        
        print(f"{new_ability.name} not added.")
        return False

    def toggle_active_ability_num(self, number):
        """
        Toggles the active ability with the given number (one-based).
        """

        if number < 1 or number > 3:
            print("Invalid number for active ability!")
            print("Are you using one-based indices? You should in this case.")
            return False
        
        self.active_abilities[number-1].toggle()
    
    def start_ability_charge(self):
        """Start charging active abilities."""

        self.charging_ability = True
        self.charge_time = 0
    
    def _charge_abilities(self):
        """Charge up the active abilities and fire if fully charged."""

        if not self.charging_ability:
            return False
        
        self.charge_time += self.game.dt * 1000
        if self.charge_time < self.req_charge_time:
            return False
        
        self._fire_active_abilities()
    
    def _fire_active_abilities(self):
        """Fire enabled active abilities."""
        
        for ability in self.active_abilities:
            if ability.is_enabled:
                ability.fire()
        self.stop_ability_charge()
        self.game.bot_tray.update()
        return True
    
    def stop_ability_charge(self):
        """Stop charging active abilities and reset charge time to 0."""

        self.charging_ability = False
        self.charge_time = 0
    
    # -------------------------------------------------------------------
    # endregion

    # region PASSIVE ABILITIES
    # -------------------------------------------------------------------
    
    def add_passive_ability(self, new_ability):
        """
        Add a passive ability to the ship. If the ability is already
        present, it is leveled up. If there is a free slot, it is added.
        If there are no free slots, a deactivated ability is replaced.
        The method returns True if the ability is added/ upgraded.
        """

        abils = self.passive_abilities

        # check if any abilities are the same; if yes, level up
        for ability in abils:
            idx = abils.index(ability)
            if type(ability) == type(new_ability):
                abils[idx].level_up()
                print(f"Leveled up {abils[idx].name} to level {abils[idx].level}.")
                return True
        
        # otherwise, check if there are blank slots
        for ability in abils:
            idx = abils.index(ability)
            if type(ability) == abilities.Blank:
                abils[idx] = new_ability
                self.game.bot_tray.update()
                print(f"Placed {abils[idx].name} into a blank slot.")
                return True
        
        # otherwise, check if there are disabled abilities
        for ability in abils:
            idx = abils.index(ability)
            if not ability.is_enabled:
                old = ability.name
                abils[idx] = new_ability
                self.game.bot_tray.update()
                print(f"Replaced disabled {old} ability with {abils[idx].name}.")
                return True
        
        print(f"{new_ability.name} not added.")
        return False

    def toggle_passive_ability_num(self, number):
        """
        Toggles the passive ability with the given number (one-based).
        """

        if number < 1 or number > 4:
            print("Invalid number for passive ability!")
            print("Are you using one-based indices? You should in this case.")
            return False
        
        self.passive_abilities[number-1].toggle()
    
    def _fire_passive_abilities(self):
        """Fire all the enabled passive abilities."""

        for ability in self.passive_abilities:
            if ability and ability.is_enabled:
                ability.fire()
    
    # -------------------------------------------------------------------
    # endregion

class SpearFish(Ship):
    """A class representing a ship with the Spear ability."""

    def __init__(self, game, image=None, base_stats=None, base_abils=None):
        """Initialize the SpearFish."""

        if image is None:
            image = helper_funcs.load_image(None, 'darkslategray3', (20, 28)) #?
        
        if base_stats is None:
            base_stats = {
                'Hit Points': 10,
                'Thrust': 5,
                'Fire Power': 5,
                'Fire Rate': 5
            }
        
        if base_abils is None:
            base_abils = {
                'active': [
                    abilities.Blank,
                    abilities.Locked,
                    abilities.Locked
                ],
                'passive': [
                    abilities.Spear,
                    abilities.Locked,
                    abilities.Locked,
                    abilities.Locked
                ]
            }
        super().__init__(game, image, base_stats, base_abils)

__all__ = ["Ship", "SpearFish"]