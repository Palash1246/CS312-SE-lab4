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

SPAWN_MIN_INTERVAL_FRAMES = 30  # CHANGED
SPAWN_MAX_INTERVAL_FRAMES = 80  # CHANGED
MIN_SPAWN_DISTANCE = 80  # CHANGED
MAX_OBJECTS_ON_SCREEN = 6  # CHANGED
OBJECT_RADIUS = 14  # CHANGED
SPAWN_X_MIN = OBJECT_RADIUS  # CHANGED
SPAWN_X_MAX = WIDTH - OBJECT_RADIUS  # CHANGED
SPAWN_POSITION_ATTEMPTS = 20  # CHANGED
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.previous_spawn_x = None  # CHANGED
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _get_spawn_x(self):
        # CHANGED: Try several random positions until one is far enough
        # CHANGED: from the previous spawn position.
        if self.previous_spawn_x is None:  # CHANGED
            return random.randint(SPAWN_X_MIN, SPAWN_X_MAX)  # CHANGED

        for _ in range(SPAWN_POSITION_ATTEMPTS):  # CHANGED
            x = random.randint(SPAWN_X_MIN, SPAWN_X_MAX)  # CHANGED
            if abs(x - self.previous_spawn_x) >= MIN_SPAWN_DISTANCE:  # CHANGED
                return x  # CHANGED

        # CHANGED: A valid position is always available on this screen.
        # CHANGED: Choose the endpoint farthest from the previous spawn.
        left_distance = abs(SPAWN_X_MIN - self.previous_spawn_x)  # CHANGED
        right_distance = abs(SPAWN_X_MAX - self.previous_spawn_x)  # CHANGED

        if left_distance >= right_distance:  # CHANGED
            return SPAWN_X_MIN  # CHANGED
        return SPAWN_X_MAX  # CHANGED

    def _spawn_object(self):
        # CHANGED: Keep every circle fully inside the screen and avoid
        # CHANGED: repeatedly using the same horizontal position.
        x = self._get_spawn_x()  # CHANGED
        self.objects.append(  # CHANGED
            FallingObject(x=x, y=-OBJECT_RADIUS, radius=OBJECT_RADIUS, speed=3)  # CHANGED
        )
        self.previous_spawn_x = x  # CHANGED

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
        self.basket.x = max(half_basket_width, min(WIDTH - half_basket_width, self.basket.x))

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()

    def update(self):
        if self.game_over:
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            # CHANGED: Only spawn when the maximum number of active
            # CHANGED: objects has not been reached.
            if len(self.objects) < MAX_OBJECTS_ON_SCREEN:  # CHANGED
                self._spawn_object()  # CHANGED

            # CHANGED: Always schedule the next spawn attempt, even when
            # CHANGED: spawning was skipped because the screen was full.
            self.frames_until_spawn = random.randint(  # CHANGED
                SPAWN_MIN_INTERVAL_FRAMES,  # CHANGED
                SPAWN_MAX_INTERVAL_FRAMES,  # CHANGED
            )  # CHANGED

        for obj in self.objects:
            obj.update()

        basket_rect = self.basket.get_rect()

        # Build a new list instead of removing objects from the
        # same list being iterated over, so adjacent catches
        # are both checked and credited.
        remaining_objects = []
        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining_objects.append(obj)

        self.objects = remaining_objects

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart.",
            )