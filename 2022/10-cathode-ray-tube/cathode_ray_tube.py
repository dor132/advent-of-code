from typing import List

INPUT_FILE_NAME = "input"

class CPU:
  cycle: int = 0
  x_reg: int = 1
  busy_count: int = 0
  current_signal_strength: int = 0
  monitor_signal_strengths: List[int] = []
  cycles_to_monitor = [cycle for cycle in range(20, 250, 40)]

  screen: List[List[str]] = [['.' for _ in range(40)] for _ in range(6)]

  def do_cycle(self) -> None:
    self.cycle += 1
    
    if self.busy_count > 0:
      self.busy_count -= 1

    self.__monitor_cpu()
    self.__draw_pixel()

  def display_screen(self) -> None:
    for line in self.screen:
      [print(pixel, end="") for pixel in line]
      print()

  def set_busy_for(self, num_cycles: int) -> None:
    self.busy_count = num_cycles

  def is_busy(self) -> bool:
    return self.busy_count != 0
  
  def __monitor_cpu(self) -> None:
    self.current_signal_strength = self.cycle * self.x_reg
    if self.cycle in self.cycles_to_monitor:
      self.monitor_signal_strengths.append(self.current_signal_strength)
  
  def __draw_pixel(self) -> None:
    pixel_index = self.cycle % 240 - 1
    row, col = pixel_index // 40, pixel_index % 40
    char = '#' if abs(self.x_reg-col) <= 1 else '.'
    self.screen[row][col] = char

def do_addx(cpu: CPU, amount: int) -> None:
  cpu.x_reg += amount

def parse_input() -> List[str]:
  with open(INPUT_FILE_NAME) as input_file:
    return input_file.readlines()

def main() -> None:
  cpu: CPU = CPU()
  commands = parse_input()

  # This design is not open to extension easily,
  # but for the purposes of this puzzle it is good enough.
  # If a more robust and scalable solution was needed here,
  # then a use of dictionary with instructions names as keys and
  # instruction properties as values would be a more appealing
  # solution.
  for command in commands:
    if command.startswith("addx"):
      cpu.set_busy_for(2)
    elif command.startswith("noop"):
      cpu.set_busy_for(1)
    
    while cpu.is_busy(): cpu.do_cycle()

    if command.startswith("addx"):
      do_addx(cpu, int(command.split(' ')[1]))

  print(sum(cpu.monitor_signal_strengths))
  cpu.display_screen()


if __name__ == "__main__":
  main()