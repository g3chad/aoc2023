from aocd import get_data
from aocd import submit
import os, sys
from collections import defaultdict
from typing import List

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def map_item(input, item):
    item_map = []
    skip = True 
    for line in input:
        if not skip and not line.strip():
            break
        if item in line:
            skip = False
            continue
        if skip:
            continue
        values = line.split(' ')
        dest_start = int(values[0])
        source_start = int(values[1])
        source_end = source_start + int(values[2]) - 1
        item_map.append((source_start, source_end, dest_start))

    return sorted(item_map)

def get_lookups(input):
    soil = map_item(input, 'soil ')
    fert = map_item(input, 'fertilizer ')
    water = map_item(input, 'water ')
    light = map_item(input, 'light ')
    temp = map_item(input, 'temperature ')
    humid = map_item(input, 'humidity ')
    loc  = map_item(input, 'location ')

    return (soil, fert, water, light, temp, humid, loc)

def get_seeds(input):
    return [int(i) for i in input[0].split(': ')[1].split(' ')]

def find_for_item(item, a_map):
    for entry in a_map:
        if item >= entry[0] and item <= entry[1]:
            return item + (entry[2] - entry[0])
    return item

def part1(input):
    """ Implementation for Part 1.
    """
    seeds = get_seeds(input)
    soil_map, fert_map, water_map, light_map, temp_map, humid_map, loc_map = get_lookups(input)
    min_loc = 999999999
    for seed in seeds:
        soil = find_for_item(seed, soil_map)
        fert = find_for_item(soil, fert_map)
        water = find_for_item(fert, water_map)
        light = find_for_item(water, light_map)
        temp = find_for_item(light, temp_map)
        humid = find_for_item(temp, humid_map)
        loc = find_for_item(humid, loc_map)
        min_loc = min(loc, min_loc)
    
    return min_loc

def get_next_sources(source_ranges, current_mappings):
    new_ranges = []
    for source_range_start, source_range_end in source_ranges:
        completed_source_range = False
        for mapping_source_start, mapping_source_end, mapping_dest_start in current_mappings:
            if source_range_start < mapping_source_start:
                if source_range_end < mapping_source_start:
                    new_ranges.append((source_range_start, source_range_end))
                    completed_source_range = True
                    break
                if source_range_end <= mapping_source_end:
                    new_ranges.append((source_range_start, mapping_source_start))
                    new_ranges.append((mapping_dest_start, mapping_dest_start + (source_range_end - mapping_source_start)))
                    completed_source_range = True
                    break
                new_ranges.append((source_range_start, mapping_source_start))
                new_ranges.append((mapping_dest_start, mapping_dest_start + (mapping_source_end - mapping_source_start)))
                source_range_start = mapping_source_end
            elif mapping_source_start <= source_range_start < mapping_source_end:
                if source_range_end <= mapping_source_end:
                    new_ranges.append((mapping_dest_start + (source_range_start - mapping_source_start), mapping_dest_start + (source_range_end - mapping_source_start)))
                    completed_source_range = True
                    break
                new_ranges.append((mapping_dest_start + (source_range_start - mapping_source_start) , mapping_dest_start + (mapping_source_end - mapping_source_start)))
                source_range_start = mapping_source_end
        if not completed_source_range:
            new_ranges.append((source_range_start, source_range_end))
    return new_ranges

def get_map_ranges(input, item, source_ranges):
    current_mappings = []
    skip = True 
    for line in input:
        if not skip and not line.strip():
            break
        if item in line:
            skip = False
            continue
        if skip:
            continue
        values = line.split(' ')
        dest_start = int(values[0])
        source_start = int(values[1])
        source_end = source_start + int(values[2]) 
        current_mappings.append((source_start, source_end, dest_start))

    return get_next_sources(source_ranges, sorted(current_mappings))

def part2(input):
    seed_ranges = []
    seed_range = input[0].split(": ")[1].split(" ")
    for i in range(0, len(seed_range), 2):
        seed_ranges.append((int(seed_range[i]), int(seed_range[i]) + int(seed_range[i+1])))
    soil_ranges = get_map_ranges(input, 'seed-to-soil', seed_ranges)
    fert_ranges = get_map_ranges(input, 'soil-to-fertilizer', soil_ranges)
    water_ranges = get_map_ranges(input, 'fertilizer-to-water', fert_ranges)
    light_ranges = get_map_ranges(input, 'water-to-light', water_ranges)
    temp_ranges = get_map_ranges(input, 'light-to-temperature', light_ranges)
    humid_ranges = get_map_ranges(input, 'temperature-to-humidity', temp_ranges)
    loc_ranges = get_map_ranges(input, 'humidity-to-location', humid_ranges)
    
    return sorted(loc_ranges)[0][0]

def get_from_file():
    with open(os.getcwd() + '/solutions/day05/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 5
    processing_g3chad = True
    if processing_g3chad:
        # processing for my personal leaderboard, get data using my configured login
        puzzle_input = get_data(day=day, year=year)
        input = parse(puzzle_input)
        print(part1(input))
        print(part2(input))
        #submit(part1(input), part="a", day=day, year=year)
        #submit(part2(input), part="b", day=day, year=year)
    else:
        # processing for the other leaderboard via file input
        puzzle_input = get_from_file()
        input = parse(puzzle_input)
        part1ans = part1(input)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
