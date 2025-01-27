# The Concert class handles operations related to concerts.
import sqlite3

# Connect to the database
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

# Create the tables
cursor.execute('''
CREATE TABLE bands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hometown TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    city TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE concerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_id INTEGER NOT NULL,
    venue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    FOREIGN KEY (band_id) REFERENCES bands (id),
    FOREIGN KEY (venue_id) REFERENCES venues (id)
);
''')

# Define classes
class Band:
    def __init__(self, name, hometown):
        self.name = name
        self.hometown = hometown
        cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", (name, hometown))
        connection.commit()
        self.band_id = cursor.lastrowid

    def play_in_venue(self, venue_title, date, time):
        venue_query = "SELECT id FROM venues WHERE title = ?"
        cursor.execute(venue_query, (venue_title,))
        venue = cursor.fetchone()
        if venue:
            venue_id = venue[0]
            query = "INSERT INTO concerts (band_id, venue_id, date, time) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (self.band_id, venue_id, date, time))
            connection.commit()
        else:
            print(f"Venue '{venue_title}' not found.")

    def all_introductions(self):
        query = """
        SELECT venues.city, bands.name, bands.hometown
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        JOIN venues ON concerts.venue_id = venues.id
        WHERE bands.id = ?
        """
        cursor.execute(query, (self.band_id,))
        concerts = cursor.fetchall()
        introductions = [f"Hello {city}!!!!! We are {self.name} and we're from {self.hometown}" for city, _, _ in concerts]
        return introductions

    @staticmethod
    def most_performances():
        query = """
        SELECT bands.name, COUNT(concerts.id) AS performance_count
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        GROUP BY bands.name
        ORDER BY performance_count DESC
        LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None

class Venue:
    def __init__(self, title, city):
        self.title = title
        self.city = city
        cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", (title, city))
        connection.commit()
        self.venue_id = cursor.lastrowid

    def concert_on(self, date):
        query = """
        SELECT bands.name, venues.city, bands.hometown
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        JOIN venues ON concerts.venue_id = venues.id
        WHERE venues.id = ? AND concerts.date = ?
        LIMIT 1
        """
        cursor.execute(query, (self.venue_id, date))
        concert = cursor.fetchone()
        if concert:
            band_name, city, hometown = concert
            return f"Hello {city}!!!!! We are {band_name} and we're from {hometown}"
        return None

    def most_frequent_band(self):
        query = """
        SELECT bands.name, COUNT(concerts.id) AS performance_count
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.venue_id = ?
        GROUP BY bands.name
        ORDER BY performance_count DESC
        LIMIT 1
        """
        cursor.execute(query, (self.venue_id,))
        result = cursor.fetchone()
        return result[0] if result else None

class Concert:
    @staticmethod
    def hometown_show(concert_id):
        query = """
        SELECT bands.hometown, venues.city
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.id = ?
        """
        cursor.execute(query, (concert_id,))
        result = cursor.fetchone()
        if result:
            hometown, city = result
            return hometown == city
        return False

    @staticmethod
    def introduction(concert_id):
        query = """
        SELECT bands.name, venues.city, bands.hometown
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.id = ?
        """
        cursor.execute(query, (concert_id,))
        result = cursor.fetchone()
        if result:
            band_name, city, hometown = result
            return f"Hello {city}!!!!! We are {band_name} and we're from {hometown}"
        return None

# Testing
# Create bands and venues
band_1 = Band("The Rolling Stones", "London")
band_2 = Band("Metallica", "Los Angeles")

venue_1 = Venue("Madison Square Garden", "New York")
venue_2 = Venue("Stadium Cairo", "Cairo")

# Schedule concerts
band_1.play_in_venue("Madison Square Garden", "2025-04-01", "20:00")
band_1.play_in_venue("Stadium Cairo", "2025-05-01", "18:00")
band_2.play_in_venue("Stadium Cairo", "2025-05-02", "19:00")

# Outputs
print("Band for Concert 1:", band_1.name)
print("Venue for Concert 1:", venue_1.title)
print("Hometown Show:", Concert.hometown_show(1))
print("Introduction:", Concert.introduction(2))
print("Concert on Date:", venue_2.concert_on("2025-05-01"))
print("Most Frequent Band at Stadium Cairo:", venue_2.most_frequent_band())
print("All Introductions for Band 1:", band_1.all_introductions())
print("Band with Most Performances:", Band.most_performances())
