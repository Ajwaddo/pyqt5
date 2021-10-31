import sqlite3
from operator import itemgetter
connection = sqlite3.connect('user.db')
myCursor = connection.cursor()

myCursor.execute("SELECT name FROM vaccinationCenters")
vacc_name = myCursor.fetchall()

for i in vacc_name:
    for j in i:
        print(j)

#