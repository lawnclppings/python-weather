import os, platformdirs, json, requests, urllib.parse #Dependencies: python-requests, python-platformdirs

#config values
default_config = {
    'key': '',
    'city': 'New+York',
    'units': 'imperial'
}
degrees = {'imperial': '°F', 'metric': '°C', 'standard': '°K'}
speed = {'imperial': 'miles/hour', 'metric': 'meters/sec', 'standard': 'meters/sec'}
known_errors = {
    401: 'Access denied, check that your key is correct in ~/.config/weather/config.json', 
    403: 'The resource you are trying to access is forbidden', 
    404: 'The resource was not found on the server.'
}
icons = {'01d': '☀', '01n': '☀', '02d': '🌤', '02n': '🌤', '03d': '🌥', '03n': '🌥', '04d': '☁', '04n': '☁', '09d': '🌧', '09n': '🌧', '10d': '🌦', '10n': '🌦', '11d': '🌩', '11n': '🌩', '13d:': '❄', '13n': '❄', '50d': '🌫', '50n': '🌫'}

def load(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default_config, f, indent=4)
    path = os.path.join(filename)
    with open(path) as f:
        config = json.load(f)
    return config

#check if dir exists and make if not exists
from platformdirs import *
if os.path.isdir(user_config_dir('weather')) == False:
    os.mkdir(user_config_dir('weather'))

#load config
config = load(user_config_dir('weather/config.json'))

url = 'https://api.openweathermap.org/data/2.5/weather?q='+urllib.parse.quote_plus(config['city'])+'&units='+config['units']+'&appid='+config['key']
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    print(data['weather'][0]['main'],icons[data['weather'][0]['icon']])
    print('Temperature: '+str(data['main']['temp'])+degrees[config['units']])
    print('Wind: '+str(data['wind']['speed'])+speed[config['units']])
else:
    print('Error',response.status_code,': ',known_errors[response.status_code])