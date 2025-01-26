Concert Management System 
This project is a Python-based system for managing concerts, bands, and venues using an SQLite database. The system allows users to track information about concerts, bands, and venues, as well as perform various operations like retrieving details, checking hometown shows, and scheduling performances.

Features 
Concert Operations:

Retrieve the band performing at a specific concert.
Retrieve the venue hosting the concert.
Check if the concert is a hometown show.
Get an introduction for the concert.
Band Operations:

List all concerts performed by a band.
List all venues where the band has performed.
Schedule a performance for the band.
Generate introductions for all concerts performed by the band.
Identify the band with the most performances.
Venue Operations:

List all concerts held at a venue.
List all bands that have performed at the venue.
Find concerts at the venue on a specific date.
Identify the band that has performed the most at the venue.
Project Structure 
Concert Class: Handles operations related to concerts, such as retrieving the band or venue, checking if a concert is a hometown show, and providing introductions.

Band Class: Manages operations related to bands, such as listing concerts and venues, scheduling performances, and identifying the most active band.

Venue Class: Manages operations related to venues, such as listing concerts and bands, retrieving specific concerts, and finding the most frequent band.

Database Schema 
The project uses an SQLite database named concerts.db, which includes the following tables:

bands: Stores band details (id, name, hometown).
venues: Stores venue details (id, title, city).
concerts: Stores concert details (id, band_id, venue_id, date).

Setup 
Prerequisites
Python 3.x
SQLite3
Author
leimila mitei