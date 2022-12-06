import heapq

INPUT_FILE_NAME = "input"

def parse_input():
  def trio_chunk(bags):
    for i in range(0, len(bags), 3):
      yield bags[i:i+3]

  trios = []
  with open(INPUT_FILE_NAME, 'r') as input_file:
    for trio in trio_chunk(input_file.readlines()):
      trios.append(list(map(str.rstrip, trio)))
  
  return trios

def find_shared_compartments_item(bags):
  # remove duplicates, sort sets and transform to list
  bags = list(map(sorted, map(set, bags)))

  # After each bag duplicated items were eliminated,
  # we can merge the lists into a single sorted list.
  # This allows us to simply look for the item that shows up
  # #bags times consequitively in the list.
  consequitive_length = len(bags)
  merged_comps = list(heapq.merge(*bags))
  for idx in range(len(merged_comps[:-1])):
    if len(set(merged_comps[idx:idx+consequitive_length])) == 1:
      return merged_comps[idx]

def get_item_priority(item: str):
  if item.islower():
    return ord(item) - ord('a') + 1

  return ord(item) - ord('A') + 27

def main():
  trios_bags = parse_input()
  print(sum(map(get_item_priority, map(find_shared_compartments_item, trios_bags))))
  

if __name__ == "__main__":
  main()
