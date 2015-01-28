## this includes the Google App Engine framework in our app
from google.appengine.ext import db
import webapp2
import models
import os
import jinja2
 
 #including jinja2 templating service
JE = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

#home page window
class Home(webapp2.RequestHandler):
    def get(self):
        template = JE.get_template('templates/index.html')
        self.response.write(template.render())

#Separate song list window        
class GetAllReviews(webapp2.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT DISTINCT artist , title FROM Review")
        template = JE.get_template('templates/songs.html')
        context = { 'reviews': q, }
        self.response.write(template.render(context))
    
#new song review addition
class PostReview(webapp2.RequestHandler):
  def post(self):
    content = self.request.get('content')
    artist = self.request.get('artist')
    title = self.request.get('title')
    rating = self.request.get('rating')
    
    #double checking for empty entries
    if content=="" or content.isspace() or artist=="" or artist.isspace() or title=="" or title.isspace() or int(rating) <1 or int(rating) > 5:
        self.response.write("Empty or faulty input detected. <a href='/addNew'>Try again</a>")
    else:
        Review = models.Review()
        Review.content = content
        Review.artist = artist
        Review.title = title
        Review.rating = int(rating)
        Review.put()
        self.response.write("Added. <a href='/allReviews'>Back to review list</a>")
    
#GetReviews show all the reviews for one particular song
class GetReviews(webapp2.RequestHandler):
    def get(self, Review=None, Sort=None):
        if Review != None:
            firstReview = models.Review.get_by_id(long(Review))
            q = models.Review.all()
            q.filter("artist =", firstReview.artist)
            q.filter("title =", firstReview.title)
            
            #sorting. r - rating, t - time(date), 0 - descending, 1 - ascending
            if Sort=="r0":
                q.order("-rating")
            elif Sort=="t0":
                q.order("-date")
            elif Sort=="r1":
                q.order("rating")
            elif Sort=="t1":
                q.order("date")
                
        template = JE.get_template('templates/reviews.html')
        
        #cumulative average score calculation
        average = 0.0
        counter = 0.0
        for rating in q:
            average = average + rating.rating
            counter += 1.0
        
        if counter>1:
            average = round(average/counter,2)
        #end of calculation
        
        context = { 'reviews': q,}
        self.response.write(template.render(context, average=average))
        
#new song review addition window. Inserts title and artist if one of the same song's id is provided
class AddNew(webapp2.RequestHandler):
    def get(self, Id=None):
        template = JE.get_template('templates/addNew.html')
        if Id != None:
            review = models.Review.get_by_id(long(Id))
            self.response.write(template.render(reviewArtist=review.artist, reviewTitle=review.title))
        else:
            self.response.write(template.render())
    
#Deletes reviews by ids. Does not handle the song lists in albums
class Delete(webapp2.RequestHandler):
    def get(self, Id=None):
        if Id != None:
            review = models.Review.get_by_id(long(Id))
            review.delete()
            self.response.write("Deleted. <a href='/allReviews'>Back to review list</a>")
        else:
            self.response.write("Unable to delete")

#album list window
class GetAllAlbums(webapp2.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT DISTINCT artist , title FROM Album")
        template = JE.get_template('templates/albums.html')
        context = { 'albums': q, }
        self.response.write(template.render(context))

#New album window. Adds the album name if id provided        
class AddNewAlbum(webapp2.RequestHandler):
    def get(self, Id=None):
        template = JE.get_template('templates/addNewAlbum.html')
        if Id != None:
            album = models.Album.get_by_id(long(Id))
            self.response.write(template.render(albumArtist=album.artist, albumTitle=album.title))
        else:
            self.response.write(template.render())
            
#addition of the new album information
class PostAlbum(webapp2.RequestHandler):
  def post(self):
    content = self.request.get('content')
    artist = self.request.get('artist')
    title = self.request.get('title')
    rating = self.request.get('rating')
    
    #double checking for empty entries
    if content=="" or content.isspace() or artist=="" or artist.isspace() or title=="" or title.isspace() or int(rating) <1 or int(rating) > 5:
        self.response.write("Empty or faulty input detected. <a href='/addNewAlbum'>Try again</a>")
    else:
        Album = models.Album()
        Album.content = content
        Album.artist = artist
        Album.title = title
        Album.rating = int(rating)
        Album.put()
        self.response.write("Added. <a href='/allAlbums'>Back to Album list</a>")
        
#GetAlbums gets a list of reviews for a specific album
class GetAlbums(webapp2.RequestHandler):
    def get(self, Album=None):
        #always true unless link manually entered
        if Album != None:
            firstAlbum = models.Album.get_by_id(long(Album))
            q = models.Album.all()
            q.filter("artist =", firstAlbum.artist)
            q.filter("title =", firstAlbum.title)
                
            template = JE.get_template('templates/album.html')
            
            #average calculation
            average = 0.0
            counter = 0.0
            for rating in q:
                average = average + rating.rating
                counter += 1.0
            
            if counter>1:
                average = round(average/counter,2)     
            #end of calculation

            q1 = db.GqlQuery("SELECT DISTINCT songArtist , songTitle FROM AlbumSong WHERE artist = :artist AND title = :title",artist=firstAlbum.artist, title=firstAlbum.title)

            context = { 'albums': q, 'songs':q1,}
            self.response.write(template.render(context, average=average))

#song addition to albums            
class AddSong(webapp2.RequestHandler):
    def get(self, Album=None, Song=None):
        #display the song list
        if Album !=None and Song==None:
            q = db.GqlQuery("SELECT DISTINCT artist , title FROM Review")
            template = JE.get_template('templates/songList.html')
            context = { 'songs': q, }
            self.response.write(template.render(context, albumId=Album))
        
        #add song
        elif Album!=None and Song !=None:
            album = models.Album.get_by_id(long(Album))
            song = models.Review.get_by_id(long(Song)) 

            q = models.AlbumSong.all()
            q.filter("artist = ", album.artist)
            q.filter("title = ", album.title)
            q.filter("songArtist = ", song.artist)
            q.filter("songTitle = ", song.title)
            
            #if q size more than zero then song is already in the album
            counter = 0
            for qs in q:
                counter+=1
            
            if counter <= 0:
                AlbumSong = models.AlbumSong()
                AlbumSong.artist = album.artist
                AlbumSong.title = album.title
                AlbumSong.songArtist = song.artist
                AlbumSong.songTitle = song.title
                AlbumSong.put()
                self.response.write("Added. <a href='/Album/" + Album + "/'>Back to Album</a>")
            else:
                self.response.write("Song already in album. <a href='/Album/" + Album + "/'>Back to Album</a>")
                