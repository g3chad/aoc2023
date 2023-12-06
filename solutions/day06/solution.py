from itertools import accumulate
    
def part1(race_data):
    """Implementation for part 1"""
    race_stats = []
    for race in race_data:
        race_time = race[0]
        race_dist_rec = race[1]
        races_won = 0
        for i in range(1, race_time+1):
            if (race_time - i) * i > race_dist_rec:
                races_won += 1
        race_stats.append(races_won)

    return list(accumulate(race_stats, (lambda x, y: x * y)))[-1]

def part2(race_data):
    """Implementation for part 2
    this could be optimized with some math in constant time or binary search I think
    to get the lower and upper bounds in constant or logn time but the brute force
    solves this pretty quickly so I left it as is. Todo to learn more about the math
    behind the constant time solution
    """
    races_won = 0
    for i in range(1, race_data[0]+1):
        if (race_data[0] - i) * i > race_data[1]:
            races_won += 1
    
    return races_won

def get_race_data1():
    # example dataset
    #return [(7,9), (15,40), (30, 200)]
    #bf dataset
    #return [(55,246), (82,1441), (64, 1012), (90,1111)]
    # g3chad dataset
    return [(62,644), (73,1023), (75, 1240), (65,1023)]

def get_race_data2():
    # example dataset
    #return (71530, 940200)
    #bf dataset
    #return (55826490, 246144110121111)    
    # g3chad dataset
    return (62737565, 644102312401023)

if __name__ == "__main__":
    print(part1(get_race_data1()))
    print(part2(get_race_data2()))