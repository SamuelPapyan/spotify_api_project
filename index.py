import requests
import json
import pandas as pd

# Pandas-ի օպցիաների կարգավորում (արտածել մաքսիմալ քանակով սյուներով և տողերով)
pd.set_option("display.max_rows", None, "display.max_columns", None)

# SpotifyAPI դասը
class SpotifyAPI:
  # Spotify API Client ID
  CLIENT_ID = '412d43b5726641bd8dffc916ec9b7751'
  # Spotify API Client Secret
  CLIENT_SECRET = 'e2a821211e824ced829641ef46c5e504'
  
  # Spotify API Auth URL
  AUTH_URL = 'https://accounts.spotify.com/api/token'
  # Spotify  API-ի հարցումների հետ աշխատելու սկզբնակետը
  BASE_URL = 'https://api.spotify.com/v1/'

  # Spotify API Auth response
  auth_response = requests.post(AUTH_URL,{
      'grant_type' : 'client_credentials',
      'client_id': CLIENT_ID,
      'client_secret' : CLIENT_SECRET
  })

  # Spotify API Auth Response Data
  auth_response_data = auth_response.json()
  # Access Token
  access_token = auth_response_data['access_token']

  # Headers
  headers = {
      'Authorization': 'Bearer {token}'.format(token=access_token)
  }

  # Ստանալ երգի տվյալները
  def get_track(self,id):
    r = requests.get(SpotifyAPI.BASE_URL + 'tracks/' + id, headers=SpotifyAPI.headers)
    r = r.json()
    return r

  # Ստանալ ալբոմի երգերի տվյալները
  def get_album_tracks(self,id):
    r = requests.get(SpotifyAPI.BASE_URL + 'albums/' + id + '/tracks?limit=30',headers=SpotifyAPI.headers)
    r = r.json()
    return r

  # Ստանալ ալբոմի տվյալները
  def get_album(self,id):
    r = requests.get(SpotifyAPI.BASE_URL + 'albums/' + id,headers=SpotifyAPI.headers)
    r = r.json()
    return r

  # Ստանալ երաժշտի ալբոմնեիր տվյալները
  def get_artist_albums(self,id):
    r = requests.get(SpotifyAPI.BASE_URL + 'artists/' + id + '/albums',headers=SpotifyAPI.headers)
    r = r.json()
    return r

  # Ստանալ երաժշտի տվյալները
  def get_artist(self,id):
    r = requests.get(SpotifyAPI.BASE_URL + 'artists/' + id,headers=SpotifyAPI.headers)
    r = r.json()
    return r

  # Արտածել ալբոմի երգերի ցուցակը
  def display_albums_track(self,album):
    artists_list = [artist["name"] for artist in album["artists"]]
    print(" & ".join(artists_list), end= " - ")
    print(album["name"])
    print("---------------------------")
    for item in album["tracks"]["items"]:
      artists_list = [artist["name"] for artist in item["artists"]]
      print(item["track_number"],end=". ")
      print(" & ".join(artists_list), end= " - ")
      print("{music_name}".format(music_no = item["track_number"],music_name = item["name"]))

  # Որոնել երաժիշտները
  def search_artist(self,search_query):
    r = requests.get(SpotifyAPI.BASE_URL + 'search?q=' + search_query +'&type=artist',headers=SpotifyAPI.headers)
    r = r.json()
    return r
  
  # Որոնել ալբոմները
  def search_album(self,search_query):
    r = requests.get(SpotifyAPI.BASE_URL + 'search?q=' + search_query +'&type=album',headers=SpotifyAPI.headers)
    r = r.json()
    return r

  # Որոնել երգերը
  def search_track(self,search_query):
    r = requests.get(SpotifyAPI.BASE_URL + 'search?q=' + search_query +'&type=track',headers=SpotifyAPI.headers)
    print(r)
    r = r.json()
    return r

