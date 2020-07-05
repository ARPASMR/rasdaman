#! /usr/bin/env python
#   Gter Copyleft 2020
#   Roberto Marzocchi
# script to import generic data in rasdaman
# the run of this file is performed by entrypoint.sh file

# adeguato per python3


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'








# library added by GTER
import os, sys, shutil, re, glob
import time
import urllib.request
import urllib.parse

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
l=len(vars)
epsg=vars[2]
#dataora=vars[0]
dato1=vars[0]
dato2=vars[1]
dataora=vars[3].split('.')[0]
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
       '"tmp_directory": "/tmp/", "crs_resolver": "http://localhost:8080/def/", ' \
       '"default_crs": "http://localhost:8080/def/crs/EPSG/0/{2}",  ' \
       '"mock": false, "automated": true, "retry": true, "retries": 5, ' \
       '"track_files": false }},  ' \
       '"input": {{ "coverage_id": "{0}", "paths": [ "{1}/{3}" ] }}, ' \
       '"recipe": {{ "name": "map_mosaic", "options": {{ "wms_import": false, ' \
       '"tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" }}  }} }}'.format(nomecoverage, path, epsg, nomeraster)


print(spazio)
print('Importo il file')
nomefile = "{}.json".format(dato)
out_file = open(nomefile, "w")
out_file.write(text)
out_file.close()
comando_import = '/opt/rasdaman/bin/wcst_import.sh %s' % nomefile
return0=os.system(comando_import)
print(return0)

# exit()
print('Rimuovo il json precedentemente creato per importare il file')
comando_rm = "rm %s" % nomefile
os.system(comando_rm)


print('Importo il WMS')
comando="curl \"http://localhost:8080/rasdaman/ows?SERVICE=WMS&VERSION=1.3.0&REQUEST=InsertWCSLayer&WCSCOVERAGEID={0}\"".format(nomecoverage)
print(comando)
print("###############################################")
return1=os.system(comando)
print(return1)


print('Modifico la legenda del file')
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
if (dato2 == 'idi' or dato1 == 'pidi'):
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c>={0} return {{red:115; green:115; blue:115}} " \
             "case $c>={1} return {{red:141; green:141; blue:141}} " \
             "case $c>={2} return {{red:166; green:166; blue:166}} " \
             "case $c>={3} return {{red:192; green:192; blue:192}} " \
             "case $c>={4} return {{red:204; green:204; blue:204}} " \
             "case $c>={5} return {{red:217; green:217; blue:217}} " \
             "case $c>={6} return {{red:243; green:243; blue:243}} " \
             "default return {{red:255; green:255; blue:255}})".format(0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0)
elif (dato) == 'rh_ana':
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c>={0} return {{red:15; green:75; blue:158}} " \
             "case $c>={1} return {{red:18; green:88; blue:184}} " \
             "case $c>={2} return {{red:20; green:100; blue:210}} " \
             "case $c>={3} return {{red:63; green:138; blue:69}} " \
             "case $c>={4} return {{red:114; green:197; blue:94}} " \
             "case $c>={5} return {{red:184; green:255; blue:0}} " \
             "case $c>={6} return {{red:246; green:255; blue:163}} " \
             "case $c>={7} return {{red:255; green:165; blue:0}} " \
             "case $c>={8} return {{red:250; green:60; blue:60}} " \
             "case $c>={9} return {{red:0; green:0; blue:0}} " \
             "default return {{red:255; green:255; blue:255}})".format(100, 90, 80, 70, 60, 50, 40, 30, 20, 0)
elif (dato) == 'rh_hdx':   
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c>={0} return {{red:105; green:0; blue:0}} " \
             "case $c>={1} return {{red:255; green:50; blue:0}} " \
             "case $c>={2} return {{red:255; green:182; blue:0}} " \
             "case $c>={3} return {{red:255; green:255; blue:0}} " \
             "case $c>={4} return {{red:15; green:150; blue:15}} " \
             "case $c>={5} return {{red:0; green:0; blue:0}} " \
             "default return {{red:255; green:255; blue:255}})".format(54, 40, 35, 30, 20, 0)
