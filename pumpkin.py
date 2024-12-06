from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *

def handle_pumpkin_region(drone, region, iteration):
    path = []

    if iteration == 0:
        path = apply_initial_pumpkin_plan(region)
    else:
        path = apply_maintence_pumpkin_plan(region)
    
    drone["execute_plot_actions"](path)

def apply_initial_pumpkin_plan(region):
    plots = region["plots"]
    plot_count = len(plots)

    item_counts = {
        Items.Pumpkin_Seed: plot_count,
        Items.Fertilizer: plot_count
    }

    do_trade(item_counts)

    path = []

    for plot in plots:
        plot["action"] = init_pumpkin_plot
        path.append(plot["coords"])

    return path

def apply_maintence_pumpkin_plan(region):
    plots = region["plots"]

    def not_ready_test(plot, _):
        return not plot["can_harvest"]

    not_ready = find_in_array(plots, not_ready_test)
    not_ready_count = len(not_ready)

    if not_ready_count == 0:
        return apply_harvest_and_replant_pumpkin_plan(region)
    else:
        return apply_scan_and_replant_pumpkin_plan(region, not_ready)

def apply_scan_and_replant_pumpkin_plan(region, not_ready):
    not_ready_count = len(not_ready)
    plots = region["plots"]
    
    item_counts = {
        Items.Pumpkin_Seed: not_ready_count,
        Items.Fertilizer: not_ready_count
    }
    
    do_trade(item_counts)

    path = []

    for plot in plots:
        if not plot["can_harvest"]:
            plot["priority"] = MAX_PRIORITY
            plot["action"] = plant_and_scan_pumpkin_plot
            
            path.append(plot["coords"])
        else:
            plot["priority"] = NO_PRIORITY
            plot["action"] = no_op

    return path

def apply_harvest_and_replant_pumpkin_plan(region):
    plots = region["plots"]
    plot_count = len(plots)
    path = []

    item_counts = {
        Items.Pumpkin_Seed: plot_count,
        Items.Fertilizer: plot_count
    }

    do_trade(item_counts)

    harvest_plot = plots[0]
    harvest_plot["priority"] = MAX_PRIORITY
    harvest_plot["action"] = harvest_and_replant_pumpkin_plot

    path.append(harvest_plot["coords"])

    for index in range(1, plot_count):
        plot = plots[index]
        plot ["priority"] = MAX_PRIORITY - 1
        plot ["action"] = plant_and_scan_pumpkin_plot

        path.append(plot["coords"])

    return path

def harvest_and_replant_pumpkin_plot(plot):
    harvest()
    plant_and_scan_pumpkin_plot(plot)

def plant_and_scan_pumpkin_plot(plot):
    plant(Entities.Pumpkin)
    use_item(Items.Fertilizer)
    use_item(Items.Water_Tank)

    merge(plot, do_scan())

def init_pumpkin_plot(plot):
    till()
    
    use_item(Items.Fertilizer)
    use_item(Items.Water_Tank)
    plant(Entities.Pumpkin)

    merge(plot, do_scan())