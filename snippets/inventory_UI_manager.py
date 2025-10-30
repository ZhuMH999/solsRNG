from snippets.constants import INV_DIMENSIONS, INV_SHOWCASE_SIZE

def get_clicked_inventory_cell(mouse_pos, visuals, inventory, current_selected):
    number_of_cells = INV_DIMENSIONS[0]
    width = INV_DIMENSIONS[1]

    mouse_x, mouse_y = mouse_pos

    for i in range(len(inventory)):
        # Compute cell position
        x_offset = (width + 5) * (i % number_of_cells)
        y_offset = (width + 5) * (i // number_of_cells)

        x = 390 + x_offset
        cell_y = 250 + visuals.inventory_info[0] + y_offset

        # Shrink cell if it's above/below bounds
        if cell_y < 245:
            height = width - (245 - cell_y)
            cell_y = 245
            if height < 0:
                height = 0
        elif cell_y > 562.5:
            height = width - (cell_y - 562.5)
            if height < 0:
                height = 0
        else:
            height = width

        # Check if mouse is inside this cell
        if x <= mouse_x <= x + width and cell_y <= mouse_y <= cell_y + height:
            return i  # Return the index of the clicked cell
    return current_selected

def cutoff_inv_scrolling(scroll_y, inventory):
    inv_info = max(scroll_y * -1, 0) * -1  # Prevents scrolling past 0 (layer 1)
    rows = manage_rows_inv(inventory)

    total_height = rows * (INV_DIMENSIONS[1] + 5)

    # If the total height off the screen is smaller than the scrolling offset, set offset as the total height off the screen
    if rows >= 6 and total_height - INV_SHOWCASE_SIZE < inv_info * -1:
        inv_info = (total_height - INV_SHOWCASE_SIZE) * -1
    # If the inventory has not extended past the screen yet, set offset as 0
    elif rows < 6:
        inv_info = 0
    return inv_info

def draw_inventory_slot(i, scroll_y):
    number_of_cells = INV_DIMENSIONS[0]
    width = INV_DIMENSIONS[1]

    x_offset = (width + 5) * (i % number_of_cells)
    y_offset = (width + 5) * (i // number_of_cells)

    x = 390 + x_offset
    text_y = 250 + scroll_y + y_offset
    cell_y = 250 + scroll_y + y_offset

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

def manage_rows_inv(inventory):
    if len(inventory) % INV_DIMENSIONS[0] == 0 and len(inventory) > 0:
        return len(inventory) // INV_DIMENSIONS[0]
    else:
        return len(inventory) // INV_DIMENSIONS[0] + 1