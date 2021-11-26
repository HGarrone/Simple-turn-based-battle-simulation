
####### librerie #############

import os
import sys
from importlib.machinery import SourceFileLoader
import math
from random import *
import numpy as np
import matplotlib.pyplot as plt
import gc

####### inizializzazione #############

#nel caso in cui il programma non trovasse il path corretto sostituirlo con file_path=<path_corretto>. Se utilizzate Windows utilizzate \\ anzichè \ nel path. 

file_path=os.path.dirname(sys.argv[0])
full_path=os.path.abspath(file_path)

prog_classi= SourceFileLoader('classi_mrpg', file_path+'\\classi_mrpg.py').load_module()
from classi_mrpg import Pg, Mago, Berserk, Arrancar, personaggi, domini, attributi, classi_combattimento, abilità_Arrancar, debolezze_Arrancar, nomi_personaggi

####### definizione delle azioni possibili #############
schivatori=[]

def schivata(soggetto):
    #soggetto.nome=getattr(soggetto, "nome")
    schivatori.append(soggetto.nome)
    print(f"{soggetto.nome} si mette in guardia, pronto a difendersi dal prossimo attacco!")

def attacca(soggetto, oggetto, schivatori):
    #soggetto.nome=getattr(soggetto, "nome")
    #oggetto.nome=getattr(oggetto, "nome")
    if oggetto.nome in schivatori:
       attacco=np.minimum(randint(1,20), randint(1,20))
       schivatori.remove(oggetto.nome)
       print(f"{oggetto.nome} era già pronto a schivare l'attacco!\n")
    else:
       attacco=randint(1,20)       
    tec=int(getattr(soggetto, "tecnica"))
    try:         
          soggetto.colpo_critico
          if getattr(soggetto, "critico"):
             colpo_tot=attacco+randint(2,10)*tec
             print("\nColpo critico!\n")
          else:
             colpo_tot=attacco+tec
    except AttributeError:
          colpo_tot=attacco+tec
    print(f"{soggetto.nome} attacca {oggetto.nome} facendo {attacco}+{tec}...\n")
    if colpo_tot > int(getattr(oggetto, "CA")):
       print(f"... colpendo con successo {oggetto.nome}!")
       danno_base=randint(1,10)+tec
       try:         
          if getattr(soggetto, "critico"):
             danno_c=int((5/2)*danno_base)
          else:
             danno_c=danno_base
       except AttributeError:
             danno_c=danno_base 
       try:         
          if oggetto.classe=="Berserk":
             res=int(oggetto.attiva_resistenza)
             danno_r=danno_c-res
             if res != 0:
                print(f"\n{oggetto.nome} sfrutta la sua resilienza e riduce il danno di {res} danni!")
          else:
              danno_r=danno_c
       except AttributeError:
              danno_r=danno_c  
       try:         
          if getattr(oggetto, "debolezza") == getattr(soggetto, "dominio"):
             danno=3*danno_r
             print(f"\n{soggetto.nome} sfrutta come dominio la debolezza di {oggetto.nome} triplicando i danni inflitti!")
          else:
              danno=danno_r
       except AttributeError:
              danno=danno_r 
       setattr=(soggetto, "danno", danno)
       new_vita=int(getattr(oggetto, "vita"))-int(danno)
       oggetto.cambio_attributo("vita", new_vita)
       print(f"\n{soggetto.nome} infligge {danno} danni a {oggetto.nome}!")
       ogg_vita=getattr(oggetto, "vita")
       print(f"\nOra {oggetto.nome} ha {ogg_vita} punti ferita!\n")
    else:
       frasi_mancato=[f"..., ma {oggetto.nome} riesce a deviare il colpo!", f"..., ma {oggetto.nome} evita il colpo all'ultimo!", f"..., ma {oggetto.nome} balza all'indietro!", f"..., ma {oggetto.nome} prevede la mossa e si difende!"]
       print(frasi_mancato[randint(0,len(frasi_mancato)-1)])
    
def difenditi(soggetto, attiva, d):                                                          #PROBLEMA: COME TORNARE A VECCHIA CA
    #soggetto.nome=getattr(soggetto, "nome")
    vecchia_CA=int(getattr(soggetto, "CA"))
    mod_CA=attiva*randint(1,3)+d*attiva*randint(1,3)
    nuova_CA= vecchia_CA+mod_CA
    soggetto.cambio_attributo("CA", nuova_CA)
    setattr(difenditi, "incremento", mod_CA)
    print(f"\nLa Classe Armatura di {soggetto.nome} passa da {vecchia_CA} a {nuova_CA}!")
    
