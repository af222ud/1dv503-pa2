import sys
import databaseManager

def start():
  "Called when starting the user interface."
  print()
  print("Welcome to the phone checker application!")
  printMainMenu()

def printMainMenu():
  "Prints the main menu."
  print()
  print("1. List all phone models.")
  print("2. Show critcally acclaimed devices.")
  print("3. Show all phone models and their GPUs.")
  print("4. Show average review score per phone manufacturer.")
  print("5. Show reviewer affinity per manufacturer.")
  print("6. Powerhouse search. Search for CPU core count and battery capacity!")
  print("7. List all attributes of a phone model.")
  print()
  print("0. Exit application")
  print()

  getMainMenuInput("Please select an option: ")

def getMainMenuInput(prompt):
  "Catches the user's input from the main menu."
  option = input(prompt)

  displayNextMenu(option)

def displayNextMenu(option):
  "Selects an action based on the user's input."
  match option:
    case '1':
      listAllPhones()
    case '2':
      listCritcallyAcclaimed()
    case '3':
      listPhonesAndGPUs()
    case '4':
      listAverageScorePerMaker()
    case '5':
      listReviewerAffinityToMaker()
    case '6':
      searchForBatteryAndCoreCombination()
    case '7':
      displayPhone()
    case '0':
      sys.exit()
    case _:
      getMainMenuInput("Please select a valid number: ")

def listAllPhones():
  "Lists every phone available."
  listOfPhones = databaseManager.getPhones()

  # Prints the menu.
  print("\nList of phone models:")
  print("---------------------")
  for value in listOfPhones:
    print("   > " + value)

  pressEnterToReturn()

def listCritcallyAcclaimed():
  "Lists all critically acclaimed devices."
  listOfPhones = databaseManager.getCriticallyAcclaimed()

  # Prints the menu.
  print("\nAcclaimed devices:")
  print("----------------------------")
  for value in listOfPhones:
    print("   > " + value[1] + " (" + str(round(value[0], 2)) + ")")

  pressEnterToReturn()

def listPhonesAndGPUs():
  "Lists every phone and its GPU."
  listOfPhones = databaseManager.getPhoneGPUs()

  # Prints the menu.
  print("\nDevices and their GPUs:")
  print("---------------------------------")
  print("     DEVICE          GPU")
  print("---------------------------------")
  for value in listOfPhones:
    print("   " + value[0] + " ---> " + value[1])

  pressEnterToReturn()

def listAverageScorePerMaker():
  "Lists the average review score per manufacturer."
  listOfMakers = databaseManager.getAverageScorePerMaker()

  # Prints the menu.
  print("\nAverage review score per maker:")
  print("----------------------------------")
  for value in listOfMakers:
    print("   > " + value[1] + " ----> " + str(round(value[0], 2)))

  pressEnterToReturn()

def listReviewerAffinityToMaker():
  "Lists each reviwer's affinity for each manufacturer."
  listOfReviewers = databaseManager.getReviewerAffinityByMaker()

  # Prints the menu.
  print("\nReviewer affinity by phone manufacturer:")
  print("------------------------------------------")
  for affinity in listOfReviewers:
    print("   > " + affinity[0] + " gives an average score of " + str(round(affinity[1], 2)) + " to " + affinity[2] + " products.")

  pressEnterToReturn()

def searchForBatteryAndCoreCombination():
  "Displays a list of phones matching the user's input."
  batterySize = inputNumber("\nPlease enter your preferred minimum battery capacity: ")
  coreCount = inputNumber("\nPlease enter your preferred minimum CPU core count: ")

  matches = databaseManager.getMatchingCoreCountAndBattery(batterySize, coreCount)

  # Prints the menu.
  print("\nMatches for the given parameters:")
  print("------------------------------------")

  # If no match was found, do not attempt to print the attributes.
  if len(matches) == 0:
    print("No matches found.")
    pressEnterToReturn()

  # If matches were found, print them in a list.
  for phone in matches:
    print("   > " + phone[0])

  pressEnterToReturn()

def inputNumber(prompt):
  "Catches user input and validates the input to match a number."
  number = input(prompt)

  # Do not accept the input while it is not a number.
  while number.isnumeric() is False:
    number = input("Please enter a valid number: ")

  return number

def displayPhone():
  "Displays a specified phone."
  model = input("\nPlease enter the model to view: ")

  result = databaseManager.searchForPhone(model)

  # If no match was found, do not attempt to display its attributes.
  if len(result) == 0:
    print("\nNo result found.")
    pressEnterToReturn()

  result = result[0] # Truncate the tuple if it exists.

  # Prints the menu.
  print("\nSearch result:")
  print("--------------------------------------------")
  print("   " + result[3] + " " + result[0]) # Prints the phone's maker and name.
  print("     - CPU:  " + result[2] + " (" + str(result[6]) + " core(s) @ " + result[5] + ")") # Prints the CPU information.
  print("     - GPU:  " + result[7]) # Prints the GPU name.
  print("     - Battery capacity: " + str(result[4]) + " mAh") # Prints the battery capacity.
  print("     - Year of release: " + str(result[1])) # Prints the year of release.
  print("     - Average review score: " + str(round(result[8], 2)))

  pressEnterToReturn()

def pressEnterToReturn():
  "Returns the user to the main menu when ENTER is pressed."
  input("\nPress ENTER to return...")

  printMainMenu()