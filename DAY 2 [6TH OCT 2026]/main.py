import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="coworking_demo",
    user="postgres",
    password="Admin@123"
)

cursor = conn.cursor()

print("Connected to PostgreSQL")

cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_id SERIAL PRIMARY KEY,
    room_name TEXT NOT NULL,
    capacity INTEGER,
    hourly_rate DECIMAL,
    status TEXT NOT NULL
)
""")

conn.commit()

print("Table created")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id    INTEGER,
    booked_by TEXT NOT NULL,
    booking_date DATE,
    hours INTEGER,
    FOREIGN KEY(room_id)REFERENCES rooms(room_id)) 
  """)

conn.commit()

print("Table created")



cursor.execute("""
INSERT INTO rooms
(room_name, capacity, hourly_rate, status)
VALUES
('Focus Room', 2, 300, 'Available'),
('Conference Room', 10, 1000, 'Available'),
('Creative Studio', 6, 700, 'Available'),
('Board Room', 15, 1500, 'Available')
""")

conn.commit()

print("Rooms inserted")


cursor.execute("""
INSERT INTO bookings
(room_id, booked_by, booking_date, hours)
VALUES
(1, 'Deepika', '2026-10-07', 2),
(2, 'Rahul', '2026-10-07', 4),
(3, 'Sneha', '2026-10-08', 3),
(4, 'Amit', '2026-10-08', 5),
(1, 'Priya', '2026-10-09', 2),
(2, 'Kiran', '2026-10-09', 6)
""")

conn.commit()

print("Bookings inserted")

#display the rooms table row by row
cursor.execute("SELECT * FROM rooms")

for row in cursor.fetchall():
    print(row)

#display bookings table row by row
cursor.execute("SELECT * FROM bookings")

for row in cursor.fetchall():
    print(row)

print("\nRooms with Capacity > 6")

cursor.execute("""
SELECT *
FROM rooms
WHERE capacity > 6
""")

for row in cursor.fetchall():
    print(row)


print("\nAvailable Rooms")

cursor.execute("""
SELECT *
FROM rooms
WHERE status = 'Available'
""")

for row in cursor.fetchall():
    print(row)


print("\nBookings by Deepika")

cursor.execute("""
SELECT *
FROM bookings
WHERE booked_by = 'Deepika'
""")

for row in cursor.fetchall():
    print(row)