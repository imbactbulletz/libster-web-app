from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import ast
from QueryBuilder import QueryBuilder

app = Flask(__name__, static_folder="./frontend", template_folder="./frontend")


app.config["MONGO_DB"] = "libster"
app.config["MONGO_URI"] = "mongodb://localhost:27017/libster"
mongo = PyMongo(app)
builder = QueryBuilder()

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


    prefixes_list = []

    for prefix in prefixes_dict:
        prefixes_list.append({'name': prefix, "value": prefixes_dict[prefix]})
    # vracamo dict prefiksa koji sadrzi odgovarajuce labele prefiksa
    return jsonify({"prefixes": prefixes_list})


@app.route("/api/getBooks", methods=["GET"])
def get_books():
    print("START")
    prefixes = mongo.db.prefixes
    books = mongo.db.books
    sentence = list()


    for argument in request.args:
        entry = list()

        parameter_data_list = request.args.getlist(argument)
        parameter_data = ast.literal_eval(parameter_data_list[0])
        print(parameter_data)
        search_term = parameter_data["prefix"]
        mapped_parameters_cursor = prefixes.find({"name": search_term}, {"value": 1, "_id": 0})
        mapped_parameters_list = list()

        for m_par in mapped_parameters_cursor:
            m_par_val = m_par["value"]
            m_par_dotified = m_par_val[:3] + '.' + m_par_val[3:]
            mapped_parameters_list.append(m_par_dotified)

        entry.append(mapped_parameters_list)
        entry.append(parameter_data["parameter"])

        sentence.append(entry)

        if "operator" in parameter_data:
            sentence.append(parameter_data["operator"])

    print(sentence)

    query = builder.build_from(sentence)


    books_cursor = books.find(query, {"_id": 0})

    output = list()
    for book in books_cursor:
        print(book)
        output.append(book)

    print("Ukupno pronadjeno:", books_cursor.count())

    print("END")

    return jsonify(output)


@app.route("/api/getMappedFields", methods=["GET"])
def get_mapped_fields():
    prefixes = mongo.db.prefixes

    for argument in request.args:
        parameter_data_list = request.args.getlist(argument)

        search_term = parameter_data_list[0]

        mapped_fields_cursor = prefixes.find({"name": search_term}, {"value": 1, "_id": 0})

        output = []

        for mapped_field in mapped_fields_cursor:
            mapped_field_val = mapped_field["value"]
            output.append({"field": mapped_field_val[:3], "subfield": mapped_field_val[3:]})

        return jsonify(mapped_fields=output)