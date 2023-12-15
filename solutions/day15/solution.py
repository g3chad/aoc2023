import os  
class BoxLine():
    class Box():
        def __init__(self, box_num: int) -> None:
            self.lens_map = {}
            self.box_num = box_num

        def remove_lens(self, label: str) -> None:
            if label in self.lens_map and self.lens_map[label]:
                del self.lens_map[label]

        def put_lens(self, label: str, focal_len: int) -> None:
            self.lens_map[label] = (label, focal_len)
            
        def calculate_focusing_power(self) -> int:
            lens_num = 0
            result = 0            
            for _,v in self.lens_map.items():
                focal_len = v[1]
                result += self.box_num * (lens_num + 1) * focal_len
                lens_num += 1

            return result
        
        @staticmethod
        def hash(seq, div: int=256):
            result = 0
            for c in seq:
                if not c.strip(): continue
                result +=ord(c)
                result *= 17
                result = result % div

            return result

    def __init__(self, num_boxes:int=256) -> None:
        self.boxes = []
        self.boxline_len = num_boxes
        for i in range(num_boxes):
            self.boxes.append(self.Box(i+1))
    
    def perform_op(self, seq: str) -> None:
        label_parts = seq.split('-') if '-' in seq else seq.split('=')
        label_parts = [label for label in label_parts if label.strip()]
        label = label_parts[0]
        box_num = self.Box.hash(label_parts[0])
        if len(label_parts) == 1: # we had a minus
            self.boxes[box_num].remove_lens(label)
        else: # we had an = so add / update lens
            focal_stren = int(label_parts[1].strip())
            self.boxes[box_num].put_lens(label, focal_stren)

    def calculate_focusing_power(self):
        total = 0
        for box in self.boxes:
            total += box.calculate_focusing_power()
        return total

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split(sep='\n')]
    
def part1(input):
    """Implementation for part 1"""
    result = 0
    sequences = input[0].split(',')
    for seq in sequences:
        result += BoxLine.Box.hash(seq.strip())

    return result 
    
def part2(input):
    """Implementation for part 2"""
    box_line = BoxLine()
    sequences = input[0].split(',')
    for seq in sequences:
        box_line.perform_op(seq)

    return box_line.calculate_focusing_power()

def get_from_file():
    with open(os.getcwd() + '/solutions/day15/bf.txt') as f:
        return "".join(f.readlines())

if __name__ == "__main__":
    input = parse(get_from_file())
    print(part1(input))
    print(part2(input))
