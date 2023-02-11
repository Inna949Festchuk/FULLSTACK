# Чтение .kml
# ИСТОЧНИК: Учебник "Learning Geospatial Analysis with Python" стр. 130
import xml.etree.ElementTree as ET
tree = ET.ElementTree(file="files/path.kml")
ns = "{http://earth.google.com/kml/2.2}"
placemark = tree.find(".//%sPlacemark" % ns)
coordinates = placemark.find("./{}LineString/{}coordinates".format(ns, ns))
vals = coordinates.text.split()
with open('files/cord_from_kml.txt', 'w') as file_cord:
    for val in vals:
        v = val.split(',')
        format = f'{v[1]} {v[0]}\n'
        file_cord.write(format)
        print(format)


   
