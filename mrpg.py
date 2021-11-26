print('''
#################################################################################################
####    Questo programma è stato ideato e sviluppato nella sua interezza da Hobey Garrone    ####
#################################################################################################
''')

####### librerie #############

import os
import sys
from importlib.machinery import SourceFileLoader
from math import *
from random import *
import numpy as np
import matplotlib.pyplot as plt
import gc

####### inizializzazione #############

#nel caso in cui il programma non trovasse il path corretto sostituirlo con file_path=<path_corretto>. Se utilizzate Windows utilizzate \\ anzichè \ nel path. 

file_path=os.path.dirname(sys.argv[0])
full_path=os.path.abspath(file_path)


prog_classi= SourceFileLoader('classi_mrpg', file_path+'\\classi_mrpg.py').load_module()
prog_azioni= SourceFileLoader('azioni_mrpg', file_path+'\\azioni_mrpg.py').load_module()
from classi_mrpg import Pg, Mago, Berserk, Arrancar, personaggi, domini, attributi, classi_combattimento, abilità_Arrancar, debolezze_Arrancar, nomi_personaggi
from azioni_mrpg import azioni_totali, azioni_Berserk, azioni_Mago, azioni_Arrancar, creazione_personaggio, creazione_nemico_base, cambiare_dominio_spell, attacco_psichico, potenziamento, rigenera, analizza, attacco_cero, cura, sonido, difenditi, attacca, azioni, azioni_con_oggetto

pg_suoiturni={}
pg_vel_dict={}
sorted_pg_vel_dict={}
##########################################################################################################################################################
#####################################                           personaggi speciali                         ############################################## 
##########################################################################################################################################################

vel1=randint(20,30)
hp1=randint(50,100)
vel2=randint(30,50)
hp2=randint(50,100)
vel3=randint(20,50)
hp3=randint(50,200)
Ulquiorra=Arrancar("Ulquiorra",str(vel2),str(hp2),str(randint(5,10)+int((100-hp2)/50)-int(vel2/60)+2),str(randint(5,8)+int(vel2/30)), str(choice(debolezze_Arrancar)), str(choice(abilità_Arrancar)))
Peppe=Mago("Peppe",str(vel1),str(hp1),str(randint(5,10)+int((100-hp1)/50)+int(vel1/5)),str(randint(5,10)+int(vel1/25)), str(choice(domini)))
Alex=Berserk("Alex",str(vel3),str(hp3),str(randint(5,10)+int(3-hp3/50)+int(vel3/10)),str(randint(5,10)+int(vel3/40)))

##########################################################################################################################################################
#####################################                  TEST CON ALEX, PEPPE E ULQUIORRA                       ############################################     
##########################################################################################################################################################

#print(Ulquiorra.Scheda_pg,"\n")
#azioni("attacca", Ulquiorra, Peppe)
#creazione_personaggio()
#print(getattr(creazione_personaggio, "nome").Scheda_pg)
#azioni("attacca", getattr(creazione_personaggio, "nome"), Ulquiorra)

#########################################################################################################################################################
#####################################                      creazione personaggio e nemic                      ###########################################     
#########################################################################################################################################################

####### chiamata funzioni di creazione personaggio e nemici  #######

for i in range(0, randint(1,5)):
    creazione_nemico_base(f"Mostro_{i}")
    
    
creazione_personaggio()


#print(f"\n personaggi= {personaggi[i]}\n")

#print(getattr(globals()[personaggi[0]], "nome"))
#print(getattr(creazione_personaggio,"nome").attributo("velocità"))
#print(getattr(creazione_nemico_base, "nome").attributo("nome"))
#print(Ulquiorra.Scheda_pg)
#print(creazione_personaggio.nome.nome)
#print(creazione_nemico_base.nome.Scheda_pg)
#for i in range(0,len(personaggi)):                                                                  
#    print(f"{personaggi[i].nome}, {personaggi[i].velocità}\n")
    
    
############################################################################################################
################################          DEFINIZIONE TURNI                #################################     
############################################################################################################ 

