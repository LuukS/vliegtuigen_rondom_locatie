# -------------------------------------------------------------------------------
# Naam:		vliegtuigbewegingen2geoevent
# Doel:		Ophalen van de data van http://xml.sensornw.net/geluidsnet
#			  om daarna aanbieden aan de geoevent server voor verdere opslag
#
# Opmerkingen: De vluchtdata uit de XML wordt niet gebruikt. Het wordt initieel wel
#			  uitgelezen uit de XML (het zit in de dictionary) maar wer wordt niets
#			  mee gedaan
#
# Auteur:	  LuukS
#
# Creatie datum:	 02-04-2019
# -------------------------------------------------------------------------------

import time, urllib.request, urllib.error, urllib.parse
import xml.dom.minidom
import requests
import rijksdriehoek

dctMeetpunten = {}
dctHogeVliegtuigen = {}
dctHogeVliegtuigenFlights = {}
dctLageVliegtuigen = {}
dctLageVliegtuigenFlights = {}

blnPrintValues = False
blnPrintKeys = False
blnPrintXML = False
blnUseProxy = False


g_locatie = [155000,463000]
g_afstand = 0


def setLocatie(locatie=[0,0]):
    global g_locatie
    g_locatie = locatie


def setAfstand(afstand=0):
    global g_afstand
    g_afstand= afstand


def isBinnenGebied(x=0,y=0):
    if (x >= g_locatie[0] - g_afstand and x <= g_locatie[0] + g_afstand) and (y >= g_locatie[1] - g_afstand and y <= g_locatie[1] + g_afstand):
        return True
    else:
        return False


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def handleMPCoordinate(point):
    print((getText(point.childNodes)))


def handleHoogVliegtuig(mp):
    for m in mp:
        dctHoogVliegtuig = {}
        strCallsign = ""
        if m.getElementsByTagName("Altitude") != []:
            altitude = m.getElementsByTagName("Altitude")[0]
            dctHoogVliegtuig["Altitude"] = getText(altitude.childNodes)
            if blnPrintValues == True:
                print((getText(altitude.childNodes)))
        if m.getElementsByTagName("Speed") != []:
            speed = m.getElementsByTagName("Speed")[0]
            dctHoogVliegtuig["Speed"] = getText(speed.childNodes)
            if blnPrintValues == True:
                print((getText(speed.childNodes)))
        if m.getElementsByTagName("Callsign") != []:
            callsign = m.getElementsByTagName("Callsign")[0]
            dctHoogVliegtuig["Callsign"] = getText(callsign.childNodes)
            if blnPrintValues == True:
                print((getText(callsign.childNodes)))
            strCallsign = getText(callsign.childNodes)
        if m.getElementsByTagName("Operator") != []:
            operator = m.getElementsByTagName("Operator")[0]
            dctHoogVliegtuig["Operator"] = getText(operator.childNodes)
            if blnPrintValues == True:
                print((getText(operator.childNodes)))
        if m.getElementsByTagName("Type") != []:
            type = m.getElementsByTagName("Type")[0]
            dctHoogVliegtuig["Type"] = getText(type.childNodes)
            if blnPrintValues == True:
                print((getText(type.childNodes)))
        if m.getElementsByTagName("Registration") != []:
            registration = m.getElementsByTagName("Registration")[0]
            dctHoogVliegtuig["Registration"] = getText(registration.childNodes)
            if blnPrintValues == True:
                print((getText(registration.childNodes)))
        if m.getElementsByTagName("_Alpha") != []:
            alpha = m.getElementsByTagName("_Alpha")[0]
            dctHoogVliegtuig["_Alpha"] = getText(alpha.childNodes)
            if blnPrintValues == True:
                print((getText(alpha.childNodes)))
        if m.getElementsByTagName("_Angle") != []:
            angle = m.getElementsByTagName("_Angle")[0]
            dctHoogVliegtuig["_Angle"] = getText(angle.childNodes)
            if blnPrintValues == True:
                print((getText(angle.childNodes)))
        if m.getElementsByTagName("_Symbol") != []:
            symbol = m.getElementsByTagName("_Symbol")[0]
            dctHoogVliegtuig["_Symbol"] = getText(symbol.childNodes)
            if blnPrintValues == True:
                print((getText(symbol.childNodes)))
        if m.getElementsByTagName("_Size") != []:
            size = m.getElementsByTagName("_Size")[0]
            dctHoogVliegtuig["_Size"] = getText(size.childNodes)
            if blnPrintValues == True:
                print(getText(size.childNodes))
        if m.getElementsByTagName("__ScaleMax") != []:
            scalemax = m.getElementsByTagName("__ScaleMax")[0]
            dctHoogVliegtuig["_ScaleMax"] = getText(scalemax.childNodes)
            if blnPrintValues == True:
                print(getText(scalemax.childNodes))
        if m.getElementsByTagName("Coordinates") != []:
            coordinates = m.getElementsByTagName("Coordinates")[0]
            lon = float(getText(coordinates.childNodes).split(",")[0])
            lat = float(getText(coordinates.childNodes).split(",")[1])
            rd_from_wgs = rijksdriehoek.wgs_to_rd(lat,lon)
            x = int(rd_from_wgs[0])
            y = int(rd_from_wgs[1])
            # rd = f"POINT({x} {y})"
            # wgs84 = f"POINT({lon} {lat})"
            rd = "POINT({} {})".format(x,y)
            wgs84 = "POINT({} {})".format(lon,lat)
            dctHoogVliegtuig["Point_RD"] = rd
            dctHoogVliegtuig["Point"] = wgs84 #getText(coordinates.childNodes)
            if blnPrintValues == True:
                print(getText(coordinates.childNodes))
        if m.getElementsByTagName("_FillColor") != []:
            fillcolor = m.getElementsByTagName("_FillColor")[0]
            dctHoogVliegtuig["_FillColor"] = getText(fillcolor.childNodes)
            if blnPrintValues == True:
                print(getText(fillcolor.childNodes))
        if m.getElementsByTagName("_LineColor") != []:
            linecolor = m.getElementsByTagName("_LineColor")[0]
            dctHoogVliegtuig["_LineColor"] = getText(linecolor.childNodes)
            if blnPrintValues == True:
                print(getText(linecolor.childNodes))
        if isBinnenGebied(x,y):
            dctHogeVliegtuigen[strCallsign] = dctHoogVliegtuig


