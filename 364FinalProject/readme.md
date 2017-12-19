Sara RamaswamySI 364Final Project README *What will this application do?This application will allow users that register for MovieWatcher Lite to keep track of movies that she has seen and not seen, as well as get ideas for movies to see; this app uses data from the omdb API to generate a list of hot_movies that can be viewed by logging in and then clicking on “This week’s hot movies.” The user can see lists of movies she has seen, not seen, and a list of directors stored in the database. *How do I run this application?
Non-local: Use it through Heroku: https://sararama364.herokuapp.com/Locally:1)Start your Postgresql server by running the following command at CLI: 
$ pg_ctl -D /usr/local/var/postgres start



2) Set up database	a.$ createdb sararamaFinal


3) Necessary modules to run the application listed in “requirements.txt.” Pip install each by running at the CLI:	a.$ pip install <module name>.	b.The necessary modules are: gunicorn, Flask, Flask-Bootstrap, Flask-Cors, 	flask-heroku, Flask-Login, Flask-Mail, Flask-Migrate, Flask-Moment, Flask-Script, Flask-SQLAlchemy, Flask-Testing, Flask WTF, pyscop2, itsdangerous, Jinja2, six, speaklater, squlalchemy-migrate, sqlparse, blinker, coverage, decorator, and requests.



4)Configure mail	a.To configure mail, edit app.config[‘ADMIN’] to be your email address to get an email when you enter a new movie into the database.	b.Export your mail credentials at the CLI		i.$ export MAIL_USERNAME=<youremail>		ii.$ echo MAIL_USERNAME			1.this ensures that your email is in the MAIL_USERNAME variable		iii.$ export MAIL_PASSWORD <your password>


5)Run the program at the command line	a.$ python sararama364.py runserver 




6)Either set up an account by registering or log-in using the following credentials to see an example of a populated database	a.Email: solivia965@gmail.com	b.Password: sararamaswamy96



**7)	Start adding movies! You must fll out all fields. 