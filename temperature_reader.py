"""
Created on Mon Apr 30 12:32:50 2018

@author: Ulysse
"""

import os
import time
import datetime
import struct
import serial
import csv

#Ouverture du port serie
print('Opening Serial ...')
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(1)

#Requette a l'arduino
ser.write(b'pool')
print('Pooling the Arduino ...')

#On attend un peu le temps que l'arduino reponde
time.sleep(1)

#On lit les six valeurs
print('Reading the Values ...')
temp = []
for i in range(6):
    data = ser.read(4)
    float_data = struct.unpack('<f', data)
    temp.append(float_data)
    print("Temperature N"+str(i)+": "+str(float_data))
time.sleep(1)

#Fermeture du port Serie
print('Closing Serial ...')
ser.close()

#Ecriture des donnees
if(temp != []):
    #Chemin d'acces du .csv courant
    day = datetime.date.today()
    path = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)
    print(path)
    
    if(not os.path.isdir('data')):
        os.mkdir('data')
    
    #Si le dossier correspondant a l'annee n'existe pas, on le creer
    if(not os.path.isdir('data/'+str(day.year))):
        os.mkdir('data/'+str(day.year))
    #de meme pour le mois
    if(not os.path.isdir("data/%04d/%02d"%(day.year, day.month))):
        os.mkdir("data/%04d/%02d"%(day.year, day.month))
        
    path = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)
    h = datetime.datetime.now().hour
    m = datetime.datetime.now().minute
    
    to_write = ["%02d:%02d:00"%(h, m)] +[temp[0][0]] +[temp[2][0]] +[temp[3][0]] +[temp[4][0]] +[temp[5][0]] +[temp[1][0]] +[0] +[0]
    
    if(not os.path.exists(path)):
        with open(path, 'w') as csv_file:
            #Ouverture du fichier
            spam_writer = csv.writer(csv_file, delimiter=';', lineterminator="\n")
            #On ajoute la ligne du debut comme le fichier n'existait pas
            spam_writer.writerow(['Heure (HH:MM:SS)'] +
                             ['T salon (°C)'] +
                             ['T chambre 1 (°C)'] +
                             ['T chambre 2 (°C)'] +
                             ['T chambre 3 (°C)'] +
                             ['T chambre combles (°C)'] +
                             ['T dehors (°C)'] +
                             ['T ballon 1 (°C)'] +
                             ['T ballon 2 (°C)'])
            spam_writer.writerow(to_write)
    else:
        with open(path, 'a') as csv_file:
            #Ouverture du fichier
            spam_writer = csv.writer(csv_file, delimiter=';', lineterminator="\n")
            #csv_file.seek(2)
            spam_writer.writerow(to_write)
        