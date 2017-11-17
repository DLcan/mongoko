# -*- coding: utf-8 -*-
# python
""" Sondurum pdf i oluşturuyor """

import datetime
from datetime import date
#import pprint
import pymongo
from pymongo import MongoClient
import mongoadr


yas_12_ay = (datetime.date.today() - datetime.timedelta(365)).isoformat()
yas_6_ay = (datetime.date.today() - datetime.timedelta(6*365/12)).isoformat()
dbsan = mongoadr.mongodbAdr()

def duzgun_tarih(tar):
    """ tarihi basarken bizim alıştığımız hale çeviriyor
        local format of date"""
    tar0 = tar.split("T")
    tar1 = tar0[0].split("-")
    tar2 = tar1[2]+"-"+tar1[1]+"-"+tar1[0]
    return tar2

yer = int(input('local veya mLAb ? Hangi database i kullanacağınızı seçin: 1/2  \n'))

if yer == 1:
    connection = MongoClient('localhost')
    c_Canlilar = connection.Koyun.Canlilar
    c_Kesilenler = connection.Koyun.Kesilenler
if yer == 2:
    connection = MongoClient(dbsan, 39122)
    c_Canlilar = connection.koyun.Canlilar
    c_Kesilenler = connection.koyun.Kesilenler

c_Canlilar.create_index([("Cinsiyet", pymongo.ASCENDING)], unique=False)
c_Canlilar.create_index([("DogumTarihi", pymongo.ASCENDING)], unique=False)
c_Canlilar.create_index([("DamizlikMi", pymongo.DESCENDING)], unique=False)

c_Canlilar.create_index([("SirtNo", pymongo.ASCENDING)], unique=True)
c_Kesilenler.create_index([("RecNo", pymongo.ASCENDING)], unique=True)

sondurum = c_Canlilar.find().sort([("Cinsiyet", pymongo.ASCENDING),
                                   ("DogumTarihi", pymongo.ASCENDING),
                                   ("DamizlikMi",pymongo.DESCENDING),
                                   ("SirtNo", pymongo.ASCENDING)])
k_cursor = c_Kesilenler.find().sort("AciklamaTarihi", pymongo.DESCENDING)


#print(yas_6_ay)
Ergindisi = c_Canlilar.find({"$and":[{"Cinsiyet":"Disi"},
                                     {"DogumTarihi":{"$lt": yas_12_ay}}]}).count()
Disikuzu = c_Canlilar.find({"$and":[{"Cinsiyet":"Disi"},
                                    {"DogumTarihi":{"$gte": yas_12_ay}}]}).count()
Damizlik = c_Canlilar.find({"$and":[{"Cinsiyet":"Erkek"},
                                    {"DamizlikMi":True}]}).count()
Adaklik = c_Canlilar.find({"$and":[{"Cinsiyet":"Erkek"},
                                   {"DogumTarihi":{"$lt": yas_6_ay}}]}).count()-Damizlik
Erkekkuzu = c_Canlilar.find({"$and":[{"Cinsiyet":"Erkek"},
                                     {"DogumTarihi":{"$gte": yas_6_ay}}]}).count()

Toplam = Ergindisi+Disikuzu+Damizlik+Adaklik+Erkekkuzu




#---------------HTML oluşturma --------------------------------
satir_basi = "    <tr>\n"
satir_sonu = "    </tr>\n"
hucre_basi = "<td>"
hucre_sonu = "</td>\n"

change_table = 0


html_out = "<html> \n"+"<body> \n"+"<head> \n <style> \n table, th, td { \n     border: 1px solid black; \n     border-collapse: collapse; \n     padding: 5px; \n     text-align: right; \n } \n "
html_out = html_out+"</style>  \n </head>  \n  <h4>Sondurum  "+duzgun_tarih(str(date.today()))+"</h4>"

#  ilk dosya oluşturuş
with open("/home/kaan/Belgeler/sondurum.html", 'w') as outfile:
    outfile.write(html_out)

#---------------------------------


left_table = " <div > <table style='width:50%;  border=0px '>\n    <tr bgcolor='#9acd32'>\n"
left_table = left_table+"      <th  colspan='2'style='text-align:center'>Durum</th>\n"
left_table = left_table+"      <th>   </th>\n"
left_table = left_table+"      <th colspan='5' style='text-align:center'>Son Kesilenler</th>\n"

left_table = left_table+"    </tr>\n"


