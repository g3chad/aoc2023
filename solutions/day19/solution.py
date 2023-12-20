import os 

# this is as ugly as it gets
# should be able to simplify expression parsing and execution, convert strings to executable expressions using lambdas
# the range handling for part 2 was tricky
# this code should be printed on a new sweater to be worn at an ugly sweater Christmas party!

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]
   
def get_workflow_info(input):
    workflows = {}
    part_ratings = []
    parsing_workflows = True
    for row in input:
        if not row.strip():
            parsing_workflows = False
            continue
        if parsing_workflows:
            key = row.split('{')[0]
            rules = row.split('{')[1].replace('}','').split(',')
            workflows[key] = rules
        else:
            part_ratings.append(row.replace('{', '').replace('}','').split(','))
    return (workflows, part_ratings)

def find_part_val(key, parts):
    for part in parts:
        part_key = part.split('=')[0]
        part_val = int(part.split('=')[1])
        if key == part_key:
            return part_val
    
    return 0
   
def eval_expr(expr, parts):
    l_side = expr[0]
    op = expr[1]
    r_side = int(expr[2:])
    part_val = find_part_val(l_side, parts)
    match op:
        case '<':
            if part_val < r_side:
                return True
            else:
                return False
        case '>':
            if part_val > r_side:
                return True
            else:
                return False
        case '=':
            if part_val == r_side:
                return True
            else:
                return False
            
    return False

def process_rule(rule, parts):
    if ':' not in rule:
        return rule.strip()
    else:
        expr = rule.split(':')[0]
        if_true = rule.split(':')[1]
        if eval_expr(expr, parts):
            return if_true
    
    return None

def process_parts(parts, workflows) -> (bool, int):
    is_accepted = False
    total = 0
    for part in parts:
        total += int(part.split('=')[1])

    accepted_or_rejected = False
    cur_step = 'in'
    while not accepted_or_rejected:
        rules = workflows[cur_step]        
        for rule in rules:
            result = process_rule(rule, parts)
            if result == None:
                continue
            elif result.strip() == 'A':
                is_accepted = True
                accepted_or_rejected = True
                break
            elif result.strip() == 'R':
                accepted_or_rejected = True
                break
            else:
                cur_step = result
                break

    return (is_accepted, total)

def part1(input):
    """Implementation for part 1"""
    workflows, part_ratings = get_workflow_info(input)
    part_totals = 0
    for parts in part_ratings:
        is_accepted,part_total = process_parts(parts, workflows)
        if is_accepted:
            part_totals += part_total

    return part_totals  
    
def process_workflow(workflows, key, x_range, m_range, a_range, s_range):
    ans = 0
    queue = [(key, x_range, m_range, a_range, s_range)]
    while queue:
        key, xr, mr, ar, sr = queue.pop()
        if key == 'A':
            r1 = len(range(xr[0], xr[1] + 1))
            r2 = len(range(mr[0], mr[1] + 1))
            r3 = len(range(ar[0], ar[1] + 1))
            r4 = len(range(sr[0], sr[1] + 1))
            ans += r1 * r2 * r3 * r4
            continue
        elif key == 'R':
            continue
        for flow in workflows[key]:
            if ':' not in flow:
                queue.append((flow, xr, mr, ar, sr))
            else:
                left_side = flow.split(':')[0][0]
                op =flow.split(':')[0][1]
                right_side = int(flow.split(':')[0][2:].strip())
                next_key = flow.split(':')[1]   

                low_xmas_rg = xr[0]
                high_xmas_rg = xr[1]
                if left_side == 'm':
                    low_xmas_rg = mr[0]
                    high_xmas_rg = mr[1]
                elif left_side == 'a':
                    low_xmas_rg = ar[0]
                    high_xmas_rg = ar[1]
                elif left_side == 's':
                    low_xmas_rg = sr[0]
                    high_xmas_rg = sr[1]

                # All to carry through to the next flow at this level, nothing to go down to the next level of the tree
                if (op == '>' and right_side >= high_xmas_rg) or (op == '<' and right_side <= low_xmas_rg):
                    continue

                # All to the next level of the tree for the next workflow key, nothing to continue to handle on this level
                if (op == '>' and right_side < low_xmas_rg) or (op == '<' and right_side > high_xmas_rg):
                    queue.append((next_key, xr, mr, ar, sr))
                    break

                # Some for the next level and some for the current level to "remember"
                if op == '>':
                    transfer = (right_side+1, high_xmas_rg)
                    passthrough = (low_xmas_rg, right_side)
                else:
                    transfer = (low_xmas_rg, right_side-1)
                    passthrough = (right_side, high_xmas_rg)

                # carry this around to the next item            
                if left_side == 'x':                    
                    xr = passthrough
                elif left_side == 'm':
                    mr = passthrough
                elif left_side == 'a':
                    ar = passthrough
                else:
                    sr = passthrough
                xr2 = tuple(list(xr).copy())
                mr2 = tuple(list(mr).copy())
                ar2 = tuple(list(ar).copy())
                sr2 = tuple(list(sr).copy())
                if left_side == 'x':                    
                    xr2 = transfer
                elif left_side == 'm':
                    mr2 = transfer
                elif left_side == 'a':
                    ar2 = transfer
                else:
                    sr2 = transfer
                queue.append((next_key, xr2, mr2, ar2, sr2))

    return ans
    
def part2(input):
    """Implementation for part 2"""
    workflows, _ = get_workflow_info(input)
    ans = process_workflow(workflows, 'in', (1,4000), (1,4000), (1,4000), (1,4000))

    return ans

def get_from_file():
    with open(os.getcwd() + '/solutions/day19/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    puzzle_input = get_from_file()
    input = parse(puzzle_input)
    part1ans = part1(input)
    part2ans = part2(input)
    print(part1ans)
    print(part2ans)
