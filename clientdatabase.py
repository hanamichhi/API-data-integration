from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import json

#parameters to start the influxdb with python client library
token = "d-DZy3fspsSbQf5z2mBKvKsPcy8HPSRJ_7M8wFI7p_ZPKh-n7e5H832AM6LgS4TvX-MCkU-CkCGOzPBcettpuw=="
org = "Aakash.Shrestha@ui.city"
bucket = "weather"

# returns JSON object as
# a dictionary
app_version = 1.30
with open('weather.json', 'r') as file:
    json_data = json.load(file)

#initializing influxdb with parameters
with InfluxDBClient(url="http://localhost:8086", token=token, org=org, default_tags={'appversion': str(app_version)}, debug=False) as client:
    '''function to flatten the json payload for retriving the data'''
    def flatten_interval(interval):
        values = interval['values']
        values['startTime'] = interval['startTime']
        return values

    # get timelines
    timelines = json_data['data']['timelines']
    # get intervals
    intervals = list(map(lambda timeline: timeline['intervals'], timelines))
    # flatten intervals
    intervals = [flatten_interval(interval) for sublist in intervals for interval in sublist]
    #changing integer values to float to get the same data type
    for i in intervals:
        if i.get('temperature') == int(i.get('temperature')):
            i['temperature']= float(i.get('temperature'))
        if i.get('humidity') == int(i.get('humidity')):
            i['humidity'] = float(i.get('humidity'))
        if i.get('windSpeed') == int(i.get('windSpeed')):
            i['windSpeed'] = float(i.get('windSpeed'))

    # write data in the buckets
    client.write_api(write_options=SYNCHRONOUS).write(bucket=bucket,
                                                      record=intervals,
                                                      record_measurement_name="weather",
                                                      record_time_key="startTime",
                                                      record_field_keys=["humidity", "temperature", "windSpeed"])