with open("/home/kaan/Belgeler/sondurum.html", 'a') as outfile:
    outfile.write(left_table)
    line_yavru = "    <tr>\n"+hucre_basi+"<b>"+ "Ergin dişi :"+ hucre_sonu+hucre_basi+ str(Ergindisi)+ hucre_sonu
    line_yavru = line_yavru+"      <td>"+"<b>"+ " "+hucre_sonu
    line_yavru = line_yavru+"      <td>"+"<b>"+ "Sırt No"+hucre_sonu
 
    line_yavru = line_yavru+"      <td>"+"<b>"+ "Kulak No"+hucre_sonu
    line_yavru = line_yavru+"      <td>"+"<b>"+ "Adı"+hucre_sonu
    line_yavru = line_yavru+"      <td>"+"<b>"+"Kesim Tarihi"+hucre_sonu
    line_yavru = line_yavru +"    </tr>\n"
    outfile.write(line_yavru)
    for i in range(5):
        k_result = k_cursor.next()

        if i == 0:
            line_yavru = "    <tr>\n"+hucre_basi+ "<b>"+"Dişi kuzu :"+ hucre_sonu+hucre_basi+ str(Disikuzu)+ hucre_sonu
        if i == 1:
            line_yavru = "    <tr>\n"+hucre_basi+ "<b>"+"Damızlık :"+ hucre_sonu+hucre_basi+ str(Damizlik)+ hucre_sonu
        if i == 2:
            line_yavru = "    <tr>\n"+hucre_basi+ "<b>"+"Adaklık :"+ hucre_sonu+hucre_basi+ str(Adaklik)+ hucre_sonu
        if i == 3:
            line_yavru = "    <tr>\n"+hucre_basi+ "<b>"+"Erkek kuzu :"+ hucre_sonu+hucre_basi+ str(Erkekkuzu)+ hucre_sonu
        if i == 4:
            line_yavru = "    <tr>\n"+hucre_basi+ "<b>"+"Toplam :"+ hucre_sonu+hucre_basi+ "<b>"+str(Toplam)+ hucre_sonu
        line_yavru = line_yavru+"      <td>"+ ""+hucre_sonu
        line_yavru = line_yavru+"      <td>"+ str(k_result["SirtNo"])+hucre_sonu

        line_yavru = line_yavru+"      <td>"+ k_result["KulakNo"]+hucre_sonu    
        line_yavru = line_yavru+"      <td>"+ k_result["Adi"]+hucre_sonu    
        line_yavru = line_yavru+"      <td>"+"  "+duzgun_tarih(str(k_result["AciklamaTarihi"]).split(' ', 1 )[0])+hucre_sonu        
        line_yavru = line_yavru +"    </tr>\n"
        outfile.write(line_yavru)   
    outfile.write("</table></div>")    
        
#------------left table
left_table = " <div > <table style='width:95%;  border='0.1'>\n    <tr bgcolor='#9acd32'>\n"
left_table = left_table+"      <th style='text-align:left'>Kulak No</th>\n"
left_table = left_table+"      <th style='text-align:center'>Sırt No</th>\n"
left_table = left_table+"      <th style='text-align:left'>İsim</th>\n"
left_table = left_table+"      <th style='text-align:left'>D.Tarihi</th>\n"
left_table = left_table+"      <th style='text-align:left'>Annesi</th>\n"
left_table = left_table+"    </tr>\n"


#--------for breaking page    other_table

other_table = " <div  style='page-break-before: always'> <table style='width:95%;  border='0.1'>\n    <tr bgcolor='#9acd32'>\n"
other_table = other_table+"      <th style='text-align:left'>KulakNo</th>\n"
other_table = other_table+"      <th style='text-align:center'>SırtNo</th>\n"
other_table = other_table+"      <th style='text-align:left'>İsim</th>\n"
other_table = other_table+"      <th style='text-align:left'>D.Tarihi</th>\n"
other_table = other_table+"      <th style='text-align:left'>Annesi</th>\n"
other_table = other_table+"    </tr>\n"


#-------------------------------------------------------------------------------


with open("/home/kaan/Belgeler/sondurum.html", 'a') as outfile:

    for post in range(sondurum.count()):
        C_result = sondurum.next()
        if post == 0:
            outfile.write(left_table)
        if  C_result["SirtNo"] == 200:         
            outfile.write("</div></table>"+other_table)

            

        if C_result["AnaRecNo"] == 0:
            arec = ""
        else:
            arec = "R  "+str(C_result["AnaRecNo"])+"  "
        anakayit = c_Canlilar.find_one({"RecNo":C_result["AnaRecNo"]})
        if anakayit is not None:
            anasirt = str(anakayit["SirtNo"])
        else:
            if C_result["AnaAdi"] == "":
                anasirt = ""
            else:
                anasirt = "__"
        tarih = duzgun_tarih(C_result["DogumTarihi"])
        line_yavru = "    <tr>\n"+hucre_basi+C_result['KulakNo']+ hucre_sonu
        line_yavru = line_yavru+"      <td style='text-align:center'>"+"<b>"+str(C_result["SirtNo"])+"</b>"+hucre_sonu
        line_yavru = line_yavru+"      <td style='text-align:left'>"+"  "+C_result["Adi"]+hucre_sonu        
        line_yavru = line_yavru+"      <td style='text-align:left'>"+"  "+tarih+hucre_sonu

        line_yavru = line_yavru+"      <td style='text-align:left'>"+"   "+anasirt+"  "+C_result["AnaAdi"]+"  "+arec+hucre_sonu
        line_yavru = line_yavru +"    </tr>\n"
        outfile.write(line_yavru)
  
    son="</html> \n"+"</body> \n"
    outfile.write(son)

print("/home/kaan/Belgeler/sondurum.html oluşturuldu")
