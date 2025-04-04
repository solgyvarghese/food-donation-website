from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # required for sessions

def connect_db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    return render_template("index.html", username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            con.commit()
        except sqlite3.IntegrityError:
            return "Username already taken. Please go back and choose another."
        con.close()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        con.close()
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return "Login failed. Please try again."
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        packets = request.form['packets']
        amount = request.form['amount']
        location = request.form['location']

        con = connect_db()
        cur = con.cursor()
        cur.execute("INSERT INTO food (name, packets, amount, location) VALUES (?, ?, ?, ?)",
                    (name, packets, amount, location))
        con.commit()
        con.close()
        return redirect('/view')
    return render_template("donate.html", username=session.get('username'))

@app.route('/view')
def view():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM food WHERE claimed = 0")
    food_items = cur.fetchall()
    con.close()
    return render_template("view_food.html", food_items=food_items, username=session.get('username'))

@app.route('/claim/<int:food_id>')
def claim(food_id):
    if 'username' not in session:
        return redirect('/login')
    con = connect_db()
    cur = con.cursor()
    cur.execute("UPDATE food SET claimed = 1 WHERE id = ?", (food_id,))
    con.commit()
    con.close()
    return redirect('/view')

if __name__ == '__main__':
    app.run(debug=True)
