import databaseManager

# Attempt to connect to the database.
connection = databaseManager.connectToDatabase()

# Attempts to create the tables needed.
databaseManager.createTables()

connection.commit()
connection.close()