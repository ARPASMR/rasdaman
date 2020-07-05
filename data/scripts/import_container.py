#! /usr/bin/env python
#   Gter Copyleft 2018
#   Roberto Marzocchi

#library added by GTER
import os,sys,shutil,re,glob
import time
import urllib

from datetime import datetime, date, timedelta

spazio="\n**************************************"

#data ieri
yesterday = date.today() - timedelta(1)


interval=15
#ora attuale
#dt=datetime.utcnow()
#Formatting datetime
#day_time=dt.strftime("%Y/%m/%d|%H:%M:%S.%f")
day=yesterday.strftime("%Y%m%d")
mese=yesterday.strftime("%Y%m")
mese_numero=int(yesterday.strftime("%m"))


print(day)
#print mese_numero
#exit()



#copia da milanone 
#host="10.10.0.7"
#user='meteo'
#pwd="METEO"
#path="/home/meteo/programmi/fwi_grid/indici/ana/"


new_percorso='/opt/rasdaman/fwi_grid/';

#connessione vpn cisco per server fuori da server ARPA
#connect="echo meteoaib | sudo -S vpnc arpa_lombardia"
#os.system(connect)



#comando='sshpass -p "%s" scp %s@%s:%s*%s* %s' %(pwd, user, host, path, day, new_percorso) 
#print spazio
#print comando
#print spazio
#os.system(comando)


#disconnect="echo meteoaib | sudo -S vpnc-disconnect"
#os.system(disconnect)


# import in rasdaman
dati=['bui', 'dc', 'dmc', 'ffmc', 'fwi', 'isi']

print(len(dati))

i=0



while i<len(dati):
    nome_dato="%s_%s" % (dati[i], day) # 
    nome_dato_mese="%s_%s" % (dati[i], mese)
    print spazio
    print nome_dato
    print spazio
    ###########################################################
    #insert file giornaliero
    text='{{"config": {{ "service_url": "http://localhost:8080/rasdaman/ows", "tmp_directory": "/tmp/", "crs_resolver":"http://localhost:8080/def/",'\
' "default_crs": "http://localhost:8080/def/crs/EPSG/0/3003",  "mock": false, "automated": true, "retry": true, "retries": 5, "track_files": false }},'\
'  "input": {{ "coverage_id": "{0}", "paths": [ "{1}{2}.txt" ] }}, "recipe": {{ "name": "map_mosaic",'\
' "options": {{ "wms_import": false, "tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" }}  }} }}'.format(nome_dato, new_percorso, nome_dato)
    #text='{"config": { "service_url": "http://localhost:8080/rasdaman/ows", "tmp_directory": "/tmp/", "crs_resolver": "http://www.opengis.net/def/",'\
