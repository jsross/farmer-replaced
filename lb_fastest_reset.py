from __builtins__ import *
from hay_farmer import *
from bush_farmer import *
from carrot_farmer import *
from tree_farmer import *
from pumpkin_farmer import *
from sunflower_farmer import *

farm_functions = {
    Entities.Grass: farm_hay,
    Entities.Bush: farm_bush,
    Entities.Carrot: farm_carrots,
    Entities.Pumpkin: farm_pumpkins,
    Entities.Tree: farm_trees,
    Entities.Sunflower: farm_sunflowers
}

item_sources = {
    Items.Hay: Entities.Grass,
    Items.Wood: Entities.Bush,
    Items.Carrot: Entities.Carrot,
    Items.Pumpkin: Entities.Pumpkin,
    Items.Power: Entities.Sunflower
}

item_order = [Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin, Items.Power]

unlock_order = [Unlocks.Carrots, Unlocks.Expand, Unlocks.Watering, Unlocks.Speed, Unlocks.Trees, Unlocks.Pumpkins, Unlocks.Expand, Unlocks.Expand, Unlocks.Speed, Unlocks.Speed, Unlocks.Speed]

def stage_0():
    speed_unlock_cost = get_cost(Unlocks.Speed)
    quick_print("Speed Cost: ", speed_unlock_cost)

    while True:
        harvest()
        if num_items(Items.Hay) >= speed_unlock_cost[Items.Hay]:
            break

    unlock(Unlocks.Speed)

    expand_unlock_cost = get_cost(Unlocks.Expand)
    quick_print("Expand Cost: ", expand_unlock_cost)

    while True:
        if can_harvest():
            harvest()
            if num_items(Items.Hay) >= expand_unlock_cost[Items.Hay]:
                break

    unlock(Unlocks.Expand)

def stage_1():
    plant_unlock_cost = get_cost(Unlocks.Plant)
    quick_print("Plant Unlock: ", plant_unlock_cost)

    while True:
        harvest()
        if num_items(Items.Hay) >= plant_unlock_cost[Items.Hay]:
            break
        move(North)

    unlock(Unlocks.Plant)

    expand_unlock_cost = get_cost(Unlocks.Expand)
    quick_print("Expand Cost: ", expand_unlock_cost)

    while True:
        if can_harvest():
            harvest()
            if num_items(Items.Wood) >= expand_unlock_cost[Items.Wood]:
                break
        plant(Entities.Bush)
        move(North)

    unlock(Unlocks.Expand)

def stage_2():

    for type in unlock_order:
        do_unlock(type)

    pass

def do_unlock(unlock_type):
    quick_print("do_unlock: ", unlock_type)
    unlock_costs = get_expanded_unlock_cost(unlock_type)

    quick_print("expanded unlock costs", unlock_costs)

    for item_type in item_order:
        if item_type not in unlock_costs:
            continue
        
        goal = unlock_costs[item_type]
        entity_type = item_sources[item_type]

        farm = farm_functions[entity_type]
        clear()
        farm(goal)

    unlock(unlock_type)

    if unlock_type == Unlocks.Trees:
        item_sources[Items.Wood] = Entities.Tree

    quick_print(unlock_type, " unlocked")

quick_print("Speed Unlock: ", get_cost(Unlocks.Speed))

stage_0()
stage_1()
stage_2()

quick_print("End")

def get_expanded_unlock_cost(unlock_type):
    expanded_costs = {}
    unlock_cost_map = get_cost(unlock_type)
    quick_print("Unlock Cost: ", unlock_cost_map)
    
    for item_type in unlock_cost_map:
        item_quantity = unlock_cost_map[item_type]
        expanded_costs[item_type] = unlock_cost_map[item_type]
        expanded_item_cost = get_expanded_item_cost(item_type, item_quantity)

        merge_costs(expanded_item_cost, expanded_costs)

    return expanded_costs

def get_expanded_item_cost(item_type, quantity):
    expanded_item_costs = {}
    entity_type = item_sources[item_type]
    entity_cost_map = get_cost(entity_type)

    for cost_key in entity_cost_map:
        expanded_item_costs[cost_key] = entity_cost_map[cost_key] * quantity

        expanded_item_cost = get_expanded_item_cost(cost_key, entity_cost_map[cost_key])
        merge_costs(expanded_item_cost, expanded_item_costs)
    
    return expanded_item_costs

def merge_costs(source, dest):
    for source_key in source:
        if source_key in dest:
            dest[source_key] += source[source_key]
        else:
            dest[source_key] = source[source_key]

    return dest