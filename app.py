from flask import Flask, render_template, request, redirect, session,flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions

@app.route('/')
def index():
    return render_template('index.html')

from flask import flash

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        address = request.form['address']
        age = request.form['age']
        sex = request.form['sex']
        username = request.form['username']
        password = request.form['password']

        try:
            conn = sqlite3.connect('pickups.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (fullname, address, age, sex, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (fullname, address, age, sex, username, password))
            conn.commit()
            conn.close()
            return redirect('/login')

        except sqlite3.IntegrityError:
            flash("Username or email already exists. Please choose another.")
            return redirect('/signup')

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
    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('pickups.db')
    conn.row_factory = sqlite3.Row  # enables pickup.equipment-style access
    cursor = conn.cursor()

    # Get user info
    cursor.execute("SELECT id, fullname, username FROM users WHERE username = ?", (session['username'],))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return redirect('/login')
    user_id = user['id']
    fullname = user['fullname']
    email = user['username']

    # Get pickups
    cursor.execute('''
        SELECT equipment, weight, dimensions, address, pickup_time, status
        FROM pickups
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (user_id,))
    pickups = cursor.fetchall()
    conn.close()

    return render_template('home.html', name=fullname, email=email, pickups=pickups)


@app.route('/request-pickup', methods=['GET', 'POST'])
def request_pickup():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        equipment = request.form['equipment']
        weight = request.form['weight']
        dimensions = request.form['dimensions']
        address = request.form['address']
        pickup_time = request.form['pickup_time']

        # Get user ID from username
        conn = sqlite3.connect('pickups.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            cursor.execute('''
                INSERT INTO pickups (user_id, equipment, weight, dimensions, address, pickup_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, equipment, weight, dimensions, address, pickup_time))
            conn.commit()
        
        conn.close()
        return redirect('/success')

    return render_template('request_pickup.html')


@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
