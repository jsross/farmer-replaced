def simulate_hay_leaderboard_run():
    unlocks = {
        Unlocks.Grass: 99,
        Unlocks.Expand: 99,
        Unlocks.Speed: 99
    }

    items = {
        Items.Power: 9999999
    }

    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_hay_run", unlocks, items, globals, seed, 5000)

    print(result)

def simulate_fastest_rest_run():
    unlocks = {}
    items = {}
    globals = {}

    seed = random() * 10000 // 1

    result = simulate("lb_fastest_reset", unlocks, items, globals, seed, 4)

    quick_print("lb_fastest_reset: ", result)