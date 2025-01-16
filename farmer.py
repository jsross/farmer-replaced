from drone import *

def execute_scan_pass(width, height, action, x_offset, y_offset):
    go_to(x_offset, y_offset)

    current_x = 0
    current_y = 0

    for x_index in range(width):
        for y_index in range(height):
            action(current_x, current_y)

            if x_index % 2 == 0:
                if y_index < height - 1:
                    move(North)
                    current_y += 1
                else:
                    move(East)
                    current_x += 1
            else:
                if y_index < height - 1:
                    move(South)
                    current_y -= 1
                else:
                    move(East)
                    current_x += 1

def execute_path_action(path, action, x_offset, y_offset):
    for coords in path:
        go_to(coords[0] + x_offset, coords[1] + y_offset)

        action(coords[0], coords[1])

def execute_dual_scan_pass(width, height, action1, action2):
     for x_index in range(width):
        for y_index in range(height):
            rem = y_index % 2

            if (x_index - rem ) % 2 == 0:
                action1()
            else:
                action2()

            move(North)
        
        move(East)

def execute_single_farmer(farmer):
    result = farmer()

    while result != None:
        status = result["status"]
        next_pass = result["next_pass"]
        delay = result["delay"]
        
        if status < 0:
            print("Farmer Failed")

            break

        if delay > 0:
            wait_till(get_time() + delay)

        result = next_pass()

def calculate_adjusted_grow_time(base_grow_time, water_level):
    speed = (4 * water_level) + 1

    return base_grow_time / speed

def maintain_plot_water():
    if num_unlocked(Unlocks.Watering) > 0 and num_items(Items.Water) > 0 and get_water() < 0.25:
        use_item(Items.Water)