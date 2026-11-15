#Loads python standard HTTP Library , to send requests from web servers and APIs 
import requests
import os
api_key = os.getenv("WEATHERSTACK_API_KEY")
city = os.getenv("WEATHER_CITY", "New York")
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"

#resuable Function to get request from api url which is weatherapi
def fetch_data(): 
    if not api_key:
        raise ValueError("WEATHERSTACK_API_KEY environment variable is not set.")
    print(f"Fetching weather data for {city} from Weatherstack API...")
    print("FETCHING Weather data from WeatherStack API......")
    try: # try and except{to catch network and server erros} so that we can be notify if the status was successfull or not
    
        response = requests.get(api_url,timeout=15) #Send an HTTP Get request 
        response.raise_for_status()#Checks the servers HTTP status code if server retuned an error, so it raise an exception
        print("API response recieved Successfully")
        return response.json() #Convert raw JSON response paylod to python dictionary for easily access key value pairs

#calling function api  that we created
    except requests.exceptions.RequestException as e: #Catches any error related to request such as NO internet , Invalid URL, HTTP error
        print(f"An error occured:{e}")
        raise #re raise the caught error so parent calling functions stay aware that excecture failed.
