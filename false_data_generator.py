import datetime
import os
import csv
import numpy as np

#Date de debut des fausses donnees
starting_day = datetime.date(2017, 7, 1)
#Date de fin des fausses donnees
ending_day = datetime.date.today()
#Nombres de jours a simuler
day_count = (ending_day-starting_day).days+1
print(day_count)




#Boucle de generation des donnees thermiques
for day in (starting_day + datetime.timedelta(n) for n in range(day_count)):
    
    #Chemin d'acces du .csv courant
    path = "data/%04d/%02d/th_%02d.csv"%(day.year, day.month, day.day)
    print(path)
    
    #Si le dossier correspondant a l'annee n'existe pas, on le creer
    if(not os.path.isdir('data/'+str(day.year))):
        os.mkdir('data/'+str(day.year))
    #de meme pour le mois
    if(not os.path.isdir("data/%04d/%02d"%(day.year, day.month))):
        os.mkdir("data/%04d/%02d"%(day.year, day.month))
    
    #creation du fichier csv
    with open(path, 'w') as csv_file:
        #Ouverture du fichier
        spam_writer = csv.writer(csv_file, delimiter=';', lineterminator="\n")
        #Nom des colomnes
        spam_writer.writerow(['Heure (HH:MM:SS)'] +
                             
                             ['T salon (°C)'] +
                             ['T chambre 1 (°C)'] +
                             ['T chambre 2 (°C)'] +
                             ['T chambre 2 (°C)'] +
                             ['T chambre combles (°C)'] +
                             ['T dehors (°C)'] +
                             ['T ballon 1 (°C)'] +
                             ['T ballon 2 (°C)'])
        #Unitee des colomnes
        for h in range(24):
            for m in range(12):
                
                #time volue lineerement entre 0 et 24 sur la journee
                time = h + 12*m/60
                #Calul des temperatures
                t_salon = round(15 - 5*np.cos(2*np.pi*time/24) +
                                np.random.rand(), 1)
                t_chambre_1 = round(17 - 3*np.cos(2*np.pi*time/24) +
                                    np.random.rand(), 1)
                t_chambre_2 = round(17 - 3*np.cos(2*np.pi*time/24) +
                                    np.random.rand(), 1)
                t_chambre_3 = round(17 - 3*np.cos(2*np.pi*time/24) +
                                    np.random.rand(), 1)
                t_chambre_combles = round(10 - 5*np.cos(2*np.pi*time/24) +
                                          np.random.rand(), 1)
                t_dehors = round(8 - 3*np.cos(2*np.pi*time/24) +
                                 np.random.rand(), 1)
                t_ballon_1 = round(60 - 20*np.cos(2*np.pi*time/24) +
                                   np.random.rand(), 1)
                t_ballon_2 = round(60 - 20*np.cos(2*np.pi*time/24) +
                                   np.random.rand(), 1)
                
                #Puis on ecrit la ligne dans le fichier .csv
                spam_writer.writerow(["%02d:%02d:00"%(h, 5*m)] +
                                     [t_salon] +
                                     [t_chambre_1] +
                                     [t_chambre_2] +
                                     [t_chambre_3] +
                                     [t_chambre_combles] +
                                     [t_dehors] +
                                     [t_ballon_1] +
                                     [t_ballon_2])




