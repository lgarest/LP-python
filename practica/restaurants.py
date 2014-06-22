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


# def to_string(string):
#     if is_string(string):
#         re1 = r"(\w+[\s\w+]*)"
#         return re.findall(re1, string)[0]
#     return string


def is_list(string):
    if not isinstance(string, list):
        return re.match(r"[\'\"]?\[.*\][\'\"]?", string) is not None
    return False


# def to_list(string):
#     if is_list(string):
#         ret = re.match(r"[\'\"]?\[(.*)\][\'\"]?", string)
#         if ret:
#             return [to_string(a) for a in ret.group(1).split(',')]
#     return


def is_tuple(string):
    print "hola"
    if not isinstance(string, tuple):
        return re.match(r"[\'\"]?\(.*\)[\'\"]?", string) is not None
    return False


# def to_tuple(string):
#     if is_tuple(string):
#         # ret = re.match(r"[\'\"]?\((.*)\)[\'\"]?", string)
#         raw = string[1:-1]
#         # print "raw:", (raw.split(', '))
#         print eval(string)
#         # for a in raw.split(', '):
#         #     print "a: *%s*" % (a)
#         # if is_string(raw.split(', ', 1)[0]):
#         #     print "raw.split(', ', 1):", (raw.split(', ', 1))
#         # print "ret:", (ret.group(1))
#         # if ret:
#         #     x = []
#         #     print ret.group(1)
#         #     ret1 = re.findall("\((.*)\)", ret.group(1))
#         #     # print ret1[0].split(', ')
#         #     # if is_string(a):
#         #     #         b = to_string(a)
#         #     #         x.append(b)
#         #     for a in ret1[0].split(', ',1):
#         #         print "a: *%s*" % (to_string(a))
#         #         x.append(a)
#         #     # for a in ret.group(1).split(', '):
#         #     #     print "a:", (a)
#         #         # if is_string(a):
#         #         #     b = to_string(a)
#         #         #     x.append(b)
#         #         # elif a[0] == "[":
#         #         #     print a[1:]
#         #         #     c1 += 1
#         #         #     # list mode
#         #         # elif a[0] == "]":
#         #         #     c1 -= 1
#         #         # elif a[0] == "(":
#         #         #     print a[1:]
#         #         #     # tuple mode
#         #         #     c2 += 1
#         #         # elif a[0] == ")":
#         #         #     c2 -= 1
#         #     return tuple(x)
#     return


# def matching(string, results, list_to_find=[]):
#     """ Devuelve una lista con los resultados de buscar el string 'string' en la lista 'list_to_find' """
#     print "string: |%s|" % (string)
#     rex_or = re.findall(r"^[\",\']*\[(.*)\][\",\']*$", string)
#     rex_and = re.findall(r"^[\",\']*\((.*)\)[\",\']*$", string)
#     single_word = re.findall(r"[\",\']*(\w+)[\",\']*", string)
#     if rex_or:
#         rex_or = rex_or[0]
#         cleaned_list = [to_string(x) for x in rex_or.split(',')]
#         print cleaned_list
#         for elem in cleaned_list:
#             pene = matching(elem, results, list_to_find)
#             print "pene: |%s|" % (pene)
#             if isinstance(pene, str):
#                 print "__string nigro"
#             print "elem:", (elem)
#             aux = search_for_word(elem, list_to_find)
#             for a in aux:
#                 results[a] = 1
#             print "OR"
#         print "results: %d" % (len(results))
#         return results.keys()

#     elif rex_and:
#         print rex_and
#         rex_and = rex_and[0]
#         cleaned_list = [to_string(x) for x in rex_and.split(',')]
#         print cleaned_list
#         aux = list_to_find
#         for elem in cleaned_list:
#             aux = search_for_word(elem, aux)
#             results = aux
#             print "AND"
#         print "results: %d" % (len(results))
#         return results

#     elif single_word:
#         single_word = single_word[0]
#         print "single_word: |%s|" % (single_word)
#         a = search_for_word(single_word, list_to_find)
#         return a

#     else:
#         print "Invalid format:", string
#         return


def matching(sentence, results, list_to_find=[]):
    """ Devuelve una lista con los resultados de buscar el string 'string' en la lista 'list_to_find' """
    try:
        if not is_string(sentence):
            sentence = eval(sentence)
    except:
        pass
    print "sentence:", sentence
    if isinstance(sentence, list):
        print "\nis_list:", sentence
        for elem in sentence:
            print "elem:", (elem)
            print "type(elem):", (type(elem))
            aux = matching(elem, [], list_to_find)
            # aux = search_for_word(elem, list_to_find)
            for a in aux:
                results[a] = 1
        return results.keys()

    elif isinstance(sentence, tuple):
        print "\nis_tuple:", sentence
        aux = list_to_find
        for elem in sentence:
            print "elem:", (elem)
            print "type(elem):", (type(elem))
            aux = matching(elem, [], aux)
            print "aux:", (aux)
            results = aux
        return results

    elif isinstance(sentence, str):
        print "\nis_string:", sentence
        a = search_for_word(sentence, list_to_find)
        for an in a:
            print "an:", (an)
        return a
    else:
        print "Invalid format:", sentence
        return


def search_for_word(pattern, list):
    results = []
    for key in list:
        expression = "(.*" + pattern + ".*)"
        match = re.findall(expression, key)
        if match:
            results.append(match[0])
    return results


def find_restaurants(req_info, restaurants):
    match_list = {}
    # a = search_for_word("Musical", restaurants.keys())
    matches = matching(req_info, match_list, restaurants)
    # print "matches:", (match_list)
    print matches
    print "matches: %d" % (len(matches))


def main():
    nos.system('ls')
    restaurants = csv_to_dict()
    a = restaurants.keys()
    # print to_tuple('(("A", "B"), ("C", ("D", "F")), "E")')
    # print to_string("'Cuba'")
    # print to_string('"|bar raccuda"')
    input_str = str(raw_input("What is your request?: \n"))
    # input_str = ."['King', 'Universal']"
    # print input_str
    # if is_string(input_str):
    #     print "str:", (input_str)
    # print "tolist_", to_list(input_str)
    # print "totuple_", to_tuple(input_str)
    find_restaurants(eval(input_str), a)
    # find_restaurants(input_str, a[:200])

if __name__ == '__main__':
    main()
