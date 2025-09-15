from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__, static_folder="assets", template_folder=".")
app.secret_key = 'fixitforce'

# Database initialization
def init_db():
    conn = sqlite3.connect('fixitforce.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  phone TEXT,
                  password TEXT NOT NULL,
                  user_type TEXT DEFAULT 'customer',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create services table
    c.execute('''CREATE TABLE IF NOT EXISTS services
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  base_price REAL)''')
    
    # Create bookings table
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  service_id INTEGER,
                  address TEXT NOT NULL,
                  city TEXT NOT NULL,
                  pincode TEXT NOT NULL,
                  customer_name TEXT NOT NULL,
                  customer_phone TEXT NOT NULL,
                  notes TEXT,
                  status TEXT DEFAULT 'pending',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (service_id) REFERENCES services (id))''')
    
    # Insert default services
    services = [
        ('Electrician', 'Wiring, appliance fitting, UPS and more', 199),
        ('Plumber', 'Leak fixes, tap replacement, bathroom works', 199),
        ('Mason', 'Small wall repairs, tiling, patchwork', 0),
        ('Painter', 'Room repainting, touch-ups, waterproofing', 299),
        ('Installation', 'Appliance and furniture installation', 249),
        ('Tools & Spare Parts', 'Tools and spare parts delivery', 99)
    ]
    
    c.executemany('INSERT OR IGNORE INTO services (name, description, base_price) VALUES (?, ?, ?)', services)
    
    # Insert test users if they don't exist
    test_users = [
        ('John Doe', 'john@example.com', '1234567890', 'password123', 'worker'),
        ('Jane Smith', 'jane@example.com', '0987654321', 'password123', 'customer')
    ]
    
    for user in test_users:
        try:
            c.execute('INSERT INTO users (name, email, phone, password, user_type) VALUES (?, ?, ?, ?, ?)', user)
        except sqlite3.IntegrityError:
            pass  # User already exists
    
    conn.commit()
    conn.close()

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('fixitforce.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database when app starts
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()
    return render_template("services.html", services=services)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(f"Login attempt: Email={email}, Password={password}")  # Debug print
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        
        print(f"User found: {user}")  # Debug print
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_type'] = user['user_type']
            print(f"Session set: {session}")  # Debug print
            
            if user['user_type'] == 'worker':
                return redirect("/dashboard")
            else:
                return redirect("/")
        else:
            print("Login failed: Invalid credentials")  # Debug print
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        user_type = request.form.get("user_type", "customer")
        
        print(f"Signup attempt: {name}, {email}, {user_type}")  # Debug print
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (name, phone, email, password, user_type) VALUES (?, ?, ?, ?, ?)',
                        (name, phone, email, password, user_type))
            conn.commit()
            conn.close()
            
            print("Signup successful")  # Debug print
            return redirect("/login")
            
        except sqlite3.IntegrityError:
            print("Signup failed: Email already exists")  # Debug print
    
    return render_template("signup.html")

@app.route("/book", methods=["POST"])
def book_service():
    service = request.form.get("service")
    address = request.form.get("address")
    city = request.form.get("city")
    pincode = request.form.get("pincode")
    name = request.form.get("name")
    phone = request.form.get("phone")
    notes = request.form.get("notes")
    
    conn = get_db_connection()
    service_row = conn.execute('SELECT id FROM services WHERE name = ?', (service,)).fetchone()
    
    if not service_row:
        conn.close()
        return redirect("/services")
    
    service_id = service_row['id']
    user_id = session.get('user_id', 1)
    
    conn.execute('''INSERT INTO bookings (user_id, service_id, address, city, pincode, 
                 customer_name, customer_phone, notes) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (user_id, service_id, address, city, pincode, name, phone, notes))
    conn.commit()
    conn.close()
    
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if session.get('user_type') != 'worker':
        return redirect("/login")
    
    conn = get_db_connection()
    jobs = conn.execute('''SELECT bookings.*, services.name as service_name 
                          FROM bookings 
                          JOIN services ON bookings.service_id = services.id 
                          ORDER BY bookings.created_at DESC''').fetchall()
    conn.close()
    
    return render_template("dashboard.html", jobs=jobs, user_name=session.get('user_name'))

@app.route("/update_status/<int:job_id>", methods=["POST"])
def update_status(job_id):
    new_status = request.form.get("status")
    
    conn = get_db_connection()
    conn.execute('UPDATE bookings SET status = ? WHERE id = ?', (new_status, job_id))
    conn.commit()
    conn.close()
    
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/book/service")
def book_service_page():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()
    return render_template("services.html", services=services)

# Debug route to view users
@app.route("/debug/users")
def debug_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return str([dict(user) for user in users])

@app.route("/index.html")
def home_html():
    return redirect("/")

@app.route("/services.html")
def services_html():
    return redirect("/services")

@app.route("/about.html")
def about_html():
    return redirect("/about")

@app.route("/contact.html")
def contact_html():
    return redirect("/contact")

@app.route("/login.html")
def login_html():
    return redirect("/login")

@app.route("/signup.html")
def signup_html():
    return redirect("/signup")

@app.route("/dashboard.html")
def dashboard_html():
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)