
from __future__ import print_function
import argparse
import pprint
import requests
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
import sqlite3
import csv
import re
import requests
import json
from bs4 import BeautifulSoup
import urllib
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from secrets import google_places_key
from secrets import *
from secrets import PLOTLY_USERNAME
from secrets import PLOTLY_API_KEY
from secrets import API_KEY
from secrets import api_key




plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


CACHE_FNAME = "SI507finalproject_cache.json" # for long term memory
CACHE_DICTION = {}


try:
    f = open(CACHE_FNAME, 'r')
    fstr = f.read()
    f.close()
    CACHE_DICTION = json.loads(fstr)
    print("using caching")
except:
    CACHE_DICTION = {}
    print("can not find data from caching")


DEFAULT_TERM = 'restaurants'
DEFAULT_LOCATION = 'Ann Arbor'
SEARCH_LIMIT = 50

headers = {"User-Agent": "hoge"}


def get_unique_key(url):
    return url


def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    #print(type(CACHE_DICTION))
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        #print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url,timeout=5, headers=headers)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[str(unique_ident)]



def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    #print(url_params)
    url = '{0}{1}'.format(host, quote(path.encode('utf8'))) # ？
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    #print("this is header")
    #print(headers)
    print(u'Querying {0} ...'.format(url + "?"))
    print("this is url ")
    #print(url)
    #baseurl = API_HOST + SEARCH_PATH
    print(url + "?")
    unique_ident = params_unique_combination(url + "?" , url_params,private_keys=API_KEY) #unique_ident is url
    #return make_request_using_cache(unique_ident)
    print("this is unique_ident")
    #p(unique_ident)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("can not find so searching ")
        #p("this is request")
        #print(request('GET', url, headers=headers, params=url_params)
        response = requests.request('GET',url+"?",headers=headers,params=url_params)
        #print(response)
        CACHE_DICTION[unique_ident] = response.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]





def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }

    print("this is url_params")
    print(url_params)
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

# the dictionary of information about restuarant

#url_params = params_d

def params_unique_combination(url, url_params,private_keys=API_KEY):
    alphabetized_keys = sorted(url_params.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}={}".format(k, url_params[k]))
    return url + "&".join(res)

