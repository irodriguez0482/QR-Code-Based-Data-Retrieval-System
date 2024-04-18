from flask import Flask, render_template, request
import sqlite3 as sql
import qrcode

conn = sql.connect('SSEData.db')
conn.row_factory = sql.Row
print("Opened database successfully")

cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/4riversSmokehouse')
def restaurant():
    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('http://127.0.0.1:5000/restaurant')
    qr.make(fit=True)
    img = qr.make_image(fill_color="purple", back_color="black")
    img.save("./static/images/qrcodes/qr4riversSmokehouse.png")
    conn = sql.connect('SSEData.db')
    conn.row_factory = sql.Row
    print("Opened database successfully in the restrictions route")
    cur = conn.cursor()

    sqlQ = ("""SELECT * FROM LakelandEatsList WHERE rowid=1;""")
    print(sqlQ)
    cur.execute(sqlQ)
    data = cur.fetchall()

    return render_template('4riversSmokehouse.html', data=data)


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