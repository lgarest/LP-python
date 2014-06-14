#!/usr/bin/python

import urllib2
import xml.etree.ElementTree as ET


class Station(object):
    setters = {
        'id': int,
        'street': str,
        'lat': float,
        'long': float,
        'height': str,
        'streetNumber': str,
        'status': str,
        'slots': int,
        'bikes': int,
    }

    def __str__(self):
        return "(%s) %s" % (self.id, self.street)


class Stations(dict):

    def __init__(self):
        super(Stations, self).__init__()

    def available_stations(self):
        return [v for s, v in filter(
            lambda v: v[1].status == "OPN", self.items())]

    def empty_stations(self):
        return [v for s, v in filter(lambda v: v[1].bikes == 0, self.items())]

    def full_stations(self):
        return [v for s, v in filter(
            lambda v: v[1].slots == 0, self.items())]

    def stations_few_bikes(self):
        return [v for s, v in filter(lambda v: v[1].bikes <= 5 and
                v[1].bikes > 0, self.items())]

    def stations_few_slots(self):
        return [v for s, v in filter(
            lambda v: v[1].slots <= 5 and v[1].slots > 0, self.items())]

    def get_nearby(self, id=None):
        if not id:
            return []
        return self[id].nearbyStationList


class Extractor(object):

    def __init__(self, url=None):
        if not url:
            print "Invalid url"
            return
        self.url = url
        r = self.request_url()
        self.xml = self.extract_xml(r)

    def request_url(self):
        return urllib2.Request(self.url)

    def extract_xml(self, request):
        a = urllib2.urlopen(request)
        b = a.read()
        a.close()
        return b


def get_stations():
    url = 'http://wservice.viabicing.cat/getstations.php?v=1'
    e = Extractor(url=url)
    root = ET.fromstring(e.xml)
    stations = Stations()
    for station in root.findall('station'):
        s = Station()
        for k, funct in s.setters.items():
            s.__setattr__(k, funct(station.find(k).text))

        s.nearbyStationList = station.findtext('nearbyStationList')
        stations[s.id] = s
    return stations

if __name__ == '__main__':
    get_stations()
