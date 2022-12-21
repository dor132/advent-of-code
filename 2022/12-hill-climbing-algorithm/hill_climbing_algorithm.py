from itertools import product
from queue import PriorityQueue

INPUT_FILE_NAME = "input"

START = "S"
END = "E"

def parse_input() -> list[str]:
  with open(INPUT_FILE_NAME, 'r') as input_file:
    return [line.strip() for line in input_file.readlines()]

def find_start(heights_map: list[str]) -> tuple[int, int]:
  for row, heights in enumerate(heights_map):
    try:
      return (row, heights.index(START))
    except:
      continue

  raise RuntimeError(f"Bad input, start ('{START}') not found.")

def find_starts(heights_map: list[str]) -> list[tuple[int, int]]:
  starts: list[tuple[int, int]] = []
  rows, cols = len(heights_map), len(heights_map[0])
  for row, col in product(range(rows), range(cols)):
    if heights_map[row][col] == 'a':
      starts.append((row, col))

  return starts

def find_end(heights_map: list[str]) -> tuple[int, int]:
  for row, heights in enumerate(heights_map):
    try:
      return (row, heights.index(END))
    except:
      continue

  raise RuntimeError(f"Bad input, start ('{END}') not found.")

def h(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
  x1, y1 = cell1
  x2, y2 = cell2
  return abs(x1-x2) + abs(y1-y2)

def get_neighbors(heights_map: list[str], cell: tuple[int, int]) -> list[tuple[int, int]]:
  x, y = cell
  neighbors = [(nx, ny) for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] 
                if 0 <= nx < len(heights_map) and 0 <= ny < len(heights_map[0])]
  return neighbors

def is_valid_move(heights_map: list[str], frm: tuple[int, int], to: tuple[int, int]) -> bool:
  frm_x, frm_y = frm
  to_x, to_y = to

  frm_ord = ord(heights_map[frm_x][frm_y])
  to_ord = ord(heights_map[to_x][to_y])
  return to_ord - frm_ord <= 1

def reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]) -> list[tuple[int, int]]:
  path = [current]
  while current in came_from.keys():
    current = came_from[current]
    path.append(current) # we return reversed list instead of inserting at 0 for efficiency

  return list(reversed(path))

def a_star(heights_map: list[str], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
  rows, cols = len(heights_map), len(heights_map[0])
  g_score = {(x, y):float('inf') for x, y in product(range(rows), range(cols))}
  f_score = {(x, y):float('inf') for x, y in product(range(rows), range(cols))}

  g_score[start] = 0
  f_score[start] = h(start, end)
  open_moves: PriorityQueue[tuple[float, tuple[int, int]]] = PriorityQueue()
  open_moves.put((f_score[start], start))

  came_from: dict[tuple[int, int], tuple[int, int]] = {}

  while not open_moves.empty():
    # pop min from open_moves, if its goal then finish
    _, current = open_moves.get()
    if current == end:
      return reconstruct_path(came_from=came_from, current=current)

    # check neighbors, and update each neighbor if new_g_score < g_score
    for neighbor in get_neighbors(heights_map, current):
      if not is_valid_move(heights_map, current, neighbor):
        continue
      tentative_g = g_score[current]+1
      if tentative_g >= g_score[neighbor]:
        continue
      came_from[neighbor] = current # for path reconstruction
      g_score[neighbor] = tentative_g
      f_score[neighbor] = tentative_g+h(neighbor, end)
      if neighbor not in [om[1] for om in open_moves.queue]:
        open_moves.put((f_score[neighbor], neighbor))

  return []

def main() -> None:
  heights_map = parse_input()
  start = find_start(heights_map)
  end = find_end(heights_map)

  heights_map[start[0]] = heights_map[start[0]].replace(START, 'a')
  heights_map[end[0]] = heights_map[end[0]].replace(END, 'z')
  
  # Part 1
  path = a_star(heights_map, start, end)
  print(len(path)-1) # -1 since start is not considered a step

  # Part 2
  starts = find_starts(heights_map)
  paths = [a_star(heights_map, s, end) for s in starts]
  paths = [p for p in paths if len(p) > 0] # filter for non existing paths
  paths = sorted(paths, key=lambda p: len(p))
  print(len(paths[0])-1)

if __name__ == "__main__":
  main()