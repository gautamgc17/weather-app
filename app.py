from flask import Flask , render_template , abort , request 
from urllib.request import urlopen
import json
import api_key 

app = Flask(__name__)

def convertToCelsius(temp):
    return round((float(temp) - 273.16) , 2)

@app.route('/')
def display():
    return render_template('index.html')

@app.route('/weather' , methods=['POST' , 'GET'])
def weather():
    if request.method == 'POST':
        city = str(request.form['city'])

        try:
            api_url = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID='+api_key.key
            api_request = urlopen(api_url).read()
        except:
            return abort(404)

        data = json.loads(api_request)

        # converting JSON data to a dictionary
        output = {
            'city' : str(data['name']),
            'country_code' : str(data['sys']['country']),
            'temperature' : str(convertToCelsius(data['main']['temp']))+'°C',
            'pressure' : str(data['main']['pressure']),
            'humidity' : str(data['main']['humidity']),
            'current_weather' : str(data['weather'][0]['description']),
            'wind_speed' : str(data['wind']['speed'])+'mph',
        } 

    return render_template('index.html' , data = output)

if __name__ == '__main__':
    app.run(debug = True)