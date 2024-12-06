from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *
from farm import *

def handle_sunflower_region(region, iteration):
    if iteration == 0:
        return apply_init_sunflower_plan(region)
    else:
        return apply_maintence_sunflower_plan(region)

def apply_init_sunflower_plan(region):
    plots = region["plots"]
    plot_count = len(plots)

    item_count = {
        Items.Sunflower_Seed: plot_count,
        Items.Fertilizer: plot_count
    }

    for plot in plots:
        plot["priority"] = MAX_PRIORITY
        plot["action"] = init_sunflower_plot

    return item_count

def apply_maintence_sunflower_plan(region):
    plots = region["plots"]
    plot_count = len(plots)

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

    if plot_count == ready_count: #If all plots are ready, harvest
        for plot in plots:
            plot["priority"] = plot["measure"]
            plot["action"] = harvest_sunflower_plot
    elif ready_count == 0:
        for plot in plots:
            plot["priority"] = MAX_PRIORITY
            plot["action"] = plant_sunflower_plot
    else:
        for plot in plots:
            plot["priority"] = NO_PRIORITY
            plot["action"] = no_op

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
