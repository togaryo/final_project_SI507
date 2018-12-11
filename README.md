
Final Project Draft for SI 507



In my final project, I try to get the information about famous places to visit in US through US News website. For this website, we can get tours, hotels and so on around each famous places. Based on the famous places, I will try to gain good restaurants  around the famous place. Finaly, I will map the location of both of them or give the information of hotels, things to do or restaurants.


1.	Data sources →For Data Source, I will use Yelp Fusion which provides information about restaurants (https://www.yelp.com/developers/documentation/v3)
In addition, I will use US news to gain information about famous places in US
(https://travel.usnews.com/rankings/best-usa-vacations/ )

2.	Data source challenge score → I will use Yelp Fusion which in Web API you haven’t used before that requires API key or HTTP Basic authorization(4 point) . In addition, I will use the website to crawl the information about famous places in US. For each famous places, we can crawl the information about the address,tours,hotels and so on. (8 points ) As a result, my point of challenge score is 12

3.	The presentation tool(s) you plan to use.
→ I will show the location of famous places to visit in US and famous restaurants,hotels and things to do  by Yelp by using mapping or show the information of hotels, things to do or restaurants.



Data sources used, including instructions for a user to access the data sources

● Any other information needed to run the program (e.g., pointer to getting started info for
plotly)

when you choose plot option, some of them does not show the central of location and can not be zoomed properly so please try to move the pointer and zoom into the area to see the location of hotels, things to do or restaurnts


● Brief description of how your code is structured, including the names of significant data
processing functions (just the 2-3 most important functions--not a complete list) and
class definitions. If there are large data structures (e.g., lists, dictionaries) that you create
to organize your data for presentation, briefly describe them.

These are main funtions and lists for my final
get_places_for_site is the function that take a name  of place and return the location of longitude and latitude such as ("44","-110")
get_location_for_all is  the function that takes list of name  and return the list of locations of longitude and latitude such as ("44","-110")
get_no_except_places is  the function that take list of name  and return the list of names that does not have errors (some data can not detected from google and US news so this function is for showing the list of name that does no have errors)
list_rest_name  is  list of names of restaurants based on one famous place
get_hotel_name is the function that take one URL about hotel and return list of hotels name
get_thingstodo_infor is the function that take one URL about things to do and return list of things to do
get_zip_all is the function that takes the location like (New_York_NY) and returns zip of lists of hotels, restaurants and things to do.
get_zip_rest is the function takes the location like (New_York_NY) and return zip of list of restaurants
get_zip_thingsto is the function takes the location like (New_York_NY) and return zip of list of things to do
get_zip_hotels is  the function takes the location like (New_York_NY) and return zip of list of hotels
create_places_db is the function that creates db called places that have data about famous places in US
create_each_place_db is the function that creates db for  each of famous places that have data about hotels, things to do and restaurant
plot_famous_places is the function that takes list of each famous places and return ploting of them


 ● Brief user guide, including how to run the program and how to choose presentation
options.


At first, you have two choice of 1 or 2 for the interactive_prompt.


1 showing all of the places by ploting by typing "all plot"


2-1 choose one of them below

Yellowstone_National_Park_WY
Maui_HI
Grand_Canyon_AZ
Yosemite_CA
New_York_NY
San_Francisco_CA
Washington_DC
Honolulu_Oahu_HI
Boston_MA
Lake_Tahoe_CA
San_Diego_CA
Chicago_IL
New_Orleans_LA
Glacier_National_Park_MT
Seattle_WA
Miami_FL
Charleston_SC
Sanibel_Island_FL
Denver_CO
Big_Sur_CA
Savannah_GA
Monterey_CA
Sedona_AZ
Zion_National_Park_UT


2-2 choose information or plot
	Description: Based on what you choose out of famous places displayed, it will show some information about hotels, restaurants or things_to_do by sentences or mapping



2-3  choose hotels, restaurants or things_to_do
	Description: Based on what you choose out of famous places displayed and how to show, what kind of information do you want to know like hotels, restaurants or things_to_do


The example of your input is like

"all plot"
"Lake_Tahoe_CA information things_to_do "
"Miami_FL plot restaurants"
"Zion_National_Park_UT information hotels"
