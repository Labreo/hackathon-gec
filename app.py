from flask import Flask, render_template, request, redirect, session,flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        address = request.form['address']
        age = request.form['age']
        sex = request.form['sex']
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('pickups.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (fullname, address, age, sex, username, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fullname, address, age, sex, username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  
        conn = sqlite3.connect('pickups.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/home')
        else:
            flash('Invalid username or password')
            return redirect('/login')

    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/request-pickup', methods=['GET', 'POST'])
def request_pickup():
    if request.method == 'POST':
        # Save pickup data (name, address, waste_type)
        return redirect('/success')
    return render_template('request_pickup.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/collector-login', methods=['GET', 'POST'])
def collector_login():
    return render_template('collector_login.html')

@app.route('/collector-dashboard')
def collector_dashboard():
    # Load pickups and show based on proximity
    return render_template('collector_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
