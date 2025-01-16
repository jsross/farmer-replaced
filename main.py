from __builtins__ import *
from simulations import *

leaderboard_run(Leaderboards.Pumpkins, "lb_pumpkin", 5000)

simlulate_cactus_leaderboard_run(500)
simluate_carrot_leaderboard_run(500)
simulate_dino_leaderboard_run(500)
simulate_hay_leaderboard_run(500)
simulate_maze_leaderboard_run(500)
# simulate_polyculture_leaderboard_run(500)
simlulate_pumpkin_leaderboard_run(1)
# simulate_sunflower_leaderboard_run(500)
simulate_wood_leaderboard_run(500)

def submit_leaderboard_runs():
    leaderboard_run(Leaderboards.Maze, "lb_maze", 1000)
    leaderboard_run(Leaderboards.Dinosaur, "lb_dino", 1000)
    leaderboard_run(Leaderboards.Polyculture, "lb_polyculture", 1000)
    leaderboard_run(Leaderboards.Cactus, "lb_cactus", 1000)
    leaderboard_run(Leaderboards.Sunflowers, "lb_sunflower", 1000)
    leaderboard_run(Leaderboards.Pumpkins, "lb_pumpkin", 5000)
    leaderboard_run(Leaderboards.Carrots, "lb_carrot", 1000)
    leaderboard_run(Leaderboards.Wood, "lb_wood_run", 1000)
    leaderboard_run(Leaderboards.Hay, "lb_hay_run", 1000)
    leaderboard_run(Leaderboards.Fastest_Reset, "lb_fastest_reset", 1)