import shutil
from flask import Flask, render_template, request, redirect, url_for
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
    qr.add_data('http://127.0.0.1:5000/qr4riversSmokehouse')
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

@app.route('/add-new-restaurant', methods=["GET", "POST"])
def add_new_restaurant():
    if request.method == "POST":
        try:
            name = request.form['name']
            location = request.form['location']
            distance = request.form['distance']
            price = request.form['price']
            review = request.form['review']

            with sql.connect("SSEData.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO LakelandEatsList (Name, Location, Distance, Price, Review) VALUES (?, ?, ?, ?, ?)", (name, location, distance, price, review))
                con.commit()
                msg = "Record successfully added"
            
            qr=qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f'http://127.0.0.1:5000/{name}')
            qr.make(fit=True)
            img = qr.make_image(fill_color="purple", back_color="black")
            img.save(f"./static/images/qrcodes/qr{name}.png")

            return redirect(url_for('database'))
        except:
            con.rollback()
            msg = "error in insert operation"

    else:
        return render_template('/add-new-restaurant.html')

if __name__ == '__main__':
    app.run(debug=True)