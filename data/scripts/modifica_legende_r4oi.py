#! /usr/bin/env python
#   Gter Copyleft 2020

import os
import urllib.request
import datetime

#pwet_idi
#pdry_idi
#rh_idi
#t2m_idi
#prec_ana
#rh_ana
#rh_hdx
#t2m_ana
#t2m_bkg
variabile='t2m_bkg'




mydate=['2020051812', '2020070315']
fmt = "%Y%m%d%H"
hour = datetime.timedelta(hours=1)
start_time,  end_time = [datetime.datetime.strptime(d, fmt) for d in mydate]
now = start_time
while now <= end_time:
    data_ora=now.strftime(fmt)
    print(data_ora)
    now += hour
    nome='{}_{}'.format(variabile,data_ora)
    dati=variabile.split('_')
    dato2=dati[1]
    dato1=dati[1]
    dato=variabile





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



    string_decoded=urllib.request.pathname2url(string)

    comando="curl \"http://localhost:8080/rasdaman/ows?service=WMS&version=1.3.0&REQUEST=DeleteStyle&LAYER={}&name=indici\"".format(nome)
    #print(comando)
    os.system(comando)

    comando="curl \"http://localhost:8080/rasdaman/ows?service=WMS&version=1.3.0&request=InsertStyle&name=indici&layer={}&abstract={}&wcpsQueryFragment={}\"".format(nome,variabile,string_decoded)
    #print(comando)
    os.system(comando)
