import os
from flask.ext.testing import TestCase
from flask_testing import LiveServerTestCase
from flask import Flask, render_template, session, redirect, request, url_for, flash
import unittest
import tempfile
import urllib.request
from flask import current_app
from sararama364 import app, db, mail
from sararama364 import User
from sararama364 import Movie
from sararama364 import Director
from sararama364 import Actor
from sararama364 import get_or_create_movie 
from sararama364 import get_or_create_actor
from sararama364 import get_or_create_director

print("hello")
class TestCase(LiveServerTestCase):

	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['LIVESERVER_PORT'] = 8943
		app.config['LIVESERVER_TIMEOUT'] = 10
		return app

	def test_server_up(self):
		response = urllib.request.urlopen(self.get_server_url())
		self.assertEqual(response.code, 200)


	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/test364db"
		db.create_all()

    #     ## include create test db in readme
    #     self.app = app.test_client()
    #     print("hello")
    #     ## export_flask_app = 
    #     user1 = User(username = "sararama", email = "solivia965@gmail.com", password = "123")

    #     get_or_create_movie(db.session, "Frozen", "Steven S", "2016", "6", "True", current_user = user1, actors_list = ["Emma", "Watson"])
    #     # try:

        # 	movie = Movie()
        # 	movie_tup = []
        # 	movie.title = "Frozen"
        # 	movie.year = "2016"

        # 	movie.rating = "6"

        # 	movie.viewed = "True"
        # 	db.session.add(movie)
        # 	db.session.commit()
        # except:
        # 	db.session.rollback()

        ## mini app (nistance of a flask app)
        ## create all tables, could do db.createall and then movie = Movie with all the stuff, db session, add movie, db sesison commit.
        ## in setup, adding one movie. 


## test helper functions

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_movie_len(self):
		x = Movie.query.all()
		self.assertEqual(len(x), 0)

    # def test_movie_len(self):
    # 	x = Movie.query.all()
    # 	self.assertEqual(len(x), 1)


    # ## get_or_Creates. if you put in same info, and query all movies, is length 1, then add a different 1 and length should be more than 1
    # ## does it have the right effect?

    # def test_valid_registration(self):
    # 	r1 = RegistrationForm():
    # 	r1.password = "hello!"
    # 	self.assertEqual()





    	## runs at the tne end always. if test fails, remove the instance 
    	## users typing in thing
    	## sillenium 
    # def test_main_html_renders(self):
    # 	d = self.app.get('/mainform')
    # 	assert b"Welcome" in d.data

    # # def login(self, username, password):
    # # 	return self.app.post('/login', data=dict(username=username, password=password), follow_redirects = True)
    # # def logout(self):
    # # 	return self.app.get('/logout,', follow_redirects = True)



    # def test_main_wtform_renders(self):
    # 	d = self.app.get('/mainform')
    # 	assert b"This week's hot movies" in d.data


    # def test_app_exists(self):
    # 	self.assertTrue(current_app is not None
    # 		)




## ides for testing and how 

#1
##passwords not the same
#2
##app exists
#3
##passwords contain only letters and numbers 
#4
## no two password hashes are the same
#5
## test that if the movie exists in database that they get this error back
#6
## test that if 
#7
#8
    # def test_mainform(self):
    # 	response = self.app.get('/mainform', follow_redirects = True)
    # 	self.assertEqual(response.status_code, 200)







if __name__ == '__main__':
	unittest.main()
# Run with this: python main_app.py runserver
    # Also provides more tools for debuggin


