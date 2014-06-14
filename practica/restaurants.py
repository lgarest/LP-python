#!/usr/bin/python

import csv
# import math
# import re
from collections import OrderedDict
from rdf2csv import convert_to_csv, Restaurant

# distancia (A, B) = R * arccos (sen (LATA) * sen (LATB) + cos (lata) * cos (LATB) * cos (LonA-LonB))

restaurants = {}


def csv_to_dict():
    try:
        csvfile = open('restaurants.csv', 'rb')
    except:
        convert_to_csv('restaurants')
        csvfile = open('restaurants.csv', 'rb')
    spamreader = csv.reader(csvfile)
    global_attributes = []
    d = {}
    count = 0
    for row in spamreader:
        if count == 0:
            global_attributes = [x.lower() for x in row]
        else:
            r = Restaurant()
            for i in xrange(0, len(global_attributes)):
                r.__setattr__(global_attributes[i], row[i])
            d[r.name + ', ' + str(count)] = r
        count += 1
    return OrderedDict(sorted(d.items(), key=lambda t: t[0]))


def main():
    restaurants = csv_to_dict()

    # req_info = raw_input("What is your request?: ")
    # easy_input1 = "['musical', 'Musical']"
    # easy_input2 = "('Musical', ['Bar', 'Club'])"
    # (['jsadfiop', 'jfsdakop'], ('jdsafkop', 'sdjfaiop'))
    # easy_input3 = "'Cuba'"
    # req_info = easy_input3

    # if re.match("\[(.*)\]", req_info):
    #     print "tipo 1: %s" % req_info
    # elif re.match("\((.*)\)", req_info):
    #     print "tipo 2: %s" % req_info
    # elif re.match("('\w+')", req_info):
    #     print "tipo 3: %s" % req_info
    # else:
    #     print "Invalid format"
    #     return

if __name__ == '__main__':
    main()
