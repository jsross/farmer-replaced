from drone import *

def execute_scan_pass(width, height, action, x_offset, y_offset):
    for x_index in range(width):
        for y_index in range(height):
            go_to(x_index + x_offset, y_index + y_offset)
            action()
                

def execute_scan_pass_with_matrix(width, height, action, matrix, x_offset, y_offset):
    for x_index in range(width):
        for y_index in range(height):
            go_to(x_index + x_offset, y_index + y_offset)

            if matrix != None:
                matrix[x_index][y_index] = action()
            else:
                action()

def execute_path_action(path, action, x_offset, y_offset, matrix):
    for coords in path:
        go_to(coords[0] + x_offset, coords[1] + y_offset)

        if matrix != None:
            matrix[coords[0]][coords[1]] = action()
        else:
            action()

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