def sonido(soggetto, attiva, spec):                                                          #PROBLEMA: COME TORNARE A VECCHIA vel
    #soggetto.nome=getattr(soggetto, "nome")
    vecchia_vel=int(getattr(soggetto, "velocità"))
    mod_vel=attiva*randint(20,50)+spec*attiva*randint(20,50)
    nuova_vel= vecchia_vel+mod_vel
    soggetto.cambio_attributo("velocità", nuova_vel)
    setattr(difenditi, "incremento", mod_vel)
    modifica_personaggio_vel(soggetto, vecchia_vel, nuova_vel)
    print(f"\n{soggetto.nome} esegue un balzo estremamente rapido. La sua velocità passa da {vecchia_vel} a {nuova_vel}!")
    
def cura(soggetto, oggetto, d):
    #soggetto.nome=getattr(soggetto, "nome")
    #oggetto.nome=getattr(oggetto, "nome")
    tec=int(getattr(soggetto, "tecnica"))
    vita_prec=int(getattr(oggetto, "vita"))
    val_cura=randint(1,20)+tec+d*randint(5,15)
    new_vita=vita_prec+val_cura
    oggetto.cambio_attributo("vita", new_vita)
    ogg_vita_finale=getattr(oggetto, "vita")
    print(f"\n{oggetto.nome} è stato curato, i suoi punti ferita passano da {vita_prec} a {ogg_vita_finale}!")
    
def attacco_cero(soggetto, oggetto, spec):
    #soggetto.nome=getattr(soggetto, "nome")
    #oggetto.nome=getattr(oggetto, "nome")
    tec=int(getattr(soggetto, "tecnica"))+spec*int(getattr(soggetto, "tecnica"))
    attacco=randint(5,25)
    colpo_tot=attacco+tec
    print(f"{soggetto.nome} usa Cero su {oggetto.nome} facendo {attacco}+{tec}...\n")
    if colpo_tot > int(getattr(oggetto, "CA")):
       print(f"... colpendo con successo {oggetto.nome}!")
       danno=randint(15,30)
    else:
       print(f"... {oggetto.nome} evita di essere travolto dal raggio, ma risente comunque dell'energia rilasciata!")
       danno=randint(0,15)
    vita_prec=int(getattr(oggetto, "vita"))
    setattr=(soggetto, "danno", danno)
    new_vita=vita_prec-int(danno)
    oggetto.cambio_attributo("vita", new_vita)
    print(f"\n{soggetto.nome} infligge {danno} danni a {oggetto.nome}!")
    ogg_vita=getattr(oggetto, "vita")
    print(f"\nOra {oggetto.nome} ha {ogg_vita} punti ferita!\n")
    
def analizza(oggetto):
    print(oggetto.Scheda_pg)
    
def rigenera(soggetto,spec):
   #soggetto.nome=getattr(soggetto, "nome")
   vita_prec=int(getattr(soggetto, "vita"))
   val_cura=randint(1,20)+spec*randint(1,20)
   new_vita=vita_prec+val_cura
   soggetto.cambio_attributo("vita", new_vita)
   sogg_vita_finale=getattr(soggetto, "vita")
   print(f"\n{soggetto.nome} si è rigenerato, i suoi punti ferita passano da {vita_prec} a {sogg_vita_finale}!")
   
def potenziamento(soggetto,d):
   #soggetto.nome=getattr(soggetto, "nome")
   vecchia_tec=int(getattr(soggetto, "tecnica"))
   nuova_tec= vecchia_tec+randint(1,5)+d*2
   soggetto.cambio_attributo("tecnica", nuova_tec)
   print(f"\n{soggetto.nome} si è potenziato, la sua tecnica passa da {vecchia_tec} a {nuova_tec}!")
   
