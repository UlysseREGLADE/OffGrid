# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 19:58:18 2018

@author: Ulysse
"""

import csv
import os
import datetime

#On liste tous les fichers a importer
files = os.listdir('ImportInverter')

#Boucle sur les fichiers
for file in files:
    
    print(file)
    day = datetime.datetime.strptime(file, 'Montchauvel_v2-%Y%m%d.csv')
    print(day)
    
    #Lecture du ficher log
    with open('ImportInverter/'+file, 'r') as csv_file:
        spamreader = csv.reader((line.replace('\0', '') for line in csv_file),
                                dialect = csv.excel_tab,
                                delimiter=';',
                                lineterminator="\n")
        
        val = []
        #Boucle de lecture ligne par ligne
        i=0
        for row in spamreader:
            if(i>=18 and row != []):
                val.append(float(row[2].replace(',', '.'))+
                           float(row[4].replace(',', '.'))+
                           float(row[6].replace(',', '.')))
                val[-1] = val[-1]/3600
            i+=1
            
    path = "data/%04d/%02d/sol_%02d.csv"%(day.year, day.month, day.day)
    
    #maintenant, on verifie que le csv batterie correspondant existe
    if(os.path.isfile(path)):
        #On va charger le fichier ligne par ligne dans ce tableau
        lines=[]
        #ouverture du fichier
        with open(path, 'r') as csv_file:
            #celui-la est bcp moins mechant que ceux de SMA
            spamreader = csv.reader(csv_file,
                                    delimiter=';',
                                    lineterminator='\n')
            for line in spamreader:
                lines.append(line)
        #maintenant, pour toues les lignes possibles, on fait les calcules
        for i in range(min(len(val), len(lines)-1)):
            lines[i+1][3] = str(val[i])
            lines[i+1][2] = str(val[i] - float(lines[i+1][4]))
        #Enfin, on reecrit le fichier
        with open(path, 'w') as csv_file:
            spam_writer = csv.writer(csv_file,
                                     delimiter=';',
                                     lineterminator="\n")
            for line in lines:
                spam_writer.writerow(line)
            