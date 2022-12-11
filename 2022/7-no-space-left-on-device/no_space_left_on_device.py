from enum import Enum
from typing import List
import operator

INPUT_FILE_NAME = "input"

class FilterBy(Enum):
  GREATER_OR_EQUAL = 0
  LESS_OR_EQUAL = 1

class TreeNode:
  name: str = None # Name of directory
  parent = None
  children = [] # List of TreeNode, denoting child directories
  files = {} # Dict where key is file name, value is file size
  size = 0

  def __init__(self, name: str, parent) -> None:
    self.name = name
    self.parent = parent
    self.children = {}
    self.files = {}
    self.size = 0

root_dir: TreeNode = TreeNode(name="/", parent=None)
current_dir: TreeNode = root_dir

COMMAND_START = "$"
MAX_DIR_SIZE = 100000
TOTAL_DISK_SIZE = 70000000
UPDATE_REQUIRED_DISK_SIZE = 30000000

def parse_input():
  with open(INPUT_FILE_NAME, 'r') as input_file:
    return list(map(str.strip, input_file.readlines()))

def is_command(line: str):
  return line.strip().startswith(COMMAND_START)

def do_command_cd(lines, line_index):
  global current_dir, root_dir
  cd_cmd = lines[line_index]
  to_dir = cd_cmd.split(' ')[2]
  if to_dir == "..":
    current_dir = current_dir.parent
  elif to_dir == "/":
    current_dir = root_dir
  else: current_dir = current_dir.children[to_dir]
  
  return 1

def do_command_ls(lines: List[str], line_index):
  starting_line = line_index
  line_index += 1
  current_line = lines[line_index]
  while not is_command(current_line):
    if current_line.startswith("dir"): do_dir(current_line)
    else: do_file(current_line)
    
    line_index += 1
    if line_index >= len(lines): break
    current_line = lines[line_index]
  
  return line_index - starting_line

command_handlers = {
  "cd": do_command_cd,
  "ls": do_command_ls
}

def extract_command(cmd: str):
  for command in command_handlers.keys():
    if command in cmd:
      return command

def do_command(lines: List[str], line_index: int) -> int:
  cmd = lines[line_index]
  return command_handlers[extract_command(cmd)](lines, line_index)

def do_dir(line: str):
  global current_dir
  dir_name = line.split(' ')[1]
  current_dir.children[dir_name] = TreeNode(name=dir_name, parent=current_dir)

def do_file(line: str):
  global current_dir
  file_size, file_name = line.split(' ')
  current_dir.files[file_name] = int(file_size)

def generate_dir_sizes(current_dir: TreeNode):
  size = sum(current_dir.files.values()) + sum(list(map(generate_dir_sizes, current_dir.children.values())))
  current_dir.size = size
  return size # return size only for recursion to work

def filter_by_size(current_dir: TreeNode, size: int, current_sizes: List[TreeNode], fil: FilterBy):
  should_include = False
  if fil == FilterBy.GREATER_OR_EQUAL:
    should_include = current_dir.size >= size
  else:
    should_include = current_dir.size <= size

  # append current directory if fits filter
  if should_include:
    current_sizes.append(current_dir)

  # walk child directories
  for child in current_dir.children.values():
    filter_by_size(current_dir=child, size=size, current_sizes=current_sizes, fil=fil)
  
  return current_sizes

def build_dir_tree(lines):
  line_index = 0
  while line_index < len(lines):
    line = lines[line_index]
    processed_lines = 0
    if is_command(line=line): 
      processed_lines = do_command(lines, line_index)
    line_index += processed_lines

def main():
  lines = parse_input()
  build_dir_tree(lines) 
  generate_dir_sizes(root_dir)
  
  # Part 1
  filtered_dirs = filter_by_size(current_dir=root_dir, size=MAX_DIR_SIZE, current_sizes=[], fil=FilterBy.LESS_OR_EQUAL)
  print(sum(map(lambda dir: dir.size, filtered_dirs)))

  # Part 2
  empty_space = TOTAL_DISK_SIZE - root_dir.size
  required_space = UPDATE_REQUIRED_DISK_SIZE - empty_space
  filtered_dirs = filter_by_size(current_dir=root_dir, size=required_space, current_sizes=[], fil=FilterBy.GREATER_OR_EQUAL)
  filtered_dirs.sort(key=operator.attrgetter('size'))
  print(filtered_dirs[0].size)
  
if __name__ == "__main__":
  main()
