import sys
import mysql.connector

cursor = None

def connectToDatabase():
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
  global cursor

  # Creates the "phones" table, if it does not already exist.
  phones = """CREATE TABLE IF NOT EXISTS phones (
                name varchar(255) COLLATE utf8mb4_unicode_ci,
                year int,
                soc varchar(255),
                maker varchar(255),
                battery varchar(255),
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
  # Creates the SQL statement to use while iterating through the list.
  statement = """INSERT IGNORE INTO phones(name, year, soc, maker, battery)
                VALUES (%s, %s, %s, %s, %s);"""

  # Execute the statement.
  executeInsertStatement(statement, listOfPhones)

def insertReviews(listOfReviews):
  # Creates the SQL statement to use while iterating through the list.
  statement = """INSERT IGNORE INTO reviews(model, reviewer, organization, score)
                VALUES (%s, %s, %s, %s);"""

  # Execute the statement.
  executeInsertStatement(statement, listOfReviews)

def insertSoCs(listOfSoCs):
  # Creates the SQL statement to use while iterating through the list.
  statement = """INSERT IGNORE INTO socs(name, clock_speed, cores, gpu)
                VALUES (%s, %s, %s, %s);"""

  # Execute the statement.
  executeInsertStatement(statement, listOfSoCs)

def executeInsertStatement(statement, listOfData):
  global cursor

  # Executes the statement for every row of data in the list.
  for row in listOfData:
    # Skip broken entries.
    if row[0] == None:
      continue

    values = row
    cursor.execute(statement, values)

def createView():
  global cursor

  statement = """CREATE OR REPLACE VIEW CriticallyAcclaimed
                AS SELECT AVG(score), model
                FROM reviews
                GROUP BY model
                HAVING AVG(score) >= 8;"""

  cursor.execute(statement)

def getPhones():
  global cursor
  phoneNames = []

  # Execute the statement...
  statement = """SELECT name
                  FROM phones;"""
  cursor.execute(statement)

  for name in cursor.fetchall():
    phoneNames.append(name[0])
  
  return phoneNames

def getCriticallyAcclaimed():
  global cursor
  criticallyAcclaimedDevices = []
  
  # Execute the statement...
  statement = """SELECT *
                FROM criticallyacclaimed"""
  cursor.execute(statement)

  for attributes in cursor.fetchall():
    criticallyAcclaimedDevices.append(attributes)

  return criticallyAcclaimedDevices

def getPhoneGPUs():
  global cursor
  listOfPhones = []

  # Execute the statement...
  statement = """SELECT phones.name, socs.gpu
                FROM phones
                INNER JOIN socs
                ON phones.soc = socs.name;"""
  cursor.execute(statement)

  for attributes in cursor.fetchall():
    listOfPhones.append(attributes)

  return listOfPhones

def getAverageScorePerMaker():
  global cursor
  listOfMakers = []

  # Execute the statement...
  statement = """SELECT AVG(reviews.score), phones.maker
                FROM reviews
                INNER JOIN phones
                ON phones.name = reviews.model
                GROUP BY phones.maker;"""
  cursor.execute(statement)

  for maker in cursor.fetchall():
    listOfMakers.append(maker)

  return listOfMakers

def getReviewerAffinityByMaker():
  global cursor
  listOfReviewers = []

  # Execute the statement...
  statement = """SELECT reviews.reviewer, AVG(reviews.score), phones.maker
                FROM reviews
                INNER JOIN phones
                ON phones.name = reviews.model
                GROUP BY reviews.reviewer, phones.maker;"""
  cursor.execute(statement)

  for values in cursor.fetchall():
    listOfReviewers.append(values)
  
  return listOfReviewers