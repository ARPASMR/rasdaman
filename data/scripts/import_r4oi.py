#! /usr/bin/env python
#   Gter Copyleft 2020
#   Roberto Marzocchi
# script to import generic data in rasdaman
# the run of this file is performed by entrypoint.sh file

# adeguato per python3


# library added by GTER
import os, sys, shutil, re, glob
import time
import urllib.request

from osgeo import gdal

import getopt  # per gestire gli input come variabili

from datetime import datetime, date, timedelta

spazio = "\n**************************************"

try:
    opts, args = getopt.getopt(sys.argv[1:], "mf:p:",
                               ["help", "file=", "path="])
except getopt.GetoptError:
    manual = 'import_r4oi.py -f <file raster> -p <path>'
    print(manual)
    sys.exit(2)
for opt, arg in opts:
    if opt == '-m':
        print('manual')
        sys.exit()
    elif opt in ("-f", "--file raster"):
        nomeraster = arg
    elif opt in ("-p", "--path"):
        path = arg


if nomeraster == '':
    print('ERROR: nome file mancante')
    sys.exit()
if path == '':
    print('ERROR: path mancante')
    sys.exit()

# salvo il percorso assoluto al file
pathfile='{0}/{1}'.format(path,nomeraster)


# nomefile deve essere del tipo variabile_EPSG_dataora
# dataora= YYYYMMGGHHMM

vars=nomeraster.split('_')
epsg=vars[1]
dataora=vars[0]
dato1=vars[2]
dato2=vars[3].split('.')[0]
format=vars[3].split('.')[1]
dato='{}_{}'.format(dato1,dato2)

print(dato)
print(epsg)
print(dataora)

nomecoverage='{0}_{1}'.format(dato,dataora)



#cerco la risoluzione del raster
print(spazio)
print("Cerco la risoluzione del raster")
raster = gdal.Open(pathfile)
gt =raster.GetGeoTransform()
print(gt)
# esempio stampa(258012.37107330866, 2.11668210080698, 0.0, 163176.6385398821, 0.0, -2.1168501270110074)
pixelSizeX = gt[1]
pixelSizeY =-gt[5]
print(pixelSizeX)
print(pixelSizeY)


###########################################################
# insert file giornaliero
# text='{"config": { "service_url": "http://localhost:8080/rasdaman/ows", "tmp_directory": "/tmp/", "crs_resolver": "http://localhost:8080/def/", "default_crs": "http://localhost:8080/def/crs/EPSG/0/3003",  "mock": false, "automated": true, "track_files": false },  "input": { "coverage_id": "{0}", "paths": [ "{1}{2}.txt" ] }, "recipe": { "name": "map_mosaic", "options": { "wms_import": true, "tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" }  } }'.format(nome_dato, new_percorso, nome_dato)
print(spazio)
print('Creo il json per importare il file')
text = '{{"config": {{ "service_url": "http://localhost:8080/rasdaman/ows", ' \
       '"tmp_directory": "/tmp/", "crs_resolver": "http://www.opengis.net/def/", ' \
       '"default_crs": "http://www.opengis.net/def/crs/EPSG/0/{2}",  ' \
       '"mock": false, "automated": true, "retry": true, "retries": 5, ' \
       '"track_files": false }},  ' \
       '"input": {{ "coverage_id": "{0}", "paths": [ "{1}/{3}" ] }, ' \
       '"recipe": {{ "name": "map_mosaic", "options": {{ "wms_import": true, ' \
       '"tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" }}  }} }}'.format(nomecoverage, path, epsg, nomeraster)


print(spazio)
print('Importo il file')
nomefile = "{}.json".format(dato)
out_file = open(nomefile, "w")
out_file.write(text)
out_file.close()
comando_import = '/opt/rasdaman/bin/wcst_import.sh %s' % nomefile
os.system(comando_import)

# exit()
print('Rimuovo il json precedentemente creato per importare il file')
comando_rm = "rm %s" % nomefile
os.system(comando_rm)



