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