#http://api.yelp.com/v2/search/?term=dinner&limit=3&location=San+Francisco%2C+CA
#https://api.yelp.com/v3/businesses/search/limit-50_location-New+York+City_term-restaurants


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """

    response = search(API_KEY, term, location)
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)



#tyring to save the data that I got in DB

DBNAME = 'restaurant.db'
conn = sqlite3.connect('restaurant.db')
cur = conn.cursor()

url = "https://travel.usnews.com/rankings/best-usa-vacations/"


url2 = "https://travel.usnews.com/rankings/best-usa-vacations/"

#baseurl2 = "https://www.si.umich.edu"

#resp = requests.get(URL, timeout=1, headers=headers)

page_text = make_request_using_cache(url2)
page_soup = BeautifulSoup(page_text, 'html.parser')

content_search = page_soup.find(class_="search-app-matches-layout-view busy-content")
content_search2 = page_soup.find_all(class_='ranking-element row collapse block-looser rank-voting-item')


list_famouse_places = []
for i in content_search2:
    s = i.find(class_ = "small-12 medium-7 column")
    place = s.find("a")["href"]
    if place != "/Grand_Teton_National_Park_WY/":
        list_famouse_places.append(place)


#print("this is list_famouse_places")
#print(list_famouse_places)


list_url_hotels= []

for i in content_search2:
    t= i.find(class_ = "small-12 medium-7 column")
    tt= t.find(class_="promo-links block-flush text-small show-for-medium-up")
    ttt = tt.find("a")["href"]
    hotel_url = "https://travel.usnews.com/" + str(ttt)
    #print(hotel_url)
    list_url_hotels.append(hotel_url)



list_things_to_do_url = []
for i in list_famouse_places:
    thingstodo_url = "https://travel.usnews.com/"+str(i)+ "/Things_To_Do/"
    list_things_to_do_url.append(thingstodo_url)


#print("this is list_things_to_do_url")
#print(list_things_to_do_url)

def get_thingstodo_infor(thingstodo_url = "https://travel.usnews.com//Yellowstone_National_Park_WY/Things_To_Do/"):
    list_things_to_do = []
    page_text__thingtodo = make_request_using_cache(thingstodo_url)
    page_soup__thingtodo = BeautifulSoup(page_text__thingtodo, 'html.parser')
    content_search_thingtodo = page_soup__thingtodo.find_all(id="things-to-do")
    name_content_search_thingtodo = content_search_thingtodo[0]
    #print("this is length ")
    #print(len(name_content_search_thingtodo))
    name_content_search_thingtodo2 =name_content_search_thingtodo.find_all("h2")

    for i in name_content_search_thingtodo2:
        #print(type(i))
        s = i.text
        #print(s)
        s = s.replace('\n','')
        s= s.replace("1",'')
        s= s.replace("2",'')
        s = s.replace("3",'')
        s= s.replace("4",'')
        s= s.replace("5",'')
        s = s.replace("6",'')
        s = s.replace("7",'')
        s = s.replace("8",'')
        s = s.replace("9",'')
        s = s.replace("0",'')
        s = s.replace("Free",'')
        s = s.replace("#",' ')
        s = s.strip(" ")
        #s = s.replace(" ","")
        #print(s)
        list_things_to_do.append(s)

    #print(len(list_things_to_do))
    return(list_things_to_do)

#print("this is get_thingstodo_infor")
#print(get_thingstodo_infor(thingstodo_url = "https://travel.usnews.com//Yellowstone_National_Park_WY//Things_To_Do/"))


def get_hotel_name(url_hotel):
    try:
        #url_hotel = "https://travel.usnews.com/Hotels/Yellowstone_National_Park_WY/"
        page_text_hotels = make_request_using_cache(url_hotel)
        page_soup_hotels = BeautifulSoup(page_text_hotels, 'html.parser')
        #print(page_soup_hotels)
        content_search_hotel = page_soup_hotels.find(class_="jpvx17-0-Box-cwadsP gAvbWw")

        #print(content_search_hotel)
        list_hotel_name= []
        content_search_hotel2 = content_search_hotel.find_all("li")
        for i in content_search_hotel2:
            hotel_name = i.find(class_ = "SimpleMultilineEllipsis-moilf2-0 kwOvSF Box-jpvx17-0 fHWjtU").text
            list_hotel_name.append(hotel_name)
        return list_hotel_name
    except:
        return("error : this is url_hotel" + str(url_hotel))

#print("this is get hote name ")
#print(get_hotel_name(url_hotel = "https://travel.usnews.com//Hotels/Monterey_CA/"))
#https://travel.usnews.com//Hotels/Miami_FL/　まる
#
#https://travel.usnews.com//Hotels/Monterey_CA/　まる
#https://travel.usnews.com//Hotels/Grand_Teton_National_Park_WY/ ばつ

list_all_infor = []
for famous_palce,urhotel,things_to_do_url in zip(list_famouse_places,list_url_hotels,list_things_to_do_url):
    list_all_infor.append(zip(famous_palce,urhotel,things_to_do_url))

#print(list_all_infor)


#here

list_famouse_places_replace = []
for i in list_famouse_places:
    replace = i.replace("/","")
    list_famouse_places_replace.append(replace)

    #print(i)
#print("this is list_famouse_places_replace")

#rint(list_famouse_places_replace)


#for i in list_famouse_places_replace:
    #try:
        #print(create_each_place_db(each_famous_place=i))
    #except:
        #print("erros in "+str(i))

list_famouse_places_location = []
for i in list_famouse_places_replace:
    replace = i.replace("_"," ")
    if len(replace.split()) > 2:
        tempo_word = replace.split()[0] + str(" ")+ replace.split()[1]
        list_famouse_places_location.append(tempo_word)
    else:
        list_famouse_places_location.append(replace)

#print("this is list_famouse_places_location")
#print(list_famouse_places_location)

#print(create_each_place_db(each_famous_place = "Lake_Tahoe_CA"))

#print(create_each_place_db(each_famous_place = "Grand_Teton_National_Park_WY"))
#print(create_each_place_db(each_famous_place = "Miami_FL"))

#print(create_each_place_db(each_famous_place = "Monterey_CA"))

def get_places_for_site(site): #taking a site and return a latituide and a longitude
    try:

        # use api key for google from secret.py

        # url variable store url
        url2 = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        # The text string on which to search
        radius = "2"
        # get method of requests module
        # return response object
        unique_ident = url2 + 'query=' + site +"&radius="+radius+ "&key=" + api_key

        x = make_request_using_cache(unique_ident)
        #print("this is x")
        #print(type(x))
        x_json = json.loads(x)

        result_location = x_json["results"][0]["geometry"]["location"]
        result_lat = str(result_location["lat"])
        result_lng = str(result_location["lng"])
        #print(result_lat)
        #print(result_lng)
        location = result_lat,result_lng
        return (location)

    except:
        return("error in " + str(site))


#print("get_places_for_site(site = Obsidian Dining Room")
#print(get_places_for_site(site = "Obsidian Dining Room"))

def get_places_for_site_latitude(site): #taking a site and return a latituide and a longitude

    try:

        # use api key for google from secret.py
        # url variable store url
        url2 = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        # The text string on which to search
        radius = "2"
        # get method of requests module
        # return response object
        unique_ident = url2 + 'query=' + site +"&radius="+radius+ "&key=" + api_key

        x = make_request_using_cache(unique_ident)
        #print("this is x")
        #print(type(x))
        x_json = json.loads(x)

        result_location = x_json["results"][0]["geometry"]["location"]
        result_lat = str(result_location["lat"])
        result_lng = str(result_location["lng"])
        #print(result_lat)
        #print(result_lng)

        return (result_lat)
    except:
        print("error in " + str(site))


#print("get_places_for_site_latitude")

#get_places_for_site_latitude(site = "     Central Park     ")

def get_places_for_site_lng(site): #taking a site and return a latituide and a longitude
    try:

        # use api key for google from secret.py
        # url variable store url
        url2 = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        # The text string on which to search
        radius = "2"
        # get method of requests module
        # return response object
        unique_ident = url2 + 'query=' + site +"&radius="+radius+ "&key=" + api_key

        x = make_request_using_cache(unique_ident)
        #print("this is x")
        #print(type(x))
        x_json = json.loads(x)

        result_location = x_json["results"][0]["geometry"]["location"]
        result_lat = str(result_location["lat"])
        result_lng = str(result_location["lng"])
        #print(result_lat)
        #print(result_lng)

        return (result_lng)

    except:
        print("error in " + str(site))




def create_places_db():
    statement = '''
    DROP TABLE IF EXISTS 'Places';
    '''
    cur.execute(statement)
    data_places = []
    #o = open("SI507finalproject_cache2.json")
    #load_places  = json.load(o)
    #print(load_places)
    #load_restaurant2 = load_restaurant["https://api.yelp.com/v3/businesses/search"]["businesses"]
    zip_row  = zip(list_famouse_places_location,list_url_hotels,list_things_to_do_url)
    count = 0
    for famous_palce,urhotel,things_to_do_url in zip_row:
        count = count +1
        data_place_row = []
        #print(load_country.index(row))
        #data_place_row.append(zip_row.index(famous_palce)+1)
        data_place_row.append(count)
        data_place_row.append(famous_palce.replace('/',''))
        data_place_row.append(get_places_for_site_latitude(site = famous_palce))
        data_place_row.append(get_places_for_site_lng(site = famous_palce))
        data_place_row.append(urhotel)
        data_place_row.append(things_to_do_url)
        data_places.append(data_place_row)
    #print("this is data_counrty[4]")
    #print(data_country[4])
    #print("this is data_places")
    #print(data_places)

    statement = '''
            CREATE TABLE 'Places' (
                'number' INTEGER PRIMARY KEY AUTOINCREMENT,
                'famous_place' TEXT NOT NULL,
                'famous_place_latitude' TEXT NOT NULL,
                'famous_place_lng' TEXT NOT NULL,
                'nearbyhotel_URL' TEXT NOT NULL,
                'things_to_do' TEXT NOT NULL
            );
        '''

    cur.execute(statement)
    for inst in data_places:
        insertion = (inst[0], inst[1], inst[2], inst[3], inst[4], inst[5])
        print(insertion)
        statement = 'INSERT INTO "Places"'
        statement += 'VALUES (?, ?, ?, ?, ?, ?)'

        cur.execute(statement,insertion)
        conn.commit()
    pass

#print(create_places_db())

def create_each_place_db(each_famous_place):
    data_restaurant = []
    search_dic =json.loads(search(API_KEY, DEFAULT_TERM, location = each_famous_place))
    print(type(search_dic))
    load_restaurant2 = search_dic["businesses"]
    #creating data base for each famoius place to get info about hotels, adress and so on
    thingstodo_url = "https://travel.usnews.com/"+ str(each_famous_place) + "/Things_To_Do/"
    hotel_url = "https://travel.usnews.com/Hotels/" + str(each_famous_place)
    list_hotels_names = get_hotel_name(hotel_url)
    list_things_to_do = get_thingstodo_infor(thingstodo_url)
    #print("list_things_to_do")
    #print(list_things_to_do)

    statement = "DROP TABLE IF EXISTS " +str(each_famous_place) + "; "
    cur.execute(statement)
    data_places_infor = []
    #o = open("SI507finalproject_cache2.json")
    #load_places  = json.load(o)
    #print(load_places)
    #load_restaurant2 = load_restaurant["https://api.yelp.com/v3/businesses/search"]["businesses"]
    #get_places_for_site(site)
    print("lengh of list_hotels_names ")
    print(len(list_hotels_names))
    print("lengh of list_things_to_do ")
    print(len(list_things_to_do))
    print("lengh of load_restaurant2 ")
    print(len(load_restaurant2))
    while len(list_hotels_names)< 50:
        list_hotels_names.append("")
    while len(list_things_to_do)< 50:
        list_things_to_do.append("")
    while len(load_restaurant2)< 50:
        load_restaurant2.append("")

    print("lengh of list_hotels_names ")
    print(len(list_hotels_names))
    print("lengh of list_things_to_do ")
    print(len(list_things_to_do))
    print("lengh of load_restaurant2 ")
    print(len(load_restaurant2))

    zip_row  = zip(list_hotels_names,list_things_to_do,load_restaurant2)
    #print("lengh of zip_row ")
    #print(len(zip_row))
    count = 0
    for hotel,things,rest in zip_row:
        count = count +1
        data_place_row = []
        #print(load_country.index(row))
        #data_place_row.append(zip_row.index(famous_palce)+1)
        try:
            data_place_row.append(count)
            data_place_row.append(hotel)
            data_place_row.append(get_places_for_site_latitude(site = hotel))
            data_place_row.append(get_places_for_site_lng(site = hotel))
        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
        try:
            data_place_row.append(count)
            data_place_row.append(things)
            data_place_row.append(get_places_for_site_latitude(site = things))
            data_place_row.append(get_places_for_site_lng(site = things))
        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")

        try:

            data_place_row.append(count)
            data_place_row.append(rest["id"])
            data_place_row.append(rest["alias"])
            data_place_row.append(rest["name"])
            data_place_row.append(rest["image_url"])
            data_place_row.append(rest["is_closed"])
            data_place_row.append(rest["url"])
            data_place_row.append(rest["review_count"])
            data_place_row.append(rest["rating"])
            location = ""
            location = location + str(rest["location"]['address1'])
            location = location + str(rest["location"]['address2'])
            location = location + str(rest["location"]['address3'])
            location = location + str(rest["location"]['city'])
            location = location + str(rest["location"]['zip_code'])
            location = location + str(rest["location"]['country'])
            location = location + str(rest["location"]['state'])
            #print("this is location")
            #print(location)
            data_place_row.append(location)
            data_place_row.append(rest["phone"])
            data_place_row.append(rest["distance"])

        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")

        data_places_infor.append(data_place_row)

    #print("this is count")
    #print(count)
    print(data_places_infor)

    statement = "CREATE TABLE " +  str(each_famous_place) + " ('hotel_number' INTEGER PRIMARY KEY AUTOINCREMENT,'hotels' TEXT NOT NULL,'hotel_latitude' TEXT,'hotel_longtude' TEXT ,'things_to_do_number' INTEGER, 'things_to_do' TEXT NOT NULL,'things_to_do_latitude' TEXT , 'things_to_do_longtide' TEXT,'rest_number' INTEGER, 'rest_id' TEXT NOT NULL,'rest_alias' TEXT NOT NULL,'rest_name' TEXT NOT NULL,'rest_image_url' TEXT NOT NULL,'rest_is_closed' TEXT NOT NULL,'rest_url' TEXT NOT NULL,'rest_review_count' INTEGER NOT NULL, "
    statement += " 'rest_rating' Float NOT NULL,'rest_location' TEXT NOT NULL,'rest_phone' REAL NOT NULL,'rest_distance' REAL); "
#13
    cur.execute(statement)

    for inst in data_places_infor:
        insertion=(inst[0], inst[1], inst[2], inst[3], inst[4], inst[5], inst[6], inst[7], inst[8], inst[9], inst[10], inst[11], inst[12], inst[13], inst[14], inst[15], inst[16], inst[17],inst[18], inst[19])
        #print(insertion)
        statement = 'INSERT INTO ' + str(each_famous_place)
        statement += ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ' #19
        cur.execute(statement,insertion)
    conn.commit()
    pass


#for i in list_famouse_places_replace:
    #print(i)
    #print(create_each_place_db(each_famous_place = i))



#print("this is get_places_for_site")

#print(get_places_for_site(site = "YellowstoneNational"))




def get_location_for_all(list):  #retuning the list of lat and long based on the list of places
    location_faumous_places = []
    for lo in list:
        print(lo)
        if "error in " + str(lo) == get_places_for_site(site = str(lo)):
            print("error in " + str(lo))
        else:
            print("showing the lat and long for the site ")
            location_faumous_places.append(get_places_for_site(site = str(lo)))
    return(location_faumous_places)


def get_no_except_places(list):
    location_faumous_places = []
    except_places = []
    for lo in list:
        print(lo)
        if "error in " + str(lo) == get_places_for_site(site = str(lo)):
            print("error in " + str(lo))
        else:
            #print("showing the lat and long for the site ")
            except_places.append(lo)
    return(except_places)


#print(" this is list of latitude and longtitude of all famous places  ")
#print(get_location_for_all(list = list_famouse_places_location))


#print("this is the the latitude and longtitude from list of hotels ")
#for i in list_url_hotels:
    #print("showing hotels names based on hotel url for each famous place ")
    #print(get_hotel_name(url_hotel = i))
    #print(get_location_for_all(list = get_hotel_name(url_hotel = i)))



#print("this is the the latitude and longtitude from list of things to do")
#list_things_to_do_url
#print("this is get_thingstodo_infor")
#print(get_thingstodo_infor(thingstodo_url = "https://travel.usnews.com//Yellowstone_National_Park_WY//Things_To_Do/"))

#for i in list_things_to_do_url:
    #print("showing the long and lati for " + str(i) )
    #print(get_location_for_all(list = get_thingstodo_infor(thingstodo_url = i)))


#print("this is the the latitude and longtitude from list of restaurants for each famous restaurant")

all_list_rest_name_long_and_lat = []
#list_rest_name = []

#for u in list_famouse_places_location:
    #search_dic =json.loads(search(API_KEY, DEFAULT_TERM, location = u))
    #load_restaurant2 = search_dic["businesses"]
    #list_rest_name = []
    #for t in load_restaurant2 :# getting list of names of resturatns based on one famous place
        #list_rest_name.append(t["name"])
    #print("list_rest_name")
    #print(list_rest_name)
    #list_rest_name_long_and_lat = get_location_for_all(list= list_rest_name)
    #print("list_rest_name_long_and_lat")
    #print(all_list_rest_name_long_and_lat.append(list_rest_name_long_and_lat))

def get_zip_all(location):
    data_restaurant = []
    search_dic =json.loads(search(API_KEY, DEFAULT_TERM, location))
    print(type(search_dic))
    load_restaurant2 = search_dic["businesses"]
    #creating data base for each famoius place to get info about hotels, adress and so on
    thingstodo_url = "https://travel.usnews.com/"+ str(location) + "/Things_To_Do/"
    hotel_url = "https://travel.usnews.com/Hotels/" + str(location)
    list_hotels_names = get_hotel_name(hotel_url)
    list_things_to_do = get_thingstodo_infor(thingstodo_url)
    #print("list_things_to_do")
    #print(list_things_to_do)

    data_places_infor = []
    #o = open("SI507finalproject_cache2.json")
    #load_places  = json.load(o)
    #print(load_places)
    #load_restaurant2 = load_restaurant["https://api.yelp.com/v3/businesses/search"]["businesses"]
    #get_places_for_site(site)
    #print("lengh of list_hotels_names ")
    #print(len(list_hotels_names))
    #print("lengh of list_things_to_do ")
    #print(len(list_things_to_do))
    #print("lengh of load_restaurant2 ")
    #print(len(load_restaurant2))
    while len(list_hotels_names)< 50:
        list_hotels_names.append("")
    while len(list_things_to_do)< 50:
        list_things_to_do.append("")
    while len(load_restaurant2)< 50:
        load_restaurant2.append("")

    #print("lengh of list_hotels_names ")
    #print(len(list_hotels_names))
    #print("lengh of list_things_to_do ")
    #print(len(list_things_to_do))
    #print("lengh of load_restaurant2 ")
    #print(len(load_restaurant2))

    zip_row  = zip(list_hotels_names,list_things_to_do,load_restaurant2)
    #print("lengh of zip_row ")
    #print(len(zip_row))
    count = 0
    for hotel,things,rest in zip_row:
        count = count +1
        data_place_row = []
        #print(load_country.index(row))
        #data_place_row.append(zip_row.index(famous_palce)+1)
        try:
            data_place_row.append(count)
            data_place_row.append(hotel)
            data_place_row.append(get_places_for_site_latitude(site = hotel))
            data_place_row.append(get_places_for_site_lng(site = hotel))
        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
        try:
            data_place_row.append(count)
            data_place_row.append(things)
            data_place_row.append(get_places_for_site_latitude(site = things))
            data_place_row.append(get_places_for_site_lng(site = things))
        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")

        try:

            data_place_row.append(count)
            data_place_row.append(rest["id"])
            data_place_row.append(rest["alias"])
            data_place_row.append(rest["name"])
            data_place_row.append(rest["image_url"])
            data_place_row.append(rest["is_closed"])
            data_place_row.append(rest["url"])
            data_place_row.append(rest["review_count"])
            data_place_row.append(rest["rating"])
            location = ""
            location = location + str(rest["location"]['address1'])
            location = location + str(rest["location"]['address2'])
            location = location + str(rest["location"]['address3'])
            location = location + str(rest["location"]['city'])
            location = location + str(rest["location"]['zip_code'])
            location = location + str(rest["location"]['country'])
            location = location + str(rest["location"]['state'])
            #print("this is location")
            #print(location)
            data_place_row.append(location)
            data_place_row.append(rest["phone"])
            data_place_row.append(rest["distance"])

        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")

        data_places_infor.append(data_place_row)

    return(data_places_infor)

def get_zip_hotels(location):
    data_restaurant = []
    hotel_url = "https://travel.usnews.com/Hotels/" + str(location)
    #print("thsi is locaiton")
    #print(location)
    #print("hotel url ")
    #print(hotel_url)
    list_hotels_names = get_hotel_name(hotel_url)

    #print("thisis list_hotels_names")
    #print(list_hotels_names)

    data_places_infor = []
    count = 0
    for hotel in list_hotels_names:
        count = count +1
        data_place_row = []
        #print(load_country.index(row))
        #data_place_row.append(zip_row.index(famous_palce)+1)
        try:
            data_place_row.append(count)
            data_place_row.append(hotel)
            data_place_row.append(get_places_for_site_latitude(site = hotel))
            data_place_row.append(get_places_for_site_lng(site = hotel))
        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")

        data_places_infor.append(data_place_row)
        #print(data_places_infor)

    return(data_places_infor)

def get_zip_thingstod(location):
    data_restaurant = []
    thingstodo_url = "https://travel.usnews.com/"+ str(location) + "/Things_To_Do/"
    list_things_to_do = get_thingstodo_infor(thingstodo_url)
    #print(list_things_to_do)
    data_places_infor = []
    count = 0
    for things in list_things_to_do:
        count = count +1
        data_place_row = []

        try:
            data_place_row.append(count)
            data_place_row.append(things)
            data_place_row.append(get_places_for_site_latitude(site = things))
            data_place_row.append(get_places_for_site_lng(site = things))
        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")

        data_places_infor.append(data_place_row)

    return(data_places_infor)


def get_zip_rest(location):
    data_restaurant = []
    search_dic =json.loads(search(API_KEY, DEFAULT_TERM, location))
    load_restaurant2 = search_dic["businesses"]
    data_places_infor = []
    count = 0
    for rest in load_restaurant2:
        count = count +1
        data_place_row = []
        try:
            data_place_row.append(count)
            data_place_row.append(rest["id"])
            data_place_row.append(rest["alias"])
            data_place_row.append(rest["name"])
            data_place_row.append(rest["image_url"])
            data_place_row.append(rest["is_closed"])
            data_place_row.append(rest["url"])
            data_place_row.append(rest["review_count"])
            data_place_row.append(rest["rating"])
            location = ""
            location = location + str(rest["location"]['address1'])
            location = location + str(rest["location"]['address2'])
            location = location + str(rest["location"]['address3'])
            location = location + str(rest["location"]['city'])
            location = location + str(rest["location"]['zip_code'])
            location = location + str(rest["location"]['country'])
            location = location + str(rest["location"]['state'])
            data_place_row.append(location)
            data_place_row.append(rest["phone"])
            data_place_row.append(rest["distance"])

        except:
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")
            data_place_row.append("")

        data_places_infor.append(data_place_row)

    return(data_places_infor)



#print("get_zip_all(location=")
#print(get_zip_rest(location= "New_York_NY")[0])
#print(get_zip_hotels(location= "New_York_NY")[0])
#print(get_zip_thingstod(location= "New_York_NY")[0])


class Hotelsinfor():
    def __init__(self,hotel_number,hotels,hotel_latitude,hotel_longtude):
        self.hotel_number = hotel_number
        self.hotels = hotels
        self.hotel_latitude= hotel_latitude
        self.hotel_longtude = hotel_longtude

    def __str__(self):
        return (str(self.hotel_number) + ". " + str(self.hotels) + " : " +"location→　" + " (" + str(self.hotel_latitude)+ ", " + str(self.hotel_longtude) + ") " )

class Thingstodoinfor():
    def __init__(self,things_to_do_number,things_to_do,things_to_do_latitude,things_to_do_longtide):

        self.things_to_do_number = things_to_do_number
        self.things_to_do = things_to_do
        self.things_to_do_latitude = things_to_do_latitude
        self.things_to_do_longtide =things_to_do_longtide

    def __str__(self):
        return (str(self.things_to_do_number) + ". " + str(self.things_to_do) + " : " +"location→" + " (" + str(self.things_to_do_latitude)+ ", " + str(self.things_to_do_longtide) + ") " )

class Restinfor():
    def __init__(self,rest_number,rest_id,rest_alias,rest_name,rest_image_url,rest_is_closed,rest_url,rest_review_count,rest_rating,rest_location,rest_phone,rest_distance):
        self.rest_number = rest_number
        self.rest_id = rest_id
        self.rest_alias= rest_alias
        self.rest_name = rest_name
        self.rest_image_url = rest_image_url
        self.rest_is_closed = rest_is_closed
        self.rest_url = rest_url
        self.rest_review_count = rest_review_count
        self.rest_rating = rest_rating
        self.rest_location = rest_location
        self.rest_phone =rest_phone
        self.rest_distance = rest_distance


    def __str__(self):
        return (str(self.rest_number) + ". " + str(self.rest_name) + " :" +"the location→" + str(self.rest_location)+ ", "+ "restaurant review count→" + str(self.rest_review_count)+ ", " + "restaurant rating→" + str(self.rest_rating)+ ", " +"restaurant'URL→" + str(self.rest_url))





def output_rest(location):
    output_rest = []
    for rest_number,rest_id,rest_alias,rest_name,rest_image_url,rest_is_closed,rest_url,rest_review_count,rest_rating,rest_location,rest_phone,rest_distance in get_zip_rest(location):
        rest_inst = Restinfor(rest_number,rest_id,rest_alias,rest_name,rest_image_url,rest_is_closed,rest_url,rest_review_count,rest_rating,rest_location,rest_phone,rest_distance)
        output_rest.append(rest_inst.__str__().replace('\u3000',''))

    return(output_rest)



def output_hotels(location):
    output_hotels = []
    for hotel_number,hotels,hotel_latitude,hotel_longtude in get_zip_hotels(location):
        hotels_inst = Hotelsinfor(hotel_number,hotels,hotel_latitude,hotel_longtude)
        output_hotels.append(hotels_inst.__str__().replace('\u3000',''))

    return(output_hotels)

#print("output_hotels(location = 'Grand_Canyon_AZ')")
#print(output_hotels(location = "Grand_Canyon_AZ"))

def output_thingstodo(location):
    output_thingstodo = []
    for things_to_do_number,things_to_do,things_to_do_latitude,things_to_do_longtide in get_zip_thingstod(location):
        things_to_do_inst = Thingstodoinfor(things_to_do_number,things_to_do,things_to_do_latitude,things_to_do_longtide)
        output_thingstodo.append(things_to_do_inst.__str__().replace('\u3000',''))
    return(output_thingstodo)



#print("output for each ")
#print(output_rest)
#print(output_hotels)
#print(output_thingstodo)




def plot_famous_places(list = list_famouse_places_location):



     # url variable store url
     url_google = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

     list_get_no_except_places = get_no_except_places(list = list_famouse_places_location)

     list_lat_plot = []
     list_log_plot= []
     for lon_lat in get_location_for_all(list_get_no_except_places):
         list_lat_plot.append(lon_lat[0])
         list_log_plot.append(lon_lat[1])

     print("this is list_lat ")
     print(list_lat_plot)
     print("this is list_log")
     print(list_log_plot)
     print("this is the length of lat log rest_name ")
     print(len(list_lat_plot))
     print(len(list_log_plot))
     print(len(list_get_no_except_places))


     data=[
             go.Scattermapbox(
             lat=list_lat_plot,
             lon=list_log_plot,
             mode='markers',
             marker=dict(
                 size=9,
                 symbol = 'star'
             ),
             text=list_get_no_except_places,
              )
              ]

     print("data")
     print(data)

     layout=go.Layout(
         autosize=True,
         hovermode='closest',
         mapbox=dict(
             accesstoken=MAPBOX_TOKEN,
             bearing=0,
             center=dict(
                 lat=38,
                 lon=-94
             ),
             pitch=0,
             zoom=2
         ),
     )
     fig = dict(data=data, layout=layout)
     return(py.plot(fig, filename='Multiple Mapbox'))

#print(plot_famous_places(list = list_famouse_places_location))

def plot_rest_for_famous_place(location):
    search_dic =json.loads(search(API_KEY, DEFAULT_TERM, location))
    load_restaurant2 = search_dic["businesses"]
    list_rest_name = []# getting list of names of resturatns based on one famous place
    for t in load_restaurant2 :
        list_rest_name.append(t["name"])
    print("this is list_rest_name") #○
    print(list_rest_name)
    print(len(list_rest_name))
    #50

    print("this is get_location_for_all(list_rest_name")
    print(get_location_for_all(list_rest_name))
    print(len(get_location_for_all(list_rest_name)))
    #38
    print("get_no_except_places")
    print(get_no_except_places(list = list_rest_name))
    print(len(get_no_except_places(list = list_rest_name)))
    list_get_no_except_places = get_no_except_places(list = list_rest_name)

    standard_lat = float(get_places_for_site(site = location)[0])
    standard_lon = float(get_places_for_site(site = location)[1])
    print("standard location ")
    print(standard_lat)
    print(standard_lon )

    av_list_lat_plot = []
    av_list_log_plot= []
    for lon_lat in get_location_for_all(list_rest_name):
        av_list_lat_plot.append(float(lon_lat[0]))
        #print(type(lon_lat[0]))
        av_list_log_plot.append(float(lon_lat[1]))
    #print(av_list_lat_plot)
    #print(av_list_log_plot)

    new_av_list_lat_plot = []
    new_av_list_lon_plot = []
    list_delite_lat = []
    for i in av_list_lat_plot:
        if (standard_lat + 2) < i or (standard_lat - 2)> i:
            list_delite_lat.append(av_list_lat_plot.index(i))
            print("beyond average")
        else:
            new_av_list_lat_plot.append(i)

    list_delite_lon = []
    for i in av_list_log_plot:
        if (standard_lon+ 2) < i or (standard_lon - 2)> i:
            list_delite_lon.append(av_list_log_plot.index(i))
            print("beyond average")
        else:
            new_av_list_lon_plot.append(i)

    print("this is new av")
    print(new_av_list_lat_plot)
    print(new_av_list_lon_plot)
    list_rest_name_long_and_lat = list(zip(new_av_list_lat_plot,new_av_list_lon_plot))
    print("this is list_rest_name_long_and_lat")
    print(list_rest_name_long_and_lat)
    #print(len(list_rest_name_long_and_lat))

    #print("this is list_delite_lat and  list_delite_lon")
    #print(list_delite_lat)
    #print(list_delite_lon)

    if len(list_delite_lat) >len(list_delite_lon):
        for i in list_delite_lat:
            #print(i)
            print(list_get_no_except_places.pop(i))
    elif len(list_delite_lat) <len(list_delite_lon):
        for i in list_delite_lon:
            #print(i)
            print(list_get_no_except_places.pop(i))

    #print("this is list_get_no_except_places")
    #print(list_get_no_except_places)
    #print(len(list_get_no_except_places))

    # url variable store url
    url_google = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    list_get_no_except_places = get_no_except_places(list = list_rest_name)
    list_lat_plot = []
    list_log_plot= []

    for lon_lat in list_rest_name_long_and_lat:
        list_lat_plot.append(lon_lat[0])
        list_log_plot.append(lon_lat[1])

    print("this is list_lat ")
    print(list_lat_plot)
    print("this is list_log")
    print(list_log_plot)
    print("this is the length of lat log rest_name ")
    print(len(list_lat_plot))
    print(len(list_log_plot))
    print(len(list_get_no_except_places))


    data=[
            go.Scattermapbox(
            lat=list_lat_plot,
            lon=list_log_plot,
            mode='markers',
            marker=dict(
                size=4,
                symbol = 'star'
            ),
            text=list_get_no_except_places,
             )
             ]
    print("data")
    print(data)
    layout=go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            bearing=0,
            center=dict(
                lat=standard_lat,
                lon=standard_lon
            ),
            pitch=0,
            zoom=10
        ),
    )
    fig = dict(data=data, layout=layout)
    return(py.plot(fig, filename='Multiple Mapbox'))


def plot_hotels_for_famous_place(location):
    url2 = "https://travel.usnews.com/rankings/best-usa-vacations/"
    page_text = make_request_using_cache(url2)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_search = page_soup.find(class_="search-app-matches-layout-view busy-content")
    content_search2 = page_soup.find_all(class_='ranking-element row collapse block-looser rank-voting-item')

    list_famouse_places = []
    for i in content_search2:
        s = i.find(class_ = "small-12 medium-7 column")
        place = s.find("a")["href"]
        if place != "/Grand_Teton_National_Park_WY/":
            list_famouse_places.append(place)

    hotel_url = "https://travel.usnews.com/Hotels/" + str(location)


    list_hotel_name = get_hotel_name(hotel_url)

    list_famouse_places_replace = []
    for i in list_famouse_places:
        replace = i.replace("/","")
        list_famouse_places_replace.append(replace)

    list_famouse_places_location = []
    for i in list_famouse_places_replace:
        replace = i.replace("_"," ")
        if len(replace.split()) > 2:
            tempo_word = replace.split()[0] + str(" ")+ replace.split()[1]
            list_famouse_places_location.append(tempo_word)
        else:
            list_famouse_places_location.append(replace)

    location = location.replace("_"," ")
    if len(replace.split()) > 2:
        tempo_word = replace.split()[0] + str(" ")+ replace.split()[1]


    print("this is get_location_for_all(list_hotel_name")
    print(get_location_for_all(list_hotel_name))
    print(len(get_location_for_all(list_hotel_name)))

    #print("this is get_location_for_all(list_rest_name")
    #print(get_location_for_all(list_rest_name))
    #print(len(get_location_for_all(list_rest_name)))

    #38
    print("get_no_except_places")
    print(get_no_except_places(list = list_hotel_name ))
    print(len(get_no_except_places(list =list_hotel_name )))
    list_get_no_except_places = get_no_except_places(list = list_hotel_name )

    standard_lat = float(get_places_for_site(site = location)[0])
    standard_lon = float(get_places_for_site(site = location)[1])
    print("standard location ")
    print(standard_lat)
    print(standard_lon )

    av_list_lat_plot = []
    av_list_log_plot= []
    for lon_lat in get_location_for_all(list_hotel_name):
        av_list_lat_plot.append(float(lon_lat[0]))
        #print(type(lon_lat[0]))
        av_list_log_plot.append(float(lon_lat[1]))
    #print(av_list_lat_plot)
    #print(av_list_log_plot)

    new_av_list_lat_plot = []
    new_av_list_lon_plot = []
    list_delite_lat = []
    for i in av_list_lat_plot:
        if (standard_lat + 2) < i or (standard_lat - 2)> i:
            list_delite_lat.append(av_list_lat_plot.index(i))
            print("beyond average")
        else:
            new_av_list_lat_plot.append(i)

    list_delite_lon = []
    for i in av_list_log_plot:
        if (standard_lon+ 2) < i or (standard_lon - 2)> i:
            list_delite_lon.append(av_list_log_plot.index(i))
            print("beyond average")
        else:
            new_av_list_lon_plot.append(i)

    print("this is new av")
    print(new_av_list_lat_plot)
    print(new_av_list_lon_plot)
    list_rest_name_long_and_lat = list(zip(new_av_list_lat_plot,new_av_list_lon_plot))
    print("this is list_rest_name_long_and_lat")
    print(list_rest_name_long_and_lat)
    #print(len(list_rest_name_long_and_lat))

    #print("this is list_delite_lat and  list_delite_lon")
    #print(list_delite_lat)
    #print(list_delite_lon)

    if len(list_delite_lat) >len(list_delite_lon):
        for i in list_delite_lat:
            #print(i)
            print(list_get_no_except_places.pop(i))
    elif len(list_delite_lat) <len(list_delite_lon):
        for i in list_delite_lon:
            #print(i)
            print(list_get_no_except_places.pop(i))

    #print("this is list_get_no_except_places")
    #print(list_get_no_except_places)
    #print(len(list_get_no_except_places))

    # url variable store url
    url_google = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    list_get_no_except_places = get_no_except_places(list = list_hotel_name)
    list_lat_plot = []
    list_log_plot= []

    for lon_lat in list_rest_name_long_and_lat:
        list_lat_plot.append(lon_lat[0])
        list_log_plot.append(lon_lat[1])

    print("this is list_lat ")
    print(list_lat_plot)
    print("this is list_log")
    print(list_log_plot)
    print("this is the length of lat log rest_name ")
    print(len(list_lat_plot))
    print(len(list_log_plot))
    print(len(list_get_no_except_places))
    data=[
            go.Scattermapbox(
            lat=list_lat_plot,
            lon=list_log_plot,
            mode='markers',
            marker=dict(
                size=4,
                symbol = 'star'
            ),
            text=list_get_no_except_places,
             )
             ]

    print("data")
    print(data)

    layout=go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            bearing=0,
            center=dict(
                lat=standard_lat,
                lon=standard_lon
            ),
            pitch=0,
            zoom=10
        ),
    )
    fig = dict(data=data, layout=layout)
    return(py.plot(fig, filename='Multiple Mapbox'))


#print(plot_hotels_for_famous_place(location = "New_York_NY"))

def plot_things_todo_for_famous_place(location):
    url2 = "https://travel.usnews.com/rankings/best-usa-vacations/"
    page_text = make_request_using_cache(url2)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_search = page_soup.find(class_="search-app-matches-layout-view busy-content")
    content_search2 = page_soup.find_all(class_='ranking-element row collapse block-looser rank-voting-item')

    list_famouse_places = []
    for i in content_search2:
        s = i.find(class_ = "small-12 medium-7 column")
        place = s.find("a")["href"]
        if place != "/Grand_Teton_National_Park_WY/":
            list_famouse_places.append(place)

    thingstodo_url = "https://travel.usnews.com/"+str(location)+ "/Things_To_Do/"

    list_thingstodo_name = get_thingstodo_infor(thingstodo_url)

    location = location.replace("_"," ")
    if len(replace.split()) > 2:
        tempo_word = replace.split()[0] + str(" ")+ replace.split()[1]

    #get_places_for_site(location)

    #50
    print("this is get_location_for_all(list_hotel_name")
    print(get_location_for_all(list_thingstodo_name))
    print(len(get_location_for_all(list_thingstodo_name)))

    #38
    print("get_no_except_places")
    print(get_no_except_places(list = list_thingstodo_name))
    print(len(get_no_except_places(list =list_thingstodo_name)))
    list_get_no_except_places = get_no_except_places(list = list_thingstodo_name)

    standard_lat = float(get_places_for_site(site = location)[0])
    standard_lon = float(get_places_for_site(site = location)[1])
    print("standard location ")
    print(standard_lat)
    print(standard_lon )

    av_list_lat_plot = []
    av_list_log_plot= []
    for lon_lat in get_location_for_all(list_thingstodo_name):
        av_list_lat_plot.append(float(lon_lat[0]))
        #print(type(lon_lat[0]))
        av_list_log_plot.append(float(lon_lat[1]))
    #print(av_list_lat_plot)
    #print(av_list_log_plot)

    new_av_list_lat_plot = []
    new_av_list_lon_plot = []
    list_delite_lat = []
    for i in av_list_lat_plot:
        if (standard_lat + 2) < i or (standard_lat - 2)> i:
            list_delite_lat.append(av_list_lat_plot.index(i))
            print("beyond average")
        else:
            new_av_list_lat_plot.append(i)

    list_delite_lon = []
    for i in av_list_log_plot:
        if (standard_lon+ 2) < i or (standard_lon - 2)> i:
            list_delite_lon.append(av_list_log_plot.index(i))
            print("beyond average")
        else:
            new_av_list_lon_plot.append(i)

    print("this is new av")
    print(new_av_list_lat_plot)
    print(new_av_list_lon_plot)
    list_rest_name_long_and_lat = list(zip(new_av_list_lat_plot,new_av_list_lon_plot))
    print("this is list_rest_name_long_and_lat")
    print(list_rest_name_long_and_lat)
    #print(len(list_rest_name_long_and_lat))

    #print("this is list_delite_lat and  list_delite_lon")
    #print(list_delite_lat)
    #print(list_delite_lon)

    if len(list_delite_lat) >len(list_delite_lon):
        for i in list_delite_lat:
            #print(i)
            print(list_get_no_except_places.pop(i))
    elif len(list_delite_lat) <len(list_delite_lon):
        for i in list_delite_lon:
            #print(i)
            print(list_get_no_except_places.pop(i))

    #print("this is list_get_no_except_places")
    #print(list_get_no_except_places)

    # url variable store url
    url_google = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    list_get_no_except_places = get_no_except_places(list = list_thingstodo_name)
    list_lat_plot = []
    list_log_plot= []

    for lon_lat in list_rest_name_long_and_lat:
        list_lat_plot.append(lon_lat[0])
        list_log_plot.append(lon_lat[1])

    print("this is list_lat ")
    print(list_lat_plot)
    print("this is list_log")
    print(list_log_plot)
    print("this is the length of lat log rest_name ")
    print(len(list_lat_plot))
    print(len(list_log_plot))
    print(len(list_get_no_except_places))


    data=[
            go.Scattermapbox(
            lat=list_lat_plot,
            lon=list_log_plot,
            mode='markers',
            marker=dict(
                size=4,
                symbol = 'star'
            ),
            text=list_get_no_except_places,
             )
             ]

    print("data")
    print(data)

    layout=go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAPBOX_TOKEN,
            bearing=0,
            center=dict(
                lat=standard_lat,
                lon=standard_lon
            ),
            pitch=0,
            zoom=10
        ),
    )
    fig = dict(data=data, layout=layout)
    return(py.plot(fig, filename='Multiple Mapbox'))


def load_help_text():
    with open('help_final.txt') as fh:
        return (fh.read())

#print("this is help")
#print(load_help_text())

#print(plot_things_todo_for_famous_place(location = "New_York_NY"))
print("This is the best places to visit according to USnews.")
print("Types one of them that you want to go")
print("if you need to help, type 'help'")
print("if you want to quit, type 'quit'")
for i in list_famouse_places_replace:
    print(i)

def process_command(command):
    try:
        s = command.split()
        print("this is s")
        print(s)
        location = s[0]
        print("this is location")
        print(s[0])
        output_all_infor = []
        if command == "help":
            print("this is help(process_commad)")
            return(load_help_text())
        elif command == "exit":
            return("bye")
        elif command == "all plot":
            print("plotting the locations of famous places in US ")
            return(plot_famous_places(list = list_famouse_places_location))
            #command = str(input("Types one of them that you want to go like 'New york information hotels' or type 'all plot' to see the location of each place by a map :" ))
            #s = command.split()

        elif location not in list_famouse_places_replace:
            return("command is wrong")

        elif s[2] == "hotels":
            print(s[2])
            if s[1] == "information":
                print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                for i in output_hotels(location):
                    #print(i)
                    output_all_infor.append(i)
                return(output_all_infor)

            elif s[1]=="plot":
                print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                return(plot_hotels_for_famous_place(location))

            else:
                return("command is wrong")

        elif s[2] == "restaurants":
            print(s[2])
            if s[1] == "information":
                print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                for i in output_rest(location):
                    output_all_infor.append(i)
                return(output_all_infor)

            elif s[1]=="plot":
                print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                return(plot_rest_for_famous_place(location))

            else:
                return("command is wrong")

        elif s[2] == "things_to_do":
            if s[1] == "information":
                print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                for i in output_thingstodo(location):
                    output_all_infor.append(i)
                return(output_all_infor)

            elif s[1]=="plot":
                print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                return(plot_things_todo_for_famous_place(location))

            else:
                return("command is wrong")

        else:
            return("command is wrong")
    except:
        return("command is wrong")




#command = str(input("Types one of them that you want to go like 'New york information hotels' or type 'all plot' to see the location of each place by a map :" ))
print(process_command(command = "Lake_Tahoe_CA plot restaurants"))



def interactive_prompt():
    while(True):
        try:
            print("This is the best places to visit according to USnews.")
            print("Types one of them that you want to go")
            print("if you need to help, type 'help'")
            print("if you want to quit, type 'quit'")
            for i in list_famouse_places_replace:
                print(i)
            command = str(input("Types one of them that you want to go like 'New york information hotels' or type 'all plot' to see the location of each place by a map :" ))
            s = command.split()
            location = s[0]
            print(location)
            output_all_infor = []
            if command == "help":
                print("this is help")
                print(load_help_text())
            elif command == "exit":
                print("bye")
                break
            elif command == "all plot":
                print("plotting the locations of famous places in US ")
                print(plot_famous_places(list = list_famouse_places_location))
            elif location not in list_famouse_places_replace:
                print("command is wrong")
            elif s[2] == "hotels":
                print(s[2])
                if s[1] == "information":
                    print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                    for i in output_hotels(location):
                        print(i)
                        output_all_infor.append(i)
                elif s[1]=="plot":
                    print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                    print(plot_hotels_for_famous_place(location))
                else:
                    print("command is wrong")
            elif s[2] == "restaurants":
                if s[1] == "information":
                    print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                    for i in output_rest(location):
                        print(i)
                        output_all_infor.append(i)
                elif s[1]=="plot":
                    print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                    print(plot_rest_for_famous_place(location))
                else:
                    print("command is wrong")
            elif s[2] == "things_to_do":
                if s[1] == "information":
                    print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                    for i in output_thingstodo(location):
                        print(i)
                        output_all_infor.append(i)
                elif s[1]=="plot":
                    print("showing " +str(s[1]) + " about "  + str(s[2]) + " in "+ str(location))
                    print(plot_things_todo_for_famous_place(location))
                else:
                    print("command is wrong")
            else:
                print("command is wrong")

        except:
            print("command is wrong")





if __name__=="__main__":
    interactive_prompt()
