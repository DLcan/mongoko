# -*- coding: utf-8 -*-
# python

import pymongo
import pprint
from pymongo import MongoClient
import mongoadr

dbsan = mongoadr.mongodbAdr()
yer = int(input ('local veya mLAb ? Hangi database i kullanacağınızı seçin: 1/2  \n'))
if yer ==1:
    connection = MongoClient('localhost')
    c_Canlilar = connection.Koyun.Canlilar
if yer ==2:
    connection = MongoClient(dbsan, 39122)
    c_Canlilar = connection.koyun.Canlilar
    print(c_Canlilar)

    
cevap = int(input ('Sırtno/RecNo/AnaRecNo seçin: 1/2/3  \n'))

#-----SırtNo
if cevap==1:
    sirtno = int(input ('Sırtno girin: '))

    #---Canlilar-----

    C_result = (c_Canlilar.find_one({"SirtNo": sirtno}))

    if C_result is not None:
        print ("C_result:")
        pprint.pprint (C_result)

    else:
        print("%s sırtnolu canlı hayvan bulunmuyor"%sirtno)

        #---Kesilenler -------
        c_Kesilenler = connection.koyun.Kesilenler
        K_result = (c_Kesilenler.find({"SirtNo": sirtno}))
        if K_result is not None:
            if K_result.count() !=0:
                print(K_result)
                print ("Kesilenler:")mongoadr.mongodbAdr()
                for K_i in range (K_result.count()):
                    pprint.pprint (K_result[K_i])
                    print("--"*20)
            
#-----RecNo
if cevap==2:

    recno = int(input ('RecNo girin: '))

    #---Canlilar-----

    C_result = c_Canlilar.find_one({"RecNo": recno})
    if C_result is not None:
        print ("C_result:")
        pprint.pprint (C_result)


    else:
        print("%s Recnolu canlı hayvan bulunmuyor"%recno)

        #---Kesilenler -------
        c_Kesilenler = connection.koyun.Kesilenler
        K_result = (c_Kesilenler.find_one({"RecNo": recno}))
        if K_result is not None:
            if K_result.count() !=0:
                print ("Kesilenler:")
                print (K_result)
        

#-----AnaRecNo
if cevap==3:

    recno = int(input ('AnaRecNo girin: '))

    #---Canlilar-----

    C_result = c_Canlilar.find({"AnaRecNo": recno})

    if C_result is not None:
        print ("C_result:")
        for C_i in range (C_result.count()):
            pprint.pprint (C_result[C_i])
            print("--"*20)

    else:
        print("%s AnaRecNolu canlı hayvan bulunmuyor"%recno)

        #---Kesilenler -------
        c_Kesilenler = connection.koyun.Kesilenler
        K_result = (c_Kesilenler.find({"AnaRecNo": recno}))
        if K_result is not None:
            if K_result.count() !=0:
                print ("Kesilenler:")
                for K_i in range (K_result.count()):
                    pprint.pprint (K_result[K_i])
                    print("--"*20)




