from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *

def handle_pumpkin_region(region, iteration):
    if iteration == 0:
        return apply_initial_pumpkin_plan(region)
    else:
        return apply_maintence_pumpkin_plan(region)

def apply_initial_pumpkin_plan(region):
    plots = region["plots"]
    plot_count = len(plots)

    item_counts = {
        Items.Pumpkin_Seed: plot_count,
        Items.Fertilizer: plot_count
    }

    do_trade(item_counts)

    for plot in plots:
        plot["priority"] = MAX_PRIORITY
        plot["action"] = init_pumpkin_plot

    return item_counts

def apply_maintence_pumpkin_plan(region):
    plots = region["plots"]


    def not_ready_test(plot, _):
        return not plot["can_harvest"]

    not_ready = find_in_array(plots, not_ready_test)
    not_ready_count = len(not_ready)
    plot_count = len(plots)
    index = 0

    if not_ready_count == 0:
        item_counts = {
            Items.Pumpkin_Seed: plot_count,
            Items.Fertilizer: plot_count
        }
        
        do_trade(item_counts)

        harvest_plot = plots[0]
        harvest_plot["priority"] = MAX_PRIORITY
        harvest_plot["action"] = harvest_and_replant_pumpkin_plot
        
        for index in range(1, plot_count):
            plot = plots[index]
            plot ["priority"] = MAX_PRIORITY - 1
            plot ["action"] = plant_and_scan_pumpkin_plot

            item_counts[Items.Pumpkin_Seed] += len(not_ready)
    else:
        item_counts = {
            Items.Pumpkin_Seed: not_ready_count,
            Items.Fertilizer: not_ready_count
        }
        
        do_trade(item_counts)

        for plot in plots:
            if not plot["can_harvest"]:
                plot["priority"] = MAX_PRIORITY
                plot["action"] = plant_and_scan_pumpkin_plot

                item_counts[Items.Pumpkin_Seed] += len(not_ready)
            else:
                plot["priority"] = NO_PRIORITY
                plot["action"] = no_op

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