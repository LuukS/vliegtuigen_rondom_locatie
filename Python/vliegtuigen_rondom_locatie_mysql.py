# -------------------------------------------------------------------------------
# Naam:		        vliegtuigen_rondom_locatie_mysql
# Doel:		        Ophalen van de data van http://xml.sensornw.net/geluidsnet
#		            om daarna de vlietguigen, welke in een opgegeven gebied rondom
#	    	        een opgegeven locatie vallen, op te slaan in een MySQL database
#
# Opmerkingen:      De vluchtdata en de meetgegevens uit de XML worden niet gebruikt.
#                   De data wordt initieel wel uitgelezen uit de XML (het zit in de
#                   dictionary) maar er wordt niets mee gedaan
#
# Auteur:	        LuukS
#
# Creatie datum:	24-04-2024
# -------------------------------------------------------------------------------
import time
import xml.dom.minidom

import rijksdriehoek as rd
import vliegtuigbewegingen as vb
import requests

from connection import Config
if Config.database.lower() != 'mysql':
    exit("Configuratie is niet voor MySQL gemaakt.")
elif Config.database.lower() == 'sqlite':
    exit("Configuratie is voor SQLite gemaakt.")

from connection import Connection

dctMeetpunten = {}
dctHogeVliegtuigen = {}
dctHogeVliegtuigenFlights = {}
dctLageVliegtuigen = {}
dctLageVliegtuigenFlights = {}

blnPrintValues = False
blnPrintKeys = False
blnPrintXML = False
blnUseProxy = False

timeout_seconds = 5
locatie = [114566,481821] # Dit is 5km naar links en 5 km naar boven van ons adres
afstand = 10000
sensornetUrl = "http://www.sensornet.nl/xml/sensornet.xml?time="
nu = time.time() * 1000

def haalSensorData(strUrl=None):
    if strUrl is not None:
        try:
            r = requests.get(url=strUrl, params=[],timeout=timeout_seconds)
            if not r.ok:
                raise Exception(f"URL '{strUrl}' gaf geen resultaat terug")
            return r
        except:
            raise Exception(f"De url {strUrl} bestaat niet, of reageert niet binnen {timeout_seconds} seconden")
    else:
        return None