# UI (Օգտռագործողի Տեսարան) դասը
class UI:
  # Կոնստրուկտորը
  def __init__(self):
    # SpotifyAPI օբյեկտը
    self._spotifyAPI = SpotifyAPI()
    print("----------------------------------------------")
    print("Welcome to Samvel Papyan's Project Spotify API")
    print("           Enjoy the world of music           ")
    print("----------------------------------------------")
    self.instruction_case_1()

  # Դասակարգիչների ընտրման ցանկ
  def instruction_case_1(self):
    print("Enter 'artist' for search artists")
    print("Enter 'album' for search albums")
    print("Enter 'track' for search tracks")
    print("Enter 'exit' for exit")
    try:
      my_input = input()
      if not my_input in ['artist','album','track','exit']:
        raise Exception()
      self.check_input(my_input)
    except:
      print("Wrong input, try again.")
      self.instruction_case_1()
    
  # Ցուցակի ստուգում
  def check_input(self, my_input):
    if my_input == 'artist':
      self.search_artist()
    if my_input == 'album':
      self.search_album()
    if my_input == 'track':
      self.search_track()
    if my_input == 'exit':
      print("Good Bye!")

  # Երաժշտի որոնում
  def search_artist(self):
    search_query = input("Search: ")
    search_results = self._spotifyAPI.search_artist(search_query)
    my_data = {
        'Artist Name':[x["name"] for x in search_results["artists"]["items"]],
        'Artist ID':[x["id"] for x in search_results["artists"]["items"]]
    }
    print(pd.DataFrame(data=my_data))
    print("--------------------------------------")
    print("Enter number of artist for select the artist")
    print("Enter 'search' for search another artist")
    print("Enter 'home' for back to the main session")
    my_input = input()
    try:
      if my_input == 'search':
        print("--------------------------------------")
        self.search_artist()
        return
      elif my_input == 'home':
        print("--------------------------------------")
        self.instruction_case_1()
      else:
        number = int(my_input)
        if not number in range(0,20):
          raise Exception()
        artist_data = self._spotifyAPI.get_artist(my_data['Artist ID'][number])
        self.get_artist(artist_data)
    except:
      print("Wrong input, try again!")
      self.search_artist()
  
  # Ալբոմի որոնում
  def search_album(self):
    search_query = input("Search: ")
    search_results = self._spotifyAPI.search_album(search_query)
    my_data = {
      'Artist_Name':[x["artists"][0]["name"] for x in search_results["albums"]["items"]],
      'Album ID':[x["id"] for x in search_results["albums"]["items"]],
      'Album_name':[x["name"] for x in search_results["albums"]["items"]],
      'Release Date':[x["release_date"] for x in search_results["albums"]["items"]]
    }
    print(pd.DataFrame(data=my_data))
    print("--------------------------------------")
    print("Enter number of album for select the album")
    print("Enter 'search' for search another album")
    print("Enter 'home' for back to the main session")
    my_input = input()
    try:
      if my_input == 'search':
        print("--------------------------------------")
        self.search_album()
        return
      elif my_input == 'home':
        print("--------------------------------------")
        self.instruction_case_1()
      else:
        number = int(my_input)
        if not number in range(0,20):
          raise Exception()
        album_data = self._spotifyAPI.get_album(my_data['Album ID'][number])
        self.get_album(album_data)
    except:
      print("Wrong input, try again!")
      self.search_album()

  # Երգերի որոնում
  def search_track(self):
    search_query = input("Search: ")
    print(search_query)
    search_results = self._spotifyAPI.search_track(search_query)
    my_data = {
        'Track Name':[x["name"] for x in search_results["tracks"]["items"]],
        'Artist Name':[x["artists"][0]["name"] for x in search_results["tracks"]["items"]],
        'Track ID':[x["id"] for x in search_results["tracks"]["items"]],
        'Release Date':[x["release_date"] for x in search_results["tracks"]["items"]]
    }
    print(pd.DataFrame(data=my_data))
    print("--------------------------------------")
    print("Enter number of track for select the track")
    print("Enter 'search' for search another track")
    print("Enter 'home' for back to the main session")
    my_input = input()
    try:
      if my_input == 'search':
        print("--------------------------------------")
        self.search_track()
        return
      elif my_input == 'home':
        print("--------------------------------------")
        self.instruction_case_1()
      else:
        number = int(my_input)
        if not number in range(0,20):
          raise Exception()
        track_data = self._spotifyAPI.get_track(my_data['Track ID'][number])
        self.get_track(track_data)
    except:
      print("Wrong input, try again!")
      self.search_track()

  # Երգի տվյալների ստացում
  def get_track(self,track_data):
    print("------------------------------------------")
    artists = [x["name"] for x in track_data["artists"]]
    print(' & '.join(artists),end=" - ")
    print(track_data["name"], end=" - ")
    print(track_data["id"])
    print("------------------------------------------")
    print("Enter 'back' to back to search")
    print("Enter 'home' to back to main menu")
    my_input = input()
    try:
      if my_input == 'home':
        print("--------------------------------------")
        self.instruction_case_1()
        return
      elif my_input == 'back':
        print("--------------------------------------")
        self.search_track()
        return
      else:
        raise Exception()
    except:
      print("Wrong input, try again!")
      self.get_track(track_data)

  # Երաժշտի տվյալների ստացում
  def get_artist(self,artist_data):
    print("------------------------------------------")
    print(artist_data["name"], end=" - ")
    print(artist_data["id"])
    print("------------------------------------------")
    print("Enter 'back' to back to search")
    print("Enter 'home' to back to main menu")
    my_input = input()
    try:
      if my_input == 'home':
        print("--------------------------------------")
        self.instruction_case_1()
        return
      elif my_input == 'back':
        print("--------------------------------------")
        self.search_track()
        return
      else:
        raise Exception()
    except:
      print("Wrong input, try again!")
      self.get_artist(artist_data)

  # Ալբոմի տվյալների ստացում
  def get_album(self,album_data):
    print("------------------------------------------")
    self._spotifyAPI.display_albums_track(album_data)
    print("------------------------------------------")
    print("Enter 'back' to back to search")
    print("Enter 'home' to back to ")
    my_input = input()
    try:
      if my_input == 'home':
        print("--------------------------------------")
        self.instruction_case_1()
        return
      elif my_input == 'back':
        print("--------------------------------------")
        self.search_track()
        return
      else:
        raise Exception()
    except:
      print("Wrong input, try again!")
      self.get_album(album_data)


# UI դասի օբյեկտ (ծրագրի սկիզբ)
UI()
