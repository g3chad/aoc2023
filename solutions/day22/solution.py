import os 

def overlapping_bricks(b1, b2):
    return max(b1[0], b2[0]) <= min(b1[3], b2[3]) and max(b1[1], b2[1]) <= min(b1[4], b2[4])
    
def drop_bricks(bricks):
    for idx, brick in enumerate(bricks):
        max_overlapping_z = 1
        for possible_brick in bricks[:idx]:
            if overlapping_bricks(brick, possible_brick):
                max_overlapping_z = max(max_overlapping_z, possible_brick[5] + 1) # index 5 is the possible highest point on a vertical brick
        # move the brick down, the lower portion of the brick (idx 2) should be sitting on top of the brick it could fall to
        brick[5] -= brick[2] - max_overlapping_z
        brick[2] = max_overlapping_z

    bricks.sort(key=lambda brick: brick[2])

    return bricks

def build_brick_support_map(bricks):
    brick_support = {idx: set() for idx in range(len(bricks))}
    brick_supported_by = {idx: set() for idx in range(len(bricks))}

    for ui, u_brick in enumerate(bricks):
        for li, l_brick in enumerate(bricks):
            if overlapping_bricks(l_brick, u_brick) and u_brick[2] == l_brick[5] + 1:
                brick_support[li].add(ui)
                brick_supported_by[ui].add(li)
    
    return (brick_support, brick_supported_by)


def part1():
    """Implementation for part 1"""
    file = 'bf'
    bricks = [list(map(int, line.replace('~', ',').split(','))) for line in open(os.getcwd() + '/solutions/day22/' + file + '.txt')]
    bricks.sort(key=lambda brick: brick[2])    
    bricks = drop_bricks(bricks)
    brick_support, brick_supported_by = build_brick_support_map(bricks)
    total = 0
    for i in range(len(bricks)):
        if all(len(brick_supported_by[j]) >= 2 for j in brick_support[i]):
            total += 1

    return total

def part2():
    """Implementation for part 2"""
    file = 'g3'
    bricks = [list(map(int, line.replace('~', ',').split(','))) for line in open(os.getcwd() + '/solutions/day22/' + file + '.txt')]
    bricks.sort(key=lambda brick: brick[2])    
    bricks = drop_bricks(bricks)
    brick_support, brick_supported_by = build_brick_support_map(bricks)
    total = 0
    # 'queue' up everything this brick supports going brick by brick
    for i in range(len(bricks)):
        # get the bricks this brick support and is the only brick supporting it which means other bricks would fall
        q = [b for b in brick_support[i] if len(brick_supported_by[b]) == 1]
        bricks_that_fall = set(q)
        bricks_that_fall.add(i)
        # go through this list of dependent bricks, it'll keep growing as we add to it new bricks that fall from this brick that falls
        while q:
            b = q.pop(0)
            for brick in brick_support[b] - bricks_that_fall:
                if brick_supported_by[brick] <= bricks_that_fall:
                    q.append(brick)
                    bricks_that_fall.add(brick)
        total += len(bricks_that_fall) - 1

    return total

if __name__ == "__main__":
    part1ans = part1()
    part2ans = part2()
    print(part1ans)
    print(part2ans)
