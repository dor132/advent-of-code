from typing import Dict, List, Set, Tuple

INPUT_FILE_NAME = "input"
# Part 1 - Length 2
# Part 2 - Length 10
ROPE_LENGTH = 10

class Move:
  direction: str
  count: int

  def __init__(self, direction: str, count: int) -> None:
    if len(direction) > 1:
      raise ValueError("Direction should be one character.")
    self.direction = direction
    self.count = count

class Location:
  MOVES_X: Dict[str, int] = {
    'L': -1,
    'R': 1
  }
  MOVES_Y: Dict[str, int] = {
    'U': 1,
    'D': -1
  }
  x: int
  y: int

  def __init__(self, x: int, y: int) -> None:
    self.x = x
    self.y = y
  
  def move(self, direction: str) -> None:
    self.x += self.MOVES_X.get(direction, 0)
    self.y += self.MOVES_Y.get(direction, 0)

def parse_input() -> List[Move]:
  def parse_move(direction: str, count: str) -> Move:
    return Move(direction=direction, count=int(count))

  with open(INPUT_FILE_NAME) as input_file:
    return [parse_move(*line.split(' ')) for line in input_file.readlines()]

def calculate_distance(loc1: Location, loc2: Location) -> int:
  return abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y)

def is_diagonal(knot1: Location, knot2: Location) -> bool:
  return knot1.x != knot2.x and knot1.y != knot2.y

def should_knot_move(knot1: Location, knot2: Location) -> bool:
  distance = calculate_distance(loc1=knot1, loc2=knot2)

  if is_diagonal(knot1=knot1, knot2=knot2):
    return distance > 2
  return distance >= 2

def calculate_knot_moves(knot1: Location, knot2: Location) -> List[Move]:
  moves: List[Move] = []

  if is_diagonal(knot1=knot1, knot2=knot2):
    # need to do two moves
    move_x = Move('R', 1) if knot1.x > knot2.x else Move('L', 1)
    move_y = Move('U', 1) if knot1.y > knot2.y else Move('D', 1)
    moves = [move_x, move_y]
  else:
    # need to do only one move
    if knot1.x > knot2.x: moves = [Move('R', 1)]
    elif knot1.x < knot2.x: moves = [Move('L', 1)]
    elif knot1.y > knot2.y: moves = [Move('U', 1)]
    else: moves = [Move('D', 1)]
  return moves

def do_knot_moves(knot: Location, moves: List[Move]) -> None:
  for move in moves:
    knot.move(move.direction)

def main() -> None:
  rope = [Location(0, 0) for _ in range(ROPE_LENGTH)]
  moves = parse_input()
  last_knot_visits: Set[Tuple[int, int]] = set()
  last_knot_visits.add((rope[-1].x, rope[-1].y))

  for move in moves:
    while move.count > 0:
      rope[0].move(direction=move.direction) # move knot1
      move.count -= 1
      
      for knot_idx in range(1, len(rope)):
        prev_knot = rope[knot_idx-1]
        current_knot = rope[knot_idx]
        if not should_knot_move(knot1=prev_knot, knot2=current_knot):
          # If we reached a knot that does not move, all following knots will not move as well.
          break
        do_knot_moves(knot=current_knot, moves=calculate_knot_moves(knot1=prev_knot, knot2=current_knot))
      last_knot_visits.add((rope[-1].x, rope[-1].y))
  
  print(len(last_knot_visits))

if __name__ == "__main__":
  main()
