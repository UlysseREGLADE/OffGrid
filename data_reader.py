import numpy as np
import datetime
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter

#dictionnaire contenant toutes les correspondances variable/colones.
v  =  {'T salon' :                     {'ref':'th', 'id':1, 'unit':'°C'},
       'T chambre 1':                  {'ref':'th', 'id':2, 'unit':'°C'},
       'T chambre 2':                  {'ref':'th', 'id':3, 'unit':'°C'},
       'T chambre 3':                  {'ref':'th', 'id':4, 'unit':'°C'},
       'T chambre combles':            {'ref':'th', 'id':5, 'unit':'°C'},
       'T dehors':                     {'ref':'th', 'id':6, 'unit':'°C'},
       'T ballon 1':                   {'ref':'th', 'id':7, 'unit':'°C'},
       'T ballon 2':                   {'ref':'th', 'id':8, 'unit':'°C'},
     
       'Debit chauffage central':      {'ref':'flux', 'id':1, 'unit':'L/s'},
       'T in chauffage central':       {'ref':'flux', 'id':2, 'unit':'°C'},
       'T out chauffage central':      {'ref':'flux', 'id':3, 'unit':'°C'},
       'Debit chauffe eau':            {'ref':'flux', 'id':4, 'unit':'L/s'},
       'T in chauffe eau':             {'ref':'flux', 'id':5, 'unit':'°C'},
       'T out chauffe eau':            {'ref':'flux', 'id':6, 'unit':'°C'},
       'Debit fourneau':               {'ref':'flux', 'id':7, 'unit':'L/s'},
       'T in fourneau':                {'ref':'flux', 'id':8, 'unit':'°C'},
       'T out fourneau':               {'ref':'flux', 'id':9, 'unit':'°C'},
       'Debit ECS':                    {'ref':'flux', 'id':10, 'unit':'L/s'},
       'T in ECS':                     {'ref':'flux', 'id':11, 'unit':'°C'},
       'T out ECS':                    {'ref':'flux', 'id':12, 'unit':'°C'},
         
       'Stock batteries':              {'ref':'sol', 'id':1, 'unit':'KWh'},
       'Entrees elec':                 {'ref':'sol', 'id':2, 'unit':'KWh/s'},
       'Sorties elec':                 {'ref':'sol', 'id':3, 'unit':'KWh/s'},
       'Tension panneaux':             {'ref':'sol', 'id':4, 'unit':'V'}}

