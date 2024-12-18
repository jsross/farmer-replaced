from __builtins__ import *
from __test_harness__ import *
from Utility import *
from bush_farmer import *

def init_tree_farm(width, height):
    execute_dual_scan_pass(width, height, init_tree_plot, init_bush_plot)

    return 0

def maintain_tree_farm(width, height):
    execute_dual_scan_pass(width, height, maintain_tree_plot, maintain_bush_plot)

    return 0

def init_tree_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    plant(Entities.Tree)
    use_item(Items.Fertilizer)

def maintain_tree_plot():
    if get_water() < 0.25:
        use_item(Items.Water)

    if(can_harvest()):
        harvest()
        
        plant(Entities.Tree)
        use_item(Items.Fertilizer)