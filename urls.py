## this includes the Google App Engine framework in our app

import webapp2
import views

urls = [(r'/', views.Home),(r'/[Hh]ome', views.Home),(r'/Delete/(?P<Id>[a-fA-F0-9]+)/?', views.Delete), (r'/addNew', views.AddNew),(r'/addNew/(?P<Id>[a-fA-F0-9]+)/?', views.AddNew), (r'/allReviews', views.GetAllReviews), (r'/postReview', views.PostReview), (r'/Review/(?P<Review>[a-fA-F0-9]+)/?', views.GetReviews),(r'/Review/(?P<Review>[a-fA-F0-9]+)/(?P<Sort>[rt][01])/?', views.GetReviews), (r'/allAlbums', views.GetAllAlbums), (r'/addNewAlbum', views.AddNewAlbum),(r'/addNewAlbum/(?P<Id>[a-fA-F0-9]+)/?', views.AddNewAlbum) , (r'/postAlbum', views.PostAlbum), (r'/Album/(?P<Album>[a-fA-F0-9]+)/?', views.GetAlbums), (r'/addSong/(?P<Album>[a-fA-F0-9]+)/?', views.AddSong), (r'/addSong/(?P<Album>[a-fA-F0-9]+)/(?P<Song>[a-fA-F0-9]+)/?', views.AddSong)]

app = webapp2.WSGIApplication(urls, debug=True)
