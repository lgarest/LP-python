#!/usr/bin/python
# -*- coding: utf-8 -*-

header = """<html>
<head>
<meta charset="UTF-8">
<title>Luis García Estrades</title>
<style>%s</style>
</head>
<body>\n<div class="c_a">"""
style = """span{color:rgb(61, 61, 61);} .c_a{text-align: center; margin-left: auto; margin-right: auto; } .l_a{text-align: left; } .r_b{border-right:solid 1px rgb(211, 204, 204); } .b_b{border-bottom:solid 1px rgb(211, 204, 204); } .b{border:solid 1px rgb(211, 204, 204); width:100%;}
"""
close_header = "</div>\n</body>\n</html>"
span = "<span>%s: {{%s}} </span>"
requested_info = "\n<span>Requested info: '%s'</span>\n"
h1 = "\n<h1>Práctica de python de Luis García Estrades</h1>\n"
end_of_restaurant = "</table></td></tr><!-- end of restaurant with stations-->"


def html_wr(html, string, value):
    try:
        return html.replace("{{" + string + "}}", str(value))
    except:
        print "variable ", string, "doesn't exist\n"
    return


def load_template(template):
    f = open(template, 'r')
    a = f.read()
    f.close()
    return a


def write_html(input, requested, stations):
    station_raw_html = load_template("templates/station.html")
    restaurant_raw_html = load_template("templates/restaurant.html")

    f = open('restaurants.html', 'w')
    f.write(header % style)
    f.write(h1)
    f.write(requested_info % input)
    f.write('<table class="c_a">\n')
    for k, v in stations.items():
        restaurant_html = restaurant_raw_html

        # fill and add the template of the restaurant
        for attr, value in v['restaurant'].__dict__.items():
            restaurant_html = html_wr(restaurant_html, str(attr), value)
        f.write(restaurant_html)

        # fill and add the template of the stations with slots
        f.write('\n<tr><td class="c_a" colspan="4" style="background-color: rgb(144, 238, 144);"><span>Stations with slots</span></td></tr>\n')
        for station in v['with_slots']:
            station_html = station_raw_html
            for key_s, value_s in station.__dict__.items():
                station_html = html_wr(station_html, str(key_s), value_s)
            f.write(station_html)

        # fill and add the template of the stations with bikes
        f.write('\n<tr><td class="c_a" colspan="4" style="background-color: rgb(173, 216, 230);"><span>Stations with bikes</span></td></tr>\n')
        for station in v['with_bikes']:
            station_html = station_raw_html
            for key_s, value_s in station.__dict__.items():
                station_html = html_wr(station_html, str(key_s), value_s)
            f.write(station_html)
        f.write("\n<!-- insert --></table></td></tr>\n")
    f.write("</table><!-- end of restaurants -->")
    f.write(close_header)
    f.close()
