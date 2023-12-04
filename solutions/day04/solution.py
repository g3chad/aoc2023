from aocd import get_data
from aocd import submit
import os
from collections import defaultdict

def parse(puzzle_input):
    """Parse input."""    
    return puzzle_input.splitlines()

def get_winners(cards):
    two_stacks = cards.split(': ')[1].split(' | ')
    winning_cards = [i for i in two_stacks[0].split(' ') if i]    
    my_cards = [i for i in two_stacks[1].split(' ') if i]

    return list(set(winning_cards) & set(my_cards))

def part1(input):
    """ Implementation for Part 1.
    """
    points = 0
    for cards in input:
        winners = get_winners(cards)
        if winners:
            prev = 1         
            for _ in range(1,len(winners)):
                prev *= 2
            points += prev

    return points 

def part2(input):
    """Implementation for Part 2
    """
    card_stacks = dict([(i+1, 1) for i in range(len(input))])    
    for cards in input:
        card_num = int(cards.split(':')[0].replace('Card ', ''))
        # probably should calc once and cache but this but this is quick thing to do
        winners = get_winners(cards)
        if not winners:
            continue
        
        for _ in range(card_stacks[card_num]):
            cur_card = card_num
            for _ in range(len(winners)):
                cur_card += 1
                card_stacks[cur_card] += 1
                
    return sum(card_stacks.values())

def get_from_file():
    with open(os.getcwd() + '/solutions/day04/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    year = 2023
    day = 4
    processing_g3chad = False
    if processing_g3chad:
        # processing for my personal leaderboard, get data using my configured login
        puzzle_input = get_data(day=day, year=year)
        input = parse(puzzle_input)
        print(part1(input))
        submit(part1(input), part="a", day=day, year=year)
        submit(part2(input), part="b", day=day, year=year)
    else:
        # processing for the other leaderboard via file input
        puzzle_input = get_from_file()
        input = parse(puzzle_input)
        part1ans = part1(input)
        part2ans = part2(input)
        print(part1ans)
        print(part2ans)
