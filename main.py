import sqlite3

# The Concert class handles operations related to concerts.
class Concert:
    def __init__(self, concert_id):
        self.concert_id = concert_id

    # Retrieve the band performing at this concert.
    def band(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT bands.id, bands.name, bands.hometown
        FROM bands
        JOIN concerts ON concerts.band_id = bands.id
        WHERE concerts.id = ?;
        """
        cursor.execute(query, (self.concert_id,))
        band = cursor.fetchone()
        connection.close()
        if band:
            return Band(band[0], band[1], band[2])  # Return a Band object.
        else:
            return None

    # Retrieve the venue where this concert is held.
    def venue(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT venues.id, venues.title, venues.city
        FROM venues
        JOIN concerts ON concerts.venue_id = venues.id
        WHERE concerts.id = ?;
        """
        cursor.execute(query, (self.concert_id,))
        venue = cursor.fetchone()
        connection.close()
        if venue:
            return Venue(venue[0], venue[1], venue[2])  # Return a Venue object.
        else:
            return None

    # Check if the concert is a hometown show (band's hometown matches the venue city).
    def hometown_show(self):
        band = self.band()
        venue = self.venue()
        if band and venue:
            return band.hometown == venue.city
        return False

    # Provide an introduction for the concert.
    def introduction(self):
        band = self.band()
        venue = self.venue()
        if band and venue:
            return f"Hello {venue.city}!!!!! We are {band.name} and we're from {band.hometown}"
        return None

# The Band class handles operations related to bands.
class Band:
    def __init__(self, band_id, name, hometown):
        self.band_id = band_id
        self.name = name
        self.hometown = hometown

    # Retrieve all concerts performed by the band.
    def concerts(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT concerts.id, concerts.date, venues.title, venues.city
        FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.band_id = ?;
        """
        cursor.execute(query, (self.band_id,))
        concerts = cursor.fetchall()
        connection.close()
        return [{"concert_id": concert[0], "date": concert[1], "venue": concert[2], "city": concert[3]} for concert in concerts]

    # Retrieve all venues where the band has performed.
    def venues(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT venues.title, venues.city
        FROM venues
        JOIN concerts ON venues.id = concerts.venue_id
        WHERE concerts.band_id = ?;
        """
        cursor.execute(query, (self.band_id,))
        venues = cursor.fetchall()
        connection.close()
        return [{"venue_title": venue[0], "city": venue[1]} for venue in venues]

    # Schedule a performance for the band at a specific venue on a specific date.
    def play_in_venue(self, venue_title, date):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()

        # Get the venue ID based on the title.
        cursor.execute("SELECT id FROM venues WHERE title = ?", (venue_title,))
        venue = cursor.fetchone()
        if venue:
            venue_id = venue[0]
            cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)", (self.band_id, venue_id, date))
            connection.commit()
            connection.close()
            return True
        connection.close()
        return False

    # Provide introductions for all concerts performed by the band.
    def all_introductions(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT venues.city FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.band_id = ?;
        """
        cursor.execute(query, (self.band_id,))
        venues = cursor.fetchall()
        connection.close()
        return [f"Hello {venue[0]}!!!!! We are {self.name} and we're from {self.hometown}" for venue in venues]

    # Find the band that has performed the most concerts.
    @staticmethod
    def most_performances():
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT bands.id, bands.name, COUNT(concerts.id) AS concert_count
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        GROUP BY bands.id
        ORDER BY concert_count DESC LIMIT 1;
        """
        cursor.execute(query)
        band = cursor.fetchone()
        connection.close()
        if band:
            return Band(band[0], band[1], None)
        return None

# The Venue class handles operations related to venues.
class Venue:
    def __init__(self, venue_id, title, city):
        self.venue_id = venue_id
        self.title = title
        self.city = city

    # Retrieve all concerts held at this venue.
    def concerts(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT concerts.id, concerts.date, bands.name, bands.hometown
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.venue_id = ?;
        """
        cursor.execute(query, (self.venue_id,))
        concerts = cursor.fetchall()
        connection.close()
        return [{"concert_id": concert[0], "date": concert[1], "band_name": concert[2], "band_hometown": concert[3]} for concert in concerts]

    # Retrieve all bands that have performed at this venue.
    def bands(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT DISTINCT bands.name, bands.hometown
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        WHERE concerts.venue_id = ?;
        """
        cursor.execute(query, (self.venue_id,))
        bands = cursor.fetchall()
        connection.close()
        return [{"band_name": band[0], "band_hometown": band[1]} for band in bands]

    # Retrieve a concert held at the venue on a specific date.
    def concert_on(self, date):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT * FROM concerts WHERE venue_id = ? AND date = ? LIMIT 1;
        """
        cursor.execute(query, (self.venue_id, date))
        concert = cursor.fetchone()
        connection.close()
        if concert:
            return Concert(concert[0])  # Return a Concert object.
        return None

    # Find the band that has performed the most at this venue.
    def most_frequent_band(self):
        connection = sqlite3.connect('db/concerts.db')
        cursor = connection.cursor()
        query = """
        SELECT bands.id, bands.name, COUNT(concerts.id) AS concert_count
        FROM bands
        JOIN concerts ON bands.id = concerts.band_id
        WHERE concerts.venue_id = ?
        GROUP BY bands.id
        ORDER BY concert_count DESC LIMIT 1;
        """
        cursor.execute(query, (self.venue_id,))
        band = cursor.fetchone()
        connection.close()
        if band:
            return Band(band[0], band[1], None)
        return None

# Test the methods
# This function sets up some test data and demonstrates the methods in the classes.
def test_methods():
    connection = sqlite3.connect('db/concerts.db')
    cursor = connection.cursor()

    # Inserting bands
    cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", ('The Rolling Stones', 'London'))
    cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", ('Metallica', 'Los Angeles'))

    # Inserting venues
    cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", ('Madison Square Garden', 'New York'))
    cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", ('The O2 Arena', 'London'))

    # Inserting concerts
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)", (1, 1, '2025-05-01'))
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)", (2, 2, '2025-06-10'))

    connection.commit()

    # Test methods
    band1 = Band(1, "The Rolling Stones", "London")
    venue1 = Venue(1, "Madison Square Garden", "New York")
    concert1 = Concert(1)

    # Print the actual band name for Concert 1
    print("Band for Concert 1:", concert1.band().name)  

    # Print the actual venue title for Concert 1
    print("Venue for Concert 1:", concert1.venue().title)  

    # Test hometown show (True/False)
    print("Hometown Show?", concert1.hometown_show())  

    # Band introduction for Concert 1
    print("Band Introduction:", concert1.introduction())  

    # All venues for band1
    print("Venues for Band:", band1.venues())  

    # All concerts for band1
    print("All Concerts for Band:", band1.concerts())  

    # All bands for venue1
    print("Bands for Venue:", venue1.bands())  

test_methods()