import databaseManager
import csvManager
import consoleUI

# Attempt to connect to the database.
connection = databaseManager.connectToDatabase()

# Attempts to create the tables needed.
databaseManager.createTables()

# Imports the data from the CSV-files.
csvManager.importDataFromCSV()

# Creates the view.
databaseManager.createView()

connection.commit()

# Handle main menu.
consoleUI.printMainMenu()

connection.close()