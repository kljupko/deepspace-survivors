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
        self.rect.midbottom = self.screen_rect.midbottom
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
        self._move(dt)
        self._fire_passive_abilities()
        self._charge_active_ability()
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
    
    def _check_alien_collisions(self):
        """Check if the ship is colliding with any aliens."""

        collisions = pygame.sprite.spritecollide(self, self.game.aliens, False)
        if not collisions:
            return False
        
        print(f"We're hit! {len(collisions)} aliens hit the ship.")
        for alien in collisions:
            self.hp -= alien.damage
            print(f"\tCurrent hp: {self.hp} (-{alien.damage})")
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
        
        return True


    def fire_bullet(self, fire_rate_bonus = 0):
        """Fire a bullet."""

        now = pygame.time.get_ticks()
        if now < self.next_bullet_time:
            return False

        self.game.bullets.add(Bullet(self.game))

        fire_rate = self.fire_rate + fire_rate_bonus
        self.next_bullet_time = now + (self.bullet_delay_ms / fire_rate)
        return True
    
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
            
            if abil.name == abilities.Blank(self.game).name:
                abils[idx] = new_ability
                return True
            
            if not abil.enabled:
                abils[idx] = new_ability
                return True
        
        return False
    
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
                return True
        
        return False
    
    def _fire_passive_abilities(self):
        """Fire all the enabled passive abilities."""

        for ability in self.passive_abilities:
            if ability and ability.enabled:
                ability.fire()
    
    def _charge_active_ability(self):
        """Fire an active ability after the charge-up time."""

        enabled_idx = None
        for i in range(len(self.active_abilities)):
            ability = self.active_abilities[i]
            if ability and ability.enabled:
                enabled_idx = i
                break

        if enabled_idx == None:
            return False
        
        charge = 2000 # ms
        touch = self.game.touch
        if touch.touch_duration and touch.touch_duration >= charge:
            self.fire_active_ability(enabled_idx)
    
    def fire_active_ability(self, index):
        """
        Fire the active ability with the given index if it is enabled.
        """
        
        ability = self.active_abilities[index]

        if not ability or not ability.enabled:
            return False
        
        self.active_abilities[index].fire()
        return True