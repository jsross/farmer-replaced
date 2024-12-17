from drone import *

def execute_scan_pass(width, height, action, matrix):
    for x_index in range(width):
        for y_index in range(height):
            if matrix != None:
                matrix[x_index][y_index] = action()
            else:
                action()

            move(North)
        
        move(East)

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