def handleLaagVliegtuig(mp):
    for m in mp:
        dctLaagVliegtuig = {}
        strCallsign = ""
        if m.getElementsByTagName("Altitude") != []:
            altitude = m.getElementsByTagName("Altitude")[0]
            dctLaagVliegtuig["Altitude"] = getText(altitude.childNodes)
            if blnPrintValues == True:
                print(getText(altitude.childNodes))
        if m.getElementsByTagName("Speed") != []:
            speed = m.getElementsByTagName("Speed")[0]
            dctLaagVliegtuig["Speed"] = getText(speed.childNodes)
            if blnPrintValues == True:
                print(getText(speed.childNodes))
        if m.getElementsByTagName("Callsign") != []:
            callsign = m.getElementsByTagName("Callsign")[0]
            dctLaagVliegtuig["Callsign"] = getText(callsign.childNodes)
            if blnPrintValues == True:
                print(getText(callsign.childNodes))
            strCallsign = getText(callsign.childNodes)
        if m.getElementsByTagName("Operator") != []:
            operator = m.getElementsByTagName("Operator")[0]
            dctLaagVliegtuig["Operator"] = getText(operator.childNodes)
            if blnPrintValues == True:
                print(getText(operator.childNodes))
        if m.getElementsByTagName("Type") != []:
            type = m.getElementsByTagName("Type")[0]
            dctLaagVliegtuig["Type"] = getText(type.childNodes)
            if blnPrintValues == True:
                print(getText(type.childNodes))
        if m.getElementsByTagName("Registration") != []:
            registration = m.getElementsByTagName("Registration")[0]
            dctLaagVliegtuig["Registration"] = getText(registration.childNodes)
            if blnPrintValues == True:
                print(getText(registration.childNodes))
        if m.getElementsByTagName("_Alpha") != []:
            alpha = m.getElementsByTagName("_Alpha")[0]
            dctLaagVliegtuig["_Alpha"] = getText(alpha.childNodes)
            if blnPrintValues == True:
                print(getText(alpha.childNodes))
        if m.getElementsByTagName("_Angle") != []:
            angle = m.getElementsByTagName("_Angle")[0]
            dctLaagVliegtuig["_Angle"] = getText(angle.childNodes)
            if blnPrintValues == True:
                print(getText(angle.childNodes))
        if m.getElementsByTagName("_Symbol") != []:
            symbol = m.getElementsByTagName("_Symbol")[0]
            dctLaagVliegtuig["_Symbol"] = getText(symbol.childNodes)
            if blnPrintValues == True:
                print(getText(symbol.childNodes))
        if m.getElementsByTagName("_Size") != []:
            size = m.getElementsByTagName("_Size")[0]
            dctLaagVliegtuig["_Size"] = getText(size.childNodes)
            if blnPrintValues == True:
                print(getText(size.childNodes))
        if m.getElementsByTagName("__ScaleMax") != []:
            scalemax = m.getElementsByTagName("__ScaleMax")[0]
            dctLaagVliegtuig["_ScaleMax"] = getText(scalemax.childNodes)
            if blnPrintValues == True:
                print(getText(scalemax.childNodes))
        if m.getElementsByTagName("Coordinates") != []:
            coordinates = m.getElementsByTagName("Coordinates")[0]
            lon = float(getText(coordinates.childNodes).split(",")[0])
            lat = float(getText(coordinates.childNodes).split(",")[1])
            rd_from_wgs = rijksdriehoek.wgs_to_rd(lat,lon)
            x = int(rd_from_wgs[0])
            y = int(rd_from_wgs[1])
            # rd = f"POINT({x} {y})"
            # wgs84 = f"POINT({lon} {lat})"
            rd = "POINT({} {})".format(x,y)
            wgs84 = "POINT({} {})".format(lon,lat)
            dctLaagVliegtuig["Point_RD"] = rd
            dctLaagVliegtuig["Point"] = wgs84 #getText(coordinates.childNodes)
            if blnPrintValues == True:
                print(getText(coordinates.childNodes))
        if m.getElementsByTagName("_FillColor") != []:
            fillcolor = m.getElementsByTagName("_FillColor")[0]
            dctLaagVliegtuig["_FillColor"] = getText(fillcolor.childNodes)
            if blnPrintValues == True:
                print(getText(fillcolor.childNodes))
        if m.getElementsByTagName("_LineColor") != []:
            linecolor = m.getElementsByTagName("_LineColor")[0]
            dctLaagVliegtuig["_LineColor"] = getText(linecolor.childNodes)
            if blnPrintValues == True:
                print(getText(linecolor.childNodes))
        if isBinnenGebied(x,y):
            dctLageVliegtuigen[strCallsign] = dctLaagVliegtuig


