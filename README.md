# ♻️ EcoConnect — Hackathon-Coding Club

EcoConnect is a Flask-based web application designed during a 24-hour hackathon to connect users with **local farms** and enable **waste collectors** to pick up waste — especially e-waste — directly from users' doorsteps. The goal is to simplify sustainable disposal while promoting local farming initiatives.

---

## 🌐 Features

### Live App URL
- https://hackathon-gec.onrender.com

### 👤 User Module
- ✅ User Signup & Login (with session tracking)
- 🏠 User Dashboard (`/home`)
- 📦 Schedule Pickup: Equipment type, weight, dimensions, address & time
- 🧾 View Previous Pickup Requests

### 🚛 Collector Module
- 🔐 Collector Signup & Login
- 📍 Access pickup requests based on proximity
- 📊 Dashboard to view and manage pickup jobs (planned: Google Maps API integration)

---

## 🗂️ Project Structure

├── README.md
├── app.py
├── init_db.py
├── pickups.db
├── requirements.txt
├── static
│   ├── img
│   │   ├── book.png
│   │   ├── collect.png
│   │   └── recycle.png
│   ├── map.js
│   └── style.css
└── templates
    ├── collector_dashboard.html
    ├── collector_login.html
    ├── collector_signup.html
    ├── home.html
    ├── index.html
    ├── login.html
    ├── request_pickup.html
    ├── signup.html
    └── success.html

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Extra**: Google Maps API , Session Handling, Flash Messaging

---

## ⚙️ Setup Instructions

1. **Clone this repo**
   ```bash
   git clone https://github.com/yourusername/hackathon-gec.git
   cd hackathon-gec

2. **Create virtual environment & install requirements**
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt

3. **Initialize the database**
   python init_db.py

4. **Initialize the database**
   python init_db.py

5. **Run the app**
   flask run

6. **Open in browser**
   Visit http://localhost:5000
   
 
