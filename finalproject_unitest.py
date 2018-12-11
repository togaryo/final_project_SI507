import unittest
from fianlproject import *

class TestDatabase(unittest.TestCase):

    def test_places_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT famous_place FROM Places'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('San Francisco',), result_list)
        self.assertIn(('Sedona AZ',), result_list)
        self.assertEqual(len(result_list), 24)

        sql = 'SELECT nearbyhotel_URL FROM Places'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('https://travel.usnews.com//Hotels/Grand_Canyon_AZ/',), result_list)
        self.assertEqual(result_list[9], ("https://travel.usnews.com//Hotels/Lake_Tahoe_CA/",))
        conn.close()


    def test_New_york_NY_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT hotels FROM New_York_NY'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Park Hyatt New York',), result_list)
        self.assertEqual(len(result_list), 50)
        conn.close()

#7

class TestHotelsSearch(unittest.TestCase):

    def test_hotel_Yellowstone_search(self):
        command = 'Yellowstone_National_Park_WY information hotels'

        results = process_command(command)
        self.assertEqual(results[0], '1. The Cody Hotel : location→ (44.5134572, -109.1029959) ')#pass

        command ='information hotels Yellowstone_National_Park_WY'
        results = process_command(command)
        self.assertEqual(results, "command is wrong")

    def test_hotel_Sanfransico_search(self):
        command ='San_Francisco_CA information hotels'
        results = process_command(command)
        self.assertEqual(results[2], '3. Four Seasons Hotel San Francisco : location→ (37.7863499, -122.4042632) ')#pass

        command ='hotels San_Francisco_CA information'
        results = process_command(command)
        self.assertEqual(results, "command is wrong")

#4

class TestThingstodoSearch(unittest.TestCase):

    def test_Thingstodo_boston_search(self):
        command ='Boston_MA information things_to_do'
        results = process_command(command)
        self.assertEqual(results[0], "1. Fenway Park : location→ (42.3466764, -71.0972178) ")#pass
        command ='Boston MA  restaurants'
        results = process_command(command)
        self.assertEqual(results, "command is wrong")

    def test_Thingstodo_Maui_search(self):
        command ='Maui_HI information things_to_do'
        results = process_command(command)
        self.assertEqual(results[2], "3. Kaanapali Beach : location→ (20.9178314, -156.6966248) ")#pass
        command ='Maui_HI Thingstodo information'
        results = process_command(command)
        self.assertEqual(results, "command is wrong")


class TestRestaurntsSearch(unittest.TestCase):

    def test_restaurants_Maui_search(self):
        command ='Maui_HI information restaurants'
        results = process_command(command)
        self.assertEqual(results[23], "24. Waikapu On 30 :the location→1486 Honoapiilani HwyWailuku96793USHI, restaurant review count→149, restaurant rating→4.5, restaurant'URL→https://www.yelp.com/biz/waikapu-on-30-wailuku?adjust_creative=XIyrLk32HHaYemz-JSeP1g&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=XIyrLk32HHaYemz-JSeP1g")#pass
        command ='Maui_HI restarant information'
        results = process_command(command)
        self.assertEqual(results, "command is wrong")

    def test_restaurant_Denver_search(self):
        command ='Denver_CO information restaurants'
        results = process_command(command)
        self.assertEqual(results [5], "6. Meadowlark Kitchen :the location→2705 Larimer StNoneDenver80205USCO, restaurant review count→328, restaurant rating→4.5, restaurant'URL→https://www.yelp.com/biz/meadowlark-kitchen-denver?adjust_creative=XIyrLk32HHaYemz-JSeP1g&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=XIyrLk32HHaYemz-JSeP1g")   # pass

        command ='Denver_CO'
        results = process_command(command)
        self.assertEqual(results, "command is wrong")

#10
unittest.main()