def handleHogeFlight(mp):
    for m in mp:
        dctHogeVliegtuigenFlight = {}
        strCallsign = ""
        if m.getElementsByTagName("rflight_id") != []:
            rflight_id = m.getElementsByTagName("rflight_id")[0]
            dctHogeVliegtuigenFlight["rflight_id"] = getText(rflight_id.childNodes)
            if blnPrintValues == True:
                print(getText(rflight_id.childNodes))
        if m.getElementsByTagName("Callsign") != []:
            callsign = m.getElementsByTagName("Callsign")[0]
            dctHogeVliegtuigenFlight["callsign"] = getText(callsign.childNodes)
            if blnPrintValues == True:
                print(getText(callsign.childNodes))
            strCallsign = getText(callsign.childNodes)
        if m.getElementsByTagName("_LineWidth") != []:
            linewidth = m.getElementsByTagName("_LineWidth")[0]
            dctHogeVliegtuigenFlight["linewidth"] = getText(linewidth.childNodes)
            if blnPrintValues == True:
                print(getText(linewidth.childNodes))
        if m.getElementsByTagName("_LineColor") != []:
            linecolor = m.getElementsByTagName("_LineColor")[0]
            dctHogeVliegtuigenFlight["linecolor"] = getText(linecolor.childNodes)
            if blnPrintValues == True:
                print(getText(linecolor.childNodes))
        if m.getElementsByTagName("_Alpha") != []:
            alpha = m.getElementsByTagName("_Alpha")[0]
            dctHogeVliegtuigenFlight["alpha"] = getText(alpha.childNodes)
            if blnPrintValues == True:
                print(getText(alpha.childNodes))
        if m.getElementsByTagName("Coordinates") != []:
            coordinates = m.getElementsByTagName("Coordinates")[0]
            lon = float(getText(coordinates.childNodes).split(",")[0])
            lat = float(getText(coordinates.childNodes).split(",")[1])
            # wgs84 = f"POINT({lon} {lat})"
            wgs84 = "POINT({} {})".format(lon,lat)
            dctHogeVliegtuigenFlight["point"] = wgs84 #getText(coordinates.childNodes)
            if blnPrintValues == True:
                print(getText(coordinates.childNodes))
        dctHogeVliegtuigenFlights[strCallsign] = dctHogeVliegtuigenFlight


