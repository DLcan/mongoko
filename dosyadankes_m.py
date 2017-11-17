# -*- coding: utf-8 -*-
# python
""" Koyun kesildiğinde makes necessary changes in MongoDb records """
from datetime import date
#import pymongo
#import json
#from datetime import datetime
#from bson.objectid import ObjectId
import datetime
import pprint
from pymongo import MongoClient
import mongoadr



TSTR = str(date.today())
#print(t)
T1 = TSTR.split("-")
#print(t1)
T2 = datetime.datetime(int(T1[0]), int(T1[1]), int(T1[2]), 0, 0)
BUGUN = T2
#SIRTNO = int(input('Sırtno girin: '))

with open('kesilenler.txt') as f:
    CONTENT = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    CONTENT = [x.strip() for x in CONTENT]

sadecelocal=2
uzakdahil=3
dbsan = mongoadr.mongodbAdr()
for kesilen in range(len(CONTENT)):
    SIRTNO = int(CONTENT[kesilen])
    #-  1.tur local, 2.nci tur uzakdb
    for yer in range(1, uzakdahil):
        if yer == 1:
            connection = MongoClient('localhost')
            c_Canlilar = connection.Koyun.Canlilar
            c_Eksikno = connection.Koyun.Eksikno
            c_Sonno = connection.Koyun.Sonno
            c_Kesilenler = connection.Koyun.Kesilenler
            print("mongodb : local  ")
        if yer == 2:
            connection = MongoClient( dbsan, 39122)
            c_Canlilar = connection.koyun.Canlilar
            c_Eksikno = connection.koyun.Eksikno
            c_Sonno = connection.koyun.Sonno
            c_Kesilenler = connection.koyun.Kesilenler
            print("mongodb : mLab  ")

        C_result = c_Canlilar.find_one({"SirtNo": SIRTNO})


        if yer == 1:
            print("local C_result:")
        if yer == 2:
            print("mLab C_result:")
        pprint.pprint(C_result)
        if C_result is not None:

            cevap1 = str(input("Kesilenlere eklensin mi?   e/h "))
            if cevap1 == 'e':
                #----- _id yi alıyor
                C_id = C_result['_id']


                #----- kesilenlere kaydetmeden önce değiştiriyor
                C_result['Aciklama'] = "Kesildi"
                C_result['AciklamaTarihi'] = BUGUN
                C_result['CanliMi'] = False

                #----- kesilenlere kaydediyor
                insert_result = c_Kesilenler.insert_one(C_result)

                print("insert_result:")
                print(insert_result)


                #----- canlilardan siliyor
                delete_result = c_Canlilar.delete_one({'_id': C_id})

                print("delete_result:")
                print(delete_result)

                #----- Eksiknolara ekliyor

                E_cursor = c_Eksikno.find()
                E_result = E_cursor.next()
                E_id = E_result['_id']

                if SIRTNO < 200:
                    c_Eksikno.update({'_id': E_id}, {'$push': {'Disi': SIRTNO}})
                if SIRTNO >= 200:
                    c_Eksikno.update({'_id': E_id}, {'$push': {'Erkek': SIRTNO}})

                #----- Sondurumdan siliyor


            else:
                print("C_result kesilmedi")
