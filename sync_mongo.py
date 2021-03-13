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
import ast
import threading


API_KEY = 'CQv024gGLhn95I06cU1QruZyQZVfej9R3211'

username = "scraper"
passwort = "2gaAbay2Z5hFMys"
client = pymongo.MongoClient(f"mongodb+srv://{username}:{passwort}@cluster0.85krh.azure.mongodb.net/db?retryWrites=true&w=majority")

username_local = "scraper"
passwort_local = "dbHack2021"
client_local = pymongo.MongoClient(f'mongodb://{username_local}:{passwort_local}@localhost:27017/')


if __name__ == '__main__':
    collection = client.db['arrivals']
    arrivals_local: Collection = client_local.db["arrivals"]
    cursor = collection.find({})
    for entry in cursor:
        print(entry)
        update_result: UpdateResult = arrivals_local.replace_one({"arrivalID": entry["arrivalID"]}, entry, upsert=True)
        if update_result.matched_count > 0:
            print(".", end="")
        else:
            print("!", end="")


