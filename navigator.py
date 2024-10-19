from __builtins__ import *

def create_path(src_x, src_y, dest_x, dest_y):
    start_op_count = get_op_count()

    current_x = src_x
    current_y = src_y

    world_size = get_world_size()
    radius = world_size / 2
    
    x_multiplier = 0
    y_multiplier = 0

    if current_x < radius and dest_x > radius:
        x_multiplier = -1
    if current_x > radius and dest_x < radius:
        x_multiplier = 1
    
    if current_y < radius and dest_y > radius:
        y_multiplier = -1
    if current_y > radius and dest_y < radius:
        y_multiplier = 1

    dest_x += world_size * x_multiplier
    dest_y += world_size * y_multiplier

    path = []

    while True:
        if current_x == dest_x and current_y == dest_y:
            break
        
        if current_x < dest_x:
            path.append(East)
            current_x += 1
        elif current_x > dest_x:
            path.append(West)
            current_x -= 1

        if current_y < dest_y:
            path.append(North)
            current_y += 1
        elif current_y > dest_y:
            path.append(South)
            current_y -= 1

    quick_print("go_to: ", get_op_count() - start_op_count)

    return path

def create_scan_paths(width, height):
    paths = []

    current_x = 0
    current_y = 0

    for x_index in range(width):
        for y_index in range(height):
            if x_index % 2 == 0:
                if y_index < height - 1:
                    paths.append([North])
                    current_y += 1
                else:
                    paths.append([East])
                    current_x += 1
            else:
                if y_index < height - 1:
                    paths.append([South])
                    current_y -= 1
                else:
                    paths.append([East])
                    current_x += 1

    return paths