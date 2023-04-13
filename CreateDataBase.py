import sqlite3 as sq

with sq.connect('dataBase.db') as connect:
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE Test (
        question TEXT,
        answer1 TEXT,
        answer2 TEXT,
        answer3 TEXT,
        answer4 TEXT,
        right answer TEXT    
    )""")




