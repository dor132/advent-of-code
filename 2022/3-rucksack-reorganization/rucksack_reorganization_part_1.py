import heapq

INPUT_FILE_NAME = "input"

def parse_input():
  def halve_bag(bag_content):
    bag_content = bag_content.rstrip()
    half_bag_size = len(bag_content) // 2
    return (bag_content[:half_bag_size], bag_content[half_bag_size:])

  with open(INPUT_FILE_NAME, 'r') as input_file:
    return list(map(halve_bag, input_file.readlines()))

def find_shared_compartments_item(bag):
  # remove duplicates, sort sets and transform to list
  comp_1, comp_2 = list(map(sorted, map(set, bag)))

  # After each compartment duplicated items were eliminated,
  # we can merge the two lists into a single sorted list.
  # This allows us to simply look for the item that shows up
  # twice consequitively in the list.
  merged_comps = list(heapq.merge(comp_1, comp_2))
  for idx in range(len(merged_comps[:-1])):
    if merged_comps[idx] == merged_comps[idx+1]:
      return merged_comps[idx]

def get_item_priority(item: str):
  if item.islower():
    return ord(item) - ord('a') + 1

  return ord(item) - ord('A') + 27

def main():
  bags = parse_input()
  print(sum(map(get_item_priority, map(find_shared_compartments_item, bags))))
  

if __name__ == "__main__":
  main()
