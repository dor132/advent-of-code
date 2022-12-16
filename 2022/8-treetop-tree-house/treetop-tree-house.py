INPUT_FILE_NAME = "input"

def parse_input():
  lines = None
  with open(INPUT_FILE_NAME, 'r') as input_file:
    lines = map(lambda line: list(line.strip()), input_file.readlines())
    lines = map(lambda line: [int(tree_height) for tree_height in line], lines)
  
  return list(lines)

def calc_visibles(tree_heights):
  max = tree_heights[0]
  visibles_indexes = [0] # first is always visible
  for index, tree_height in enumerate(tree_heights[1:], 1):
    if tree_height > max:
      max = tree_height
      visibles_indexes.append(index)

  return visibles_indexes

def calc_view_distance(tree_heights):
  view_distance = 0
  for tree in tree_heights[1:]:
    if tree >= tree_heights[0]:
      view_distance += 1
      break
    view_distance += 1

  return view_distance
    

def main():
  tree_heights = parse_input()
  visible_trees = set()
  for idx in range(len(tree_heights)):
    row = tree_heights[idx]
    col = [r[idx] for r in tree_heights]
    row_indexes = {(idx, visible_index) for visible_index in calc_visibles(row)}
    reversed_row_indexes = {(idx, len(row)-1-visible_index) for visible_index in calc_visibles(list(reversed(row)))}

    col_indexes = {(visible_index, idx) for visible_index in calc_visibles(col)}
    reversed_col_indexes = {(len(col)-1-visible_index, idx) for visible_index in calc_visibles(list(reversed(col)))}

    visible_trees |= row_indexes | col_indexes | reversed_row_indexes | reversed_col_indexes

  scenic_views = []
  for row in range(len(tree_heights)):
    for col in range(len(tree_heights[row])):
      left = calc_view_distance(tree_heights=list(reversed(tree_heights[row][:col+1])))
      right = calc_view_distance(tree_heights=tree_heights[row][col:])

      tree_col = [r[col] for r in tree_heights]
      top = calc_view_distance(tree_heights=list(reversed(tree_col[:row+1])))
      down = calc_view_distance(tree_heights=tree_col[row:])

      scenic_views.append(left*right*top*down)
  
  print(max(scenic_views))

  

if __name__ == "__main__":
  main()
