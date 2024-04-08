import json

from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://ka3akovdanil:yIp4DNZayIVeJYBw@cluster0.to2oyrf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tlsAllowInvalidCertificates=True)

db = client.hw

with open("quotes.json", "r") as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.authors.find_one({"fullname": quote["author"]})
    if author:
        db.quotes.insert_one({
            "quote": quote["quote"],
            "tags": quote["tags"],
            "author": ObjectId(author["_id"])
        })