def handleLageFlight(mp):
    for m in mp:
        dctLageVliegtuigenFlight = {}
        strCallsign = ""
        if m.getElementsByTagName("rflight_id") != []:
            rflight_id = m.getElementsByTagName("rflight_id")[0]
            dctLageVliegtuigenFlight["rflight_id"] = getText(rflight_id.childNodes)
            if blnPrintValues == True:
                print(getText(rflight_id.childNodes))
        if m.getElementsByTagName("Callsign") != []:
            callsign = m.getElementsByTagName("Callsign")[0]
            dctLageVliegtuigenFlight["callsign"] = getText(callsign.childNodes)
            if blnPrintValues == True:
                print(getText(callsign.childNodes))
            strCallsign = getText(callsign.childNodes)
        if m.getElementsByTagName("_LineWidth") != []:
            linewidth = m.getElementsByTagName("_LineWidth")[0]
            dctLageVliegtuigenFlight["linewidth"] = getText(linewidth.childNodes)
            if blnPrintValues == True:
                print(getText(linewidth.childNodes))
        if m.getElementsByTagName("_LineColor") != []:
            linecolor = m.getElementsByTagName("_LineColor")[0]
            dctLageVliegtuigenFlight["linecolor"] = getText(linecolor.childNodes)
            if blnPrintValues == True:
                print(getText(linecolor.childNodes))
        if m.getElementsByTagName("_Alpha") != []:
            alpha = m.getElementsByTagName("_Alpha")[0]
            dctLageVliegtuigenFlight["alpha"] = getText(alpha.childNodes)
            if blnPrintValues == True:
                print(getText(alpha.childNodes))
        if m.getElementsByTagName("Coordinates") != []:
            coordinates = m.getElementsByTagName("Coordinates")[0]
            dctLageVliegtuigenFlight["point"] = getText(coordinates.childNodes)
            if blnPrintValues == True:
                print(getText(coordinates.childNodes))
        dctLageVliegtuigenFlights[strCallsign] = dctLageVliegtuigenFlight


def handleHogeVliegtuigen(mps):
    for mp in mps:
        if mp.getElementsByTagName("Plane") != []:
            handleHoogVliegtuig(mp.getElementsByTagName("Plane"))
        if mp.getElementsByTagName("Flight") != []:
            handleHogeFlight(mp.getElementsByTagName("Flight"))


def handleLageVliegtuigen(mps):
    for mp in mps:
        if mp.getElementsByTagName("Plane") != []:
            handleLaagVliegtuig(mp.getElementsByTagName("Plane"))
        if mp.getElementsByTagName("Flight") != []:
            handleLageFlight(mp.getElementsByTagName("Flight"))