def attacco_psichico(soggetto, oggetto):
    #soggetto.nome=getattr(soggetto, "nome")
    #oggetto.nome=getattr(oggetto, "nome")
    tec=int(getattr(soggetto, "tecnica"))
    vel_prec=int(getattr(oggetto, "velocità"))
    riduzione_vel=randint(0,20)+tec
    new_vel=vel_prec-riduzione_vel
    oggetto.cambio_attributo("velocità", new_vel)
    ogg_vel_finale=getattr(oggetto, "velocità")
    modifica_personaggio_vel(oggetto, vel_prec, new_vel)
    print(f"\n{oggetto.nome} subisce un attacco psichico, la sua velocità passa da {vel_prec} a {ogg_vel_finale} e il suo movimento viene ridotto.")   
        
def cambiare_dominio_spell(soggetto):
    cambio_dominio=True            
    while cambio_dominio: 
        print("\nPossibili dimini del mago:\n")
        for i in range(0,len(domini)):
              print(domini[i]) 
        risposta_dominio=input("\nQuale dominio scegli?") 
        if risposta_dominio in domini:
              soggetto.cambio_dominio(risposta_dominio)
              cambio_dominio=False
        else:
              cambio_dominio=True

########################################################################################################################################################################
########################################## definizione delle funzioni di creazione delle azioni ########################################################################
########################################################################################################################################################################



