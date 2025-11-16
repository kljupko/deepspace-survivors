"""
A module containing all the playable ships.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
if TYPE_CHECKING:
    from ..game import Game

import pygame

from .entity import Entity
from .aliens import Alien
from .bullet import Bullet
from .powerups import PowerUp
from ..mechanics import abilities as abs, stats
from ..utils import config, helper_funcs

class StatsDict(TypedDict):
    
    """A class representing a dictionary of ship stats."""

    hit_points: stats.HitPoints
    thrust: stats.Thrust
    fire_power: stats.FirePower
    fire_rate: stats.FireRate

class StatValuesDict(TypedDict):
    """A class representing a dictionary of initial stat values."""

    hit_points: int
    thrust: int
    fire_power: int
    fire_rate: int

class AbilityLoadoutDict(TypedDict):
    """A class representing a ship's initial loadout of abs."""

    active_1: type[abs.Active] | None
    active_2: type[abs.Active] | None
    active_3: type[abs.Active] | None
    passive_1: type[abs.Passive] | None
    passive_2: type[abs.Passive] | None
    passive_3: type[abs.Passive] | None
    passive_4: type[abs.Passive] | None

class AbilitySlotsDict(TypedDict):
    """A class representing a ship's ability slots."""

    active_1: abs.Slot
    active_2: abs.Slot
    active_3: abs.Slot
    passive_1: abs.Slot
    passive_2: abs.Slot
    passive_3: abs.Slot
    passive_4: abs.Slot

