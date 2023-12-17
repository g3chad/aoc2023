import os 

g_visited = set()

class Beam():
    def __init__(self, grid, pos: tuple = (0,-1), dir: str = 'R') -> None:
        self.pos = pos
        self.dir = dir
        self.grid = grid
        self.ROWS = len(grid)
        self.COLS = len(grid[0])
        self.visited = set()
        self.energized = set()
        if self._valid_pos(pos): self.energized.add(pos)
    
    def _valid_pos(self, pos):
        row = pos[0]
        col = pos[1]
        if row < 0 or row >= self.ROWS or col < 0 or col >= self.COLS:
            return False
        else:
            return True

    def move(self):
        new_pos = None
        match self.dir:            
            case 'R':
                new_pos = (self.pos[0], self.pos[1] + 1)
            case 'L':
                new_pos = (self.pos[0], self.pos[1] - 1)
            case 'U':
                new_pos = (self.pos[0] - 1, self.pos[1])
            case 'D':
                new_pos = (self.pos[0] + 1, self.pos[1])
        global g_visited # hack, have to come back with fresh eyes to find out why my localized visited checks are not working
        if (new_pos[0], new_pos[1], self.dir) in g_visited:
            self.can_move = False
            return (False, None)
        else:
            g_visited.add((new_pos[0], new_pos[1], self.dir))
        
        if (new_pos, self.dir) in self.visited or not self._valid_pos(new_pos):
            self.can_move = False
            return (False, None)
                
        # we can move
        self.pos = new_pos
        self.visited.add((new_pos, self.dir))
        self.energized.add(new_pos)
        new_beams = [] # we might create new beams if we hit a splitter in the right dir
        tile = self.grid[new_pos[0]][new_pos[1]]
        match tile:
            case '/':
                if self.dir == 'R':
                    self.dir = 'U'
                elif self.dir == 'L':
                    self.dir = 'D'
                elif self.dir == 'D':
                    self.dir = 'L'
                elif self.dir == 'U':
                    self.dir = 'R'
                return (True, None)
            case '\\':
                if self.dir == 'R':
                    self.dir = 'D'
                elif self.dir == 'L':
                    self.dir = 'U'
                elif self.dir == 'D':
                    self.dir = 'R'
                elif self.dir == 'U':
                    self.dir = 'L'
                return (True, None)
            case '-':
                if self.dir == 'D' or self.dir == 'U':
                    # assume that current beam is done and these are two new beams
                    l_beam = Beam(self.grid, new_pos, 'L')
                    l_beam.visited = self.visited.copy()
                    new_beams.append(l_beam)
                    r_beam = Beam(self.grid, new_pos, 'R')
                    r_beam.visited = self.visited.copy()
                    new_beams.append(r_beam)

                    return (False, new_beams)
            case '|':
                if self.dir == 'L' or self.dir == 'R':
                    # assume that current beam is done and these are two new beams
                    up_beam = Beam(self.grid, new_pos, 'U')
                    up_beam.visited = self.visited.copy()
                    new_beams.append(up_beam)
                    down_beam = Beam(self.grid, new_pos, 'D')
                    down_beam.visited = self.visited.copy()
                    new_beams.append(down_beam)

                    return (False, new_beams)
            
        return (True, None)

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]
    
def part1(input, start=(0,-1), dir='R'):
    """Implementation for part 1"""
    grid = []
    for row in input:
        grid.append([c for c in row])
    energized = set()
    beams = [ Beam(grid, start, dir) ]
    moving_beams = [beam for beam in beams]
    while moving_beams:        
        for beam in moving_beams:
            valid_beam, new_beams = beam.move()
            if not valid_beam:
                if energized:
                    for e in beam.energized:
                        energized.add(e)
                else:
                    energized = beam.energized.copy()
                beams.remove(beam)                
            if new_beams and len(new_beams) > 0:
                beams = beams + new_beams
        moving_beams = [beam for beam in beams]

    for beam in beams:
        energized = energized.update(beam.energized)
    
    return len(energized)
    
def get_start_points(input):
    starting_points = []
    grid = []
    for row in input:
        grid.append([c for c in row])
    ROWS = len(grid)
    COLS = len(grid[0])
    for r in range(ROWS):
        for c in range(COLS):
            # D
            if r == 0:
                starting_points.append((-1, c, 'D'))
                if c == 0:
                    starting_points.append((0, -1, 'R'))
                if c == COLS - 1:
                    starting_points.append((0, COLS, 'L'))
            # R
            if r > 0 and r < ROWS - 1 and c == 0:
                starting_points.append((r, -1, 'R'))
            # L
            if r > 0 and r < ROWS - 1 and c == COLS - 1:
                starting_points.append((r, COLS, 'L'))
            # U
            if r == ROWS - 1:
                starting_points.append((ROWS, c, 'U'))
                if c == 0:
                    starting_points.append((r, -1, 'R'))
                if c == COLS - 1:
                    starting_points.append((r, COLS, 'L'))
    
    return starting_points
    
def part2(input):
    """Implementation for part 2"""
    max_energy = 0
    starting_points = get_start_points(input)
    for start_pt in starting_points:
        global g_visited
        g_visited = set()
        start = (start_pt[0], start_pt[1])
        dir = start_pt[2]
        e = part1(input, start, dir)
        max_energy = max(e, max_energy)

    return max_energy

def get_from_file():
    with open(os.getcwd() + '/solutions/day16/g3.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    print(part1(input))
    print(part2(input))
