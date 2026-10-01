"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_BOOST_BASKET = (70, 180, 255)  # CHANGED
COLOR_TEXT = (255, 255, 255)
COLOR_BOOST_TEXT = (80, 220, 255)  # CHANGED
COLOR_COOLDOWN_TEXT = (255, 190, 80)  # CHANGED


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(
            surface,
            obj.color,
            (int(obj.x), int(obj.y)),
            obj.radius,
        )

    # CHANGED: Change the basket color while its speed boost is active.
    basket_color = (  # CHANGED
        COLOR_BOOST_BASKET if basket.is_boost_active() else COLOR_BASKET  # CHANGED
    )  # CHANGED
    pygame.draw.rect(
        surface,
        basket_color,  # CHANGED
        basket.get_rect(),
        border_radius=6,
    )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(
        center=(surface.get_width() // 2, surface.get_height() // 2)
    )
    surface.blit(surf, rect)


def draw_boost_status(surface, font, basket):  # CHANGED
    if basket.is_boost_active():  # CHANGED
        remaining = basket.get_boost_remaining_seconds()  # CHANGED
        text = f"BOOST ACTIVE - {remaining}s"  # CHANGED
        draw_text(surface, font, text, (10, 62), COLOR_BOOST_TEXT)  # CHANGED
    elif basket.is_boost_ready():  # CHANGED
        draw_text(  # CHANGED
            surface,  # CHANGED
            font,  # CHANGED
            "Boost ready (SPACE)",  # CHANGED
            (10, 62),  # CHANGED
            COLOR_TEXT,  # CHANGED
        )  # CHANGED
    else:  # CHANGED
        cooldown_seconds = (basket.cooldown_frames + 59) // 60  # CHANGED
        text = f"Boost cooldown - {cooldown_seconds}s"  # CHANGED
        draw_text(  # CHANGED
            surface,  # CHANGED
            font,  # CHANGED
            text,  # CHANGED
            (10, 62),  # CHANGED
            COLOR_COOLDOWN_TEXT,  # CHANGED
        )  # CHANGED