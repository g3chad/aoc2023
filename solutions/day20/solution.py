import os 
import math
from collections import defaultdict, deque

# more ugliness, coding fast and late at night to solve the puzzle
# we have to find and track the cycles in part 2 and trying to reuse
# some code from P1, just needed to refactor better to avoid all this
SCOPE = []
final_four = []
rx_sender = ''

class Module:
    def __init__(self, type) -> None:
        if type == '%':
            self.type = 'FF'
            self.state = 'off'
            self.pulse = 'low'
        elif type == '&':
            self.type = 'CON'
            self.state = ''
            self.pulse = 'low'
        else:
            self.type = type
            self.state = ''
            self.pulse = 'low'
        self.destinations = []
        self.inputs = {}
    
    def toggle_ff(self):
        if self.state == 'on':
            self.state = 'off'
        else:
            self.state = 'on'
    
    def add_dests(self, dests):
        for d in dests:
            if d not in self.destinations:
                self.destinations.append(d)

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]

def build_network(input):
    global SCOPE, rx_sender
    network = {}
    for line in input:
        module = line.split(' -> ')[0].strip()
        module_name = ''
        if module[0] == '&' or module[0] == '%':
            network[module[1:]] = Module(module[0])
            module_name = module[1:]
        else:
            network[module] = Module(module)
            module_name = module
        destinations = line.split(' -> ')[1].strip().split(', ')
        network[module_name].add_dests(destinations) 
        if 'rx' in destinations:
            rx_sender = module_name
    
    for k,_ in network.items():
        if network[k].type == 'CON':            
            for lookup, mod in network.items():
                if k in mod.destinations:
                    network[k].inputs[lookup] = 'low'
    
    # build our scope for part 2    
    for k, m in network.items():
        if rx_sender in m.destinations:
            SCOPE.append(k)

    return network

def press_button(network, button_press, part='1'):
    BROADCASTER = 'broadcaster'
    LOW = 'low'
    FLIP_FLOP = 'FF'
    CONJUNCTION = 'CON'
    ON = 'on'
    OFF = 'off'
    HIGH = 'high'
    low_count = high_count = 0
    BUTTON = 'button'
    queue = deque()
    queue.append((BUTTON, BROADCASTER, LOW))
    while queue:
        source_mod, recvr_mod_nm, pulse = queue.popleft()        
        global SCOPE, final_four, rx_sender
        if part == '2' and recvr_mod_nm == rx_sender and source_mod in SCOPE and pulse == HIGH:
            final_four.append(button_press)
            if len(final_four) == 4:
                return (0,0,math.lcm(*final_four))
        if pulse == LOW:
            low_count += 1
        elif pulse == HIGH:
            high_count += 1
        else:
            print(' !!!!! strange pulse detected')
        if recvr_mod_nm == BROADCASTER:
            for dest in network[recvr_mod_nm].destinations:
                queue.append((BROADCASTER, dest, pulse))
        else:
            if recvr_mod_nm not in network:
                continue
            module = network[recvr_mod_nm]
            if module.type == FLIP_FLOP and pulse == LOW:
                module.toggle_ff()
                signal = LOW
                if module.state == ON:
                    signal = HIGH
                module.pulse = signal
                for dest in module.destinations:
                    queue.append((recvr_mod_nm, dest, signal))
            elif module.type == CONJUNCTION:
                module.pulse = pulse
                if source_mod in module.inputs:
                    module.inputs[source_mod] = pulse
                signal = LOW
                for _,v in module.inputs.items():
                    if v == LOW:
                        signal = HIGH
                        break
                for dest in module.destinations:
                    queue.append((recvr_mod_nm, dest, signal))
    
    return (low_count, high_count, 0)
        
def print_network(network):
    for k, v in network.items():
        print(f' module {k} (which is a {v.type}) outputs to {v.destinations} ', end=' ') 
        if network[k].type != 'CON':
            print('') 
        else:
            print(f' - with inputs {network[k].inputs}')

def check_network(network, add_missing=False):
    to_add = []
    for _,v in network.items():
        for d in v.destinations:
            if d not in network:
                if not add_missing:
                    print(f'missing {d}')
                else:
                    to_add.append(d)
    if to_add:
        for d in to_add:            
            network[d] = Module(d)                                    

def part1(input, tries=1000):
    """Implementation for part 1"""
    network = build_network(input)
    l_count = h_count = 0
    for i in range(tries):
        l, h, _ = press_button(network, i+1)
        l_count += l
        h_count += h
    
    return l_count * h_count
    
def part2(input):
    """Implementation for part 2"""
    network = build_network(input)
    i = 0
    while True:
        _, _, lcm = press_button(network, i+1, part='2')
        if lcm > 0:
            return lcm
        i += 1
    
def get_from_file():
    with open(os.getcwd() + '/solutions/day20/g3.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
