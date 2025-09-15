import sqlite3


conn = sqlite3.connect('fixitforce.db')
cursor = conn.cursor()

print("=== USERS TABLE ===")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(user)

print("\n=== SERVICES TABLE ===")
cursor.execute("SELECT * FROM services")
services = cursor.fetchall()
for service in services:
    print(service)

print("\n=== BOOKINGS TABLE ===")
cursor.execute("SELECT * FROM bookings")
bookings = cursor.fetchall()
for booking in bookings:
    print(booking)

conn.close()