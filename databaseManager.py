import sys
import mysql.connector

cursor = None

def connectToDatabase():
  try:
    global cursor

    # Attempts to connect to the specified database.
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='karlsson_franzen_pa2')
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
      cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='karlsson_franzén')
      cursor = cnx.cursor()

      return cnx
    except:
      print('There was an error when attempting to create the database or connect to mySQL. The application will now close.')
      sys.exit()
