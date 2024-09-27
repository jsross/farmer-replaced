def do_wall_follow(drone, check_goal):
    start_op_count = get_op_count()
    drone_get_last_move = drone["get_last_move"]
     
    do_move = drone["do_move"]
    get_coords = drone["get_coords"]
	last_move = None
	
    def try_moves(directions):
        success = False
        
        for index in range(len(directions)):
            direction = directions[index]
            success = do_move(direction)

            if success:
                break
    
    visited = {}

    while True:
        if check_goal():
             quick_print("do_wall_follow: ", get_op_count() - start_op_count)

             return True

        if last_move == North:
            try_moves([West, North, East, South])
        elif last_move == East:
            try_moves([North, East, South, West])
        elif last_move == South:
            try_moves([East, South, West, North])
        elif last_move == West:
            try_moves([South, West, North, East])
        else:
            try_moves([West, North, East, South])
            
        current_coords = get_coords()

        last_move = drone_get_last_move()

        if current_coords in visited and visited[current_coords] == last_move:
            return False

        visited[get_coords()] = drone_get_last_move()