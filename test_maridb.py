# Module Imports
import mariadb
import sys
import json

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="1234",
        host="127.0.0.1",
        port=3306,
        database="pokedex"

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

cur.execute("""select  *
from pokemonstats p
    inner join regionfound r
    on  p.PKMN_ID = r.PKMN_ID
    inner join pokemoninfo pin
    on p.PKMN_ID = pin.PKMN_ID 
    inner join evolutions e 
    on p.PKMN_ID = e.PKMN_ID 
    inner join pokemonstats ps
    on p.PKMN_ID = ps.PKMN_ID
    inner join typechart tc
    on p.PKMN_ID = tc.PKMN_ID
    inner join pokemonweight pw
    on p.PKMN_ID = pw.PKMN_ID
    where p.PKMN_ID = 5;""")

row_headers=[x[0] for x in cur.description]
rv = cur.fetchall()
json_data = []
for result in rv:
    json_data.append(dict(zip(row_headers,result)))

print(json_data)
# for x in cur:
#     print(f"{x}")
conn.commit()
conn.close()