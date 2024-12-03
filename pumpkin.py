from __builtins__ import *
from __test_harness__ import *
from Utility import *
from drone import *

def apply_initial_pumpkin_plan(region):
    plots = region["plots"]
    
    item_counts = {
        Items.Pumpkin_Seed: len(plots)
    }

    for plot in plots:
        plot_plan = plot["plan"]
        plot["priority"] = MAX_PRIORITY
        plot_plan.append([init_pumpkin_plot, plot])
    
    return item_counts

def apply_maintence_pumpkin_plan(region):
    plots = region["plots"]

    item_counts = {
        Items.Pumpkin_Seed: len(plots)
    }

    def not_ready_test(plot, _):
        return not plot["can_harvest"]

    not_ready = find_in_array(plots, not_ready_test)
    not_ready_count = len(not_ready)
    plot_count = len(plots)
    index = 0

    if not_ready_count == 0:
        harvest_plot = plots[0]
        harvest_plot["priority"] = 15
        harvest_plot["plan"].append([harvest_and_replant_pumpkin_plot, harvest_plot])
        
        for index in range(1, plot_count):
            plot = plots[index]
            plot_plan = plot["plan"]

            plot["priority"] = 14
            plot_plan.append([plant_and_scan_pumpkin_plot, plot])

            item_counts[Items.Pumpkin_Seed] += len(not_ready)
    else:
        for plot in plots:
            if not plot["can_harvest"]:
                plot["priority"] = MAX_PRIORITY
                item_counts[Items.Pumpkin_Seed] += len(not_ready)
                plot["plan"].append([plant_and_scan_pumpkin_plot, plot])
            else:
                plot["priority"] = NO_PRIORITY

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