#Boucle de generation des donnees thermiques
for day in (starting_day + datetime.timedelta(n) for n in range(day_count)):
    
    #Chemin d'acces du .csv courant
    path = "data/%04d/%02d/flux_%02d.csv"%(day.year, day.month, day.day)
    print(path)
    
    #Si le dossier correspondant a l'annee n'existe pas, on le creer
    if(not os.path.isdir('data/'+str(day.year))):
        os.mkdir('data/'+str(day.year))
    #de meme pour le mois
    if(not os.path.isdir("data/%04d/%02d"%(day.year, day.month))):
        os.mkdir("data/%04d/%02d"%(day.year, day.month))
    
    #creation du fichier csv
    with open(path, 'w') as csv_file:
        #Ouverture du fichier
        spam_writer = csv.writer(csv_file, delimiter=';', lineterminator="\n")
        #Nom des colomnes
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

        for h in range(24):
            for m in range(12):
                #Calcul des flux thermiques
                deb_centre = 0.5*0.001/3600
                t_in_centre = round(19 - np.cos(2*np.pi*time/24) +
                                      np.random.rand()*0.1, 1)
                t_out_centre = round(20 - np.cos(2*np.pi*time/24) +
                                       np.random.rand()*0.1, 1)
                deb_eau = 0.2*0.001/3600
                t_in_eau = round(17 - np.cos(2*np.pi*time/24) +
                                      np.random.rand()*0.1, 1)
                t_out_eau = round(18 - 0.5*np.cos(2*np.pi*time/24) +
                                       np.random.rand()*0.1, 1)
                deb_fourneau = 0.7*0.001/3600
                t_in_fourneau = round(19 - 0.5*np.cos(2*np.pi*time/24) +
                                      np.random.rand()*0.1, 1)
                t_out_fourneau = round(21 - np.cos(2*np.pi*time/24) +
                                       np.random.rand()*0.1, 1)
                deb_ecs = 0.3*0.001/3600
                t_in_ecs = round(17 - np.cos(2*np.pi*time/24) +
                                      np.random.rand()*0.1, 1)
                t_out_ecs = round(29 - 0.3*np.cos(2*np.pi*time/24) +
                                       np.random.rand()*0.1, 1)
                
                #Puis on ecrit la ligne dans le fichier .csv
                spam_writer.writerow(["%02d:%02d:00"%(h, 5*m)] +
                                     [deb_centre] +
                                     [t_in_centre] +
                                     [t_out_centre] +
                                     [deb_eau] +
                                     [t_in_eau] +
                                     [t_out_eau] +
                                     [deb_fourneau] +
                                     [t_in_fourneau] +
                                     [t_out_fourneau] +
                                     [deb_ecs] +
                                     [t_in_ecs] +
                                     [t_out_ecs])

#Boucle de generation des donnees thermiques
for day in (starting_day + datetime.timedelta(n) for n in range(day_count)):
    
    #Chemin d'acces du .csv courant
    path = "data/%04d/%02d/sol_%02d.csv"%(day.year, day.month, day.day)
    print(path)
    
    #Si le dossier correspondant a l'annee n'existe pas, on le creer
    if(not os.path.isdir('data/'+str(day.year))):
        os.mkdir('data/'+str(day.year))
    #de meme pour le mois
    if(not os.path.isdir("data/%04d/%02d"%(day.year, day.month))):
        os.mkdir("data/%04d/%02d"%(day.year, day.month))
      
    #creation du fichier csv
    with open(path, 'w') as csv_file:
        #Ouverture du fichier
        spam_writer = csv.writer(csv_file, delimiter=';', lineterminator="\n")
                #Nom des colomnes
        spam_writer.writerow(['Heure (HH:MM:SS)'] +
                             ['StockBatteries (KWh)'] +
                             ['EntreesElec (KWh/s)'] +
                             ['SortiesElec (KWh/s)'] +
                             ['TensionPanneaux (V)'])
        
        for h in range(24):
            for m in range(12):
                #Donnees electriques
                stock_bat = round(10 - 9*np.sin(2*np.pi*time/24) +
                                  np.random.rand()*0.1, 1)
                entree_elec = round(3600*(70 - 30*np.cos(2*np.pi*time/24) +
                                    np.random.rand()), 1)
                sortie_elec = round(3600*(50 - 20*np.cos(2*np.pi*time/24) +
                                    np.random.rand()), 1)
                tension = round(18 - 18*np.cos(0.2 + 2*np.pi*time/24), 1)
                
                #Puis on ecrit la ligne dans le fichier .csv
                spam_writer.writerow(["%02d:%02d:00"%(h, 5*m)] +
                                     [stock_bat] +
                                     [entree_elec] +
                                     [sortie_elec] +
                                     [tension])