elif (dato) == 't2m_ana' or (dato) == 't2m_bkg' :   
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c>={0} return {{red:228; green:0; blue:213}} " \
             "case $c>={1} return {{red:200; green:0; blue:170}} " \
             "case $c>={2} return {{red:173; green:0; blue:128}} " \
             "case $c>={3} return {{red:145; green:0; blue:85}} " \
             "case $c>={4} return {{red:118; green:0; blue:43}} " \
             "case $c>={5} return {{red:90; green:0; blue:0}} " \
             "case $c>={6} return {{red:105; green:0; blue:0}} " \
             "case $c>={7} return {{red:120; green:0; blue:0}} " \
             "case $c>={8} return {{red:135; green:0; blue:0}} " \
             "case $c>={9} return {{red:150; green:0; blue:0}} " \
             "case $c>={10} return {{red:165; green:0; blue:0}} " \
             "case $c>={11} return {{red:179; green:0; blue:0}} " \
             "case $c>={12} return {{red:192; green:0; blue:0}} " \
             "case $c>={13} return {{red:208; green:10; blue:0}} " \
             "case $c>={14} return {{red:225; green:20; blue:0}} " \
             "case $c>={15} return {{red:240; green:35; blue:0}} " \
             "case $c>={16} return {{red:255; green:50; blue:0}} " \
             "case $c>={17} return {{red:255; green:73; blue:0}} " \
             "case $c>={18} return {{red:255; green:96; blue:0}} " \
             "case $c>={19} return {{red:255; green:112; blue:0}} " \
             "case $c>={20} return {{red:255; green:128; blue:0}} " \
             "case $c>={21} return {{red:255; green:146; blue:0}} " \
             "case $c>={22} return {{red:255; green:164; blue:0}} " \
             "case $c>={23} return {{red:255; green:182; blue:0}} " \
             "case $c>={24} return {{red:255; green:200; blue:0}} " \
             "case $c>={25} return {{red:255; green:218; blue:0}} " \
             "case $c>={26} return {{red:255; green:236; blue:0}} " \
             "case $c>={27} return {{red:255; green:255; blue:0}} " \
             "case $c>={28} return {{red:213; green:255; blue:0}} " \
             "case $c>={29} return {{red:191; green:255; blue:0}} " \
             "case $c>={30} return {{red:170; green:255; blue:0}} " \
             "case $c>={31} return {{red:149; green:239; blue:0}} " \
             "case $c>={32} return {{red:128; green:223; blue:0}} " \
             "case $c>={33} return {{red:143; green:207; blue:36}} " \
             "case $c>={34} return {{red:157; green:192; blue:73}} " \
             "case $c>={35} return {{red:172; green:207; blue:109}} " \
             "case $c>={36} return {{red:186; green:223; blue:146}} " \
             "case $c>={37} return {{red:201; green:239; blue:182}} " \
             "case $c>={38} return {{red:215; green:255; blue:219}} " \
             "case $c>={39} return {{red:255; green:255; blue:255}} " \
             "case $c>={40} return {{red:180; green:240; blue:255}} " \
             "case $c>={41} return {{red:150; green:210; blue:250}} " \
             "case $c>={42} return {{red:120; green:185; blue:250}} " \
             "case $c>={43} return {{red:80; green:165; blue:245}} " \
             "case $c>={44} return {{red:60; green:150; blue:245}} " \
             "case $c>={45} return {{red:40; green:130; blue:240}} " \
             "case $c>={46} return {{red:30; green:110; blue:235}} " \
             "case $c>={47} return {{red:20; green:100; blue:210}} " \
             "case $c>={48} return {{red:18; green:88; blue:184}} " \
             "case $c>={49} return {{red:15; green:75; blue:158}} " \
             "case $c>={50} return {{red:13; green:63; blue:132}} " \
             "case $c>={51} return {{red:10; green:50; blue:105}} " \
             "case $c>={52} return {{red:51; green:42; blue:130}} " \
             "case $c>={53} return {{red:92; green:34; blue:155}} " \
             "case $c>={54} return {{red:133; green:26; blue:180}} " \
             "case $c>={55} return {{red:174; green:18; blue:205}} " \
             "case $c>={56} return {{red:215; green:9; blue:230}} " \
             "case $c>={57} return {{red:255; green:0; blue:255}} " \
             "case $c>={58} return {{red:255; green:26; blue:255}} " \
             "case $c>={59} return {{red:255; green:51; blue:255}} " \
             "case $c>={60} return {{red:255; green:77; blue:255}} " \
             "case $c>={61} return {{red:255; green:102; blue:255}} " \
             "case $c>={62} return {{red:255; green:128; blue:255}} " \
             "default return {{red:255; green:255; blue:255}})".format(39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23)
