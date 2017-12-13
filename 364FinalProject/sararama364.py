import os
import unittest
from flask import Flask, render_template, session, redirect, request, url_for, flash
import requests
import json
from flask_script import Manager, Shell

# New imports were needed for additional stuff for login
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError, RadioField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from threading import Thread


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/sararamaFinal"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.googleemail.com'
app.config['MAIL_PORT'] = 587 #default
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') # TODO export to your environs -- may want a new account just for this. It's expecting gmail, not umich
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = '[Tweet App]' 
app.config['MAIL_SENDER'] = 'Admin <solivia965@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')


manager = Manager(app)
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# mail = Mail(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

login_manager.init_app(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Movie=Movie, Director=Director, Actor=Actor)

manager.add_command("shell", Shell(make_context=make_shell_context))

def send_timely_email(app, message):
	with app.app_context():
		mail.send(message)

def send_email(to, subject, template, **kwargs):
	message = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, send = app.config['MAIL_SENDER'], recipients=[to])
	message.body = render_template(template + '.txt', **kwargs)
	message.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_timely_email, args=[app, message])
	return thr

##Association tables 
## Users and Movies
# usermovies = db.Table('usermovies', db.Column('user_id', db.Integer, db.ForeignKey('users.id')), db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')))

#association Table between songs and playlists
# on_playlist = db.Table('on_playlist',db.Column('user_id', db.Integer, db.ForeignKey('songs.id')),db.Column('playlist_id',db.Integer, db.ForeignKey('playlists.id')))
## Movies and Actors 
moviesactors= db.Table('moviesactors', db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')), db.Column('actor_id', db.Integer, db.ForeignKey('actors.id')))
##name anything you want, just needs to be in secondary , contains association table to rep. many to many between songs and playlists
## whatever name you use for association table is the one that matters in secondary. 
## whatever foreign key should go in one column and the other
## id is unique in songs, and id unique for playlists so we wantin the relationship on_playlist a user_id is one thing we want in every row, and a playlist_id in every row. Want every unique combination of song id and playlist id that exists
## if a song is on a playlist, that song id and that playlist id should go together. there are many unique pairs of song and playlist ids. this is what the association table sets up
## make sure you have db.relationship in one of the models. what in my app is liek songs and playlists? which is the song and which is the playlist? use as model to set up.
## have association table to say "here are the unique pairs that match these two up?"



## Models 
class User(UserMixin, db.Model):
	__tablename__= "users"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255), unique = True, index = True)
	email = db.Column(db.String(64), unique = True, index = True)
	password_hash = db.Column(db.String(128))
	# movies = db.relationship("Movie", secondary = usermovies, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

class Director(db.Model):
	__tablename__ = "directors"
	id = db.Column(db.Integer, primary_key=True )
	name = db.Column(db.String(255))
	movies = db.relationship('Movie', backref = 'Director')
	##association table is backref, ##foreign key is just to connect them on IDs

##If one to many, in the one. if user has many playlists. in that case, each playlist need a user id. so for example, in user, you have playlist= 
##db.relationship(with backref to user), but don't need association table. one to many. insider user model, say" these are all the playlists", in class playlist, 
## eveyr playlist has user id, so use FOREIGN KEY (represents the user_id in playlists we refer to!)

class Actor(db.Model):
	__tablename__ = "actors"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))

class Movie(db.Model):
	__tablename__ = "movies"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))
	# actor_id = db.Column(db.Integer, db.ForeignKey("actors.id"))
	actors = db.relationship("Actor", secondary = moviesactors, backref=db.backref('movies', lazy='dynamic'), lazy='dynamic')
	rating = db.Column(db.String(255))
	## referring to my table 
	year = db.Column(db.String(255))
	viewed = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

	def __repr__(self):
		return "{} with actors: {} and a rating of: {}, made in year:{}. SEEN: {}".format(self.title, self.actors, self.rating, self.year, self.viewed)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


## forms
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class MovieForm(FlaskForm):
	title = StringField("What is the title of the movie?", validators=[Required()])
	director = StringField("Who is the director of the movie?", validators=[Required()])
	year = StringField("What year was this movie released?", validators=[Required()])
	rating = StringField("What was the rating of this movie?", validators=[Required()])
	viewed = RadioField('Have you seen this movie?', choices=[('true', 'true'), ('false', 'false')])
	actors = StringField("Please provide a comma separated list of actors in the movie here:", validators=[Required()])
	submit = SubmitField('Submit')



def get_or_create_director(db_session, director_name):
	director = db_session.query(Director).filter_by(name= director_name).first()
	if director:
		return director
	else:
		print("creating new director in table")
		director = Director(name = director_name)
		db_session.add(director)
		db_session.commit()
		return director

def get_or_create_actor(db_session, actor):
	actor_tuple = db_session.query(Actor).filter_by(name = actor).first()
	if actor_tuple:
		print("returning actor that exists")
		return actor_tuple
	print("creating new actor in table")
	actor_tuple = Actor(name = actor)
	db_session.add(actor_tuple)
	db_session.commit()
	return actor_tuple

