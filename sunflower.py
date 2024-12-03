from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *

def apply_init_sunflower_plan(region):
    plots = region["plots"]

    item_count = {
        Items.Sunflower_Seed: len(plots)
    }

    for plot in plots:
        plot_plan = plot["plan"]
        plot["priority"] = MAX_PRIORITY

        plot_plan.append([init_sunflower_plot, plot])

    return item_count

def apply_maintence_sunflower_plan(region):
    plots = region["plots"]

    current_timestamp = get_time()

    def ready_test(plot, _):
        if plot["entity_type"] != Entities.Sunflower:
            return False
        
        if plot["can_harvest"]:
            return True

        if current_timestamp - plot["timestamp"] > 6:
            return True

        return False

    ready = find_in_array(plots, ready_test)

    ready_count = len(ready)

    if len(plots) == ready_count:
        for plot in plots:
            plot["priority"] = plot["measure"]
            plot["plan"].append([harvest_sunflower_plot, plot])
    elif ready_count == 0:
        for plot in plots:
            plot["priority"] = MAX_PRIORITY
            plot["plan"].append([plant_sunflower_plot, plot])
    else:
        for plot in plots:
            plot["priority"] = NO_PRIORITY
			
def init_sunflower_plot(plot):
    till()

    use_item(Items.Fertilizer)
    use_item(Items.Water_Tank)
    plant(Entities.Sunflower)

    merge(plot, do_scan())

def plant_sunflower_plot(plot):
    use_item(Items.Fertilizer)
    use_item(Items.Water_Tank)
    plant(Entities.Sunflower)

    merge(plot, do_scan())

def harvest_sunflower_plot(plot):
    harvest()
    merge(plot, do_scan())
