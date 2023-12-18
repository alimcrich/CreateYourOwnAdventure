import random

# Constants
DIRECTIONS = ["west", "east", "north", "south", "go back"]
WEAPONS = ["axe", "sword", "nunchucks", "wooden stick"]
YES_NO = ["yes", "no"]

# Global Variables
game_points = 0
quit_game = False

# Function to print the game map
def print_map(x, y):
    print(f"You are at coordinates ({x}, {y}).")

# Function to handle encounters
def encounter(location, x, y):
    print_map(x, y)
    location()

# Implement your location-specific functions here
def encounter_boar():
    print("A boar comes out of nowhere and runs towards you! You can attack...or run away...")
    answer = yes_no("Do you attack?")
    #attack of run away
    if (answer is True):
      attack("boar", 1)

def climb_tree():
    print("You come into a clearing and there seems to be a very tall tree.")
    answer = yes_no("Would you like to climb it?")
    #climb tree
    if (answer is True):
      print("You climb the tree. You can see how to get out the forest, it's to the east.")
    else:
      print("You don't bother climbing the tree.")

def enter_cave():
    print("You find a cave")
    answer = yes_no("Would you like to enter?")
    #bear
    if (answer is True):
      print("You enter the cave. There is a bear! It starts attacking you.")
      answer = yes_no("Do you attack?")
      if (answer is True):
        attack("bear", 1)
      else:
        print("You run away! The bear damages you on your way out of the cave. You lose 5 game points")
        global game_points
        game_points -= 5
    else:
      print("You don't enter the cave.")

def inspect_fallen_tree():
    print("A tree has fallen in your way")
    answer = yes_no("Would you like to inspect it?")
    if (answer is True):
      print("You inspect the fallen tree, it's hollow! You find some treasure! You win 10 game points")
      global game_points
      game_points += 10

def trapped_in_hunters_trap():
    print("You get stuck in a hunters trap! You lose 5 game points")
    global game_points
    game_points -= 5

def encounter_stag():
    print("The forest thins and you find a clearing, there is a lone stag.")
    answer = yes_no("Do you attack?")
    if (answer is True):
      attack("stag", 1)
    else:
      print("You run away!")

def explore_ruins_with_treasure():
    print("You find some ruins.")
    answer = yes_no("Do you explore them?")
    if (answer is True):
      #treasure
      print("You look around. You see a glint. You investigate.")
      print("You've found treasure! You win 10 game points")
      global game_points
      game_points += 10
    else:
      print("You don't bother looking around.")

def explore_ruins_without_treasure():
  print("You find some ruins.")
  answer = yes_no("Do you explore them?")
  if (answer is True):
    print("You look around, but to no avail, there is nothing here.")
  else:
    print("You don't bother looking around.")

# Other game functions
def game_end():
  print("The forest thins, you've found the exit!")
  global game_points
  print(f"Well done! You finished the game. You scored {game_points} game points.")
  if (game_points < 10):
    print(f"You didn't score enough points to win though.")
  else:
    print("Congratulations! You scored enough game points to win.")
  answer = yes_no("Would you like to play again?")
  if (answer is True):
    print("Something happens. The world spins. You find yourself back at the beginning of the forest!")
    main()
  else:
    print("Too bad. Next time!")
    global quit_game
    quit_game = True


def choose_weapon(name):
  global weaponChoice
  weaponChoice = ""
  print("To begin this quest, you must choose a weapon! Pick from the following:")
  for weapon in WEAPONS:
      print(weapon)
  while(weaponChoice not in WEAPONS):
      weaponChoice = input("Which weapon would you like to choose:")
  print(f"Good choice {name}!")

def attack(prey, turn):
  prompt = ""
  points = 0
  if (turn == 1):
    prompt = f"You are about to attack the {prey}. Rolling dice..."
    points = 5
  else:
    prompt = f"Attacking again! Rolling dice..."
    points = 10
  print(prompt)
  outcomes = [f"The {prey} got away!", f"You dealt a horrible blow with your {weaponChoice}, the {prey} has taken a horrible wound. You score {points} points.", f"The {prey} is dead! You score {points} points."]
  number = roll_dice()
  outcome = ""
  if (number < 3):
      outcome = outcomes[0]
  elif turn < 3:
      outcome = outcomes[1]
  else:
      outcome = outcomes[2]

  response = print(f"You rolled a {number}, {outcome}")
  if (outcome == outcomes[1] or outcome == outcomes[2]):
    global game_points
    game_points += points
    if (outcome == outcomes[1]):
      response = yes_no("Would you like to keep attacking?")
      if (response is True):
        turn += 1
        attack(prey, turn)

def yes_no(question):
  response = ""
  while response not in YES_NO:
    response = input(question)
    if str(response) == "yes":
      return True
    elif str(response) == "no":
      return False
    else:
      print("I didn't understand that. Try again\n")

def roll_dice():
  return random.randint(1,6)

def default_location():
  print("The forest continues...")

# Game Map
game_map = {
    (0, 0): encounter_boar,
    (0, 1): default_location,
    (0, 2): climb_tree,
    (0, 3): game_end,
    (1, 0): default_location,
    (1, 1): enter_cave,
    (1, 2): default_location,
    (1, 3): inspect_fallen_tree,
    (2, 0): trapped_in_hunters_trap,
    (2, 1): default_location,
    (2, 2): default_location,
    (2, 3): default_location,
    (3, 0): default_location,
    (3, 1): default_location,
    (3, 2): encounter_stag,
    (3, 3): default_location,
    (4, 0): explore_ruins_with_treasure,
    (4, 1): explore_ruins_without_treasure,
    (4, 2): default_location,
    (4, 3): default_location
}

# Main game loop
def main():
  previous_moves = []
  x, y = 4, 2
  game_points = 0
  name = input("What is your name, adventurer?\n")
  print(f"Greetings, {name}. Let us go on a quest!")
  choose_weapon(name)
  print("You find yourself on the edge of a giant forest.")
  global quit_game
  while quit_game is False:
    valid = True
    print("Available directions:", ", ".join(DIRECTIONS))
    direction = input("Which way do you go?\n").lower()
    if direction in DIRECTIONS:
        if direction == "go back":
            x, y = previous_moves.pop()
        else:
            previous_moves.append((x, y))
            if direction == "west" and y > 0:
                y -= 1
            elif direction == "east" and y < 3:
                y += 1
            elif direction == "north" and x > 0:
                x -= 1
            elif direction == "south" and x < 4:
                x += 1
            else:
              valid = False
            if valid:
              encounter(game_map.get((x, y), default_location), x, y)
            else:
              print("The way is blocked.")
    else:
        print("Invalid direction. Try again.")

if __name__ == "__main__":
    main()