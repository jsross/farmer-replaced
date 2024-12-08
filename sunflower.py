from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *
from farm import *

def handle_sunflower_region(drone, region, iteration):
    path = []

    if iteration == 0:
        path = apply_init_sunflower_plan(region)
    else:
        path = apply_maintence_sunflower_plan(region)

    drone["execute_plot_actions"](path)

def apply_init_sunflower_plan(region):
    plots = region["plots"]
    plot_count = len(plots)

    item_counts = {
        Items.Sunflower_Seed: plot_count,
        Items.Fertilizer: plot_count
    }

    do_trade(item_counts)

    path = []

    for plot in plots:
        plot["priority"] = MAX_PRIORITY
        plot["action"] = init_sunflower_plot
        path.append(plot["coords"])

    return path

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

        item_counts = {
            Items.Sunflower_Seed: plot_count,
            Items.Fertilizer: plot_count
        }

        do_trade(item_counts)
    else:
        for plot in plots:
            plot["priority"] = NO_PRIORITY
            plot["action"] = no_op

    path = []

    for priority in range(MAX_PRIORITY, 1, -1):
        prioritized = select_object_from_array(plots, {"priority": priority})

        for plot in prioritized:
            path.append(plot["coords"])
        
    return path

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
