from time import sleep
import pymongo as pymongo
import requests
from pymongo.collection import Collection
from pymongo.results import UpdateResult
username = "scraper"
passwort = "2gaAbay2Z5hFMys"
client = pymongo.MongoClient(f"mongodb+srv://{username}:{passwort}@cluster0.85krh.azure.mongodb.net/db?retryWrites=true&w=majority")

arrivals: Collection = client.db["arrivals"]
delays: Collection = client.db["delays"]
pipeline = [
    {
        '$match': {
            '$or': [
                {
                    'timeType': 'REAL'
                }, {
                    'timeType': 'PREVIEW'
                }
            ]
        }
    }, {
        '$addFields': {
            'date': {
                '$toDate': '$time'
            },
            'dateSchedule': {
                '$toDate': '$timeSchedule'
            }
        }
    }, {
        '$addFields': {
            'dateDifferenceMs': {
                '$subtract': [
                    '$date', '$dateSchedule'
                ]
            }
        }
    }, {
        '$project': {
            'station': 1,
            'time': 1,
            'timeSchedule': 1,
            'arrivalID': 1,
            'dateDifferenceMs': 1,
            'transport': 1
        }
    }, {
        '$out': 'delays'
    }
]

while True:
    print(f"Aggregating Delays... from {arrivals.count_documents({})} arrivals...")
    arrivals.aggregate(pipeline)
    print(f"Currently {delays.count_documents({})} delays recorded...")
    sleep(60)