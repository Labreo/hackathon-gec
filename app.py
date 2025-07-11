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
            return redirect('/collector-dashboard')
        else:
            flash('Invalid username or password')
            return redirect('/collector-login')

    return render_template('collector_login.html')

@app.route('/collector-dashboard')
def collector_dashboard():
    if 'username' not in session:
        return redirect('/collector-login')

    conn = sqlite3.connect('pickups.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get collector's address or city (if stored)
    cursor.execute("SELECT address FROM users WHERE username = ?", (session['username'],))
    collector = cursor.fetchone()
    city_filter = collector['address'].split(',')[-1].strip() if collector else None

    if city_filter:
        cursor.execute('''
            SELECT id, equipment, weight, dimensions, address, pickup_time, status
            FROM pickups
            WHERE status = 'pending' AND address LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{city_filter}%',))
    else:
        cursor.execute('''
            SELECT id, equipment, weight, dimensions, address, pickup_time, status
            FROM pickups
            WHERE status = 'pending'
            ORDER BY timestamp DESC
        ''')

    pickups = cursor.fetchall()
    conn.close()

    return render_template('collector_dashboard.html', pickups=pickups)


@app.route('/mark-collected/<int:pickup_id>', methods=['POST'])
def mark_collected(pickup_id):
    conn = sqlite3.connect('pickups.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE pickups SET status = 'collected' WHERE id = ?", (pickup_id,))
    conn.commit()
    conn.close()
    return redirect('/collector-dashboard')




@app.route('/collector-signup', methods=['GET', 'POST'])
def collector_signup():
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
            return redirect('/collector-login')

        except sqlite3.IntegrityError:
            flash("Username or email already exists. Please choose another.")
            return redirect('/collector-signup')

    return render_template('collector_signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