elif (dato) == 'prec_ana':
    string = "switch " \
             "case $c=-9999 return{{red:0; green:0; blue:0}} " \
             "case $c >={0} return {{red:174; green:18; blue:205}} " \
             "case $c>={1} return {{red:92; green:34; blue:155}} " \
             "case $c>={2} return {{red:10; green:50; blue:105}} " \
             "case $c>={3} return {{red:15; green:75; blue:158}} " \
             "case $c>={4} return {{red:20; green:100; blue:210}} " \
             "case $c>={5} return {{red:40; green:130; blue:240}} " \
             "case $c>={6} return {{red:60; green:150; blue:245}} " \
             "case $c>={7} return {{red:80; green:165; blue:245}} " \
             "case $c>={8} return {{red:120; green:185; blue:250}} " \
             "case $c>={9} return {{red:150; green:210; blue:250}} " \
             "case $c>={10} return {{red:180; green:240; blue:250}} " \
             "case $c>={11} return {{red:225; green:255; blue:255}} " \
             "default return {{red:255; green:255; blue:255}})".format(100, 63, 40, 25, 16, 10, 6.3, 4.0, 2.5, 1.6, 1.0, 0)
#elif (dati[i]) == 'fwi':
#    j = 0
#    while j < 12:  # month counter
#        if i == mese_numero:
#            string = "switch case $c=-9999 return{{red:0; green:0; blue:0}} case $c >={0} return {{red:139; green:35; blue:35}} case $c>={1} return {{red:255; green:0; blue:0}} case $c>={2} return {{red:255; green:127; blue:0}} case $c>={3} return {{red:255; green:255; blue:0}} case $c>={4} return {{red:50; green:205; blue:50}} case $c>=0 return {{red:0; green:100; blue:0}} default return {{red:255; green:255; blue:255}})".format(
#                fwi[j][0], fwi[j][1], fwi[j][2], fwi[j][3], fwi[j][4])
#        j += 1


#string_decoded = urllib.request.pathname2url(string)

#string_decoded = urllib.parse.urlencode(string, quote_via=urllib.parse.quote)
string_decoded = urllib.parse.quote(string)


# print string_decoded

print("###############################################")
html_string = "service=WMS&version=1.3.0&request=InsertStyle&name=indici&layer={}&abstract={}&wcpsQueryFragment={}".format(nomecoverage, dato, string_decoded)
html_string_decoded=urllib.parse.quote(html_string)
#comando="wget -o legenda.html \"http://localhost:8080/rasdaman/ows?{}\"".format(html_string_decoded)
#using curl instead wget
comando="curl \"http://localhost:8080/rasdaman/ows?{}\"".format(html_string)
print(comando)
print("###############################################")
return2=os.system(comando)

print('return2',return2)

os.system("rm ows*")
#os.system("rm legenda.html")

ret=return0+return1+return2

if ret==0:
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}OK: return code 0{bcolors.ENDC}{bcolors.ENDC}" )
    rm_import="rm {}/{}".format(path,nomeraster)
    rm_analisi="s3cmd --access_key=$MINIO_ACCESS_KEY --secret_key=$MINIO_SECRET_KEY --host=$MINIO_HOST:$MINIO_PORT --host-bucket=$MINIO_HOST:$MINIO_PORT --config=config_minio.txt  --force rm s3://analisi/{}".format(nomeraster)
    print(rm_import)
    print (rm_analisi)
    os.system(rm_import)
    os.system(rm_analisi)
else:
    command_logger='logger -i -p user.error -s -t PREVISORE-T -P514 -n 10.10.0.15 "Errore importazione su RASDAMAN mappa {0}. R0={1} R1={2} R2={3}"'.format(nomecoverage, return0, return1, return2)
    os.system(command_logger)
#else:
#    print(f"{bcolors.FAIL}{bcolors.BOLD}ERROR: return code{}?{bcolors.ENDC}{bcolors.ENDC} ".format(ret))



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
