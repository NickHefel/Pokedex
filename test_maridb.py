# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="1234",
        host="127.0.0.1",
        port=3306,
        database="test"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# cur.execute("""CREATE TABLE Persons (
#     PersonID int,
#     LastName varchar(255),
#     FirstName varchar(255),
#     Address varchar(255),
#     City varchar(255)
# );""")
# conn.commit()
# cur.execute("INSERT INTO persons (PersonID, LastName, FirstName, Address, City) VALUES ('1', 'HEFEL', 'NICK', 'lol', 'ED');")

cur.execute("""SELECT * FROM Persons;""")

for x in cur:
    print(f"{x}")
conn.commit()
conn.close()