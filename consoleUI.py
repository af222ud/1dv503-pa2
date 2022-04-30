import sys
import databaseManager

def printMainMenu():
  print()
  print("1. List all phone models.")
  print("2. Show critcally acclaimed devices.")

  print("0. Exit application")

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
      showCritcallyAcclaimed()
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

def showCritcallyAcclaimed():
  listOfPhones = databaseManager.getCriticallyAcclaimed()

  print("\nAcclaimed devices:")
  print("--------------------")
  for value in listOfPhones:
    print("   > " + value[1] + " (" + str(round(value[0], 2)) + ")")

  pressEnterToReturn()

def pressEnterToReturn():
  input("\nPress ENTER to return...")
  printMainMenu()