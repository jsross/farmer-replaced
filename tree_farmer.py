from __builtins__ import *
from __test_harness__ import *
from Utility import *

def init_tree_plot():
    use_item(Items.Fertilizer)
    use_item(Items.Water_Tank)
    plant(Entities.Tree)

def maintain_tree_plot():
    if(can_harvest()):
        harvest()
        use_item(Items.Fertilizer)
        use_item(Items.Water_Tank)
        plant(Entities.Tree)