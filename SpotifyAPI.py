import imghdr
import requests
import os
import urllib.request
from PIL import Image
os.system("cls")

# FILE IN WHICH THE ACCESS TOKEN IS
file = open('spotify_access_token.txt', 'r')
access_token = file.read()


artist_name = input("Enter Artist Name: ").replace(' ', '+')

my_headers = {'Authorization': 'Bearer {access_token}'.format(
    access_token=access_token)}
base_url = "https://api.spotify.com/v1/search"
query = '?query='+artist_name
qType = 'type=artist'
limit = 'limit=1'
url = base_url+query+'&'+qType+'&'+limit

# GETTING RESPONSE FOR THE ARTIST ENTERED BY THE USER
art_response = requests.get(url, headers=my_headers)
if(art_response.status_code == 401):
    print('API TOKEN HAS EXPIRED')
    exit()

artist_info = art_response.json()

# ASSIGNING IMPORTANT DATA TO VARIABLES
image_url = artist_info['artists']['items'][0]['images'][0]['url']

image = urllib.request.urlretrieve(image_url, 'prof_image')

img = Image.open('prof_image')
name = artist_info['artists']['items'][0]['name']
spotify_link = artist_info['artists']['items'][0]['external_urls']['spotify']
followers = artist_info['artists']['items'][0]['followers']['total']
genres = artist_info['artists']['items'][0]['genres']
spotify_id = artist_info['artists']['items'][0]['id']

rel_url = 'https://api.spotify.com/v1/artists/{id}/related-artists'.format(  # RESPONSE FOR RELATED ARTISTS
    id=spotify_id)

rel_response = requests.get(rel_url, headers=my_headers)
rel_info = rel_response.json()

top_tracks_url = 'https://api.spotify.com/v1/artists/{id}/top-tracks?market={country}'.format(  # RESPONSE FOR TOP TRACKS
    id=spotify_id, country='IN')
top_tracks_resp = requests.get(top_tracks_url, headers=my_headers)
top_tracks_info = top_tracks_resp.json()

rel_names = []  # LOOP FOR RELATED ARTIST'S NAMES AND FOLLOWERS, AND TOP TRACKS FOR USER ENTERED ARTIST
rel_followers = []
top_tracks = []
for i in range(5):
    rel_names.append(rel_info['artists'][i]['name'])
    rel_followers.append(rel_info['artists'][i]['followers']['total'])
    top_tracks.append(top_tracks_info['tracks'][i]['name'])

img.show()
print('Artist Name: ', name)  # PRINTING EVERYTHING IN A SOMEWHAT NEAT FORMAT
print("Link: ", spotify_link)
print("Followers: ", followers)
print("Genres: ", genres)
print("Spotify ID: ", spotify_id)
print('\n-------TOP TRACKS-------')
for i in range(5):
    print(top_tracks[i])
print('------------------------')
print('\n*****Related Artists*****\n')
for i in range(5):
    print('Name: ', rel_names[i], ' \n\t Followers: ', rel_followers[i])
