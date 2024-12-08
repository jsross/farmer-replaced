from __builtins__ import *
from __test_harness__ import *
from Utility import *

def init_tree_plot():
    plant(Entities.Tree)

def maintain_tree_plot():
    if(can_harvest()):
        harvest()
    
    plant(Entities.Tree)