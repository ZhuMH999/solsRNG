from snippets.constants import gears_list, crafting_list, items_list

def get_crafting_scroll_total_height(i):
    total_height = 0
    for t in crafting_list[i]:
        if type(t) == str or t == []:
            continue
        total_height += -20 * len(t)
    return total_height

def clip_vertical(rect_top, rect_height, visible_top, visible_bottom):
    rect_bottom = rect_top + rect_height

    # Clamp top and bottom
    clamped_top = max(rect_top, visible_top)
    clamped_bottom = min(rect_bottom, visible_bottom)

    visible_height = clamped_bottom - clamped_top

    if visible_height <= 0:
        return None  # completely outside

    return clamped_top, visible_height
