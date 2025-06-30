import redis
import redis.exceptions
import requests
import json
from urllib.parse import quote

r_host='127.0.0.1'
r_port='6379'
r_db='0'

api_key='1c06a8585e4b5ab12a2573f85a9b92ce'
city=(input("Enter the City name e.g. London, New York")).strip()
URL=(f"http://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={api_key}")

def weather_data():
    global city
    if not city :
        print("Empty input is not valid")
        return None
    try:
        redis_con=redis.Redis(r_host,r_port,r_db)
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}")
        return None
    except redis.exceptions.RedisError as e:
        print(f"Redis error: {e}")
        return None
    r_data=redis_con.get(city)
    if r_data is not None:
        return json.loads(r_data.decode('utf-8'))
    else:
        try:
            city=quote(city)
            response=requests.get(URL)
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}")
            return None
        if response.status_code==200:
            data=response.json()
            r_data={
            'Temperature':data['main']['temp'],
            'Description':data['weather'][0]['description'],
            'Humidity':data['main']['humidity']
            }
            r_json=json.dumps(r_data)
            redis_con.set(city,r_json)
            return r_data
        if response.status_code==401:
            print("Authentication error: Invalid API Key")
        elif response.status_code == 404:
            print("City not found")
        elif response.status_code == 500:
            print(f"Server error: {response.status_code}")
        else:
            print(f"Unhandled error: {response.status_code}")

def display_data(weather_d):
    if weather_d is None:
        return None
    print("\n======= Weather Report ======")
    for key, value in weather_d.items():
        print(f"{key:<12}: {value}")
    print("=================================\n")
        

if __name__ == "__main__":
    data=weather_data()
    display_data(data)