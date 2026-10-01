"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    # CHANGED: Check both horizontal and vertical overlap so objects are
    # CHANGED: only caught when they have actually reached the basket.
    obj_left = obj.x - obj.radius  # CHANGED
    obj_right = obj.x + obj.radius  # CHANGED
    obj_top = obj.y - obj.radius  # CHANGED
    obj_bottom = obj.y + obj.radius  # CHANGED

    # CHANGED: Require the falling object's circle bounds to overlap
    # CHANGED: the basket bounds in both directions.
    horizontal_overlap = obj_right >= basket_rect.left and obj_left <= basket_rect.right  # CHANGED
    vertical_overlap = obj_bottom >= basket_rect.top and obj_top <= basket_rect.bottom  # CHANGED

    return horizontal_overlap and vertical_overlap  # CHANGED