#################################################################
# LEGENDE
# le legende sono scritte dal basso verso l'alto
# tra 0 e X1 è l'ultimo case che si legge e poi si sale
# il valore di X1 si scrive nel penultimo case e poi  a salire
# il primo if crea la legenda per gli idi (che sono tutte uguali)
# gli altri elif creano le legende per
# rh_ana
# prec ana
#
#
#
#################################################################
if (dato2) == 'idi':
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c >={0} return {{red:139; green:35; blue:35}} " \
             "case $c>={1} return {{red:255; green:0; blue:0}} " \
             "case $c>={2} return {{red:255; green:127; blue:0}} " \
             "case $c>={3} return {{red:255; green:255; blue:0}} " \
             "case $c>={4} return {{red:50; green:205; blue:50}} " \
             "case $c>=0 return {{red:0; green:100; blue:0}} " \
             "default return {{red:255; green:255; blue:255}})".format(90, 61, 41, 25, 10)
elif (dato) == 'rh_ana':
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c >={0} return {{red:139; green:35; blue:35}} " \
             "case $c>={1} return {{red:255; green:0; blue:0}} " \
             "case $c>={2} return {{red:255; green:127; blue:0}} " \
             "case $c>={3} return {{red:255; green:255; blue:0}} " \
             "case $c>={4} return {{red:50; green:205; blue:50}} " \
             "case $c>=0 return {{red:0; green:100; blue:0}} " \
             "default return {{red:255; green:255; blue:255}})".format(425, 300, 190, 80, 40)
elif (dato) == 'prec_ana':
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c >={0} return {{red:139; green:35; blue:35}} " \
             "case $c>={1} return {{red:255; green:0; blue:0}} " \
             "case $c>={2} return {{red:255; green:127; blue:0}} " \
             "case $c>={3} return {{red:255; green:255; blue:0}} " \
             "case $c>={4} return {{red:50; green:205; blue:50}} " \
             "case $c>=0 return {{red:0; green:100; blue:0}} " \
             "default return {{red:255; green:255; blue:255}})".format(92, 89, 85, 79, 70)
#elif (dati[i]) == 'fwi':
#    j = 0
#    while j < 12:  # month counter
#        if i == mese_numero:
#            string = "switch case $c=-9999 return{{red:0; green:0; blue:0}} case $c >={0} return {{red:139; green:35; blue:35}} case $c>={1} return {{red:255; green:0; blue:0}} case $c>={2} return {{red:255; green:127; blue:0}} case $c>={3} return {{red:255; green:255; blue:0}} case $c>={4} return {{red:50; green:205; blue:50}} case $c>=0 return {{red:0; green:100; blue:0}} default return {{red:255; green:255; blue:255}})".format(
#                fwi[j][0], fwi[j][1], fwi[j][2], fwi[j][3], fwi[j][4])
#        j += 1


string_decoded = urllib.request.pathname2url(string)

# print string_decoded

comando = "wget \"http://localhost:8080/rasdaman/ows?service=WMS&version=1.3.0&request=InsertStyle&name=indici&layer={}&abstract={}&wcpsQueryFragment={}\"".format(
    nomecoverage, dato, string_decoded)
# print comando
os.system(comando)
os.system("rm ows*")


###########################################################
# riepilogo mensile
#text = '{"config": { "service_url": "http://localhost:8080/rasdaman/ows",
# "tmp_directory": "/tmp/", "crs_resolver": "http://www.opengis.net/def/",
# "default_crs": "http://www.opengis.net/def/crs/EPSG/0/3003",
# "mock": false, "automated": true, "retry": true, "retries": 5, "track_files": false },
# "input": { "coverage_id": "%s", "paths": [ "%s%s*" ] },
# "recipe": { "name": "time_series_irregular",
# "options": {"time_parameter": { "filename": { "regex": "(.*)_(.*)", "group": "2" },
# "datetime_format": "YYYYMMDD"}, "time_crs": "http://www.opengis.net/def/crs/OGC/0/AnsiDate",
# "tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" }  } }' % (nome_dato_mese, new_percorso, nome_dato_mese)
#nomefile = "%s.json" % dati[i]
#out_file = open(nomefile, "w")
#out_file.write(text)
#out_file.close()
#comando_import = '/opt/rasdaman/bin/wcst_import.sh %s' % nomefile
#os.system(comando_import)



# questa parte non serve più perchè questo comando agisce per singola mappa, non fa un ciclo
#print(spazio)
#print("%d s of pause in order to restart the importer" % interval)
#print(spazio)

#time.sleep(interval)
