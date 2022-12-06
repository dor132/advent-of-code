INPUT_FILE_NAME = 'input'

BASE_SCORES = {
  'A': 1, # ROCK
  'B': 2, # PAPER
  'C': 3  # SCISSORS
}
LOSES = {
  'A': 'C',
  'B': 'A',
  'C': 'B'
}
DRAWS = {
  'A': 'A',
  'B': 'B',
  'C': 'C'
}
WINS = {
  'A': 'B',
  'B': 'C',
  'C': 'A'
}
MOVES = {
  'X': LOSES,
  'Y': DRAWS,
  'Z': WINS
}
MATCH_SCORE = {
  'X': 0,
  'Y': 3,
  'Z': 6  
}

def parse_match(match_line):
  return match_line.rstrip().split(' ')

def parse_input():
  with open(INPUT_FILE_NAME, 'r') as input_file:
    matches = list(map(parse_match, input_file.readlines()))
  return matches

def did_win(p1, p2):
  if WINS[p2] == p1:
    return 6 # win
  if DRAWS[p2] == p1:
    return 3 # draw
  return 0

def get_match_score_part_1(match):
  p1, p2 = match
  return BASE_SCORES[p2] + did_win(p1, p2)

def get_match_score_part_2(match):
  p1, p2 = match
  move = MOVES[p2][p1]
  return BASE_SCORES[move] + MATCH_SCORE[p2]

def main():
  print(sum(map(get_match_score_part_2, parse_input())))

if __name__ == "__main__":
  main()