def handleMeetPunten(mps):
    for mp in mps:
        dctMeetpunt = {}
        strMp = ""
        if mp.getElementsByTagName("meetpunt") != []:
            meetpunt = mp.getElementsByTagName("meetpunt")[0]
            strMp = getText(meetpunt.childNodes)
            dctMeetpunt["meetpuntid"] = getText(meetpunt.childNodes)
            if blnPrintValues == True:
                print(getText(meetpunt.childNodes))
        if mp.getElementsByTagName("Straat") != []:
            straat = mp.getElementsByTagName("Straat")[0]
            dctMeetpunt["Straat"] = getText(straat.childNodes)
            if blnPrintValues == True:
                print(getText(straat.childNodes))
        if mp.getElementsByTagName("postcode") != []:
            postcode = mp.getElementsByTagName("postcode")[0]
            dctMeetpunt["postcode"] = getText(postcode.childNodes)
            if blnPrintValues == True:
                print(getText(postcode.childNodes))
        if mp.getElementsByTagName("plaats") != []:
            plaats = mp.getElementsByTagName("plaats")[0]
            dctMeetpunt["plaats"] = getText(plaats.childNodes)
            if blnPrintValues == True:
                print(getText(plaats.childNodes))
        if mp.getElementsByTagName("dBA") != []:
            dBA = mp.getElementsByTagName("dBA")[0]
            dctMeetpunt["dBA"] = getText(dBA.childNodes)
            if blnPrintValues == True:
                print(getText(dBA.childNodes))
        if mp.getElementsByTagName("status") != []:
            status = mp.getElementsByTagName("status")[0]
            dctMeetpunt["status"] = getText(status.childNodes)
            if blnPrintValues == True:
                print(getText(status.childNodes))
        if mp.getElementsByTagName("_Size") != []:
            size = mp.getElementsByTagName("_Size")[0]
            dctMeetpunt["_Size"] = getText(size.childNodes)
            if blnPrintValues == True:
                print(getText(size.childNodes))
        if mp.getElementsByTagName("_Alpha") != []:
            alpha = mp.getElementsByTagName("_Alpha")[0]
            dctMeetpunt["_Alpha"] = getText(alpha.childNodes)
            if blnPrintValues == True:
                print(getText(alpha.childNodes))
        if mp.getElementsByTagName("Point") != []:
            point = mp.getElementsByTagName("Coordinates")[0]
            lon = float(getText(point.childNodes).split(",")[0])
            lat = float(getText(point.childNodes).split(",")[1])
            rd_from_wgs = rijksdriehoek.wgs_to_rd(lat,lon)
            x = int(rd_from_wgs[0])
            y = int(rd_from_wgs[1])
            # rd = f"POINT({x} {y})"
            # wgs84 = f"POINT({lon} {lat})"
            rd = "POINT({} {})".format(x,y)
            wgs84 = "POINT({} {})".format(lon,lat)
            dctMeetpunt["Point_RD"] = rd
            dctMeetpunt["Point"] = wgs84 #getText(point.childNodes)
            if blnPrintValues == True:
                print(getText(point.childNodes))
        if mp.getElementsByTagName("_URL") != []:
            url = mp.getElementsByTagName("_URL")[0]
            dctMeetpunt["_URL"] = getText(url.childNodes)
            if blnPrintValues == True:
                print(getText(url.childNodes))
        if mp.getElementsByTagName("_FillColor") != []:
            fillcolor = mp.getElementsByTagName("_FillColor")[0]
            dctMeetpunt["_FillColor"] = getText(fillcolor.childNodes)
            if blnPrintValues == True:
                print(getText(fillcolor.childNodes))
        if mp.getElementsByTagName("_Symbol") != []:
            symbol = mp.getElementsByTagName("_Symbol")[0]
            dctMeetpunt["_Symbol"] = getText(symbol.childNodes)
            if blnPrintValues == True:
                print(getText(symbol.childNodes))
        if mp.getElementsByTagName("_ScaleMax") != []:
            scalemax = mp.getElementsByTagName("_ScaleMax")[0]
            dctMeetpunt["_ScaleMax"] = getText(scalemax.childNodes)
            if blnPrintValues == True:
                print(getText(scalemax.childNodes))
        if isBinnenGebied(x,y):
            dctMeetpunten[strMp] = dctMeetpunt


def handleGeluidsnet(geluidsnetxml):
    meetpunten = geluidsnetxml.getElementsByTagName("meetpunt")
    hogevliegtuigen = geluidsnetxml.getElementsByTagName("hoge_vliegtuigen")
    lagevliegtuigen = geluidsnetxml.getElementsByTagName("lage_vliegtuigen")
    handleMeetPunten(meetpunten)
    handleHogeVliegtuigen(hogevliegtuigen)
    handleLageVliegtuigen(lagevliegtuigen)


