from snippets.constants import INV_DIMENSIONS, INV_SHOWCASE_SIZE, items_list, ITEMS_DIMENSIONS

def get_clicked_inventory_cell(mouse_pos, visuals, inventory, current_selected, dimensions, group_by_type=False):
    mouse_x, mouse_y = mouse_pos
    add_y = 0

    if group_by_type:
        items_sorted = sorted(inventory, key=lambda x: ['Potion', 'Rune', 'Tool', 'Material', 'Misc', 'Event'].index(items_list[x][-1]))
        current_type = None
        j = 0

    for i in range(len(inventory)):
        if group_by_type and items_list[items_sorted[i]][-1] != current_type:
            add_y += (ITEMS_DIMENSIONS[1] + 5) * ((j + 5) // ITEMS_DIMENSIONS[0])
            current_type = items_list[items_sorted[i]][-1]
            add_y += 40
            j = 0

        # Compute cell position
        x, cell_y, width, height, _, _ = draw_inventory_slot(j if group_by_type else i, visuals.inventory_info[0], dimensions, add_y)
        if group_by_type:
            j += 1

        # Check if mouse is inside this cell
        if x <= mouse_x <= x + width and cell_y <= mouse_y <= cell_y + height:
            if group_by_type:
                return items_sorted[i]
            return i  # Return the index of the clicked cell
    return current_selected

def cutoff_inv_scrolling(scroll_y, inventory, group_by_type=False):
    inv_info = max(scroll_y * -1, 0) * -1  # Prevents scrolling past 0 (layer 1)

    total_height = manage_height_inv(inventory, group_by_type)

    if total_height > INV_SHOWCASE_SIZE:
        if inv_info * -1 > total_height - INV_SHOWCASE_SIZE:
            inv_info = (INV_SHOWCASE_SIZE - total_height)
    else:
        inv_info = 0

    return inv_info

def draw_inventory_slot(i, scroll_y, dimensions, text_offset_y=0):
    number_of_cells = dimensions[0]
    width = dimensions[1]

    x_offset = (width + 5) * (i % number_of_cells)
    y_offset = (width + 5) * (i // number_of_cells)

    x = 390 + x_offset
    text_y = 250 + scroll_y + y_offset + text_offset_y
    cell_y = 250 + scroll_y + y_offset + text_offset_y

    if cell_y < 245:
        height = width - (245 - cell_y)  # reduce height by the amount above 245
        cell_y = 245  # clamp top
        if height < 0:
            height = 0  # don't allow negative height
    elif cell_y > 562.5:
        height = width - (cell_y - 562.5)
        if height < 0:
            height = 0
    else:
        height = width

    return x, cell_y, width, height, x + width / 2, text_y + width / 2

def manage_height_inv(inventory, group_by_type=False):
    current_type = None
    y_offset = 0
    j = 0

    if group_by_type:
        items_sorted = sorted(inventory, key=lambda x: ['Potion', 'Rune', 'Tool', 'Material', 'Misc', 'Event'].index(items_list[x][-1]))
    else:
        items_sorted = inventory[:]

    if group_by_type:
        for i in range(len(items_sorted)):
            if items_list[items_sorted[i]][-1] != current_type:
                y_offset += (ITEMS_DIMENSIONS[1] + 5) * ((j + 5) // ITEMS_DIMENSIONS[0])
                j = 0
                current_type = items_list[items_sorted[i]][-1]
                y_offset += 40
            j += 1

        total_height = y_offset + ITEMS_DIMENSIONS[1] + 5

    else:
        total_height = ((len(inventory) + 6) // INV_DIMENSIONS[0]) * (INV_DIMENSIONS[1] + 5)

    return total_height