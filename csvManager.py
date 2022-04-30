import csv
import sys
import databaseManager

phones = None
socs = None
reviews = None

def importDataFromCSV():
  global phones
  global socs
  global reviews

  readFiles()

  phones = importCSV(phones)
  socs = importCSV(socs)
  reviews = importCSV(reviews)

  databaseManager.insertPhones(phones)
  databaseManager.insertReviews(reviews)
  databaseManager.insertSoCs(socs)

def readFiles():
  "Imports the CSV data."
  try:
    # Open the files.
    phonesFile = open('phones.csv')
    reviewsFile = open('reviews.csv')
    socsFile = open('socs.csv')

    global phones
    global socs
    global reviews

    # Import the CSV-data.
    phones = csv.reader(phonesFile)
    socs = csv.reader(socsFile)
    reviews = csv.reader(reviewsFile)
  except:
    print('There was an issue opening the CSV-files. The application will now close.')
    sys.exit()

def importCSV(file):
  "Iterates through the CSV data, adds it to a list and returns it."
  # Initialize list and header skipping bool.
  csvAsList = []
  skipHeader = True

  # Iterate through the entire file.
  for row in file:
    # Skips the header.
    if skipHeader:
      skipHeader = False
      continue

    # Create a list from the row and add it to the list.
    csvAsList.append(list(row))

  return csvAsList