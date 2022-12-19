from dataclasses import dataclass
from functools import reduce
from typing import Dict, List
from math import lcm

INPUT_FILE_NAME = "input"
PART = 2
NUM_ROUNDS = 10000

@dataclass
class Monkey:
  items: List[int]
  operation: str
  divis_by_test: int
  action: Dict[bool, int]
  __inspections_counter: int = 0

  # Returns a dict where key is item and value
  # is monkey to pass that item to.
  def do_turn(self) -> Dict[int, List[int]]:
    pass_map: Dict[int, List[int]] = {}
    for item in self.items:
      item_worry_level: int = self.inspect(item)
      if item_worry_level in pass_map.keys():
        pass_map[item_worry_level].append(self.action[bool(item_worry_level % self.divis_by_test == 0)])
      else:
        pass_map[item_worry_level] = [self.action[bool(item_worry_level % self.divis_by_test == 0)]]
    
    self.items.clear()
    return pass_map
  
  def inspect(self, worry_level: int) -> int:
    self.__inspections_counter += 1
    return eval(self.operation.replace('old', str(worry_level)))
  
  def num_inspections(self) -> int:
    return self.__inspections_counter

def parse_input() -> List[Monkey]:
  with open(INPUT_FILE_NAME, "r") as input_file:
    def parse_monkey(lines: str) -> Monkey:
      parsed_lines = [line.strip() for line in lines.split('\n')]
      items = [int(item) for item in parsed_lines[1].lstrip("Starting items: ").split(", ")]
      operation = parsed_lines[2].split(' = ')[1]
      divis_by_test = int(parsed_lines[3].lstrip('Test: divisible by '))
      action = {
        True: int(parsed_lines[4].lstrip('If true: throw to monkey ')),
        False: int(parsed_lines[5].lstrip('If false: throw to monkey '))
      }

      return Monkey(items=items,
                    operation=operation,
                    divis_by_test=divis_by_test,
                    action=action)

    return [parse_monkey(monkey_desc) for monkey_desc in input_file.read().split('\n\n')]

def pass_item(item: int, tos: List[Monkey]) -> None:
  [to.items.append(item) for to in tos]

def reduce_worry_levels(monkeys: List[Monkey], d: int) -> None:
  for m in monkeys:
    m.items = list(map(lambda item: item % d, m.items))

def main() -> None:
  monkeys = parse_input()

  # Setting each item to modulo the LCM of all divisors 
  # works because it does not change the original item's worry
  # level modulo the monkey's modulo test.
  # Not doing this will lead to VERY large numbers slowing
  # the program at round ~45 to about 1 second per round.
  items_lcm = lcm(*[m.divis_by_test for m in monkeys])
  
  for round in range(NUM_ROUNDS):
    print(f"Round {round}\r", end="")
    for monkey in monkeys:
      pass_map = monkey.do_turn()
      for item, tos in pass_map.items():
        pass_item(item, [monkeys[to] for to in tos])
    if PART == 2:
      reduce_worry_levels(monkeys, items_lcm)

  print(reduce(lambda a, b: a*b.num_inspections(), sorted(monkeys, key=lambda m: m.num_inspections(), reverse=True)[:2], 1))

if __name__ == "__main__":
  main()