def get_or_create_movie(db_session, title, director, year , rating , viewed, current_user, actors_list = [] ):
	movie = db_session.query(Movie).filter_by(title = title, user_id = current_user.id).first()
	if movie:  
		return movie
	else:
		print("creating new movie in table")
		movie = Movie(title = title, year = year, rating = rating, viewed = viewed)
		## ask about 165
		new_director = get_or_create_director(db_session, director)
		movie.director_id = new_director.id
		movie.user_id = current_user.id
		# print(title)
		# print(director)
		# print(year)
		# print(rating)
		# print(viewed)
		# print(actors_list)
		for actor in actors_list:
			actor  = actor.strip()
			actor = get_or_create_actor(db_session, actor)
			movie.actors.append(actor)
			print(actor.id)
			# movie.actor_id.append(actor.id)
		db_session.add(movie)
		db_session.commit()
		return movie


# Need get_or_create_functions here
# do I need a get_or_Create_user function? or does the login take care of this? I think the login takes care of this.
# get_or_create_user NOT necessary
#get_or_Create_movie: call getorcreatedirector and getorcreateactor in this function.
#get_or_Create_director
#get_or_Create_actor


#View Function 1
@app.route('/mainform', methods=['GET', 'POST'])
def mainform():
	movies = Movie.query.all()

	num_movies = len(movies)
	form = MovieForm()
	if form.validate_on_submit():
		if db.session.query(Movie).filter_by(title = form.title.data).first():
			flash("You've already saved that movie. Please enter a different one!")
		else:
			x = form.actors.data
			actors_list = x.split(",")
			print(actors_list)
			get_or_create_movie(db.session, form.title.data, form.director.data, form.year.data, form.rating.data, form.viewed.data, current_user, actors_list)
			return redirect(url_for('see_all_movies'))
	return render_template('mainform.html', form=form, num_movies = num_movies)

#View Function 2
@app.route('/see_all_movies')
def see_all_movies():
	all_movies = []
	# movies = Movie.query.all()
	movies = db.session.query(Movie).filter_by(viewed = "true").all()
	num_movies = len(movies)
	for movie in movies:
		movie_title = movie.title 
		# print(movie_title)
		movie_rating = movie.rating
		# print(movie_rating)
		movie_year = movie.year
		# print(movie_year)
		movie_viewed = movie.viewed
		# print(movie_viewed)
		movie_tuple = movie_title, movie_rating, movie_year, movie_viewed
		all_movies.append(movie_tuple)
		# print(all_movies)
	return render_template('see_all_movies.html', all_movies = all_movies, num_movies = num_movies)

# View Function 3
@app.route('/unseen_movies')
def unseen_movies():
	unseen = []
	movies = db.session.query(Movie).filter_by(viewed = "false").all()
	num_movies = len(movies)
	for movie in movies:
		movie_title = movie.title
		movie_rating = movie.rating
		movie_year = movie.year
		movie_viewed = movie.viewed
		movie_tuple = movie_title, movie_rating, movie_year, movie_viewed, movie_viewed
		unseen.append(movie_tuple)
	return render_template('unseen_movies.html', all_movies = unseen, num_movies = num_movies)

## View Function 4
@app.route('/see_all_directors')
def see_all_directors():
	all_directors = []
	directors = Director.query.all()
	num_directors = len(directors)
	for director in directors:
		director_name = director.name
		director_tuple = director_name
		all_directors.append(director_tuple)
	return render_template('see_all_directors.html', all_directors = all_directors, num_directors = num_directors)

## View Function 5
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



## Controllers, helpers, edit these
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('mainform'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))


@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        congrats = "Congratulations on joining Movie Watcher Lite by Sara Ramaswamy"
        send_email(form.email.data, 'New Account', 'mail/new_account', congrats)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

## Main routes

## Index
## Login or logout

## Main.html
## has the form, query the Movie table, filter by title, and user, call get_or_Creater_user. first()

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."


# @app.route('/movies', methods = ['POST,' 'GET'])
# def hot_movies():
# 	return render_template('hotmoviesform.html')

# @app.route('/movie/<movietitle>', methods = ['POST', 'GET'])
# def hot_movie(movietitle):
# 	if request.method == 'GET' or request.method== 'POST':
# 		result = request.args
# 		params = {}
# 		params['t'] = movietitle
# 		resp = requests.get('http://www.omdbapi.com/?apikey=91f54722&', params = params)
# 		data_return = json.loads(resp.text)
# 		r = json.dumps(data_return, indent = 2)
# 		print(r)
# 		return render_template('hotmovie.html', info = data_return)

## View Function 6
@app.route('/movies', methods = ['POST,' 'GET'])
def hot_movies():
	# return render_template('hotmoviesform.html')
	return "hello"

## View Function 7
@app.route('/movies/<movietitle>', methods = ['POST', 'GET'])
def hot_movie(movietitle):
	if request.method == 'GET':
		result = request.args
		params = {}
		params['t'] = movietitle
		resp = requests.get('http://www.omdbapi.com/?apikey=91f54722&', params = params)
		data_return = json.loads(resp.text)
		r= json.dumps(data_return, indent = 2)

		# params['original_title'] = movietitle
		# resp = requests.get('https://api.themoviedb.org/3/movie/550?api_key=a1340ab54960df121c876f6de730fc2d', params = params)
		# data_return = json.loads(resp.text)
		# r = json.dumps(data_return, indent = 2)
		return render_template('hotmovie.html', info = data_return)

@app.route('/test_route')
def test_route():
	return render_template("hotmoviesform.html")
## to do:
## arguments for the get_or_create functions


##Unit Testing
# class TestCase(unittest.TestCase):
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/sararamaFinal"
#         self.app = app.test_client()
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()





if __name__ == '__main__':
    db.create_all()
    manager.run() # Run with this: python main_app.py runserver
    # Also provides more tools for debuggin



