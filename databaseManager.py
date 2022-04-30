import sys
import mysql.connector

cursor = None

def connectToDatabase():
  "Attempts to connect to the database."
  try:
    global cursor

    # Attempts to connect to the specified database.
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='karlsson_franzén_pa2')
    cursor = cnx.cursor()

    return cnx
  except:
    try:
      # If the database was not found, first attempt to connect to mySQL...
      print("Database does not exist, attempting to create it...")
      cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
      cursor = cnx.cursor()

      # Then attempt to create the database.
      cursor.execute("CREATE DATABASE IF NOT EXISTS karlsson_franzén_pa2;")
      print("Database was created successfully.")

      # Connect to the newly created database.
      cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='karlsson_franzén_pa2')
      cursor = cnx.cursor()

      return cnx
    except:
      print('There was an error when attempting to create the database or connect to mySQL. The application will now close.')
      sys.exit()

def createTables():
  "Attempts to create the tables, if they do not already exist."
  global cursor

  # Creates the "phones" table, if it does not already exist.
  phones = """CREATE TABLE IF NOT EXISTS phones (
                name varchar(255) COLLATE utf8mb4_unicode_ci,
                year int,
                soc varchar(255),
                maker varchar(255),
                battery int,
                PRIMARY KEY (name));"""

  # Creates the "reviews" table, if it does not already exist.
  reviews = """CREATE TABLE IF NOT EXISTS reviews (
                model varchar(255) COLLATE utf8mb4_unicode_ci,
                reviewer varchar(255),
                organization varchar(255),
                score int,
                PRIMARY KEY(model, organization));"""

  # Creates the "SoCs" table, if it does not already exist.
  socs = """CREATE TABLE IF NOT EXISTS socs (
              name varchar(255),
              clock_speed varchar(255),
              cores int,
              gpu varchar(255),
              PRIMARY KEY(name));"""

  # Execute the queries.
  cursor.execute(phones)
  cursor.execute(reviews)
  cursor.execute(socs)

def insertPhones(listOfPhones):
  "Attempts to insert the passed list of phones into the database."
  # Creates the SQL statement to use while iterating through the list.
  statement = """INSERT IGNORE INTO phones(name, year, soc, maker, battery)
                VALUES (%s, %s, %s, %s, %s);"""

  # Execute the statement.
  executeInsertStatement(statement, listOfPhones)

def insertReviews(listOfReviews):
  "Attempts to insert the passed list of reviews into the database."
  # Creates the SQL statement to use while iterating through the list.
  statement = """INSERT IGNORE INTO reviews(model, reviewer, organization, score)
                VALUES (%s, %s, %s, %s);"""

  # Execute the statement.
  executeInsertStatement(statement, listOfReviews)

def insertSoCs(listOfSoCs):
  "Attempts to insert the passed list of SoCs into the database."
  # Creates the SQL statement to use while iterating through the list.
  statement = """INSERT IGNORE INTO socs(name, clock_speed, cores, gpu)
                VALUES (%s, %s, %s, %s);"""

  # Execute the statement.
  executeInsertStatement(statement, listOfSoCs)

def executeInsertStatement(statement, listOfData):
  "Attempts to insert the passed list of data using the passed insert statement."
  try:  
    global cursor

    # Executes the statement for every row of data in the list.
    for row in listOfData:
      # Skip broken entries.
      if row[0] == None:
        continue

      values = row
      cursor.execute(statement, values)
  except:
    print("Data insertion failed. The application will now close.")
    sys.exit()

def createView():
  "Attempts to create the critically acclaimed view."
  global cursor

  statement = """CREATE OR REPLACE VIEW CriticallyAcclaimed
                AS SELECT AVG(score), model
                FROM reviews
                GROUP BY model
                HAVING AVG(score) >= 8;"""
  cursor.execute(statement)

def getPhones():
  "Returns the names of all phones in the database."
  global cursor
  phoneNames = []

  statement = """SELECT name
                  FROM phones;"""
  cursor.execute(statement)

  # Append the phones to the list.
  for name in cursor.fetchall():
    phoneNames.append(name[0])
  
  return phoneNames

def getCriticallyAcclaimed():
  "Returns a list of all phones with an average review score of 8 or above."
  global cursor
  criticallyAcclaimedDevices = []
  
  statement = """SELECT *
                FROM criticallyacclaimed"""
  cursor.execute(statement)

  # Append the attributes (names and average review score) to the list.
  for attributes in cursor.fetchall():
    criticallyAcclaimedDevices.append(attributes)

  return criticallyAcclaimedDevices

def getPhoneGPUs():
  "Returns a list of every phone and its respective GPU."
  global cursor
  listOfPhones = []

  statement = """SELECT phones.name, socs.gpu
                FROM phones
                INNER JOIN socs
                ON phones.soc = socs.name;"""
  cursor.execute(statement)

  # Adds the names of the phones and their GPUs to the list.
  for attributes in cursor.fetchall():
    listOfPhones.append(attributes)

  return listOfPhones

def getAverageScorePerMaker():
  "Returns the average score per manufacturer."
  global cursor
  listOfMakers = []

  statement = """SELECT AVG(reviews.score), phones.maker
                FROM reviews
                INNER JOIN phones
                ON phones.name = reviews.model
                GROUP BY phones.maker;"""
  cursor.execute(statement)

  # Adds the average review score of each manufacturer and their names to the list.
  for maker in cursor.fetchall():
    listOfMakers.append(maker)

  return listOfMakers

def getReviewerAffinityByMaker():
  "Returns a list of each reviewer's affinity for each manufacturer."
  global cursor
  listOfReviewers = []

  statement = """SELECT reviews.reviewer, AVG(reviews.score), phones.maker
                FROM reviews
                INNER JOIN phones
                ON phones.name = reviews.model
                GROUP BY reviews.reviewer, phones.maker;"""
  cursor.execute(statement)

  # Adds the reviewer's name, average score per manufacturer and the manufacturer's name to the list.
  for values in cursor.fetchall():
    listOfReviewers.append(values)
  
  return listOfReviewers

def getMatchingCoreCountAndBattery(batteryCapacity, coreCount):
  "Returns every phone that matches the passed battery capacity and CPU core count."
  global cursor
  listOfMatches = []

  statement = """SELECT name
                FROM phones
                WHERE battery >= %s
                AND soc IN(
                  SELECT name
                  FROM socs
                  WHERE cores >= %s);"""
  cursor.execute(statement, [batteryCapacity, coreCount])

  # Adds the name of each phone matching the query into the list.
  for values in cursor.fetchall():
    listOfMatches.append(values)
  
  return listOfMatches

def searchForPhone(name):
  "Returns every attribute of the passed phone and its SoC."
  global cursor
  matchDetails = []

  statement = """SELECT phones.*, socs.clock_speed, socs.cores, socs.gpu
                FROM phones
                LEFT JOIN socs
                ON socs.name = phones.soc
                WHERE phones.name LIKE %s"""
  cursor.execute(statement, [name])

  # Adds the attributes into the list.
  for attribute in cursor.fetchall():
    matchDetails.append(attribute)

  return matchDetails