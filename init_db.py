import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO employee (fname, lname, sex, job) VALUES (?, ?, ?, ?)",
            ('lydia', 'bell', 'female', 'designer'))

cur.execute("INSERT INTO employee (fname, lname, sex, job) VALUES (?, ?, ?, ?)",
            ('jason', 'rover', 'male', 'developer'))

connection.commit()
connection.close()