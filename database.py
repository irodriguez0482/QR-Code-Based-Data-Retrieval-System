from flask import Flask, render_template, request
import sqlite3 as sql

conn = sql.connect('SSEData.db')
conn.row_factory = sql.Row
print("Opened database successfully")

cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/database')
def database():
    conn = sql.connect('SSEData.db')
    conn.row_factory = sql.Row
    print("Opened database successfully in the restrictions route")
    cur = conn.cursor()

    sqlQ = ("""SELECT * FROM LakelandEatsList;""")
    print(sqlQ)

    headings = ("ID", "Name", "Location", "Distance", "Price", "Review")

    username = "user"

    cur.execute(sqlQ)
    data = cur.fetchall()
    return render_template('database.html', username=username, headings=headings, data=data)


if __name__ == '__main__':
    app.run(debug=True)