from flask import Flask, request, jsonify
import os
import requests 
from groq import Groq 
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
VALID_TOKEN = os.getenv('VALID_TOKEN')
API_AI = os.getenv('API_AI')

groq_client = Groq(api_key=API_AI)

@app.route('/weather-advice', methods=['POST'])  
def get_weather_advice():
    data = request.json  
    
    if data.get('token') != VALID_TOKEN:
        return jsonify({"error": "Invalid token"}), 401
    
    requester_name = data.get('requester_name')
    location = data.get('location')
    date = data.get('date')
    query_type = data.get('query_type', 'clothing')
    
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={API_KEY}&unitGroup=metric"
    response = requests.get(url)
    weather_data = response.json()
    
    day_data = weather_data['days'][0]
    temp = day_data['temp']
    wind_speed = day_data['windspeed']
    humidity = day_data['humidity']
    conditions = day_data['conditions']
    precipitation = day_data.get('precip', 0)
    
    if query_type == 'uav':  
        prompt = f"""Analyze this weather data for {location} on {date} for UAV/drone flight:
- Temperature: {temp}°C
- Wind speed: {wind_speed} km/h
- Humidity: {humidity}%
- Conditions: {conditions}
- Precipitation: {precipitation} mm

Provide:
1. Is it safe to fly a drone? (Yes/No/Caution)
2. Best time window for flight (if available in hourly data)
3. Recommended altitude range
4. Specific warnings or considerations

Keep response concise and structured."""
    else: 
        prompt = f"""Analyze this weather for {location} on {date}:
- Temperature: {temp}°C
- Wind speed: {wind_speed} km/h
- Humidity: {humidity}%
- Conditions: {conditions}
- Precipitation: {precipitation} mm

Suggest appropriate clothing and accessories. Be specific and practical. Keep it brief."""
    
    ai_response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",  
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
    )
    
    ai_advice = ai_response.choices[0].message.content
    
    result = {
        "requester_name": requester_name,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "location": location,
        "date": date,
        "query_type": query_type,
        "weather": {
            "temp_c": temp,
            "wind_kph": wind_speed,
            "pressure_mb": day_data['pressure'],
            "humidity": humidity,
            "conditions": conditions
        },
        "ai_advice": ai_advice
    }
    
    return jsonify(result)

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.json
    
    if data.get('token') != VALID_TOKEN:
        return jsonify({"error": "Invalid token"}), 401
    
    requester_name = data.get('requester_name')
    location = data.get('location')
    date = data.get('date')
    
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={API_KEY}&unitGroup=metric"
    response = requests.get(url)
    weather_data = response.json()
    
    result = {
        "requester_name": requester_name,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "location": location,
        "date": date,
        "weather": {
            "temp_c": weather_data['days'][0]['temp'],
            "wind_kph": weather_data['days'][0]['windspeed'],
            "pressure_mb": weather_data['days'][0]['pressure'],
            "humidity": weather_data['days'][0]['humidity']
        }
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
