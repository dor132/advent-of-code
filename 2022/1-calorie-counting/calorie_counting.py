INPUT_FILE_NAME = "input"

def parse_input():
  with open(INPUT_FILE_NAME, 'r') as input_file:
    elves_strings = "".join(input_file.readlines()).split('\n\n') # split to elves as string chunks
    elves_strings_splitted = map(lambda x: x.split('\n'), elves_strings) # split chunks into list of strings
    return list(map(lambda calories_list: map(int, calories_list), elves_strings_splitted)) # convert each string to int

def main():
  elves_calories = parse_input()
  elves_summed_cals = list(map(sum, elves_calories))

  top_three_elves = 0
  for _ in range(3):
    curr_max = max(elves_summed_cals)
    elves_summed_cals.remove(curr_max)

    top_three_elves += curr_max

  print(top_three_elves)

if __name__ == "__main__":
  main()
