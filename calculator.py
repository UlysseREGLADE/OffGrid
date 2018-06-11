import const
import datetime
import data_reader as dr

def t_elec(survie = False):
    #On prend le temps courrant
    now = datetime.datetime.now()
    ago = now - datetime.timedelta(14)
    delta = datetime.timedelta(14).total_seconds()
    entree_elec_moy = dr.get_integrale(dr.v['Entrees elec'], ago, now)/delta
    sortie_elec_moy = dr.get_integrale(dr.v['Sorties elec'], ago, now)/delta
    
    #Si on est en mode survie, on compare a la sortie min
    if(survie):
        sortie_elec_moy = const.conso_elec_mini
    
    if(entree_elec_moy>sortie_elec_moy or sortie_elec_moy-entree_elec_moy==0):
        return "infini"
    else:
        delta_bat = (const.stock_batteries_maxi-const.stock_batteries_mini)
        delta_elec = (sortie_elec_moy-entree_elec_moy)
        
        return datetime.timedelta(seconds=delta_bat/delta_elec)

def t_thermique(survie=False):
    #On prend le temps courant
    now = datetime.datetime.now()
    ago = now - datetime.timedelta(14)
    delta = datetime.timedelta(14).total_seconds()
    
    #Calcule des flux
    
    #Flux chauffage central
    fcc=dr.measures.sub(dr.get_values(dr.v['T in chauffage central'], ago, now),
                        dr.get_values(dr.v['T out chauffage central'], ago, now))
    fcc=dr.measures.mul(fcc,
                        dr.get_values(dr.v['Debit chauffage central'], ago, now))
    fccm = fcc.integrate(ago, now)*const.c_eau/delta
    #Flux du chauffe eau
    fce=dr.measures.sub(dr.get_values(dr.v['T in chauffe eau'], ago, now),
                        dr.get_values(dr.v['T out chauffe eau'], ago, now))
    fce=dr.measures.mul(fce,
                        dr.get_values(dr.v['Debit chauffe eau'], ago, now))
    fcem = fce.integrate(ago, now)*const.c_calo/delta
    #Flux fourneau
    ff=dr.measures.sub(dr.get_values(dr.v['T in fourneau'], ago, now),
                        dr.get_values(dr.v['T out fourneau'], ago, now))
    ff=dr.measures.mul(ff,
                        dr.get_values(dr.v['Debit fourneau'], ago, now))
    ffm = ff.integrate(ago, now)*const.c_eau/delta
    
    #Si on n'est pas en mode survie
    if(not survie):
        #Flux ECS
        fecs=dr.measures.sub(dr.get_values(dr.v['T in ECS'], ago, now),
                            dr.get_values(dr.v['T out ECS'], ago, now))
        fecs=dr.measures.mul(fecs,
                            dr.get_values(dr.v['Debit ECS'], ago, now))
        fecsm = fecs.integrate(ago, now)*const.c_eau/delta
        
        #Entrees et sorties des ballons
        entrees_ballons = ffm + fcem
        sorties_ballons = fccm + fecsm
        
        #Energies dans les ballons
        t_ballon_1 = dr.get_single_value(dr.v['T ballon 1'], now)
        if(t_ballon_1 > const.t_ballon_mini):
            stock_e_ballon_1 = const.v_ballon*const.c_eau*(t_ballon_1-const.t_ballon_mini)
        else:
            stock_e_ballon_1 = 0
        t_ballon_2 = dr.get_single_value(dr.v['T ballon 2'], now)
        if(t_ballon_2 > const.t_ballon_mini):
            stock_e_ballon_2 = const.v_ballon*const.c_eau*(t_ballon_2-const.t_ballon_mini)
        else:
            stock_e_ballon_2 = 0
        stock_e_ballon = stock_e_ballon_1 + stock_e_ballon_2
        
        #Calcule du temps
        if(sorties_ballons<entrees_ballons or sorties_ballons-entrees_ballons==0):
            return "infini"
        else:
            ret = stock_e_ballon/(sorties_ballons-entrees_ballons)
            return datetime.timedelta(seconds=ret)
    
    else:
        texm = dr.get_integrale(dr.v['T dehors'], ago, now)/delta
        tinecsm = dr.get_integrale(dr.v['T in ECS'], ago, now)/delta
        tintm = (dr.get_integrale(dr.v['T chambre 1'], ago, now)+
                 dr.get_integrale(dr.v['T chambre 2'], ago, now)+
                 dr.get_integrale(dr.v['T chambre 3'], ago, now)+
                 dr.get_integrale(dr.v['T salon'], ago, now)+
                 dr.get_integrale(dr.v['T chambre combles'], ago, now))/(5*delta)
        flux_ecs_survie = const.debit_ecs_mini*const.c_eau*(const.t_ballon_mini-tinecsm)
        flux_chauf_centre_survie = fccm*(const.t_chauffage_mini-texm)/(tintm-texm)
        
        #Entrees et sorties des ballons
        entrees_ballons = ffm + fcem
        sorties_ballons = flux_chauf_centre_survie + flux_ecs_survie
        
        #Energies dans les ballons
        t_ballon_1 = dr.get_single_value(dr.v['T ballon 1'], now)
        if(t_ballon_1 > const.t_ballon_mini):
            stock_e_ballon_1 = const.v_ballon*const.c_eau*(t_ballon_1-const.t_ballon_mini)
        else:
            stock_e_ballon_1 = 0
        t_ballon_2 = dr.get_single_value(dr.v['T ballon 2'], now)
        if(t_ballon_2 > const.t_ballon_mini):
            stock_e_ballon_2 = const.v_ballon*const.c_eau*(t_ballon_2-const.t_ballon_mini)
        else:
            stock_e_ballon_2 = 0
        stock_e_ballon = stock_e_ballon_1 + stock_e_ballon_2 + const.v_chauffage*const.c_air*(tintm-const.t_chauffage_mini)
        
        #Calcule du temps
        if(sorties_ballons<entrees_ballons or sorties_ballons-entrees_ballons==0):
            return "infini"
        else:
            ret = stock_e_ballon/(sorties_ballons-entrees_ballons)
            return datetime.timedelta(seconds=ret)


def indic_maison():
    #On prend le temps courant
    now = datetime.datetime.now()
    
    mini = min(dr.get_single_value(dr.v['T salon'], now),
               dr.get_single_value(dr.v['T chambre 1'], now),
               dr.get_single_value(dr.v['T chambre 2'], now),
               dr.get_single_value(dr.v['T chambre 3'], now),
               dr.get_single_value(dr.v['T chambre combles'], now))
    
    if(mini > 19):
        return 'vert'
    elif(mini > 15):
        return 'orange'
    else:
        return 'rouge'
    
def indic_ecs():
    #On prend le temps courant
    now = datetime.datetime.now()
    
    maxi = max(dr.get_single_value(dr.v['T ballon 1'], now),
               dr.get_single_value(dr.v['T ballon 2'], now))
    
    if(maxi > 50):
        return 'vert'
    elif(maxi > 35):
        return 'orange'
    else:
        return 'rouge'

def indic_elec():
    t_electrique = t_elec()
    
    if(t_electrique=="infini" or t_electrique>datetime.timedelta(10)):
        return 'vert'
    elif(t_electrique>datetime.timedelta(3)):
        return 'orange'
    else:
        return 'rouge'

#print(t_thermique(survie=True))