def creazione_personaggio():
    print("\n\t\t\t Creazione del personaggio \t\t\t\n")
    while True:
        nome_personaggio=input("\nQual'è il nome del tuo personaggio?\n")
        if nome_personaggio not in nomi_personaggi:
           break
        else:
           print("\nQuesto nome appartiene già ad un altro personaggio in gioco. Scegline un altro!\n")
           continue  
           
    while True:
        risposta_classe=input(f"\nQuale classe tra le seguenti vuoi sceglier?{classi_combattimento}\n")
        if risposta_classe in classi_combattimento:
           classe_personaggio=risposta_classe
           break
        else:
           print(f"\nClasse non riconosciuta, scegliera tra: {classi_combattimento}\n")
           continue
    if classe_personaggio == "Arrancar":
       vel_personaggio=randint(30,60)
       print(f"\nLa tua velocità estratta casualmente è: {vel_personaggio}")
       input()
       hp_personaggio=randint(50,100)
       print(f"\nI tuoi punti ferita estratti casualmente sono: {hp_personaggio}")
       input()
       tec_personaggio=randint(5,10)+int(vel_personaggio/30)
       print(f"\nIl valore della tua tecnica estratta casualmente è: {tec_personaggio}")
       input()
       abilità_personaggio=abilità_Arrancar[randint(0,len(abilità_Arrancar)-1)]
       print(f"\nL'abilità del tuo personaggio estratta casualmente è: {abilità_personaggio}")
       input()
       debolezza_personaggio=debolezze_Arrancar[randint(0,len(debolezze_Arrancar)-1)]
       print(f"\nLa debolezza del tuo personaggio estratta casualmente è: {debolezza_personaggio}")
       input()
       globals()[nome_personaggio]=Arrancar(nome_personaggio,str(vel_personaggio),str(hp_personaggio),str(randint(5,10)+7-hp_personaggio//20 -vel_personaggio//60), str(tec_personaggio), str(debolezza_personaggio), str(abilità_personaggio))
       print(f"{globals()[nome_personaggio].Scheda_pg}\n")
       
    elif classe_personaggio == "Mago":
       vel_personaggio=randint(20,30)
       print(f"\nLa tua velocità estratta casualmente è: {vel_personaggio}")
       input()
       hp_personaggio=randint(50,100)
       print(f"\nI tuoi punti ferita estratti casualmente sono: {hp_personaggio}")
       input()
       tec_personaggio=randint(5,10)+int(vel_personaggio/40)
       print(f"\nIl valore della tua tecnica estratta casualmente è: {tec_personaggio}")
       input()
       dominio_personaggio=domini[randint(0,len(domini)-1)]
       print(f"\nL'abilità del tuo personaggio estratta casualmente è: {dominio_personaggio}")
       input()
       globals()[nome_personaggio]=Mago(nome_personaggio,str(vel_personaggio),str(hp_personaggio),str(randint(5,10)+5-hp_personaggio//20+vel_personaggio//5),str(tec_personaggio), str(dominio_personaggio))
       print(f"{globals()[nome_personaggio].Scheda_pg}\n")
       
    elif classe_personaggio == "Berserk":
       vel_personaggio=randint(20,50)
       print(f"\nLa tua velocità estratta casualmente è: {vel_personaggio}")
       input()
       hp_personaggio=randint(50,200)
       print(f"\nI tuoi punti ferita estratti casualmente sono: {hp_personaggio}")
       input()
       tec_personaggio=randint(5,10)+int(vel_personaggio/40)
       print(f"\nIl valore della tua tecnica estratta casualmente è: {tec_personaggio}")
       input()
       globals()[nome_personaggio]=Berserk(nome_personaggio,str(vel_personaggio),str(hp_personaggio),str(randint(5,10)+int(3-hp_personaggio/50)+int(vel_personaggio/10)),str(tec_personaggio))
       print(f"{globals()[nome_personaggio].Scheda_pg}\n")   

    else:
       vel_personaggio=randint(10,30)
       print(f"\nLa tua velocità estratta casualmente è: {vel_personaggio}")
       input()
       hp_personaggio=randint(30,100)
       print(f"\nI tuoi punti ferita estratti casualmente sono: {hp_personaggio}")
       input()
       tec_personaggio=randint(1,8)+int(vel_personaggio/20)
       print(f"\nIl valore della tua tecnica estratta casualmente è: {tec_personaggio}")
       input()
       globals()[nome_personaggio]=Pg(nome_personaggio,str(vel_personaggio),str(hp_personaggio),str(randint(5,10)+int(3-hp_personaggio/50)+int(vel_personaggio/10)),str(tec_personaggio))
       print(f"{globals()[nome_personaggio].Scheda_pg}\n")   
    
    setattr(creazione_personaggio, "nome", nome_personaggio)
    setattr(globals()[nome_personaggio], "nome", nome_personaggio)
    
def creazione_nemico_base(nome_nemico):
    vel_nemico=randint(10,40)
    hp_nemico=randint(20,60)
    tec_nemico=randint(1,10)+int(vel_nemico/20)
    globals()[nome_nemico]=Pg(nome_nemico,str(vel_nemico),str(hp_nemico),str(randint(5,13)+int(3-hp_nemico/40)+int(vel_nemico/10)),str(tec_nemico))
    setattr(creazione_nemico_base, "nome", globals()[nome_nemico])
    
def modifica_personaggio_vel(chi, vecchia_vel, nuova_vel):
    try:
        if chi.classe == "Arrancar":
           tec_prec=int(chi.tecnica)
           tec_nuova=tec_prec-int(vecchia_vel/30)+int(nuova_vel/30)
           setattr(chi, "tecnica", str(tec_nuova))
           CA_prec=int(chi.CA)
           CA_nuova=CA_prec+vecchia_vel//60-nuova_vel//60
           setattr(chi, "CA", str(CA_nuova))     
        elif chi.classe == "Mago":
           tec_prec=int(chi.tecnica)
           tec_nuova=tec_prec-int(vecchia_vel/40)+int(nuova_vel/40)
           setattr(chi, "tecnica", str(tec_nuova))
           CA_prec=int(chi.CA)
           CA_nuova=CA_prec+nuova_vel//5-vecchia_vel//5
           setattr(chi, "CA", str(CA_nuova)) 
        elif chi.classe == "Berserk":
           tec_prec=int(chi.tecnica)
           tec_nuova=tec_prec-int(vecchia_vel/40)+int(nuova_vel/40)
           setattr(chi, "tecnica", str(tec_nuova))
           CA_prec=int(chi.CA)
           CA_nuova=CA_prec-int(vecchia_vel/10)+int(nuova_vel/10)
           setattr(chi, "CA", str(CA_nuova))
        else:
           tec_prec=int(chi.tecnica)
           tec_nuova=tec_prec-int(vecchia_vel/20)+int(nuova_vel/20)
           setattr(chi, "tecnica", str(tec_nuova))
           CA_prec=int(chi.CA)
           CA_nuova=CA_prec-int(vecchia_vel/10)+int(nuova_vel/10)
           setattr(chi, "CA", str(CA_nuova))
    except AttributeError:
       tec_prec=int(chi.tecnica)
       tec_nuova=tec_prec-int(vecchia_vel/20)+int(nuova_vel/20)
       setattr(chi, "tecnica", str(tec_nuova))
       CA_prec=int(chi.CA)
       CA_nuova=CA_prec-int(vecchia_vel/10)+int(nuova_vel/10)
       setattr(chi, "CA", str(CA_nuova))
    
    
########################################################################################################################################################################
#################################### definizione della funzione "azioni" che contiene tutte le altre azione ############################################################
########################################################################################################################################################################

azioni_totali=["attacca", "analizza", "schiva", "cambio dominio", "cura", "attacco psichico", "attiva potenziamento", "attiva difesa", "rigenerazione", "sonido", "attacco cero"] 
azioni_Berserk=azioni_totali[0:3]
azioni_Mago=azioni_totali[0:8]
azioni_Arrancar=azioni_totali[0:3]+azioni_totali[8:11]
azioni_con_oggetto=["attacca", "analizza", "cura", "attacco psichico", "attacco cero"]

def azioni(azione, soggetto, oggetto):
    if azione.casefold() == "attacca":
       schivatori
       attacca(soggetto, oggetto, schivatori)
    elif azione.casefold() == "analizza":
       analizza(oggetto)
    elif azione.casefold() == "schiva":
       schivata(soggetto)
       
    elif getattr(soggetto, "classe") == "Mago":
        if azione.casefold() == "cambio dominio":
           cambiare_dominio_spell(soggetto)      
        elif azione.casefold() == "cura":
           if getattr(soggetto, "dominio")=="cura":
              d=1
           else:
              d=0
           cura(soggetto, oggetto,d)
        elif azione.casefold() == "attacco psichico":
           attacco_psichico(soggetto, oggetto)
        elif azione.casefold() == "attiva potenziamento":
           if getattr(soggetto, "dominio")=="potenziamento":
              d=1
           else:
              d=0
           potenziamento(soggetto,d)
        elif azione.casefold() == "attiva difesa":
           attiva=1
           if getattr(soggetto, "dominio")=="difesa":
              d=1
           else:
              d=0
           difenditi(soggetto, attiva,d)
           
    elif getattr(soggetto, "classe") == "Arrancar":
        if azione.casefold() == "rigenerazione":
           if getattr(soggetto, "specialità")=="rigenerazione":
              spec=1
           else:
              spec=0
           rigenera(soggetto,spec)
        elif azione.casefold() == "sonido":
           attiva=1
           if getattr(soggetto, "specialità")=="sonido":
              spec=1
           else:
              spec=0
           sonido(soggetto,attiva,spec)
        elif azione.casefold() == "attacco cero":
           if getattr(soggetto, "specialità")=="cero":
              spec=1
           else:
              spec=0
           attacco_cero(soggetto, oggetto, spec)
    else:
        print("\nNessuna azione correttamente selezionata!\n")
              
########################################################################
##################### Test con Peppe e Ulquiorra #######################
########################################################################
    
#vel1=randint(20,30)
#hp1=randint(50,100)
#vel2=randint(30,50)
#hp2=randint(50,100)
#Peppe=Mago("Peppe",str(vel1),str(hp1),str(randint(5,10)+int((100-hp1)/50)+int(vel1/5)),str(randint(5,10)+int(vel1/25)), str(choice(domini))) 
#Ulquiorra=Arrancar("Ulquiorra",str(vel2),str(hp2),str(randint(5,10)+int((100-hp2)/50)+int(vel2/5)+2),str(randint(5,10)-int(vel2/40)), str(choice(domini)), str(choice(abilità_Arrancar))) 
#print("\n", Peppe.Scheda_pg)
#print("\n", Ulquiorra.Scheda_pg)
#attacca(Peppe, Ulquiorra)
#print("\n", Ulquiorra.Scheda_pg)
#attacco_cero(Ulquiorra, Peppe)
#print("\n", Peppe.Scheda_pg)
#cura(Peppe,Peppe)
#print("\n", Peppe.Scheda_pg)

#creazione_personaggio()
#print(globals()[creazione_personaggio.nome].Scheda_pg)                              #funziona qui, ma non su mrpg

#print(getattr(Peppe, "vita"))       
#print("\n", personaggi)
#Peppe.cambio_attributo("vita",100)
#print("\n", Peppe.attributo("vita"))
#print("\nVecchio dominio: ", Peppe.dominio)
#Peppe.cambio_dominio("psico")
#print("\nNuovo dominio:", Peppe.dominio)











































