"""
GameEngine: owns the basket and all falling objects.

Starter version: basket movement and spawning both work at a basic
level (Tasks 2 and 3 ask you to improve them), there's no speed boost
yet (Task 4 builds it from scratch), and catch detection has two
known bugs (see game/collision.py and the catch-checking loop below)
that Task 1 asks you to fix.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_MIN_INTERVAL_FRAMES = 30
SPAWN_MAX_INTERVAL_FRAMES = 80
MIN_SPAWN_DISTANCE = 80
MAX_OBJECTS_ON_SCREEN = 6
OBJECT_RADIUS = 14
SPAWN_X_MIN = OBJECT_RADIUS
SPAWN_X_MAX = WIDTH - OBJECT_RADIUS
SPAWN_POSITION_ATTEMPTS = 20
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.previous_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _get_spawn_x(self):
        if self.previous_spawn_x is None:
            return random.randint(SPAWN_X_MIN, SPAWN_X_MAX)

        for _ in range(SPAWN_POSITION_ATTEMPTS):
            x = random.randint(SPAWN_X_MIN, SPAWN_X_MAX)
            if abs(x - self.previous_spawn_x) >= MIN_SPAWN_DISTANCE:
                return x

        left_distance = abs(SPAWN_X_MIN - self.previous_spawn_x)
        right_distance = abs(SPAWN_X_MAX - self.previous_spawn_x)

        if left_distance >= right_distance:
            return SPAWN_X_MIN
        return SPAWN_X_MAX

    def _spawn_object(self):
        x = self._get_spawn_x()
        self.objects.append(
            FallingObject(x=x, y=-OBJECT_RADIUS, radius=OBJECT_RADIUS, speed=3)
        )
        self.previous_spawn_x = x

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Clamp using half the basket width because basket.x
        # represents the center of the basket.
        half_basket_width = self.basket.width / 2
        self.basket.x = max(
            half_basket_width,
            min(WIDTH - half_basket_width, self.basket.x),
        )

    def handle_keydown(self, key):
        if self.game_over:
            return

        if key == pygame.K_r and self.game_over:  # CHANGED
            self.__init__()

        if key == pygame.K_SPACE:  # CHANGED
            self.basket.activate_boost()  # CHANGED

    def update(self):
        if self.game_over:
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_OBJECTS_ON_SCREEN:
                self._spawn_object()

            self.frames_until_spawn = random.randint(
                SPAWN_MIN_INTERVAL_FRAMES,
                SPAWN_MAX_INTERVAL_FRAMES,
            )

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()

        remaining_objects = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining_objects.append(obj)

        self.objects = remaining_objects

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [
                o for o in self.objects if not o.is_past_bottom(HEIGHT)
            ]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

        # CHANGED: Update the boost frame counters after the current
        # CHANGED: frame's movement and collision processing.
        self.basket.update_boost()  # CHANGED

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(
            surface,
            font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36),
        )

        # CHANGED: Show the current boost status during gameplay.
        if not self.game_over:  # CHANGED
            renderer.draw_boost_status(surface, font, self.basket)  # CHANGED

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart.",
            )