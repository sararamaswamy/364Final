import omdb
import requests
import json
# movie_info = omdb.title("Mean Girls")
# print(movie_info)
# params = {}
# params['t'] = "Argo"
# resp = requests.get('http://www.omdbapi.com/?apikey=91f54722&', params = params)
# data_return = json.loads(resp.text)
# r = json.dumps(data_return, indent = 2)
# print(data_return["Title"])				
# print(data_return['Director'])
# print(data_return['Actors'])
# print(data_return['Year'])
# print(data_return['imdbRating'])

##title
## director
## actors
# year
## rating
##watched 

params = {}
params['original_title'] = "Argo"
resp = requests.get('https://api.themoviedb.org/3/movie/550?api_key=a1340ab54960df121c876f6de730fc2d', params = params)
data_return = json.loads(resp.text)
r = json.dumps(data_return, indent = 2)
print(data_return["original_title"])
print(data_return["overview"])
print(data_return["release_date"])
