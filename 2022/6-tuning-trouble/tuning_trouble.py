INPUT_FILE_NAME = "input"


START_OF_PACKET_SECTION = 0
START_OF_MESSAGE_SECTION = 1

SECTION_LENGTHS = [4, 14]

def parse_input():
  with open(INPUT_FILE_NAME, 'r') as input_file:
    return input_file.readlines()[0]

def is_distinct_chars(chars):
  return len(set(chars)) == len(chars)

def is_distinct_of_length(chars, start_index, length):
  return is_distinct_chars(chars[start_index:start_index+length])

def find_in_message(chars, section):
  length = SECTION_LENGTHS[section]
  index = 0
  while index < len(chars)-length:
    if is_distinct_of_length(chars, index, length):
      return index+length
    index += 1

def main():
  chars = parse_input()

  print(find_in_message(chars, START_OF_PACKET_SECTION))
  print(find_in_message(chars, START_OF_MESSAGE_SECTION))


if __name__ == "__main__":
  main()