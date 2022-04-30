import databaseManager
import csvManager
import consoleUI

# Attempt to connect to the database.
connection = databaseManager.connectToDatabase()

# Attempts to create the tables needed.
databaseManager.createTables()

# Imports the data from the CSV-files.
csvManager.importDataFromCSV() # Move functionality to UI later...

databaseManager.createView()

connection.commit()

# Handle main menu.
consoleUI.printMainMenu()

connection.close()