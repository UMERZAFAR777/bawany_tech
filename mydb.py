import mysql.connector


database = mysql.connector.connect(
    user = 'root',
    host = 'localhost',
    passwd = 'umer2222',
)


cursorObject = database.cursor()

cursorObject.execute("CREATE DATABASE work")



print("All Done....!")











