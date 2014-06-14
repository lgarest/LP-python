#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import csv

from HTMLParser import HTMLParser

allrest = []


class Restaurant(object):
    owner = ""
    email = ""
    url = ""
    phone1 = ""
    phone2 = ""
    address = ""
    neighborhood = ""
    postal_code = ""
    district = ""


class MHTMLParser(HTMLParser):

    crest = Restaurant()
    ctag = ""

    def handle_starttag(self, tag, attrs):
        self.ctag = tag
        if tag == 'v:vcard':
            self.crest = Restaurant()
        elif tag == 'v:url' and len(attrs) > 0:
            self.crest.url = attrs[0][1]
        elif tag == 'rdf:description' and len(attrs) > 0:
            mail = attrs[0][1][7:]
            if re.match("[\w+\.?]+@\w+\.\w+", mail):
                self.crest.email = mail

    def handle_endtag(self, tag):
        self.ctag = ""
        if tag == 'v:vcard':
            allrest.append(self.crest)

    def handle_data(self, data):
        if self.ctag == 'v:fn':
            if not hasattr(self.crest, "name"):
                self.crest.name = data
            else:
                self.crest.name += data
        elif self.ctag == 'v:street-address':
            self.crest.address = data
        elif self.ctag == 'v:latitude':
            self.crest.latitude = data
        elif self.ctag == 'v:longitude':
            self.crest.longitude = data
        elif self.ctag == 'xv:district':
            self.crest.district = data
        elif self.ctag == 'xv:neighborhood':
            self.crest.neighborhood = data
        elif self.ctag == 'v:postal-code':
            self.crest.postal_code = data
        elif self.ctag == 'v:locality':
            self.crest.locality = data
        elif self.ctag == 'v:region':
            self.crest.region = data
        elif self.ctag == 'v:country-name':
            self.crest.country_name = data
        elif self.ctag == 'rdf:value':
            if re.match("\+\d\d\s.*", data):
                if not self.crest.phone1:
                    self.crest.phone1 = data
                else:
                    self.crest.phone2 = data
            elif re.match("[A-Z]+\s?", data):
                self.crest.owner = " ".join(re.findall("[A-Z]+", data))


def convert_to_csv(filename):
    try:
        f = open(filename + '.rdf', 'rb')
    except:
        print "The file '%s' doesn't exist" % (filename)
        return
    rdfSource = f.read()
    f.close()

    parser = MHTMLParser()
    parser.feed(rdfSource)

    nf = open(filename + '.csv', 'wb')
    csvfile = csv.writer(nf)

    csvfile.writerow(["Name"] + ["Address"] + ["Locality"] + ["Region"] + ["Country_name"] + ["Phone1"] + ["Phone2"] + ["Url"] + ["Email"] + ["Owner"] + ["Neighborhood"] + ["Postal_code"] + ["District"] + ["Latitude"] + ["Longitude"])
    for x in allrest:
        csvfile.writerow([x.name] + [x.address] + [x.locality] + [x.region] + [x.country_name] + [x.phone1] + [x.phone2] + [x.url] + [x.email] + [x.owner] + [x.neighborhood] + [x.postal_code] + [x.district] + [x.latitude] + [x.longitude])
    nf.close()


if __name__ == '__main__':
    convert_to_csv("restaurants")
