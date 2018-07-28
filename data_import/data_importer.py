import re
import datetime
from pymongo import MongoClient

# UNIMARC
row_separator = "\036"
unit_separator = "\037"


# file names
path_knjige = "./files/knjige.txt"
path_prefiksi = "./files/prefiksi.txt"
path_prefiksi_sr = "./files/PrefixNames_sr.properties"
path_log_err = "./files/error.log"


# database connection
try:
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.libster

except:
    print("Could not connect to the database")

file_err = open(path_log_err, "w")

file = open(path_knjige, "r")
for line in file:
    print("line:", line)
    fields = line.split(row_separator, len(line))  # splitting line into fields
    post_data = dict()  # a dictionary that holds the content of a document

    for field in fields:

        field_data_dict = dict()  # a dictionary for every field in the document

        field_name = field[0:3]  # extracting field names
        field_indicator = field[3:5]  # extracting indicator
        field_data_dict.update({"field_indicator": field_indicator})  # adding field indicator to our field data dictionary

        sub_fields = field.split(unit_separator, len(field))  # splitting field into subfields
        sub_fields.pop(0)  # removing first "subfield" because it actually isn't a subfield "- it contains field name and field indicator"

        for sub_field in sub_fields:
            subfield_name = sub_field[0:1]  # name of the subfield is the first character in the subfield
            subfield_value = sub_field[1:]  # value of the subfield are all the characters after first character (first character is subfield_name)

            if subfield_value != "" and subfield_value != "\n": # we're interested only in subfields which are not empty - no use of empty subfields
                field_data_dict.update({subfield_name:subfield_value})

        if len(field_data_dict) > 2:  # we want to add only fields which have subfields - the reason why we put >2 is because of indicator <K,V> pair.
                                      # if nothing else besides indicator exists, the dictionary will contain 2 elements
            post_data.update({field_name: field_data_dict})

    db.books.insert(post_data)


file = open(path_prefiksi, "r")
pattern = re.compile("^[A-Z][A-Z]-[0-9][0-9][0-9][a-z]")  # regex that all prefixes should match
for line in file:
    if pattern.match(line):  # if pattern matches

        prefix_dict = dict()  # a dictionary that represents a document
        prefix_pair = line.split("-", len(line))  # spliting line into <K,V> pair
        prefix_name = prefix_pair[0]  # first part of the string is name
        prefix_value = prefix_pair[1]  # the second one is value

        #  adding to the dictionary
        prefix_dict.update({"name": prefix_name})
        prefix_dict.update({"value": prefix_value})

        db.prefixes.insert(prefix_dict)  # inserting into db

    else:  # in case there was an error, the error is written into error.log file

        err = "[" + datetime.datetime.now().ctime() + "]" + " Could not write: " + line
        file_err.write("[" + datetime.datetime.now().ctime() + "]" + " Could not write: " + line)


file = open(path_prefiksi_sr, "r")
pattern = re.compile("^[A-Z][A-Z]=.*")  # regex that all prefixes should match
for line in file:
    if pattern.match(line):

        prefix_dict = dict()
        prefix_pair = line.split("=", len(line))
        prefix_name = prefix_pair[0]
        prefix_value = prefix_pair[1]

        prefix_dict.update({"name": prefix_name})
        prefix_dict.update({"value": prefix_value})

        db.prefixes_sr.insert(prefix_dict)
    else:
        file_err.write("[" + datetime.datetime.now().ctime() + "]" + " Could not write: " + line)
