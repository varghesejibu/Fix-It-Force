# Fix It Force 🔧

> **On-demand home services — connecting homeowners with trusted local tradespeople.**

Fix It Force is a two-sided marketplace web application that lets customers instantly book verified workers (electricians, plumbers, masons, painters, and more) while giving workers a dedicated dashboard to manage their jobs.

---

## ✨ Features

- **Service Booking** — multi-step booking form; customers pick a service, enter their address and contact details, and submit
- **Worker & Customer Accounts** — unified registration with role-based access (`customer` / `worker`)
- **Worker Dashboard** — post-login view showing pending and assigned job requests
- **Service Catalogue** — pre-seeded list of home services with base pricing
- **Responsive UI** — mobile-friendly navbar with hamburger menu
- **Zero external DB dependency** — SQLite database bundled with the project

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 · Flask |
| Frontend | HTML5 · CSS3 (custom stylesheet) |
| Database | SQLite 3 |
| Session handling | Flask server-side sessions |

---

## 📁 Project Structure

```
Fix-It-Force/
├── app.py              # Flask application — routes, DB init, session logic
├── view_table.py       # Dev utility to inspect SQLite tables in the terminal
├── fixitforce.db       # SQLite database
│
├── index.html          # Landing / home page
├── about.html          # About the platform
├── contact.html        # Contact page
├── services.html       # Service listing + multi-step booking form
├── dashboard.html      # Worker dashboard (post-login)
├── login.html          # Login form
├── signup.html         # Registration form (workers & customers)
│
└── assets/
    ├── css/style.css   # Global stylesheet
    └── images/         # Logo and imagery
```

---

## 🗄️ Database Schema

Three tables are created automatically on first run:

### `users`
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | |
| email | TEXT | Unique |
| phone | TEXT | |
| password | TEXT | |
| user_type | TEXT | `'customer'` or `'worker'` |
| created_at | TIMESTAMP | Auto |

### `services` (pre-seeded)
| Service | Description | Base Price |
|---|---|---|
| Electrician | Wiring, appliance fitting, UPS and more | ₹199 |
| Plumber | Leak fixes, tap replacement, bathroom works | ₹199 |
| Mason | Small wall repairs, tiling, patchwork | Free |
| Painter | Room repainting, touch-ups, waterproofing | ₹299 |
| Installation | Appliance and furniture installation | ₹249 |
| Tools & Spare Parts | Tools and spare parts delivery | ₹99 |

### `bookings`
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| user_id | INTEGER | FK → users |
| service_id | INTEGER | FK → services |
| address | TEXT | |
| city | TEXT | |
| pincode | TEXT | |
| customer_name | TEXT | |
| customer_phone | TEXT | |
| notes | TEXT | Optional |
| status | TEXT | Default `'pending'` |
| created_at | TIMESTAMP | Auto |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/varghesejibu/Fix-It-Force.git
cd Fix-It-Force

# 2. Install dependencies
pip install flask

# 3. Run the app
python app.py
```

Open your browser at `http://127.0.0.1:5000`.

The SQLite database and all tables are created automatically on first run.

---

## 🔄 How It Works

```
Customer                        Worker
   │                               │
   ▼                               │
Visits site                        │
   │                               │
   ▼                               │
Browses Services page              │
   │                               │
   ▼                               │
Fills booking form                 │
   │                               │
   ▼                               │
Flask saves booking           Worker logs in
to SQLite (status=pending)         │
                                   ▼
                          Worker Dashboard shows
                          pending bookings
```

---

## ⚠️ Notes for Production

- **Passwords** are currently stored as plain text — replace with `werkzeug.security.generate_password_hash` before deploying
- **Secret key** is hardcoded (`'fixitforce'`) — move to an environment variable
- Consider migrating from SQLite to PostgreSQL or MySQL for multi-user deployments

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
