from pymongo import MongoClient

def get_mongodb():
    client = MongoClient(
        "mongodb+srv://ka3akovdanil:yIp4DNZayIVeJYBw@cluster0.to2oyrf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        tlsAllowInvalidCertificates=True)

    db = client.hw
    return db


