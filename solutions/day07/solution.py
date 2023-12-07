from aocd import get_data
from aocd import submit
import os
from collections import Counter

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def get_hand_rank_jokers(hand):
    if hand == 'JJJJJ':
        return 7 # best we can do 
    counts = dict(Counter(hand))
    number_of_Js = counts['J']
    sorted_counts = sorted(counts.items(), key=lambda x:x[1])
    greatest = sorted_counts[-1][0]
    if greatest == 'J':
        greatest = sorted_counts[-2][0]
    for _ in range(number_of_Js):
        hand = hand.replace('J', greatest, 1)
    counts = dict(Counter(hand))
    return get_hand_rank(counts)

def get_hand_rank(counts):
    # A: 5
    # A: 4, K: 1
    # A: 3, K: 2
    # A: 3, K: 1, T: 1
    # A: 2, K: 2, T: 1
    # A: 2, K: 1, Q: 1, J: 1
    # A: 1, K: 1, J: 1, T: 1, 8: 1
    num_entries = len(counts)
    vals = sorted(counts.values())
    if num_entries == 1:
        return 7
    elif num_entries == 2 and vals[1] == 4:
        return 6
    elif num_entries == 2:
        return 5
    elif num_entries == 3 and vals[-1] == 3:
        return 4
    elif num_entries == 3:
        return 3
    elif num_entries == 4:
        return 2
    else:
        return 1
    
def get_weight(weight):
    if len(weight) == 1:
        weight = '0' + weight
    return weight

def get_rank(hand):
    weights = ['0', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    counts = dict(Counter(hand))
    rank = get_hand_rank(counts)
    sort_key = str(rank)
    weight = ''
    for c in hand:
        weight += get_weight(str(weights.index(c)))
    
    return sort_key + weight

def get_rank_with_jokers(hand):
    weights = ['0', 'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    counts = dict(Counter(hand))
    rank_as_is = get_hand_rank(counts)
    if hand == 'JK3JT':
        print('JK3JT')
    rank_with_jokers = get_hand_rank_jokers(hand) if 'J' in hand else rank_as_is
    rank = max(rank_as_is, rank_with_jokers)
    sort_key = str(rank)
    weight = ''
    for c in hand:
        weight += get_weight(str(weights.index(c)))
    
    return sort_key + weight

def part1(input):
    """ Implementation for Part 1.
    """
    hand_points = []
    for hand_data in input:
        hand = hand_data.split(' ')[0]
        points = hand_data.split(' ')[1]
        rank = get_rank(hand)
        hand_points.append((rank, int(points)))
    score = 0
    ranks = sorted(hand_points)
    for i, entry in enumerate(ranks):
        score += entry[1] * (i+1)
    
    return score

def part2(input):
    """Implementation for Part 2
    """
    hand_points = []
    for hand_data in input:
        hand = hand_data.split(' ')[0]
        points = hand_data.split(' ')[1]
        rank = get_rank_with_jokers(hand)
        hand_points.append((rank, int(points)))
    score = 0
    ranks = sorted(hand_points)
    for i, entry in enumerate(ranks):
        score += entry[1] * (i+1)
    
    return score


def get_from_file():
    with open(os.getcwd() + '/solutions/day07/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 7
    processing_g3chad = True
    if processing_g3chad:
        # processing for my personal leaderboard, get data using my configured login
        puzzle_input = get_data(day=day, year=year)
        input = parse(puzzle_input)
        print(part1(input))
        #submit(part1(input), part="a", day=day, year=year)
        submit(part2(input), part="b", day=day, year=year)
    else:
        # processing for the other leaderboard via file input
        puzzle_input = get_from_file()
        input = parse(puzzle_input)
        part1ans = part1(input)
        part2ans = part2(input)
        # print(part1ans)
        print(part2ans)
        #test cases
        assert get_hand_rank_jokers('J7777') == 7
        assert get_hand_rank_jokers('66A9J') == 4
        assert get_hand_rank_jokers('99J99') == 7
        assert get_hand_rank_jokers('99JTT') == 5
        assert get_hand_rank_jokers('JQAQQ') == 6
        assert get_hand_rank_jokers('JAAAJ') == 7
        assert get_hand_rank_jokers('92AKJ') == 2
        assert get_hand_rank_jokers('JJJJJ') == 7
