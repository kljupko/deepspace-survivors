"""
A module containing all the playable ships.
"""

import pygame
from entity import Entity
from bullet import Bullet

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
        self.base_speed_x = 100
        self.speed_x, self.speed_y = self._calculate_relative_speed()

        # ship stats
        self.hp = 3
        self.thrust = 1
        self.next_bullet_time = pygame.time.get_ticks()
        self.bullet_delay_ms = 1000 * 3
        self.fire_rate = 3
        self.fire_power = 1
        self.active_abilities = [None, False, False]
        self.passive_abilities = [None, False, False, False]
    
    # override Entity update method
    def update(self, dt):
        """Update the ship."""

        self._move(dt)
        self._fire_passive_abilities()
        self._check_alien_collisions()
    
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

    def fire_bullet(self, fire_rate_bonus = 0):
        """Fire a bullet."""

        now = pygame.time.get_ticks()
        if now < self.next_bullet_time:
            return False

        self.game.bullets.add(Bullet(self.game))

        fire_rate = self.fire_rate + fire_rate_bonus
        self.next_bullet_time = now + (self.bullet_delay_ms / fire_rate)
        return True
    
    def add_passive_ability(self, ability):
        """
        Add a passive ability to the ship. If the ability is already
        present, it is leveled up. If there is a free slot, it is added.
        If there are no free slots, a deactivated ability is replaced.
        The method returns True if the ability is added/ upgraded.
        """

        abils = self.passive_abilities

        if ability in abils:
            # TODO: level up the ability
            print("Leveled up the ability.")
            return True
        
        if None in abils: # None represents a free slot
            abils[abils.index(None)] = ability
            print("Added ability to a free slot.")
            return True
        
        for abil in abils:
            if abil and not abil.activated:
                abil = ability
                print("Replaced a deactivated ability.")
                return True
        
        print("Failed to add ability.")
        return False
    
    def add_active_ability(self, ability):
        """
        Add an active ability to the ship if there are free slots.
        The method returns True if the ability is added/ upgraded.
        """

        abils = self.active_abilities
        
        if None in abils: # None represents a free slot
            abils[abils.index(None)] = ability
            print("Added ability to a free slot.")
            return True
        
        print("Failed to add ability.")
        return False
    
    def _fire_passive_abilities(self):
        """Fire all the enabled passive abilities."""

        for passive in self.passive_abilities:
            if passive and passive.enabled:
                passive.fire()
    
    def fire_active_ability(self, index):
        """
        Fire the active ability with the given index if it is enabled.
        """
        
        ability = self.active_abilities[index]

        if not ability or not ability.enabled:
            return False
        
        self.active_abilities[index].fire()
        return True