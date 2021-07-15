import requests
import json
import time
import logging
from datetime import datetime
import csv
from influxdb import InfluxDBClient


logging.basicConfig(filename='my_app2.log',level=logging.INFO)


def return_count():

    # Do the request
    headers = {'Content-Type': 'application/json'}
    url = 'https://portal.rockgympro.com/portal/public/a67951f8b19504c3fd14ef92ef27454d/occupancy?&iframeid=occupancyCounter&fId=1784'
    r = requests.get(url, data= headers)

    # Parse text
    txt = r.text.replace('\n','').replace("\\",'')
    start_index = txt.find('data')+6
    end_index = txt[start_index:].find('};')+start_index-1
    subset = txt[start_index:end_index].replace("'",'"').replace(' ','')
    subset = subset[:-1]+'}'

    # Convert to json
    res_json = json.loads(subset)

    return res_json

def main():

    while True:

        try:
            logging.info('Running extraction...')
            res = return_count()
            
            for centre in res: 
                vals = res[centre]

                current = float(vals['count'])
                cap= float(vals['capacity'])
                cur_time = str(datetime.utcnow())
                client = InfluxDBClient('localhost', 8086, database='ravensdb')


                json_body = [{
                "measurement": "climbers",
                "time": cur_time,
                "tags": {
                    "centre": centre
                        },
                "fields": {
                    "value": current,
                    "capacity":cap
                }}]

                client.write_points(json_body)

            logging.info(f'Finished extraction, found {current} climbers. Sleeping...')
            time.sleep(300)
        except Exception as e:
            logging.exception(e)


if __name__ == "__main__":
    main()