def verwerkGeluidsnet(geluidsnetxml):
    global dctMeetpunten
    global dctHogeVliegtuigen
    global dctHogeVliegtuigenFlights
    global dctLageVliegtuigen
    global dctLageVliegtuigenFlights
    dctMeetpunten = {}
    dctHogeVliegtuigen = {}
    dctHogeVliegtuigenFlights = {}
    dctLageVliegtuigen = {}
    dctLageVliegtuigenFlights = {}

    handleGeluidsnet(geluidsnetxml)
    return[dctMeetpunten,dctHogeVliegtuigen,dctLageVliegtuigen]

def main():
    nu = time.time() * 1000
    print("Bijvoorbeeld: http://www.sensornet.nl/xml/sensornet.xml?time=1344334080659")
    print("http://www.sensornet.nl/xml/sensornet.xml?time=%i" % (nu))
    strUrl = "http://www.sensornet.nl/xml/sensornet.xml?time=%i" % (nu)
    try:
        r = requests.get(url=strUrl, params=[])
        if not r.ok:
            raise Exception("URL '{}' gaf geen resultaat terug".format(strUrl))
    except:
        raise Exception
    # proxy_support = urllib2.ProxyHandler({'http': 'http://cacheflow.nic.agro.nl:8080/'})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)

    # y = urllib.request.urlopen(strUrl)
    # # print content type header
    # i = y.info()
    # if "Content-Type" in i:
    #     print("Content-Type: %s" % (i["Content-Type"]))
    # else:
    #     print("Content-Type: text/plain")
    #
    # strXML = y.read()
    # y.close()
    # strSplit = "</Geluidsnet>"
    # strHogeVliegtuigenSplit = "</hoge_vliegtuigen>"
    # strEersteDeel = str(strXML).split(strSplit)[0]
    # strTweedeDeel = str(strXML).split(strSplit)[1]
    # strGeldigeXML = strEersteDeel + strTweedeDeel + strSplit
    geluidsnet = xml.dom.minidom.parseString(r.content)
    handleGeluidsnet(geluidsnet)
    if blnPrintKeys == True:
        print("Toon waarden")
        print("Keys meetpunten:")
        print(list(dctMeetpunten.keys()))
        print(dctMeetpunten[list(dctMeetpunten.keys())[1]])
        print("Keys hoge vliegtuigen:")
        print(list(dctHogeVliegtuigen.keys()))
        print(dctHogeVliegtuigen[list(dctHogeVliegtuigen.keys())[1]])
        print("Keys vluchten hoge vliegtuigen:")
        print(list(dctHogeVliegtuigenFlights.keys()))
        print(dctHogeVliegtuigenFlights[list(dctHogeVliegtuigenFlights.keys())[1]])
        print("Keys lage vliegtuigen:")
        print(list(dctLageVliegtuigen.keys()))
        print(dctLageVliegtuigen[list(dctLageVliegtuigen.keys())[1]])
        print("Keys vluchten lage vliegtuigen:")
        print(list(dctLageVliegtuigenFlights.keys()))
        print(dctLageVliegtuigenFlights[list(dctLageVliegtuigenFlights.keys())[1]])

    # Sla de gevonden gegevens op in de GeoEvent Server
    # 1 - Meetpunten
    # Op te sturen XML:
    # <meetpunt>
    #  <meetpunt>mp247</meetpunt>
    #  <Straat>In de Pollack</Straat>
    #  <postcode>6438GG</postcode>
    #  <plaats>Oirsbeek</plaats>
    #  <dBA>50</dBA>
    #  <status>OK</status>
    #  <_Size>35</_Size>
    #  <_Alpha>57</_Alpha>
    #  <Point>
    #	<Coordinates>5.9042292,50.9481125</Coordinates>
    #  </Point>
    #  <x>5.9042292</x>
    #  <y>50.9481125</y>
    #  <_URL>http://www.sensornet.nl/project/awacs</_URL>
    #  <_FillColor>0x00ff33</_FillColor>
    #  <_Symbol>Punt</_Symbol>
    #  <_ScaleMax>5000000</_ScaleMax>
    # </meetpunt>
    strFields = "meetpuntid,Straat,postcode,plaats,dBA,status,_Size,_Alpha,Point,Point_RD,_URL,_FillColor,_Symbol,_ScaleMax"
    for key in list(dctMeetpunten.keys()):
        impl = xml.dom.minidom.getDOMImplementation()
        newdoc = impl.createDocument(None, "meetpunt", None)
        top_element = newdoc.documentElement
        dctMeetpunt = dctMeetpunten[key]
        if dctMeetpunt != {}:
            for fld in strFields.split(","):
                if fld != "Point_RD":
                    try:
                        waarde = dctMeetpunt[fld]
                    except:
                        waarde = ''
                    newtag = impl.createDocument(None, fld, None)
                    tag_element = newtag.documentElement
                    text = newtag.createTextNode(waarde)
                    tag_element.appendChild(text)
                    top_element.appendChild(tag_element)
                elif fld == "Point_RD":
                    try:
                        waarde_x = dctMeetpunt[fld].split(",")[0]
                    except:
                        waarde_x = ''
                    try:
                        waarde_y = dctMeetpunt[fld].split(",")[1]
                    except:
                        waarde_y = ''
                    try:
                        waarde_coords = dctMeetpunt[fld]
                    except:
                        waarde_coords = ''
                    newtagp = impl.createDocument(None, "Point", None)
                    top_elementp = newtagp.documentElement
                    newtagc = impl.createDocument(None, "Coordinates", None)
                    tag_elementc = newtagc.documentElement
                    textc = newtagc.createTextNode(waarde_coords)
                    tag_elementc.appendChild(textc)
                    top_elementp.appendChild(tag_elementc)
                    top_element.appendChild(top_elementp)
                    newtagx = impl.createDocument(None, "x", None)
                    tag_elementx = newtagx.documentElement
                    textx = newtagx.createTextNode(waarde_x)
                    tag_elementx.appendChild(textx)
                    top_element.appendChild(tag_elementx)
                    newtagy = impl.createDocument(None, "y", None)
                    tag_elementy = newtagy.documentElement
                    texty = newtagy.createTextNode(waarde_y)
                    tag_elementy.appendChild(texty)
                    top_element.appendChild(tag_elementy)
            # Verstuur xml naar geoevent server
            if blnPrintXML:
                print(top_element.toxml())
            top_element = None

    # 2 - Hoge vliegtuigen
    # Op te sturen XML (voor hoge en lage vliegtuigen):
    # <Plane>
    #  <Altitude>10043 m</Altitude>
    #  <Speed>866 km/h</Speed>
    #  <Callsign>THY1988</Callsign>
    #  <Operator>Turkish Airlines</Operator>
    #  <Type>Airbus A321 231</Type>
    #  <Registration>TC-JSA</Registration>
    #  <_Alpha>50</_Alpha>
    #  <_Angle>109</_Angle>
    #  <_Symbol>Plane</_Symbol>
    #  <_Size>10</_Size>
    #  <__ScaleMax>10000000</__ScaleMax>
    #  <Point>
    #	<Coordinates>6.48468,50.1293</Coordinates>
    #  </Point>
    #  <_FillColor>0x00FF00</_FillColor>
    #  <_LineColor>0x00FF00</_LineColor>
    # </Plane>
    # Op te sturen XML voor vluchten (hiermee gebeurt nog niets)
    # <Flight>
    #  <rflight_id>9186713</rflight_id>
    #  <Callsign>THY1988</Callsign>
    #  <_LineWidth>5</_LineWidth>
    #  <_LineColor>0x00FF00</_LineColor>
    #  <_Alpha>10</_Alpha>
    #  <Linestring>
    #	<Coordinates>6.484680,50.129300</Coordinates>
    #  </Linestring>
    # </Flight>

    strFields = "Altitude,Speed,Callsign,Operator,Type,Registration,_Alpha,_Angle,_Symbol,_Size,_ScaleMax,Point,_FillColor,_LineColor"
    for key in list(dctHogeVliegtuigen.keys()):
        impl = xml.dom.minidom.getDOMImplementation()
        newdoc = impl.createDocument(None, "Plane", None)
        top_element = newdoc.documentElement
        dctVliegtuig = dctHogeVliegtuigen[key]
        if dctVliegtuig != {}:
            for fld in strFields.split(","):
                if fld != "Point":
                    try:
                        waarde = dctVliegtuig[fld]
                    except:
                        waarde = ''
                    newtag = impl.createDocument(None, fld, None)
                    tag_element = newtag.documentElement
                    text = newtag.createTextNode(waarde)
                    tag_element.appendChild(text)
                    top_element.appendChild(tag_element)
                elif fld == "Point":
                    try:
                        waarde_x = dctVliegtuig[fld].split(",")[0]
                    except:
                        waarde_x = ''
                    try:
                        waarde_y = dctVliegtuig[fld].split(",")[1]
                    except:
                        waarde_y = ''
                    try:
                        waarde_coords = dctVliegtuig[fld]
                    except:
                        waarde_coords = ''
                    newtagp = impl.createDocument(None, "Point", None)
                    top_elementp = newtagp.documentElement
                    newtagc = impl.createDocument(None, "Coordinates", None)
                    tag_elementc = newtagc.documentElement
                    textc = newtagc.createTextNode(waarde_coords)
                    tag_elementc.appendChild(textc)
                    top_elementp.appendChild(tag_elementc)
                    top_element.appendChild(top_elementp)
                    newtagx = impl.createDocument(None, "x", None)
                    tag_elementx = newtagx.documentElement
                    textx = newtagx.createTextNode(waarde_x)
                    tag_elementx.appendChild(textx)
                    top_element.appendChild(tag_elementx)
                    newtagy = impl.createDocument(None, "y", None)
                    tag_elementy = newtagy.documentElement
                    texty = newtagy.createTextNode(waarde_y)
                    tag_elementy.appendChild(texty)
                    top_element.appendChild(tag_elementy)
            # Verstuur xml naar geoevent server
            if blnPrintXML:
                print(top_element.toxml())
            top_element = None

    # 3 - Lage vliegtuigen
    for key in list(dctLageVliegtuigen.keys()):
        impl = xml.dom.minidom.getDOMImplementation()
        newdoc = impl.createDocument(None, "Plane", None)
        top_element = newdoc.documentElement
        dctVliegtuig = dctLageVliegtuigen[key]
        if dctVliegtuig != {}:
            for fld in strFields.split(","):
                if fld != "Point":
                    try:
                        waarde = dctVliegtuig[fld]
                    except:
                        waarde = ''
                    newtag = impl.createDocument(None, fld, None)
                    tag_element = newtag.documentElement
                    text = newtag.createTextNode(waarde)
                    tag_element.appendChild(text)
                    top_element.appendChild(tag_element)
                elif fld == "Point":
                    try:
                        waarde_x = dctVliegtuig[fld].split(",")[0]
                    except:
                        waarde_x = ''
                    try:
                        waarde_y = dctVliegtuig[fld].split(",")[1]
                    except:
                        waarde_y = ''
                    try:
                        waarde_coords = dctVliegtuig[fld]
                    except:
                        waarde_coords = ''
                    newtagp = impl.createDocument(None, "Point", None)
                    top_elementp = newtagp.documentElement
                    newtagc = impl.createDocument(None, "Coordinates", None)
                    tag_elementc = newtagc.documentElement
                    textc = newtagc.createTextNode(waarde_coords)
                    tag_elementc.appendChild(textc)
                    top_elementp.appendChild(tag_elementc)
                    top_element.appendChild(top_elementp)
                    newtagx = impl.createDocument(None, "x", None)
                    tag_elementx = newtagx.documentElement
                    textx = newtagx.createTextNode(waarde_x)
                    tag_elementx.appendChild(textx)
                    top_element.appendChild(tag_elementx)
                    newtagy = impl.createDocument(None, "y", None)
                    tag_elementy = newtagy.documentElement
                    texty = newtagy.createTextNode(waarde_y)
                    tag_elementy.appendChild(texty)
                    top_element.appendChild(tag_elementy)
            # Verstuur xml naar geoevent server
            if blnPrintXML:
                print(top_element.toxml())
            top_element = None


if __name__ == '__main__':
    print("Welkom bij het script waarmee vliegtuigbewegingen van dit moment worden opgeslagen in de database")
    try:
        main()
    except Exception as err:
        print("Er ging iets fout")