vel_tot=0
vel_min=1000
for persona in personaggi:
   vel_tot+=int(getattr(persona, "velocità"))
   if int(getattr(persona, "velocità")) < vel_min:
      vel_min=int(getattr(persona, "velocità"))
for persona in personaggi:      
   suoi_turni=int(round(float(getattr(persona, "velocità"))/vel_min))
   pg_suoiturni.setdefault(persona.nome,suoi_turni)
   pg_vel_dict.setdefault(persona.nome, int(getattr(persona, "velocità")))

sorted_pg_vel_list=sorted(pg_vel_dict.items(), key=lambda x: x[1], reverse=True)
sorted_pg_vel_dict=dict(sorted_pg_vel_list)
pg_suoiturni_list=list(pg_suoiturni.items())

numero_turni=0
for p in pg_suoiturni.keys():
   numero_turni+=pg_suoiturni[p]


z=0
n_turni_prec=0
turni=[]
for n in range(0,numero_turni):
   turni.append(0)
    
j=0
while j >= 0 and j<= numero_turni-1:
   salto=pg_suoiturni[sorted_pg_vel_list[j-n_turni_prec][0]]
   ripetizione=salto-1
   for i in range(j, j+1+ripetizione):
       turni[i]=sorted_pg_vel_list[j-n_turni_prec][0]
   n_turni_prec+=ripetizione
   j+=salto
    
#print(f"\n turni= {turni}\n")
       
input()    

      
############################################################################################################
####################################          combattimento                #################################     
############################################################################################################      
ciclo=0
combattimento=True

