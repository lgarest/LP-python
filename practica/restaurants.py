#!/usr/bin/python

import csv
import os as nos
# import math
import re
from collections import OrderedDict
from rdf2csv import convert_to_csv, Restaurant

# distancia (A, B) = R * arccos (sen (LATA) * sen (LATB) + cos (lata) * cos (LATB) * cos (LonA-LonB))

restaurants = {}


def csv_to_dict():
    """
    Transforms the restaurants.csv into a dict with key, the name of the restaurant and value it's attributes
    """
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


def is_string(string):
    re1 = r"[\"\']?\w+[\s\w*]*[\"\']?"
    return re.match(re1, string) is not None


def is_list(string):
    if not isinstance(string, list):
        return re.match(r"[\'\"]?\[.*\][\'\"]?", string) is not None
    return False


def is_tuple(string):
    if not isinstance(string, tuple):
        return re.match(r"[\'\"]?\(.*\)[\'\"]?", string) is not None
    return False


def matching(sentence, results, list_to_find=[]):
    """
    Returns a list matching the pattern 'sentence' into the list 'list_to_find'
    """
    try:
        if not is_string(sentence):
            sentence = eval(sentence)
    except:
        pass
    if isinstance(sentence, list):
        for elem in sentence:
            aux = matching(elem, {}, list_to_find)
            for a in aux:
                results[a] = 1
        return results.keys()
    elif isinstance(sentence, tuple):
        aux = list_to_find
        for elem in sentence:
            aux = matching(elem, {}, aux)
            results = aux
        return results
    elif isinstance(sentence, str):
        a = search_for_word(sentence, list_to_find)
        return a
    else:
        print "invalid format:", sentence
        return


def search_for_word(pattern, list):
    """
    Searchs for a pattern inside a list
    """
    results = []
    try:
        # try to descompose the pattern string
        expression = "(.*" + eval(pattern) + ".*)"
    except:
        # can't be descomposed
        expression = "(.*" + pattern + ".*)"
    for key in list:
        match = re.findall(expression, key)
        if match:
            results.append(match[0])
    return results


def find_restaurants(req_info, restaurants):
    match_list = {}
    matches = matching(req_info, match_list, restaurants)
    # print "matches: %s" % (matches)
    # print "matches: %s" % (len(matches))


def main():
    nos.system('ls')
    restaurants = csv_to_dict()
    a = restaurants.keys()
    input_str = str(raw_input("What is your request?: \n"))
    find_restaurants(eval(input_str), a)

if __name__ == '__main__':
    main()
