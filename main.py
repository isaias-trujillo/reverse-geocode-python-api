from waitress import serve
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World 🌎!'

# create a GET route to health check
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

# create a GET route to get the current date and time
@app.route('/api/v1/clock', methods=['GET'])
def current_time():
    now = datetime.now(ZoneInfo("America/Lima"))
    return jsonify({
        'iso': now.isoformat(),
        'unix': now.timestamp(),
        'utc': now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        'timezone': now.strftime("%Z"),
    })

# create a GET route for the API with parameters: latitude, longitude
@app.route('/api/v1/reverse-geocode', methods=['GET'])
def reverse_geocode():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')

    if latitude is None or str(latitude).strip() == '':
        return jsonify({'error': 'latitude is required'})

    if longitude is None or str(longitude).strip() == '':
        return jsonify({'error': 'longitude is required'})

    # check if latitude and longitude are valid numbers
    try:
        float(latitude)
    except ValueError:
        return jsonify({'error': 'latitude is not a valid number, provided: {}'.format(latitude)})
    try:
        float(longitude)
    except ValueError:
        return jsonify({'error': 'longitude is not a valid number, provided: {}'.format(longitude)})

    try:
        # create a geocoder object
        geolocator = Nominatim(user_agent="reverse-geocode-python-api")

        # reverse geocode the coordinates
        location = geolocator.reverse(f'{latitude}, {longitude}')

        # return the location as a JSON object
        return jsonify(location.raw)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
