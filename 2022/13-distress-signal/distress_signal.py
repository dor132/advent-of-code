from enum import Enum
from operator import is_


INPUT_FILE_NAME = "input"

item = int | list[int]
packet = list[item]
packets_pair = tuple[packet, packet]

class IS_IN_ORDER(Enum):
  NO=0,
  MAYBE=1,
  YES=2

def parse_input() -> list[packets_pair]:
  def parse_packets_pair(pair: str) -> packets_pair:
    return [eval(p) for p in pair.split('\n')] # type: ignore    

  with open(INPUT_FILE_NAME, 'r') as input_file:
    packets_pairs = input_file.read().split('\n\n')
    return [parse_packets_pair(pair) for pair in packets_pairs]

def are_parts_ordered(zipped_items: tuple[item, item]) -> IS_IN_ORDER:
  left, right = zipped_items
  if type(left) == int and type(right) == int:
    if int(left) < int(right): return IS_IN_ORDER.YES # type: ignore
    elif int(left) > int(right): return IS_IN_ORDER.NO # type: ignore
    return IS_IN_ORDER.MAYBE
  elif type(left) == list and type(right) == int:
    return indecisive_is_pair_order((left, [right])) # type: ignore
  elif type(left) == int and type(right) == list:
    return indecisive_is_pair_order(([left], right)) # type: ignore
  
  # both lists
  return indecisive_is_pair_order(zipped_items) # type: ignore

def indecisive_is_pair_order(pair: packets_pair) -> IS_IN_ORDER:
  left, right = pair
  for zipped_items in zip(left, right):
    is_ordered = are_parts_ordered(zipped_items)
    if is_ordered != IS_IN_ORDER.MAYBE:
      return is_ordered
    # else continue, do nothing
  
  if len(left) == len(right):
    return IS_IN_ORDER.MAYBE

  return IS_IN_ORDER.YES if len(left) < len(right) else IS_IN_ORDER.NO

def is_pair_ordered(pair: packets_pair) -> bool:
  left, right = pair
  for zipped_items in zip(left, right):
    is_ordered = are_parts_ordered(zipped_items)
    if is_ordered == IS_IN_ORDER.NO:
      return False
    elif is_ordered == IS_IN_ORDER.YES:
      return True
    # else continue, do nothing

  return len(left) <= len(right)

def is_in_order(packets: list[packet]) -> bool:
  for idx in range(len(packets)-1):
    if not is_pair_ordered((packets[idx], packets[idx+1])):
      return False

  return True

def index_out_of_order(packets: list[packet]) -> int:
  for idx in range(len(packets)-1):
    if not is_pair_ordered((packets[idx], packets[idx+1])):
      return idx+1

  return -1

def move_to_place(packets: list[packet], idx: int) -> list[packet]:
  while not is_in_order(packets[:idx+1]):
    packets[idx-1], packets[idx] = packets[idx], packets[idx-1]
    idx -= 1
  
  return packets

def is_locator_packet(packet: packet) -> bool:
  return len(packet) == 1 and packet[0] in [[2], [6]]

def main() -> None:
  pairs = parse_input()

  # Part 1 (we slice the last pair because it's only relevant for part 2)
  print(sum([idx+1 for idx, pair in enumerate(pairs[:-1]) if is_pair_ordered(pair)]))

  # Part 2
  packets = [packet for pair in pairs for packet in pair]
  last_index = 0 # used as a small optimization, to avoid re-ordering already ordered sections
  while not is_in_order(packets[last_index:]):
    out_of_order_idx = index_out_of_order(packets[last_index:]) + last_index
    last_index = out_of_order_idx
    
    packets = move_to_place(packets, out_of_order_idx)
  
  locator_indexes = [i+1 for i, packet in enumerate(packets) if is_locator_packet(packet)]
  print(locator_indexes[0] * locator_indexes[1])

if __name__ == "__main__":
  main()