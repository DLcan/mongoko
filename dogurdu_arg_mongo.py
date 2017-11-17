# -*- coding: utf-8 -*-
# python

import pymongo
import pprint
from datetime import datetime
from datetime import date
from pymongo import MongoClient
import argparse
import mongoadr

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--sirtno")
ap.add_argument("-r", "--recno")
ap.add_argument('integers', metavar='N', type=int , nargs='+',
                    help='-s for sirtno, -r for recno, ilk sayı yeni doğan erkek, ikinci sayı yeni doğan dişi')

args = ap.parse_args()
#print(args)
#print (args.integers[0])
#python arg.py -r 623 1 1
#Namespace(integers=[1, 1], recno='623', sirtno=None)
if len(args.integers)!=2 or ((args.sirtno is None)and(args.recno is None)):
    durum=False
else:
    durum=True

yeni_kayit = {}
erkeksay = 0
disisay = 0

sonDisiNo  = 0
sonErkekNo = 0
sonRec   = 0      
AnaRecNo = 0
AnaAdi = ""

donem = "10_2017"   #-------------yeni dogumlar döneminde değişecek-----
babalarrecno = [430,441,455]                   #---- ---------------------
babaadlari = ["AB","AO","ABA"]                 #---- ----------------------

bugun = str(date.today())

