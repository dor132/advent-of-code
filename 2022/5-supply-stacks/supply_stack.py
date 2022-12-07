from typing import List
INPUT_FILE_NAME = "input"

CRATE_MOVER = 9001

def parse_stack(stacks_input, stack_index):
  # This is limited to only read crates marked by a single letter.
  # For our purposes, it's sufficient.
  # Filter is done since for each stack that is loaded with less crates than
  # the maximal one, spaces will be added instead of letters of actual crates.
  # We need to eliminate such 'empty' crates.
  return list(filter(lambda crate: crate.strip() != '', map(lambda line: line[stack_index], stacks_input)))

def parse_stacks(stacks_input: List[str]):
  stacks_input = list(reversed(stacks_input))
  stacks_base_lines, stacks_input = stacks_input[0], stacks_input[1:]

  stacks = []
  stack_num = 1
  try:
    while True:
      stack_index = stacks_base_lines.index(str(stack_num))
      stacks.append(parse_stack(stacks_input, stack_index))

      stack_num += 1

  except ValueError:
    return stacks

def parse_moves(moves_input):
  # parses a single line of the form 'move X from Y to Z'
  def parse_move(move_input: str):
    move_input = move_input.lstrip('move ')
    move_input = move_input.replace(' from ', ',')
    move_input = move_input.replace(' to ', ',')
    return list(map(int, move_input.split(',')))

  return list(map(parse_move, moves_input))

def parse_input():
  with open(INPUT_FILE_NAME, 'r') as input_file:
    lines = list(map(lambda line: line.rstrip('\n'), input_file.readlines()))

  # completely empty line is the separator because of rstrip above
  input_separate_line = lines.index('')
  return parse_stacks(lines[:input_separate_line]), parse_moves(lines[input_separate_line+1:])

def move_crates(stacks: List[List[str]], moves: List[List[int]]):
  def perform_move(move):
    count, frm, to = move
    # from and to in the input are 1-based index, transform to 0-based index
    frm -= 1
    to -= 1
    if CRATE_MOVER == 9000:
      stacks[to] += reversed(stacks[frm][-count:])
    else:
      # CrateMover 9001, do not reverse crates order
      stacks[to] += stacks[frm][-count:]
    stacks[frm] = stacks[frm][:-count]
  
  list(map(perform_move, moves))

def main():
  stacks, moves = parse_input()
  move_crates(stacks, moves)
  print("".join(list(map(lambda stack: stack.pop(), stacks))))

if __name__ == "__main__":
  main()