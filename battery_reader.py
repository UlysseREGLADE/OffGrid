# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:50:53 2018

@author: Ulysse
"""

import csv
import os
import datetime
import data_reader

#Charge nominale de la batterie
nominal_charge = 10.66 #kWh

#On liste tous les fichers a importer
files = os.listdir('ImportBattery')

#Boucle sur les fichiers
for file in files:
    
    #Si les fichiers ne sont pas des logs on ne fait rien !
    if(file.split('.')[1] == 'LOG'):
        
        print(file)
        
        #Lecture du ficher log
        with open('ImportBattery/'+file, 'r') as csv_file:
            spamreader = csv.reader(csv_file,
                                    delimiter=';',
                                    lineterminator="\n")
            
            #Boucle de lecture ligne par ligne
            val = data_reader.measures()
            i=0
            for row in spamreader:
                if(i>13):
                    date = datetime.datetime.strptime(row[0],
                                                      '%d.%m.%Y %H:%M:%S')
                    val.app([date, float(row[8])*nominal_charge/100])
                i+=1
        
        #Creation du ficher .csv correspondant dans la base de donnees
        #Chemin d'acces du .csv courant*
        day = datetime.datetime.strptime(file, 'SI%d%m%y.LOG')
        path = "data/%04d/%02d/sol_%02d.csv"%(day.year, day.month, day.day)
        print(path)
        
        if(not os.path.isdir('data')):
            os.mkdir('data')
        
        #Si le dossier correspondant a l'annee n'existe pas, on le creer
        if(not os.path.isdir('data/'+str(day.year))):
            os.mkdir('data/'+str(day.year))
        #de meme pour le mois
        if(not os.path.isdir("data/%04d/%02d"%(day.year, day.month))):
            os.mkdir("data/%04d/%02d"%(day.year, day.month))
            
        path = "data/%04d/%02d/sol_%02d.csv"%(day.year, day.month, day.day)
        
        with open(path, 'w') as csv_file:
            #Ouverture du fichier
            spam_writer = csv.writer(csv_file,
                                     delimiter=';',
                                     lineterminator="\n")
                    #Nom des colomnes
            spam_writer.writerow(['Heure (HH:MM:SS)'] +
                                 ['StockBatteries (kWh)'] +
                                 ['EntreesElec (kWh/s)'] +
                                 ['SortiesElec (kWh/s)'] +
                                 ['EntreeBatterie (kWh/s)'])
            
            for h in range(24):
                for m in range(12):
                    time = day.replace(hour=h, minute=5*m)
                    #Donnees electriques
                    stock_bat = val.get(time)[1]
                    entree_elec = 0
                    sortie_elec = 0
                    tension = val.derivate_glob(time)
                    
                    #Puis on ecrit la ligne dans le fichier .csv
                    spam_writer.writerow(["%02d:%02d:00"%(h, 5*m)] +
                                         [stock_bat] +
                                         [entree_elec] +
                                         [sortie_elec] +
                                         [tension])