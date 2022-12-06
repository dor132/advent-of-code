from typing import List, Tuple, Text

INPUT_FILE_NAME = "input"

def parse_elf(pair: Text) -> Tuple[int]:
  return tuple(map(lambda section: int(section), pair.split('-')))

def parse_elves_pair(line: Text) -> Tuple[int]:
  pairs = line.split(',')
  elf1 = parse_elf(pairs[0])
  elf2 = parse_elf(pairs[1])

  return (elf1, elf2)

def parse_input() -> List[Tuple[int]]:
  elves_pairs = []
  with open(INPUT_FILE_NAME, 'r') as input_file:
    elves_pairs = list(map(parse_elves_pair, input_file.readlines()))
  return elves_pairs

def is_fully_contained(elves_pair):
  (x, y), (w, z) = elves_pair
  return (x <= w and y >= z) or (w <= x and z >= y)

def is_intersecting(elves_pair):
  (x, y), (w, z) = elves_pair
  return (x < w and y >= w) or (w < x and z >= x)

def is_ovelapping(elves_pair):
  return is_intersecting(elves_pair=elves_pair) or is_fully_contained(elves_pair=elves_pair)

def main():
  pairs = parse_input()
  print(sum(map(is_ovelapping, pairs)))

if __name__ == "__main__":
  main()