##models.py
##
## This file describes the data model of the reviewing system.

from google.appengine.ext import db
    
class Album(db.Model):
    date = db.DateTimeProperty(auto_now=True)
    content = db.StringProperty(multiline=True)
    artist = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    rating = db.IntegerProperty()
    
class Review(db.Model):
    date = db.DateTimeProperty(auto_now=True)
    content = db.StringProperty(multiline=True)
    artist = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    rating = db.IntegerProperty()

class AlbumSong(db.Model):
    artist = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    songArtist = db.StringProperty(multiline=False)
    songTitle = db.StringProperty(multiline=False)