class measures(object):
    
    def __init__(self, vals=None):
        if(vals!=None):
            self.vals = np.array(vals)
            self.vals = np.array(sorted(self.vals, key=lambda x:x[0]))
            self.sort = True
        else:
            self.vals = None
            self.sort = False
        
    def app(self, val):
        if(not (self.vals is None)):
            self.vals = np.append(self.vals, [val], axis=0)
            self.sort = False
        else:
            self.sort = True
            self.vals = np.array([val])
    
    def sub(a, b):
        #Si la liste n'est pas triee, on commence par le faire
        if(not a.sort):
            a.vals = np.array(sorted(a.vals, key=lambda x:x[0]))
            a.sort = True
        if(not b.sort):
            b.vals = np.array(sorted(b.vals, key=lambda x:x[0]))
            b.sort = True
        
        #On multiplie les deux tableaux
        c = measures()
        for val in a.vals:
            c.app([val[0], val[1]-b.get(val[0])[1]])
        for val in b.vals:
            if(not(val[0] in c.vals)):
                c.app([val[0], val[1]-a.get(val[0])[1]])
        
        #On retourne
        return c
    
    def mul(a, b):
        #Si la liste n'est pas triee, on commence par le faire
        if(not a.sort):
            a.vals = np.array(sorted(a.vals, key=lambda x:x[0]))
            a.sort = True
        if(not b.sort):
            b.vals = np.array(sorted(b.vals, key=lambda x:x[0]))
            b.sort = True
        
        #On multiplie les deux tableaux
        c = measures()
        for val in a.vals:
            c.app([val[0], val[1]*b.get(val[0])[1]])
        for val in b.vals:
            if(not(val[0] in c.vals)):
                c.app([val[0], val[1]*a.get(val[0])[1]])
        
        #On retourne
        return c
    
    def get(self, date):
        #Si la liste n'est pas triee, on commence par le faire
        if(not self.sort):
            self.vals = np.array(sorted(self.vals, key=lambda x:x[0]))
            self.sort = True
        
        #On commence par gerer les cas pathologiques
        if(len(self.vals)==0):
            return [None, 0]
        if(date < self.vals[0, 0]):
            return [0, self.vals[0, 1]]
        if(date >= self.vals[-1, 0]):
            return [len(self.vals)-1, self.vals[-1, 1]]
        
        #On recherche l'intervl ou se trouve la date demandee par dichotomie
        index_l, index_r = 0, len(self.vals)-1
        while(index_r-index_l != 1):
            new_index = int((index_r+index_l)/2)
            if(self.vals[new_index, 0] > date):
                index_r = new_index
            else:
                index_l = new_index
        
        
        #On fait l'apporx affine par morceaux
        big_delta = (self.vals[index_r, 0]-self.vals[index_l, 0]).seconds
        small_delta = (date-self.vals[index_l, 0]).seconds
        r=(small_delta/big_delta)*(self.vals[index_r, 1]-self.vals[index_l, 1])
        return [index_l, self.vals[index_l, 1]+r]
    
    def integrate(self, start, end):
        
        #Recuperation des indexs de fin et de debut
        index_l, index_r = self.get(start)[0], self.get(end)[0]
        
        #Gestion du cas pathologique
        if((index_l is None) or (index_r is None)):
            return 0
        
        #Calcul de l'integrale
        integrale = 0
        for i in range(index_l, index_r):
            delta = (self.vals[i, 0]-self.vals[i+1, 0]).seconds
            avg = (self.vals[i, 1] + self.vals[i+1, 1])/2
            integrale += delta * avg
        return integrale

def get_values(val, start, end):
    first_date = start.date() - datetime.timedelta(1)
    last_date = end.date() + datetime.timedelta(1)
    day_count = (last_date-first_date).days+1
    
    ret = measures()
    
    for day in (first_date + datetime.timedelta(n) for n in range(day_count)):
        #Chemin d'access vers le .csv du jour
        path="data/%04d/%02d/%s_%02d.csv"%(day.year,
                                           day.month,
                                           val['ref'],
                                           day.day)
        #Si le ficheir existe on le lit
        if(os.path.isfile(path)):
            with open(path, 'r') as csv_file:
                spamreader = csv.reader(csv_file,
                                        delimiter=';',
                                        lineterminator="\n")
                
                #Boucle de lecture des ligne du .csv
                i=0
                for row in spamreader:
                    if(i>=1):
                        now_str = str(day) + " " + row[0]
                        #On verifie que la cellule n'est pas vide
                        if(row[val['id']]!=''):
                            dt=datetime.datetime.strptime(now_str,
                                                          '%Y-%m-%d %H:%M:%S')
                            mea = float(row[val['id']])
                            ret.app([dt, mea])
                    i+=1
        
    return ret
    
def get_single_value(val, date):
    table=get_values(val,date-datetime.timedelta(1),date+datetime.timedelta(1))
    return table.get(date)[1]

def get_integrale(val, start, end):
    table=get_values(val, start, end)
    return table.integrate(start, end)

def plot_val(var, start, end, path):
    """
    Generate a graph of a given variable between the starting and the ending
    date. The graph is stored at the direction of the path, which can be a
    string or an IOString.
    """
    
    a = get_values(var, start, end)
    a.vals = np.array(sorted(a.vals, key=lambda x:x[0]))
    x, y = a.vals[:, 0], a.vals[:, 1]
    
    fig, ax = plt.subplots()
    ax.plot_date(x, y, 'r-')
    
    ax.set_xlabel('Date')
    ax.set_ylabel(var['unit'])
    
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    fig.autofmt_xdate()

    plt.savefig(path, format='png')

#print(get_single_value(v['T salon'], datetime.datetime.now()))