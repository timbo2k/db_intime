# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import urllib.request
import urllib.parse
from time import sleep

import requests
import pymongo
from pymongo.collection import Collection
from pymongo.results import UpdateResult
import json


API_KEY = 'CQv024gGLhn95I06cU1QruZyQZVfej9R3211'

username = "scraper"
passwort = "2gaAbay2Z5hFMys"
client = pymongo.MongoClient(f"mongodb+srv://{username}:{passwort}@cluster0.85krh.azure.mongodb.net/db?retryWrites=true&w=majority")
headers = {
        'DB-Api-Key': API_KEY,
        'Cookie': 'TS015a6fe4=0121ca1b9579397db5b6076b7b14b2cf812d1606e18e47344a7861dc0636c42e29ba104be98a095d71c4fdc2433f7bdee5065fd721'
    }


def request_api(station_eva):
    payload = {}

    url = 'https://gateway.businesshub.deutschebahn.com/ris-boardspublic/trial/v1/public/arrivals/{}'.format(station_eva)
    response = requests.request("GET", url, headers=headers, data=payload)

    arrivals: Collection = client.db["arrivals"]
    for entry in response.json()["arrivals"]:

        update_result: UpdateResult = arrivals.replace_one({"arrivalID": entry["arrivalID"]}, entry, upsert=True)
        if update_result.matched_count > 0:
            print(".", end="")
        else:
            print("!", end="")
        print("")


def req(station_ava, loop=False):
    if loop:
        print("looped request to {}".format(station_ava))
        while (True):
            request_api(station_ava)
            print("Sleep 30s")
            sleep(30)
            print("next iteration")
    else:
        print("single request to {}".format(station_ava))
        request_api(station_ava)


if __name__ == '__main__':
    # search for all stations
    payload = {}
    stationCount = 0
    offset = 275600
    largeStations = []
    f = open("stations.txt", "w")

    initial = True
    while offset < 310000:
        url = "https://gateway.businesshub.deutschebahn.com/ris-stations/v1/stop-places?offset={}&limit=100".format(offset)
        response = requests.request("GET", url, headers=headers, data=payload)

        for entry in response.json()["stopPlaces"]:
            #print(offset)
            #print(entry)
            #print("{}: {}".format(entry['evaNumber'],entry['availableTransports']))
            f.write("{}\n".format(entry))
            if initial:
                f.close()
                f = open("stations.txt", "a")

            if 'HIGH_SPEED_TRAIN' in entry['availableTransports'] or 'INTERCITY_TRAIN' in entry['availableTransports'] or 'INTER_REGIONAL_TRAIN' in entry['availableTransports']:
                largeStations.append(entry['evaNumber'])
        offset = offset + 100
        print("Offset {}: Stations: {}".format(offset,largeStations))
    print("found large stations: {}".format(len(largeStations)))
    f.close()
    # for station in largeStations:
    #     req(station)