class Ship(Entity):
    """Base class that manages the player ship."""

    name: str = "Base Ship"
    description: str = "The basic ship. Parent class to other ships."
    image: pygame.Surface = helper_funcs.load_image(None, 'green')

    def __init__(self,
                 game: Game,
                 name: str | None = None,
                 description: str | None = None,
                 image: pygame.Surface | None = None,
                 base_stat_values: StatValuesDict | None = None,
                 ability_loadout: AbilityLoadoutDict | None = None,
                 ):
        """Initialize the ship."""

        if image is None:
            image = Ship.image
        
        super().__init__(game, image)

        if name is None:
            name = Ship.name
        self.name = name

        if description is None:
            description = Ship.description
        self.description = description

        if base_stat_values is None:
            base_stat_values = {
                'hit_points': 3,
                'thrust': 3,
                'fire_power': 1,
                'fire_rate': 3
            }
        self.stats: StatsDict = {
            'hit_points': stats.HitPoints(self, base_stat_values['hit_points']),
            'thrust': stats.Thrust(self, base_stat_values['thrust']),
            'fire_power': stats.FirePower(self, base_stat_values['fire_power']),
            'fire_rate': stats.FireRate(self, base_stat_values['fire_rate']),
        }
        self.apply_stat_upgrades()

        self.ability_slots: AbilitySlotsDict = {
            'active_1': abs.Slot(self.game, abs.Active),
            'active_2': abs.Slot(self.game, abs.Active, True),
            'active_3': abs.Slot(self.game, abs.Active, True),
            'passive_1': abs.Slot(self.game, abs.Passive),
            'passive_2': abs.Slot(self.game, abs.Passive, True),
            'passive_3': abs.Slot(self.game, abs.Passive, True),
            'passive_4': abs.Slot(self.game, abs.Passive, True),
        }
        self.apply_slot_unlocks()
        if ability_loadout is None:
            ability_loadout = {
                'active_1': None,
                'active_2': None,
                'active_3': None,
                'passive_1': None,
                'passive_2': None,
                'passive_3': None,
                'passive_4': None,
            }
        self.ability_loadout = ability_loadout
        self.apply_ability_loadout()
        self.charging_ability = False
        self.apply_charge_time_upgrades()
        self.charge_time = 0

        self.bullet_delay_ms = 1000 * 3
        self.bullet_cooldown_ms = self.bullet_delay_ms

        # set position
        self.x = self.game.play_rect.centerx - self.rect.width//2
        self.y = self.bounds["bottom"]
        self.rect.x, self.rect.y = int(self.x), int(self.y)

        self.moving_left = False
        self.moving_right = False

    # region INIT HELPER FUNCTIONS
    # -------------------------------------------------------------------
     
    def apply_stat_upgrades(self):
        """Apply purchased upgrades to the ship's stats."""

        ups = self.game.upgrades

        self.stats['hit_points'].modify_stat(ups['hit_points'].level)
        self.stats['thrust'].modify_stat(ups['thrust'].level)
        self.stats['fire_power'].modify_stat(ups['fire_power'].level)
        self.stats['fire_rate'].modify_stat(ups['fire_rate'].level)
    
    def apply_slot_unlocks(self):
        """Apply purchased upgrades to the ship's ability slots."""
        
        max_active_slots = self.game.upgrades['active_slots'].level + 1
        max_passive_slots = self.game.upgrades['passive_slots'].level + 1

        if max_active_slots >= 2:
            self.ability_slots['active_2'].set_is_locked(False)
        if max_active_slots >= 3:
            self.ability_slots['active_3'].set_is_locked(False)
        
        if max_passive_slots >= 2:
            self.ability_slots['passive_2'].set_is_locked(False)
        if max_passive_slots >= 3:
            self.ability_slots['passive_3'].set_is_locked(False)
        if max_passive_slots >= 4:
            self.ability_slots['passive_4'].set_is_locked(False)
    
    def apply_ability_loadout(self,):
        """Apply the given ability loadout to the ship's slots."""

        self.ability_slots['active_1'].set_ability(self.ability_loadout['active_1'])
        self.ability_slots['active_2'].set_ability(self.ability_loadout['active_2'])
        self.ability_slots['active_3'].set_ability(self.ability_loadout['active_3'])
        self.ability_slots['passive_1'].set_ability(self.ability_loadout['passive_1'])
        self.ability_slots['passive_2'].set_ability(self.ability_loadout['passive_2'])
        self.ability_slots['passive_3'].set_ability(self.ability_loadout['passive_3'])
        self.ability_slots['passive_4'].set_ability(self.ability_loadout['passive_4'])

    def apply_charge_time_upgrades(self):
        """Apply the purchased upgrades to ability charge time."""

        base_time = config.required_ability_charge
        upgrade_level = self.game.upgrades['charge_time'].level
        self.req_charge_time = base_time * 0.9**upgrade_level

    # -------------------------------------------------------------------
    # endregion init helper functions

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
    
    def take_damage(self, damage: int):
        """
        Reduces the ship's HP by the given damage.
        Ends the session at 0 HP.
        """

        self.stats['hit_points'].modify_stat(-damage)
        self.game.bot_tray.update()

        if self.stats['hit_points'].value <= 0:
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
            # ensure alien is a subclass of Alien
            if not isinstance(alien, Alien):
                continue
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
            # ensure the powerup is a subclass of Powerup
            if not isinstance(powerup, PowerUp):
                continue
            powerup.apply()
        
        # TODO: figure out a way to change ui on powerup pickup
        #   probably in the powerup.apply method
        
        return True
    
    # -------------------------------------------------------------------
    # endregion collision checking

    def fire_bullet(self, fire_rate_bonus: int = 0):
        """Fire a bullet."""

        fire_rate = self.stats['fire_rate'].value + fire_rate_bonus
        if self.bullet_cooldown_ms < self.bullet_delay_ms / fire_rate:
            return False

        self.game.bullets.add(Bullet(self.game))
        self.bullet_cooldown_ms = 0
        return True
    
    # region ABILITY SLOTS AND ABILITIES
    # -------------------------------------------------------------------
    
    def get_valid_slot_for(self, ability_class: type[abs.Ability]):
        """
        Return the first valid slot where an ability of the given class can fit.
        Return None if there are no valid slots.
        """

        for slot in self.ability_slots.values():
            if not isinstance(slot, abs.Slot):
                continue

            if slot.can_accept_ability(ability_class):
                return slot
        
        return None                

    def start_ability_charge(self):
        """Start charging active abs."""

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
        """Fire enabled active abs."""
        
        self.ability_slots['active_1'].fire_ability()
        self.ability_slots['active_2'].fire_ability()
        self.ability_slots['active_3'].fire_ability()
        self.stop_ability_charge()
        self.game.bot_tray.update()
        return True
    
    def stop_ability_charge(self):
        """Stop charging active abilities and reset charge time to 0."""

        self.charging_ability = False
        self.charge_time = 0
        
    def _fire_passive_abilities(self):
        """Fire all the enabled passive abs."""

        self.ability_slots['passive_1'].fire_ability()
        self.ability_slots['passive_2'].fire_ability()
        self.ability_slots['passive_3'].fire_ability()
        self.ability_slots['passive_4'].fire_ability()
    
    # -------------------------------------------------------------------
    # endregion ability slots and abilities

class SpearFish(Ship):
    """A class representing a ship with the Spear ability."""

    name = "SpearFish"
    description = "A ship with a high fire rate and the Spear passive ability."
    image = helper_funcs.load_image(None, 'darkslategray3', (20, 28))

    def __init__(self, game: Game):
        """Initialize the SpearFish."""

        name = SpearFish.name
        description = SpearFish.description
        image = SpearFish.image
        base_stat_values: StatValuesDict = {
            'hit_points': 10,
            'thrust': 5,
            'fire_power': 5,
            'fire_rate': 5
        }
        ability_loadout: AbilityLoadoutDict = {
            'active_1': None,
            'active_2': None,
            'active_3': None,
            'passive_1': abs.Spear,
            'passive_2': None,
            'passive_3': None,
            'passive_4': None
        }
        super().__init__(game, name, description, image, base_stat_values, ability_loadout)

__all__ = ["Ship", "SpearFish"]