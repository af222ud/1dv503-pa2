import databaseManager
import csvManager

# Attempt to connect to the database.
connection = databaseManager.connectToDatabase()

# Attempts to create the tables needed.
databaseManager.createTables()

# Imports the data from the CSV-files.
csvManager.importDataFromCSV()

connection.commit()
connection.close()