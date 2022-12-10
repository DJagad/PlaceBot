# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
#import wikipedia
from geopy.geocoders import Nominatim
from .database_connectivity import DataUpdate

class ActionCheckWeather(Action):
    
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher, tracker, domain):
        api_key = '058850b5af40e7d01acd9b7fa5457dd4'
        loc = tracker.get_slot('location_weather')
        print(loc)
        current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
        print(current)
        country=current['sys']['country']
        city=current['name']
        condition = current['weather'][0]['main'    ]
        temperature_c = current['main']['temp']
        humidity = current['main']['humidity']
        wind_mph = current['wind']['speed']
        response = """It is currently {} in {} at theat the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
        dispatcher.utter_message(response)
        return []

class Actioncheckplaces(Action):
    
    def name(self) -> Text:
        return "action_get_places"

    def run(self, dispatcher, tracker, domain):
        api_key = '614d628d8c7f4e50acde6c8584bab81b'
        loc = tracker.get_slot('location')
        radius = tracker.get_slot('radius')
        places = tracker.get_slot('type_of_places')
        geolocator = Nominatim(user_agent="MyApp")
        locate = geolocator.geocode(loc)
        lat =  locate.latitude
        long = locate.longitude
        print("type_of_places:- ", places.lower())
        req = requests.get("https://api.geoapify.com/v2/places?categories=tourism.{}&filter=circle:{},{},{}&limit=5&apiKey={}".format(places.lower(),long,lat,radius,api_key)).json() 
        response = ""
        for i in range(0,5):
            response+=str(i+1)
            response+=". "
            response+=req['features'][i]['properties']['name']
            response+="\n"
            response+="         Address:- "
            response+=req['features'][i]['properties']['formatted']
            response+="\n"
        print("Inside the Actioncheckplaces class")
        dispatcher.utter_message(response)
        return []

#Adding in later part
#Storing into the database 

class ActionFeedback(Action):
    
    def name(self) -> Text:
        return "action_feedback"

    def run(self, dispatcher, tracker, domain):
        
        DataUpdate(tracker.get_slot("location"),tracker.get_slot("type_of_places"),tracker.get_slot("radius"),tracker.get_slot("location_weather"))
        dispatcher.utter_message("Thanks for your valuable feedback.")
        return []