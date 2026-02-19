# Title: Trains 
# This program prints the data for all trains in Ireland to the console
# Using the Irish rail API to retrieve the data
# Auther: Stephen Kerr

# 1. Get the data

# Imports
import requests
import csv
from xml.dom.minidom import parseString # parse the api content (XML)

# setting up the url and get() request
url = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML'
page = requests.get(url)

# reading the XML
doc = parseString(page.content)

# Test
# print(doc.toprettyxml())

# save the data to the data to an xml file
with open("trainxml.xml","w") as xmlfp:
    doc.writexml(xmlfp)



objTrainPositionsNodes = doc.getElementsByTagName("objTrainPositions")
for objTrainPositionsNode in objTrainPositionsNodes:
    traincodenode = objTrainPositionsNode.getElementsByTagName("TrainLatitude").item(0)
    traincode = traincodenode.firstChild.nodeValue.strip()
    print (traincode)