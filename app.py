from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import pprint
app = Flask(__name__, static_folder="./frontend", template_folder="./frontend")

app.config["MONGO_DB"] = "libster"
app.config["MONGO_URI"] = "mongodb://localhost:27017/libster"
mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/getPrefixes", methods=['GET'])
def get_prefix_list():
    prefixes_sr = mongo.db.prefixes_sr  # kolekcija prefixes_sr
    prefixes = mongo.db.prefixes  # kolekcija prefixes

    prefixes_cursor = prefixes.find({}, {'_id': 0, 'value': 0})  # izvrsava se query koji ne vraca id i value od dokumenta, a zatim vraca cursor
    prefixes_dict = dict()

    #  smestamo prefikse u dictionary
    for item in prefixes_cursor:
        prefixes_dict[item.get('name')] = ''


    prefixes_sr_cursor = prefixes_sr.find({}, {'_id': 0})  # izvrsava se query koji vraca sve osim id a zatim vraca cursor
    prefixes_sr_dict = dict()

    # smestamo imena prefiksa u odgovarajuci dictionary
    for item in prefixes_sr_cursor:
        prefixes_sr_dict[item.get('name')] = item.get('value')


    # ukoliko se ime prefiksa nalazi u dict koji sadrzi imena prefiksa onda smestamo ime prefiksa u prefikse
    for prefix in prefixes_dict:
        if prefix in prefixes_sr_dict:
            prefixes_dict[prefix] = prefixes_sr_dict[prefix]



    # vracamo dict prefiksa koji sadrzi odgovarajuce labele prefiksa
    return jsonify(prefixes_dict)

