from __builtins__ import *

def simlulate_cactus_leaderboard_run(speed):
    unlocks = {
        Unlocks.Pumpkins: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Fertilizer: 99,
        Unlocks.Cactus: 99
    }

    items = {
        Items.Power: 99999,
        Items.Carrot: 99999,
        Items.Pumpkin: 99999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_cactus", unlocks, items, globals, seed, speed)
    minutes = result // 60
    seconds = result % 60

    quick_print("simlulate_pumpkin_leaderboard_run time: ", minutes, ":", seconds)

def simluate_carrot_leaderboard_run(speed):
    unlocks = {
        Unlocks.Pumpkins: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Fertilizer: 99,
        Unlocks.Carrots: 99
    }

    items = {
        Items.Power: 999999999,
        Items.Wood: 999999999,
        Items.Hay: 999999999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_carrot", unlocks, items, globals, seed, speed)
    minutes = result // 60
    seconds = result % 60

    quick_print("simluate_carrot_leaderboard_run time: ", minutes, ":", seconds)

def simulate_dino_leaderboard_run(speed):
    unlocks = {
        Unlocks.Pumpkins: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Fertilizer: 99,
        Unlocks.Dinosaurs: 99
    }

    items = {
        Items.Power: 99999,
        Items.Pumpkin: 99999999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_dino", unlocks, items, globals, seed, speed)

    quick_print(result)

    minutes = result // 60
    seconds = result % 60

    quick_print("simulate_dino_leaderboard_run time: ", minutes, ":", seconds)    

def simulate_fastest_reset_run():
    unlocks = {}
    items = {}
    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_fastest_reset", unlocks, items, globals, seed, 4)

    quick_print("lb_fastest_reset time: ", result // 60, ":", result % 60)

def simulate_hay_leaderboard_run(speed):
    unlocks = {
        Unlocks.Grass: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Operators: 99,
        Unlocks.Watering: 99
    }

    items = {
        Items.Power: 99999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_hay_run", unlocks, items, globals, seed, speed)

    quick_print(result)

    minutes = result // 60
    seconds = result % 60

    quick_print("simulate_hay_leaderboard_run time: ", minutes, ":", seconds)

def simulate_maze_leaderboard_run(speed):
    unlocks = {
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Mazes: 99
    }

    items = {
        Items.Power: 9999999,
        Items.Weird_Substance: 999999999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_maze", unlocks, items, globals, seed, speed)
    minutes = result // 60
    seconds = result % 60

    quick_print("simulate_maze_leaderboard_run time: ", minutes, ":", seconds)

def simulate_polyculture_leaderboard_run(speed):
    unlocks = {
        Unlocks.Carrots: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Fertilizer: 99,
        Unlocks.Polyculture: 99,
        Unlocks.Watering: 99,
        Unlocks.Trees: 99
    }

    items = {
        Items.Power: 99999,
        Items.Carrot: 99999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_polyculture", unlocks, items, globals, seed, speed)
    minutes = result // 60
    seconds = result % 60

    quick_print("simulate_polyculture_leaderboard_run time: ", minutes, ":", seconds)

def simlulate_pumpkin_leaderboard_run(speed):
    unlocks = {
        Unlocks.Pumpkins: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Fertilizer: 99
    }

    items = {
        Items.Power: 99999,
        Items.Carrot: 99999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_pumpkin", unlocks, items, globals, seed, speed)
    minutes = result // 60
    seconds = result % 60

    quick_print("simlulate_pumpkin_leaderboard_run time: ", minutes, ":", seconds)

def simulate_sunflower_leaderboard_run(speed):
    unlocks = {
        Unlocks.Pumpkins: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Fertilizer: 99,
        Unlocks.Sunflowers: 99
    }

    items = {
        Items.Carrot: 99999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_sunflower", unlocks, items, globals, seed, speed)
    minutes = result // 60
    seconds = result % 60

    quick_print("simulate_sunflower_leaderboard_run time: ", minutes, ":", seconds)

def simulate_wood_leaderboard_run(speed):
    unlocks = {
        Unlocks.Trees: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99,
        Unlocks.Plant: 99,
        Unlocks.Fertilizer: 99,
        Unlocks.Watering: 99
    }

    items = {
        Items.Power: 99999,
        Items.Carrot: 99999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_wood_run", unlocks, items, globals, seed, speed)
    minutes = result // 60
    seconds = result % 60

    quick_print("simulate_wood_leaderboard_run time: ", minutes, ":", seconds)