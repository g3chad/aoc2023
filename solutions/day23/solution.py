import os 
import sys

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def dfs(mat, maxi, visited, length, i, j, dest, cache, honor_slope = True):
 
    slopes = { '^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1) }

    if (i < 0 or j < 0 or i == len(mat) or j == len(mat[0]) or visited[i][j]) or mat[i][j] == '#':
        return
    
    if (i == dest[0] and j == dest[1]):
        maxi[0] = max(maxi[0], length) 
        return    

    visited[i][j] = True
 
    # Recursive call in all 4 directions but
    # if we have to honor slope then we need to know if
    # we're on a slope and only go that direction
    char = mat[i][j]
    if honor_slope and char in ('^', '>', 'v', '<'):
        next_step = slopes[char]
        next_i = i + next_step[0]
        next_j = j + next_step[1]
        dfs(mat, maxi, visited, length + 1, next_i, next_j, dest, cache, honor_slope)
    else:
        dfs(mat, maxi, visited, length + 1, i, j - 1, dest, cache, honor_slope)
        dfs(mat, maxi, visited, length + 1, i + 1, j, dest, cache, honor_slope)
        dfs(mat, maxi, visited, length + 1, i - 1, j, dest, cache, honor_slope)
        dfs(mat, maxi, visited, length + 1, i, j + 1, dest, cache, honor_slope)
 
    visited[i][j] = False

def longestPath(mat,  src, dest, honor_slope = True):
 
    maxi = [0]*1
    maxi[0] = 0
 
    ROWS = len(mat) 
    COLS = len(mat[0])
 
    visited = [[0 for x in range(COLS)] for y in range(ROWS)]
 
    # DFS for the matrix considering every path with back tracking, horrible runtime!
    dfs(mat, maxi, visited, 0, src[0], src[1], dest, set(), honor_slope)
 
    return maxi[0]

def part1(input):
    """Implementation for part 1"""
    grid = [[c for c in row] for row in input]
    src = [0, 1]
    dest = [len(grid) - 1, len(grid[0]) - 2]

    return longestPath(grid, src, dest)

def part2(input):
    """Implementation for part 2"""
    # need to do edge compaction to make this work in a reasonable time
    # build a graph and then compact down to relevant points to consider
    # then we can build a graph mapping the points to other points with
    # the steps from point to point, skipping a bunch of unncessary points
    # I think the input makes this possible 
    grid = [[c for c in row] for row in input]
    start = (0,1)
    end = (len(grid) - 1, len(grid[0]) - 2)
    points = [start,end]
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '#':
                continue
            num_neighbors = 0
            for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or grid[nr][nc] == '#':
                    continue
                else:
                    num_neighbors += 1
            if num_neighbors >= 3:
                points.append((r,c))
    # build adj graph
    directions = [(-1, 0), (1,0), (0,-1), (0,1)]
    graph = { p: {} for p in points }
    for sr, sc in points:
        stack = [(0, sr, sc)]
        seen = {(sr, sc)}
        while stack:
            n,r,c = stack.pop()
            if n != 0 and (r,c) in points:
                graph[(sr,sc)][(r,c)] = n
                continue
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or grid[nr][nc] == '#' or (nr,nc) in seen:
                    continue
                else:
                    stack.append((n + 1, nr, nc))
                    seen.add((nr,nc))
    seen = set()
    #print(graph)
    # dfs through the compressed optimized graph until we get to the end
    def dfs(point):
        if point == end:
            return 0
        m = -float("inf")
        seen.add(point)
        for next in graph[point]:
            if next not in seen:
                m = max(m, dfs(next) + graph[point][next])
        seen.remove(point)

        return m

    return dfs(start)
        


def get_from_file():
    with open(os.getcwd() + '/solutions/day23/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
