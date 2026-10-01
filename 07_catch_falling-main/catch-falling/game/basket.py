"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


NORMAL_SPEED = 5  # CHANGED
BOOST_SPEED = 9  # CHANGED
BOOST_DURATION_FRAMES = 180  # CHANGED
BOOST_COOLDOWN_FRAMES = 300  # CHANGED


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=NORMAL_SPEED):  # CHANGED
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.normal_speed = speed  # CHANGED
        self.boost_speed = BOOST_SPEED  # CHANGED
        self.speed = self.normal_speed  # CHANGED
        self.boosted_frames = 0
        self.cooldown_frames = 0  # CHANGED

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )

    def activate_boost(self):
        if self.boosted_frames > 0 or self.cooldown_frames > 0:  # CHANGED
            return False  # CHANGED

        self.boosted_frames = BOOST_DURATION_FRAMES  # CHANGED
        self.cooldown_frames = BOOST_COOLDOWN_FRAMES  # CHANGED
        self.speed = self.boost_speed  # CHANGED
        return True  # CHANGED

    def update_boost(self):
        if self.boosted_frames > 0:  # CHANGED
            self.boosted_frames -= 1  # CHANGED

            if self.boosted_frames == 0:  # CHANGED
                self.speed = self.normal_speed  # CHANGED

        if self.cooldown_frames > 0:  # CHANGED
            self.cooldown_frames -= 1  # CHANGED

    def is_boost_active(self):
        return self.boosted_frames > 0  # CHANGED

    def is_boost_ready(self):
        return self.boosted_frames == 0 and self.cooldown_frames == 0  # CHANGED

    def get_boost_remaining_seconds(self):
        return (self.boosted_frames + 59) // 60  # CHANGED