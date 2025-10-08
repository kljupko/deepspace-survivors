"""
A module containing all the playable ships.
"""

import pygame
from entity import Entity
from bullet import Bullet
import abilities

class Ship(Entity):
    """Base class that manages the player ship."""

    def __init__(self, game):
        """Initialize the ship."""
        
        super().__init__(game)

        # TODO: load ship as an image
        self.color = "green"

        # overwrite Entity's center position
        self.rect.midtop = self.screen_rect.centerx, self.bounds["bottom"]
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # allow the ship to move horizontally
        self.base_speed_x = self.game.config.base_speed
        self._calculate_relative_speed()
        self.moving_left = False
        self.moving_right = False

        # ship stats
        self.hp = 3
        self.thrust = 1
        self.next_bullet_time = pygame.time.get_ticks()
        self.bullet_delay_ms = 1000 * 3
        self.fire_rate = 3
        self.fire_power = 1

        # abilities
        self.charge = None
        self.required_charge = None
        self.active_abilities = [
            abilities.Blank(self.game),
            abilities.Locked(self.game),
            abilities.Locked(self.game)
        ]
        self.passive_abilities = [
            abilities.Blank(self.game),
            abilities.Locked(self.game),
            abilities.Locked(self.game),
            abilities.Locked(self.game)
        ]
    
    # override Entity update method
    def update(self, dt):
        """Update the ship."""

        self._steer()
        # TODO: use thrust for speed
        self._move(dt)
        self._fire_active_abilities()
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
    
    # region COLLISION CHECKING
    # -------------------------------------------------------------------

    def _check_alien_collisions(self):
        """Check if the ship is colliding with any aliens."""

        collisions = pygame.sprite.spritecollide(self, self.game.aliens, False)
        if not collisions:
            return False
        
        for alien in collisions:
            self.hp -= alien.damage
            ui_elem = self.game.bottom_tray.elements["ship_hp"]
            ui_elem.update(self.hp)
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

        now = pygame.time.get_ticks()
        if now < self.next_bullet_time:
            return False

        self.game.bullets.add(Bullet(self.game))

        fire_rate = self.fire_rate + fire_rate_bonus
        self.next_bullet_time = now + (self.bullet_delay_ms / fire_rate)
        return True
    
    # region ACTIVE ABILITIES
    # -------------------------------------------------------------------

    def add_active_ability(self, new_ability):
        """
        Add an active ability to the ship if there are free slots.
        The method returns True if the ability is added/ upgraded.
        """

        abils = self.active_abilities
        
        for abil in abils:
            idx = abils.index(abil)

            if abil.name == abilities.Blank(self.game).name:
                abils[idx] = new_ability
                ui_element = self.game.bottom_tray.elements[f"passive_{idx+1}"]
                ui_element.action = abils[idx].toggle
                return True
        
        return False
    
    def start_ability_charge(self):
        """Start charging active abilities."""

        if self.charge is None:
            req = self.game.config.required_ability_charge
            self.charge = pygame.time.get_ticks()
            self.required_charge = self.charge + req
            return True
        return False
    
    def cancel_ability_charge(self):
        """Cancel charging active abilities."""

        self.charge = None
        self.required_charge = None
    
    def _fire_active_abilities(self):
        """Fire enabled active abilities if the charge is complete."""

        if self.charge is None:
            return False
        
        if self.charge < self.required_charge:
            self.charge = pygame.time.get_ticks()
            return False
        
        for ability in self.active_abilities:
            if ability.enabled:
                ability.fire()
        self.cancel_ability_charge()
        return True
    
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

        for abil in abils:
            idx = abils.index(abil)

            if abil.name == new_ability.name:
                # TODO: level up the ability
                return True
            
            if abil.name == abilities.Blank(self.game).name or not abil.enabled:
                abils[idx] = new_ability
                ui_element = self.game.bottom_tray.elements[f"passive_{idx+1}"]
                ui_element.action = abils[idx].toggle
                return True
        
        return False
    
    def _fire_passive_abilities(self):
        """Fire all the enabled passive abilities."""

        for ability in self.passive_abilities:
            if ability and ability.enabled:
                ability.fire()
    
    # -------------------------------------------------------------------
    # endregion