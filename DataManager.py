import datetime
import pymongo
import os
from bson.objectid import ObjectId


def connect_db():
    try:
        client = pymongo.MongoClient("<connection-string>")
        db = client.<database_name>
        return db["<collection_name>"]
    except Exception as error:
        print("Error while connecting to db: ", error)
        log_progress("Error while connecting to db: " + str(error), "ERROR")
        raise error


def insert_data(data):
    try:
        metadb = connect_db()
        metadb.insert_many(data.to_dict(orient="records"))
        return True
    except Exception as err:
        print("Error while inserting records: ", err)
        log_progress("Error while inserting records: " + str(err), "ERROR")
        raise err


def get_last_entry_date(source_name):
    try:
        metadb = connect_db()
        date = datetime.datetime.min

        if metadb.count_documents({}) > 0:
            temp = list(
                metadb.find(
                    {"URL": {"$regex": source_name, "$options": "i"}}, {"_id": 0, "Date": 1}).sort("Date", -1).limit(1))
            if not temp == []:
                date = temp[0]["Date"]
        return date
    except Exception as error:
        print("Error while fetching last date entry: ", error)
        log_progress("Error while fetching last date entry: " + str(error), "ERROR")
        raise error


def get_url_list(source_name):
    try:
        metadb = connect_db()

        temp = list(
            metadb.find(
                {"URL": {"$regex": source_name, "$options": "i"},
                 "Body": {"$exists": False}},
                {"_id": 1, "URL": 1}).limit(10))

        return temp
    except Exception as error:
        print("Error while fetching url list: ", error)
        log_progress("Error while fetching url list: " + str(error), "ERROR")
        raise error


def update_metadata(data):
    try:
        metadb = connect_db()
        for row in data.iterrows():
            record = row[1].to_dict()

            metadb.update_one(
                {'_id': ObjectId(record.get('_id'))},
                {'$set': {'Body': record.get('Body'), 'record_flag': 0}})
        return True
    except Exception as err:
        print("Error while updating record flag: ", err)
        log_progress("Error while updating record flag: " + str(err), "ERROR")
        raise err


def log_progress(text, log_type):
    date = datetime.datetime.today()
    filename = "incident_pipeline_log_" + str(date.year) + "_" + str(date.month) + "_" + str(date.day) + ".txt"

    if os.path.exists(filename):
        write_type = 'a'
    else:
        write_type = 'w'

    with open(filename, write_type) as file_writer:
        if log_type.lower() == "error":
            file_writer.write(str(datetime.datetime.today()) + ":: Error :: " + str(text) + "\n")
        else:
            file_writer.write(str(datetime.datetime.today()) + ":: Info :: " + str(text) + "\n")
