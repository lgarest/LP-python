#!/usr/bin/python
import csv
import math
import os as _os
import re

from collections import OrderedDict
from rdf2csv import convert_to_csv, Restaurant

# distancia (A, B) = R * arccos (sen (LATA) * sen (LATB) + cos (lata) * cos (LATB) * cos (LonA-LonB))

# dict containing the restaurants
restaurants = {}


def csv_to_dict():
    """
    transforms the restaurants.csv file into a dict, with key as the name of the restaurant and value as it's attributes
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
    """ returns if the content of the string is a string """
    return re.match(r"[\"\']?\w+[\s\w*]*[\"\']?", string) is not None


def is_list(string):
    """ returns if the content of the string is a list """
    if not isinstance(string, list):
        return re.match(r"[\'\"]?\[.*\][\'\"]?", string) is not None
    return False


def is_tuple(string):
    """ returns if the content of the string is a tuple """
    if not isinstance(string, tuple):
        return re.match(r"[\'\"]?\(.*\)[\'\"]?", string) is not None
    return False


def matching(sentence, results, list_to_find=[]):
    """ *Recursive*
    returns a list matching the pattern 'sentence' into the list 'list_to_find'
    """
    try:
        if not is_string(sentence):
            sentence = eval(sentence)
    except:
        pass
    if isinstance(sentence, list):
        # list type -> OR
        for elem in sentence:
            aux = matching(elem, {}, list_to_find)
            for a in aux:
                results[a] = 1
        return results.keys()
    elif isinstance(sentence, tuple):
        # tuple type -> AND
        aux = list_to_find
        for elem in sentence:
            aux = matching(elem, {}, aux)
            results = aux
        return results
    elif isinstance(sentence, str):
        # string type -> search for the pattern
        a = search_for_word(sentence, list_to_find)
        return a
    else:
        print "invalid format:", sentence
        return


def search_for_word(pattern, list):
    """ searchs for a pattern inside a list """
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
    """ Auxiliar function calling then matching function """
    return matching(req_info, {}, restaurants)


def main():
    restaurants = csv_to_dict()
    restaurants_names = restaurants.keys()
    input_str = raw_input("What is your request?: \n")
    requested_restaurants = find_restaurants(
        eval(input_str), restaurants_names)
    print "requested_restaurants: %s" % (requested_restaurants)

if __name__ == '__main__':
    main()
