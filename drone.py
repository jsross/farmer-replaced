def create_drone():
    action_plans = []
	entity_handlers = {}

    def execute_action_plan(action_plan):
        plan_len = len(action_plan)
        cursor = 0

        while True:
            if 0 > cursor or cursor > plan_len - 1:
                break

            action = action_plan[cursor]

            result = action()

            if result == None:
                result = 0

            if result < 0:
                break

            if result > 0:
                cursor = result
            else:
                cursor += 1

    def go_to(coord):
        origin_x = get_pos_x()
        origin_y = get_pos_y()
        x = coord[0]
        y = coord[1]
        
        while True:
            moved = False
            current_x = get_pos_x()
            current_y = get_pos_y()
				
            if current_x < x:
                moved = moved or move(East)
            elif current_x > x:
                moved = moved or move(West)

            if current_y < y:
                moved = moved or move(North)
            elif current_y > y:
                moved = moved or move(South)
                
            if not moved:
                break
		
	def follow_path(path):
		for coord in path:
			go_to(coord)
			           
	def scan():
		x = get_pos_x()
		y = get_pos_y()
		
		plot = game_board["get_node"]((x,y))
		plot["entity_type"] = get_entity_type()
		plot["water_level"] = get_water()
		plot["scan_time"] = get_time()
		plot["can_harvest"] = can_harvest()
		plot["ground_type"] = get_ground_type()
		
    def farm():
        x = get_pos_x()
        y = get_pos_y()
        
        entity_type = farm_plan[x][y]
        plot = game_board["get_node"]((x,y))

        if entity_type in entity_handlers:
            handler = entity_handlers[entity_type]
            handler(x, y)

        pass
        
    def register_entity_handler(key, handler):
		entity_handlers[key] = handler
    	
    drone = {
		"execute_action_plan": execute_action_plan,
        "farm": farm,
        "scan": scan,
        "go_to": go_to,
        "follow_path": follow_path,
        "register_entity_handler": register_entity_handler
    }

    return drone