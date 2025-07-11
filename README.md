# hackathon-gec
User:login,home screen,schedule a pickup(details),store in database.Pickup login.Get information.according to proxmity.Pickup(Possible implementation of google maps api) 
ecoconnect/
├── app.py
├── requirements.txt
├── /templates/
│   ├── index.html             # Landing page
│   ├── signup.html            # User registration
│   ├── login.html             # User login
│   ├── home.html              # After login dashboard
│   ├── request_pickup.html    # Form to schedule pickup
│   ├── success.html           # After form submission
│   ├── collector_login.html   # Separate login for pickup agents
│   ├── collector_dashboard.html  # View pickup requests
├── /static/
│   ├── style.css              # CSS styles
│   └── map.js (optional)      # JS for maps integration
└── /data/
    └── pickups.db (SQLite) or JSON
This is the project scehmca