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
    use_item(Items.Fertilizer)
    use_item(Items.Water)
    plant(Entities.Tree)

def maintain_tree_plot():
    if(can_harvest()):
        harvest()
        use_item(Items.Fertilizer)
        use_item(Items.Water)
        plant(Entities.Tree)