#' "default_crs": "http://www.opengis.net/def/crs/EPSG/0/3003",  "mock": false, "automated": true, "retry": true, "retries": 5, "track_files": false },'\
#'  "input": { "coverage_id": "%s", "paths": [ "%s%s.txt" ] }, "recipe": { "name": "map_mosaic", '\
#'"options": { "wms_import": true, "tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" }  } }' % ( nome_dato, new_percorso, nome_dato)
    print(text)
    nomefile= "%s.json"% dati[i]    
    out_file = open(nomefile,"w")
    out_file.write(text)
    out_file.close()
    comando_import='/opt/rasdaman/bin/wcst_import.sh %s' %nomefile
    os.system(comando_import)
    print('IMPORT WCS TERMINATO')

    comando_wms='curl "http://localhost:8080/rasdaman/ows?SERVICE=WMS&VERSION=1.3.0&REQUEST=InsertWCSLayer&WCSCOVERAGEID={0}"'.format(nome_dato)
    return_wms=os.system(comando_wms)
    print(return_wms)
    if return_wms==0:
        print('IMPORT WMS TERMINATO')
    else:
        print('IMPORT WMS CON PROBLEMI')
        
    
    
    #exit()
    comando_rm="rm %s" %nomefile
    os.system (comando_rm)
    
    
    ###########################################################
    #legenda 
    
    #fwi cambia di mese in mese
    fwi=[[4, 7, 11, 18, 26], [ 4, 8, 13, 20, 30], [ 5, 9, 16, 27, 43], [ 6, 11, 21, 36, 58], [ 6, 13, 23, 41, 64], [ 6, 12, 22, 39, 67], [ 6, 13, 23, 41, 68], [ 7, 13, 24, 43, 73], [ 6, 12, 23, 40, 67], [ 6, 11, 19, 32, 52], [ 5, 9, 16, 26, 40], [ 5, 9, 15, 24, 37]]
    
    if (dati[i])=='bui':
        string="switch case $c=-9999 return{{red:0; green:0; blue:0}} case $c >={0} return {{red:139; green:35; blue:35}} case $c>={1} return {{red:255; green:0; blue:0}} case $c>={2} return {{red:255; green:127; blue:0}} case $c>={3} return {{red:255; green:255; blue:0}} case $c>={4} return {{red:50; green:205; blue:50}} case $c>=0 return {{red:0; green:100; blue:0}} default return {{red:255; green:255; blue:255}})".format(90,61,41,25,10)
    elif (dati[i])=='dc':
        string="switch case $c=-9999 return{{red:0; green:0; blue:0}} case $c >={0} return {{red:139; green:35; blue:35}} case $c>={1} return {{red:255; green:0; blue:0}} case $c>={2} return {{red:255; green:127; blue:0}} case $c>={3} return {{red:255; green:255; blue:0}} case $c>={4} return {{red:50; green:205; blue:50}} case $c>=0 return {{red:0; green:100; blue:0}} default return {{red:255; green:255; blue:255}})".format(425,300,190,80,40)
    elif (dati[i])=='ffmc':
        string="switch case $c=-9999 return{{red:0; green:0; blue:0}} case $c >={0} return {{red:139; green:35; blue:35}} case $c>={1} return {{red:255; green:0; blue:0}} case $c>={2} return {{red:255; green:127; blue:0}} case $c>={3} return {{red:255; green:255; blue:0}} case $c>={4} return {{red:50; green:205; blue:50}} case $c>=0 return {{red:0; green:100; blue:0}} default return {{red:255; green:255; blue:255}})".format(92,89,85,79,70)
    elif (dati[i])=='fwi':
        j=0
        while j<12: # month counter
            if i==mese_numero:
                string="switch case $c=-9999 return{{red:0; green:0; blue:0}} case $c >={0} return {{red:139; green:35; blue:35}} case $c>={1} return {{red:255; green:0; blue:0}} case $c>={2} return {{red:255; green:127; blue:0}} case $c>={3} return {{red:255; green:255; blue:0}} case $c>={4} return {{red:50; green:205; blue:50}} case $c>=0 return {{red:0; green:100; blue:0}} default return {{red:255; green:255; blue:255}})".format(fwi[j][0],fwi[j][1],fwi[j][2],fwi[j][3],fwi[j][4])
            j+=1
    elif (dati[i])=='isi':
        string="switch case $c=-9999 return{{red:0; green:0; blue:0}} case $c >={0} return {{red:139; green:35; blue:35}} case $c>={1} return {{red:255; green:0; blue:0}} case $c>={2} return {{red:255; green:127; blue:0}} case $c>={3} return {{red:255; green:255; blue:0}} case $c>={4} return {{red:50; green:205; blue:50}} case $c>=0 return {{red:0; green:100; blue:0}} default return {{red:255; green:255; blue:255}})".format(16,9,5,2,1)
        
    
    string_decoded=urllib.pathname2url(string)


    #print string_decoded

    comando = "curl \"http://localhost:8080/rasdaman/ows?service=WMS&version=1.3.0&request=InsertStyle&name=indici&layer={}&abstract={}&wcpsQueryFragment={}\"".format(nome_dato, dati[i], string_decoded)
    print comando
    return_style=os.system (comando)
    print(return_style)
    if return_style==0:
        print('STILE ASSOCIATO AL WMS CON SUCCESSO')
    else:
	print('ERRORE SU ASSOCIAZIONE STILE')
    os.system ("rm ows*")
    
    
    ###########################################################
    #riepilogo mensile
    text='{"config": { "service_url": "http://localhost:8080/rasdaman/ows", "tmp_directory": "/tmp/", "crs_resolver": "http://localhost:8080/def/",'\
' "default_crs": "http://localhost:8080/def/crs/EPSG/0/3003",  "mock": false, "automated": true, "retry": true, "retries": 5, "track_files": false },'\
' "input": { "coverage_id": "%s", "paths": [ "%s%s*" ] }, "recipe": { "name": "time_series_irregular", "options": {"time_parameter": { "filename": { "regex": "(.*)_(.*)", "group": "2" },'\
' "datetime_format": "YYYYMMDD"}, "time_crs": "http://localhost:8080/def/crs/OGC/0/AnsiDate", "tiling": "ALIGNED [0:1023, 0:1023] TILE SIZE 4194304" } } }' % ( nome_dato_mese, new_percorso, nome_dato_mese)
    print(text)
    nomefile= "%s.json"% dati[i]    
    out_file = open(nomefile,"w")
    out_file.write(text)
    out_file.close()
    comando_import='/opt/rasdaman/bin/wcst_import.sh %s' %nomefile
    os.system (comando_import)
    print spazio
    print "%d s of pause in order to restart the importer" % interval
    print spazio
    time.sleep(interval)
    i+=1