while combattimento:
   ciclo+=1
   if ciclo == 1:
      print(f"\n\n-----------------------------------    Inizio del combatimento     -----------------------------------\n\n")
   else:
      print(f"\n\n-----------------------------------    Fine Turno {ciclo-1}     -----------------------------------\n\n")
   input()
   print(f"\nProssimi turni= {turni}\n")
   soggetto_stringa=turni[0]
   turni.pop(0)
   turni.append(soggetto_stringa)
   
   for p in personaggi:
      if p.nome==soggetto_stringa:
         soggetto=p
    
   if personaggi.index(soggetto)<len(personaggi)-1:
      oggetto=personaggi[personaggi.index(soggetto)+1]
   else:
      oggetto=personaggi[0]
   
   print("\n\n---------------------------------------------------------------------------------------------------")
   print(f"\n--------------------------------------Turno di {soggetto.nome}-------------------------------------\n")
   print("---------------------------------------------------------------------------------------------------\n")
   
   ############ azione giocatore ############  
   
   if soggetto.nome==creazione_personaggio.nome:
      print(f"Le tue azioni disponibili sono:")
      if soggetto.classe== "Mago":
         print(f"      {azioni_Mago}\n")
      elif soggetto.classe== "Arrancar":
         print(f"      {azioni_Arrancar}\n")
      else:
         print(f"      {azioni_Berserk}\n")
         
      ciclo_azione=True   
      while ciclo_azione:
         azione=input("Quale azione vuoi effettuare?")
         if soggetto.classe== "Mago" and azione.casefold() in azioni_Mago:
            ciclo_azione=False 
         elif soggetto.classe== "Arrancar" and azione.casefold() in azioni_Arrancar:
            ciclo_azione=False 
         elif azione.casefold() in azioni_Berserk:
            ciclo_azione=False 
         else:
            ciclo_azione=True 
                     
     
      if azione.casefold() in azioni_con_oggetto:
         print(f"\nScegli il target di {azione} tra:\n") 
         ciclo_target=True          
         for target in personaggi:
            print(f"{target.nome}\n")
         while ciclo_target:
             oggetto_stringa=input("\nChi hai scelto? ") 
             for p in personaggi:
                 if ciclo_target:
                     if p.nome==oggetto_stringa or p==oggetto_stringa: 
                        oggetto=p
                        ciclo_target=False
                     else:
                        ciclo_target=True
   

   ############ azione mostri ############           
   else:
      try:
         if soggetto.classe== "Mago":
            azione=azioni_Mago[randint(0, len(azioni_Mago)-1)]
         elif soggetto.classe== "Arrancar":
            azione=azioni_Arrancar[randint(0, len(azioni_Arrancar)-1)]
         else:
            azione=azioni_Berserk[randint(0, len(azioni_Berserk)-1)]        
      except AttributeError:
         azione=azioni_Berserk[randint(0, len(azioni_Berserk)-1)]
      
            
         
      if azione in azioni_con_oggetto:
         if azione.casefold()=="cura":
            oggetto=soggetto
         else:
            scelta_target_nemici=True
            while scelta_target_nemici:
               oggetto=personaggi[randint(0,len(personaggi)-1)]
               if oggetto.nome!=soggetto_stringa:
                  scelta_target_nemici=False
               else:
                  scelta_target_nemici=True            
      if azione.casefold()=="analizza" or azione.casefold()=="cambio dominio":
         azione="attacca"
                    
   
   ############  Chiamata alla funzione di azione ed effetti aggiuntivi legati ai turni   ################
   
   ogg_nome=getattr(oggetto,"nome")
   if azione in azioni_con_oggetto: 
      print(f"\n{soggetto.nome} decide di usare {azione} su {ogg_nome} \n") 
   else:
      print(f"\n{soggetto.nome} decide di usare {azione}\n") 
      
   
   azioni(azione,soggetto,oggetto)
   
   turni_bersaglio=0
   if azione.casefold() == "sonido":
      turni.insert(0, soggetto_stringa)
      turni.pop(len(turni)-1)
   elif azione.casefold()=="attacco psichico":
      for i in range(0, len(turni)):
         if turni[i]==oggetto.nome:
            turni_bersaglio+=1
      if turni_bersaglio > 2:
         turni.remove(oggetto.nome)
      else:
         print(f"\n ...,ma {oggetto.nome} è già abbastanza lento, quindi non perderà turni!")
      if soggetto.dominio=="psico":
         print(f"\n{soggetto.nome} usa il dominio {soggetto.dominio} per bloccare ulteriormente {oggetto.nome}!")
         turni.remove(oggetto.nome)
    
   
   ############ rimozione dei personaggi con HP <=0  ################
   
   
   posiz=[]
   recess=0
   for al in personaggi:
      if int(al.vita) <= 0:
         frasi_morte=[f"{al.nome} viene massacrato!", f"{al.nome} viene ucciso da un colpo micidiale!", f"{al.nome} è fuori dal combattimento!",f"{al.nome} perde la vita!"]
         print(frasi_morte[randint(0, len(frasi_morte)-1)])
         for i in range(0,len(turni)):
             if turni[i]==al.nome:
                posiz.append(i-recess)
                recess+=1
         personaggi.remove(al) 
      for j in range(0,len(posiz)):
          turni.pop(posiz[j])
      posiz.clear()   
   
   ############ Vittoria o sconfitta   ################
   
   altri=[]
   for p in personaggi:
      if p.nome!=creazione_personaggio.nome:
         altri.append(p)    
         
   if len(altri)==0:
      print("------------------------------------------------------------------------------------------------------------")
      print("---------------------------------          Congratulations        ------------------------------------------")
      print("---------------------------------             YOU WIN             ------------------------------------------")
      print("------------------------------------------------------------------------------------------------------------")
      combattimento=False
         
   for p in personaggi:
      if p.nome == creazione_personaggio.nome:
         protagonista=p   
         
   if int(protagonista.vita) <=0:
      print("------------------------------------------------------------------------------------------------------------")
      print("---------------------------------             YOU LOSE!           ------------------------------------------")
      print("---------------------------------         TRY ANOTHER TIME        ------------------------------------------")
      print("------------------------------------------------------------------------------------------------------------")
      combattimento=False
   else:
      continue