#---yeni doğanlara isim koymak için isim listesi alıyor--
with open('/home/kaan/Belgeler/Data/Koyun/isimler.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 


def  yeni_dogum_olustur(cinsiyet):
   
    D_result = c_Dogumlar.insert_one({
    "Donem":donem,
    "AnaRecNo": AnaRecNo,
    "AnaAdi":AnaAdi ,
    "Adi":  yeni_kayit["Adi"] ,
    "SirtNo": yeni_kayit["SirtNo"],           
    "RecNo": sonRec,
    "KulakNo": "TR77-______",
    "BabalarRecNo": babalarrecno,
    "BabaAdlari" : babaadlari, 
    "Cinsiyet":cinsiyet,
    "DogumTarihi": bugun,
         
    })
    
    return D_result


def bos_kayit_olustur(cinsiyet):
    global yeni_kayit,sonRec,sonErkekNo,sonDisiNo
    if cinsiyet=="Disi":
        yeni_kayit["KocaVerilme"] = False
        if len(E_result["Disi"])>0:
            yeni_kayit["SirtNo"] = E_result["Disi"].pop(-1)
            c_Eksikno.update( { _id: E_result["_id"] }, { '$pop': {"Disi": 1 } } ) #Eksikno dan sayı aldığımız için eksiliyor
        else:
            sonDisiNo = sonDisiNo +1
            yeni_kayit["SirtNo"] = sonDisiNo
            c_Sonno.update( { _id: S_result["_id"] }, { '$set': { "Disi": sonDisiNo } } )#Sonnoyu kullandığımız için sonno[Disi] 1 artıyor
               
    if cinsiyet=="Erkek":
        yeni_kayit["DamizlikMi"] = False
        if len(E_result["Erkek"])>0:
            yeni_kayit["SirtNo"] = E_result["Erkek"].pop(-1)
            c_Eksikno.update( { '_id': E_result["_id"] }, { '$pop': { "Erkek": 1 } } )#Eksikno dan sayı aldığımız için eksiliyor
        else:
            sonErkekNo = sonErkekNo +1
            yeni_kayit["SirtNo"] = sonErkekNo
            c_Sonno.update( { '_id': S_result["_id"] }, { '$set': { "Erkek": sonErkekNo } } )#Sonnoyu kullandığımız için sonno[Erkek] 1 artıyor
               
               

    sonRec = sonRec + 1
    c_Sonno.update( { '_id': S_result["_id"] }, { '$set': { "RecNo": sonRec } } )#Sonnoyu kullandığımız için sonno[RecNo] 1 artıyor
               
    yeni_kayit["Adi"] =  content[sonRec-495]

    yeni_kayit["CanliMi"] = True
    
    yeni_kayit["AciklamaTarihi"] = bugun
    yeni_kayit["BabalarRecNo"] = babalarrecno
    yeni_kayit["BabaAdlari"] = babaadlari
    yeni_kayit["RecNo"] =  sonRec
    yeni_kayit["Cinsiyet"] = cinsiyet
    yeni_kayit["AnaAdi"] = AnaAdi
    yeni_kayit["AnaRecNo"] = AnaRecNo
    yeni_kayit["KulakNo"] = "TR77-______"
    yeni_kayit["DogumTarihi"] = bugun
    yeni_kayit["Aciklama"] = "Arazide dogdu"
    
    C_update_result = c_Canlilar.insert_one({
        "Adi":  yeni_kayit["Adi"] ,
        "SirtNo": yeni_kayit["SirtNo"],           
        "CanliMi":True,

        "RecNo": sonRec,
        "KulakNo": "TR77-______",
        "AnaRecNo": AnaRecNo,
        "AnaAdi":AnaAdi,
        "BabalarRecNo": babalarrecno,
        "BabaAdlari" : babaadlari, 
        "Cinsiyet":cinsiyet,
        "DogumTarihi": bugun,
       
        "Aciklama": "Arazide dogdu",
        "AciklamaTarihi":bugun ,
        
        "KocaVerilme": False,
        "DamizlikMi": False
        })
    return C_update_result  
               
#-------------end of def bos_kayit_olustur------------    

#yer = int(input ('local veya mLAb ? Hangi database i kullanacağınızı seçin: 1/2  \n'))
for yer in range(1,3):
    if yer ==1:
        connection = MongoClient('localhost')
        c_Canlilar = connection.Koyun.Canlilar
        c_Eksikno = connection.Koyun.Eksikno
        c_Sonno = connection.Koyun.Sonno
        c_Dogumlar = connection.Koyun.Dogumlar
        print("mongodb : local  ")
    if yer ==2:
        connection = MongoClient(mongodbAdr, 39122)
        c_Canlilar = connection.koyun.Canlilar
        c_Eksikno = connection.koyun.Eksikno
        c_Sonno = connection.koyun.Sonno
        c_Dogumlar  = connection.koyun.Dogumlar   
        print("mongodb : mLab  ")

    #cevap = int(input ('Doguran anayı bulmak için arama yöntemi seçin : Sırtno/RecNo/AnaRecNo : 1/2/3 '))

    bulundu = False
    #-----SırtNo
    if durum  and args.recno is None:
        sirtno = int(args.sirtno)

        #---Canlilar-----

        C_result = (c_Canlilar.find_one({"SirtNo": sirtno}))

        if C_result is not None:
            print ("C_result:")
            pprint.pprint (C_result)
            bulundu = True
        else:
            print("%s sırtnolu canlı hayvan bulunmuyor"%sirtno)



    #-----RecNo
    if durum  and args.sirtno is None:

        recno = int(args.recno)

        #---Canlilar-----

        C_result = (c_Canlilar.find_one({"RecNo": recno}))

        if C_result is not None:
            print ("C_result:")
            pprint.pprint (C_result)
            bulundu = True

        else:
            print("%s Recnolu canlı hayvan bulunmuyor"%recno)


    if bulundu :

        #---Dogumlar-----



        #---Eksikno-----

        E_result = (c_Eksikno.find_one())

        #---Sonno-----

        S_result = (c_Sonno.find_one())

        sonDisiNo  = int(S_result["Disi"])  #--dişilerin otomatik verilen son sırt numarası
        sonErkekNo = int(S_result["Erkek"]) #--erkeklerin otomatik verilen son sırt numarası
        sonRec     = int(S_result["RecNo"])   #--son verilen RecNo


        erkeksay = int(args.integers[0])
        disisay = int(args.integers[1])


        AnaRecNo = C_result["RecNo"]
        AnaAdi = C_result["Adi"]    

        if (erkeksay+disisay)>0:
            #Ana kaydını update
            Ana_result = c_Canlilar.update_one({"_id": C_result["_id"]}, {'$set': {'Aciklama': "Dogurdu",  "AciklamaTarihi": bugun ,"SonDogurmaTarihi":bugun}})



            if erkeksay > 0:
                #erkekler için loop 
                for i_e in range(erkeksay):
                    cinsiyet = "Erkek"
                    bos_kayit_olustur(cinsiyet)
                    yeni_dogum_olustur(cinsiyet)#Dogumlara kayıt ekliyor



            if disisay > 0:               
                #disiler için loop 
                for i_d in range(disisay): 
                    cinsiyet = "Disi"
                    bos_kayit_olustur(cinsiyet)
                    yeni_dogum_olustur(cinsiyet)#Dogumlara kayıt ekliyor