def start():
    # coord_rd = [[121687, 487484], # Amsterdam
    #             [ 92565, 437428], # Rotterdam
    #             [176331, 317462]] # Maastricht
    #
    # coord_wgs = [[52.37422, 4.89801], # Amsterdam
    #             [51.92183, 4.47959], # Rotterdam
    #             [50.84660, 5.69006]] # Maastricht
    #
    # for x, y in coord_rd:
    #     print (rd.rd_to_wgs(x,y))
    #
    # for phi, lam in coord_wgs:
    #     print (rd.wgs_to_rd(phi, lam))
    global timeout_seconds
    global locatie
    global afstand
    global sensornetUrl
    global nu
    global dctMeetpunten
    global dctHogeVliegtuigen
    global dctHogeVliegtuigenFlights
    global dctLageVliegtuigen
    global dctLageVliegtuigenFlights

    print("start")
    try:
        conn = Connection()
        cur = conn.db.cursor()
        if conn.isConnected():
            cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'test_db' AND table_name in('hoge_vliegtuigen','lage_vliegtuigen','meetpunten');""")
            listOfTables = cur.fetchall()
            if len(listOfTables) != 3:
                exit("Niet alle benodigde tabellen zijn beschikbaar in de database")
            else:
                print(f"De benodige {len(listOfTables)} tabellen zijn gevonden: {listOfTables}")
    except Exception as e:
        print(e)
        print("Geen verbinding met MySQL kunnen maken")
        return False

    print(timeout_seconds)
    print(locatie)
    print(rd.rd_to_wgs(locatie[0], locatie[1]))
    print(afstand)

    vb.setAfstand(afstand)
    vb.setLocatie(locatie)
    print(vb.isBinnenGebied(119566,486821))
    strUrl = "http://www.sensornet.nl/xml/sensornet.xml?time=%i" % (nu)
    print(f"URL: {strUrl}")
    try:
        r = haalSensorData(strUrl)
        if r is not None:
            sensornetData = xml.dom.minidom.parseString(r.content)
        else:
            print("Geen url opgegeven")
    except Exception as err:
        print(err)
        return False

    dctMeetpunten = {}
    dctLageVliegtuigen = {}
    dctMeetpunten = {}
    dctLageVliegtuigenFlights = {}
    dctHogeVliegtuigenFlights = {}
    dctMeetpunten,dctHogeVliegtuigen,dctLageVliegtuigen = vb.verwerkGeluidsnet(sensornetData)

    print(f"Meetpunten: {dctMeetpunten}")
    print(f"Hoge vliegtuigen: {dctHogeVliegtuigen}")
    print(f"Lage vliegtuigen: {dctLageVliegtuigen}")

    # INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
    strFieldsMP = "meetpuntid,Straat,postcode,plaats,dBA,status,_Size,_Alpha,Point_RD,Point,_URL,_FillColor,_Symbol,_ScaleMax"
    strFieldsV = "Altitude,Speed,Callsign,Operator,Type,Registration,_Alpha,_Angle,_Symbol,_Size,Point_RD,Point,_FillColor,_LineColor"

    strInsertMP = f"INSERT INTO meetpunten ({strFieldsMP}) VALUES ('UB081','Uiterweg','1431 AS','Aalsmeer',46,'OK',31,55,'110342,475386','4.733033,52.264695','http://www.sensornet.nl/project/aalsmeer/aalsmeer','0x00ff66','Punt',5000000)"
    strInsertV = f"INSERT INTO lage_vliegtuigen ({strFieldsV}) VALUES ('30 m','81 km/h','KLM974','','','',50,171,'Plane',10,'108915,483983','4.710959, 52.341841','0x000000','0x000000')"

    for key in list(dctMeetpunten.keys()):
        dctMeetpunt = dctMeetpunten[key]
        if dctMeetpunt != {}:
            strValuesMP = ""
            for fld in strFieldsMP.split(","):
                if fld == "postcode":
                    strValuesMP += f"'{dctMeetpunt[fld].replace(' ','')}',"
                else:
                    strValuesMP += f"'{dctMeetpunt[fld]}',"
            strInsertMP = f"INSERT INTO meetpunten ({strFieldsMP}) VALUES ({strValuesMP[0:-1]})"
            # print(strInsertMP)
            cur.execute(strInsertMP)
            conn.commit()
            # print(cur.lastrowid)

    for key in list(dctLageVliegtuigen.keys()):
        dctVliegtuig = dctLageVliegtuigen[key]
        if dctVliegtuig != {}:
            strValuesLV = ""
            for fld in strFieldsV.split(","):
                strValuesLV += f"'{dctVliegtuig[fld]}',"
            strInsertLV = f"INSERT INTO lage_vliegtuigen ({strFieldsV}) VALUES ({strValuesLV[0:-1]})"
            # print(strInsertLV)
            cur.execute(strInsertLV)
            conn.commit()
            # print(cur.lastrowid)

    for key in list(dctHogeVliegtuigen.keys()):
        dctVliegtuig = dctHogeVliegtuigen[key]
        if dctVliegtuig != {}:
            strValuesHV = ""
            for fld in strFieldsV.split(","):
                strValuesHV += f"'{dctVliegtuig[fld]}',"
            strInsertHV = f"INSERT INTO hoge_vliegtuigen ({strFieldsV}) VALUES ({strValuesHV[0:-1]})"
            # print(strInsertHV)
            cur.execute(strInsertHV)
            conn.commit()
            # print(cur.lastrowid)
    cur = None
    conn.close()
    conn = None
    dctMeetpunten = {}
    dctHogeVliegtuigen = {}
    dctHogeVliegtuigenFlights = {}
    dctLageVliegtuigen = {}
    dctLageVliegtuigenFlights = {}
    print("Succesvol data opgehaald en verwerkt")
    return True


if __name__ == "__main__":
    start()
