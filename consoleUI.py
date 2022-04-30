import sys
import databaseManager

def start():
  print()
  print("Welcome to the phone checker application!")
  printMainMenu()

def printMainMenu():
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
  option = input(prompt)

  displayNextMenu(option)

def displayNextMenu(option):
  match option:
    case '1':
      # Display all models.
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
  listOfPhones = databaseManager.getPhones()

  print("\nList of phone models:")
  print("---------------------")
  for value in listOfPhones:
    print("   > " + value)

  pressEnterToReturn()

def listCritcallyAcclaimed():
  listOfPhones = databaseManager.getCriticallyAcclaimed()

  print("\nAcclaimed devices:")
  print("----------------------------")
  for value in listOfPhones:
    print("   > " + value[1] + " (" + str(round(value[0], 2)) + ")")

  pressEnterToReturn()

def listPhonesAndGPUs():
  listOfPhones = databaseManager.getPhoneGPUs()

  print("\nDevices and their GPUs:")
  print("---------------------------------")
  print("     DEVICE          GPU")
  print("---------------------------------")
  for value in listOfPhones:
    print("   " + value[0] + " ---> " + value[1])

  pressEnterToReturn()

def listAverageScorePerMaker():
  listOfMakers = databaseManager.getAverageScorePerMaker()

  print("\nAverage review score per maker:")
  print("----------------------------------")
  for value in listOfMakers:
    print("   > " + value[1] + " ----> " + str(round(value[0], 2)))

  pressEnterToReturn()

def listReviewerAffinityToMaker():
  listOfReviewers = databaseManager.getReviewerAffinityByMaker()

  print("\nReviewer affinity by phone manufacturer:")
  print("------------------------------------------")
  for affinity in listOfReviewers:
    print("   > " + affinity[0] + " gives an average score of " + str(round(affinity[1], 2)) + " to " + affinity[2] + " products.")

  pressEnterToReturn()

def searchForBatteryAndCoreCombination():
  batterySize = inputNumber("\nPlease enter your preferred battery capacity: ")
  coreCount = inputNumber("\nPlease enter your preferred CPU core count: ")

  matches = databaseManager.getMatchingCoreCountAndBattery(batterySize, coreCount)

  print("\nMatches for the given parameters:")
  print("------------------------------------")

  if len(matches) == 0:
    print("No matches found.")
    pressEnterToReturn()

  for phone in matches:
    print("   > " + phone[0])

  pressEnterToReturn()

def inputNumber(prompt):
  number = input(prompt)

  while number.isnumeric() is False:
    number = input("Please enter a valid number: ")

  return number

def displayPhone():
  model = input("\nPlease enter the model to view: ")

  result = databaseManager.searchForPhone(model)

  if len(result) == 0:
    print("\nNo result found.")
    pressEnterToReturn()

  result = result[0]

  print("\nSearch result:")
  print("--------------------------------------------")
  print("   " + result[3] + " " + result[0])
  print("     - CPU:  " + result[2] + " (" + str(result[6]) + " core(s) @ " + result[5] + ")")
  print("     - GPU:  " + result[7])
  print("     - Battery capacity: " + str(result[4]) + " mAh")
  print("     - Year of release: " + str(result[1]))

  pressEnterToReturn()

def pressEnterToReturn():
  input("\nPress ENTER to return...")
  printMainMenu()