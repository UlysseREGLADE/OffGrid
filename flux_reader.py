# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 20:00:32 2018

@author: Ulysse
"""

import os
import time
import datetime
import csv

#excecution du programme de lecture ModBus
dn = os.path.dirname(__file__)
print(dn)
os.system(dn+"/MBSheet/MBSheete.exe /S:"+dn+"/MBSheet/slist2.csv /Z:"+dn+"/MBSheet/Log.csv  /L ")

#Recuperation des valeurs d'interet du log dans la liste data
with open('MBSheet/Log.csv', 'r') as csv_file:
    spamreader = csv.reader(csv_file,
                            delimiter=';',
                            lineterminator="\n")
    
    data = []
    row_i = [11, 12, 13, 45, 46, 47, 79, 80, 81, 113, 114, 115]
    i=0
    for row in spamreader:
        if(i in row_i):
            data.append(float(row[7]))
        i+=1

print(data)
time.sleep(1)

#Supression du log courrant
myfile="MBSheet/Log.csv"
if os.path.isfile(myfile):
    os.remove(myfile)

#Ecriture des donnees
if(data != []):
    #Chemin d'acces du .csv courant
    day = datetime.date.today()
    path = "data/%04d/%02d/flux_%02d.csv"%(day.year, day.month, day.day)
    print(path)
    
    if(not os.path.isdir('data')):
        os.mkdir('data')
    
    #Si le dossier correspondant a l'annee n'existe pas, on le creer
    if(not os.path.isdir('data/'+str(day.year))):
        os.mkdir('data/'+str(day.year))
    #de meme pour le mois
    if(not os.path.isdir("data/%04d/%02d"%(day.year, day.month))):
        os.mkdir("data/%04d/%02d"%(day.year, day.month))
        
    path = "data/%04d/%02d/flux_%02d.csv"%(day.year, day.month, day.day)
    h = datetime.datetime.now().hour
    m = datetime.datetime.now().minute
    
    to_write = ["%02d:%02d:00"%(h, m)] + [(data[6]+data[3])/3600]+[(data[7]+data[4])/2]+[(data[8]+data[5])/2] + [data[9]/3600]+[data[10]]+[data[11]] + [data[0]/3600]+[data[1]]+[data[2]] + [0]+[0]+[0]
    
    if(not os.path.exists(path)):
        with open(path, 'w') as csv_file:
            #Ouverture du fichier
            spam_writer = csv.writer(csv_file, delimiter=';', lineterminator="\n")
            #On ajoute la ligne du debut comme le fichier n'existait pas
            spam_writer.writerow(['Heure (HH:MM:SS)'] +
                             ['Debit chauffage central (L/s)'] +
                             ['T in chauffage central (°C)'] +
                             ['T out chauffage central (°C)'] +
                             ['Debit chauffe eau (L/s)'] +
                             ['T in chauffe eau (°C)'] +
                             ['T out chauffe eau (°C)'] +
                             ['Debit fourneau (L/s)'] +
                             ['T in fourneau (°C)']  +
                             ['T out fourneau (°C)'] +
                             ['Debit ECS (L/s)'] +
                             ['T in ECS (°C)'] +
                             ['T out ECS (°C)'])
            spam_writer.writerow(to_write)
    else:
        with open(path, 'a') as csv_file:
            #Ouverture du fichier
            spam_writer = csv.writer(csv_file, delimiter=';', lineterminator="\n")
            #csv_file.seek(2)
            spam_writer.writerow(to_write)