import redis
import json
from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)

@app.route("/weather/<city>")
def get_weather(city):
    key = f"weather:{city}"
    cached_data = redis_client.get(key)

    if cached_data:
        parsed_data = json.loads(cached_data)
        return jsonify(parsed_data)

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={API_KEY}&contentType=json"
    response = requests.get(url)
    print(response)
    print(API_KEY)
    print(city)
    if response.status_code == 200:
        data = response.json()
        json_string = json.dumps(data)
        redis_client.set(key, json_string, ex=600)
        return jsonify(data)
    else:
        return jsonify({"error": "Не вдалося отримати погоду"}), 500
    

if __name__ == "__main__":
    app.run(debug=True)