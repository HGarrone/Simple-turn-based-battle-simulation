
####### librerie #############

import os
import sys
#from importlib.machinery import SourceFileLoader
import math
from random import *
import numpy as np
import matplotlib.pyplot as plt
import gc

####### importo altri programmi e determino il path #############

#nel caso in cui il programma non trovasse il path corretto sostituirlo con file_path=<path_corretto>. Se utilizzate Windows utilizzate \\ anzichè \ nel path. 

file_path=os.path.dirname(sys.argv[0])
full_path=os.path.abspath(file_path)
#mrpg= SourceFileLoader('mrpg', file_path+'\\mrpg.py').load_module()

####### inizializzazione #############

attributi=["velocità","vita","CA","tecnica","tiro_colpire","danno"]
classi_combattimento=["Mago", "Berserk", "Arrancar"]
domini=["fuoco", "acqua", "terra", "aria", "elettricità", "gravità", "psico", "cura", "potenziamento", "difesa"]
abilità_Arrancar=["rigenerazione", "sonido", "cero"]
debolezze_Arrancar=domini[0:6]+["nessuno"]
personaggi=[]
nomi_personaggi=[]
classi_programma=[]

###### classe genitore ################

class Pg:

    tiro_colpire=0
    danno=0
    n_pg=0
    
    def __init__(self,nome,velocità,vita,CA,tecnica):     #classe che viene inizializzata con __init__ e deve avere self come primo input e le proprietà devono essere chiamate con self.proprietà=proprietà
        self.nome=nome
        self.velocità=velocità
        self.vita=vita
        self.CA=CA
        self.tecnica=tecnica
        Pg.n_pg+=1
        personaggi.append(self)
        nomi_personaggi.append(self.nome)
        classi_programma.append(type(self).__name__)
        
    @classmethod                                                        ###decoratore per far passare classe a costruttore alternativo
    def da_stringa(cls, stringa_nemico, *args):                                ### metodo a cui si passa classe e non istanza self che legge da stringa
        nome, velocità, vita, CA, tecnica=stringa_nemico.split(";")
        return cls(nome, velocità, vita, CA, tecnica, *args)   
    @classmethod
    def nome_classe(cls):
        return cls.__name__    
    @property        
    def Scheda_pg (self):                                     #funzione interna alla classe che restituisce la scheda o l'istanza come istanza.funzione(), classe.funzione(istanza)
        return f"\nCombattente:    nome: {self.nome}\n\t\tvelocità: {self.velocità}\n\t\tvita: {self.vita}\n\t\tCA: {self.CA}\n\t\ttecnica: {self.tecnica}\n"   #è uguale usare Pg.tiro_colpire o self.tiro_colpire perchè tiro_colpire è una variabile di classe quindi ce l'hanno anche tutte le classi_programma 
    @property
    def trova_classe_con_array (self):
        return classi_programma[personaggi.index(self.nome)]
    @classmethod
    def trova_classe (cls, nome, stringa):
        return [type(obj).__name__ for obj in gc.get_objects() if isinstance(obj, cls) and getattr(obj, nome)==stringa]
    @property        
    def __str__(self):                                                                                                                                                                                                                      
        return f"Nome {self.nome}"
    @property
    def __repr__(self):
        return f"Nome{self.nome}, istanza" 
    
    def attributo(self, attrib):
        return getattr(self, attrib)
    
    def cambio_attributo (self, attrib, value):
        setattr(self,attrib,value)
        return getattr(self, attrib)
        
        
#######################################################
##################### classi figlie ###################
#######################################################


class Arrancar(Pg):
      pass
      classe="Arrancar"
      tiro_colpire=0
      danno=0
      def __init__(self,nome,velocità,vita,CA,tecnica,debolezza,specialità=None):
        super().__init__(nome,velocità,vita,CA,tecnica)
        self.debolezza=debolezza       
        if specialità is None:
            self.specialità = []
        else:
            self.specialità = []
            self.specialità.append(specialità)  
      @property            
      def Scheda_pg(self):
        scheda=f"\t\tClasse: {Arrancar.classe}\n\t\tSpecialità: {self.specialità}\n\t\tDebolezza: {self.debolezza}\n"
        return super().Scheda_pg+scheda
      def aggiungi_specialità(self,nuova_specialità):
        if nuova_specialità not in self.specialità:
           self.specialità.append(nuova_specialità)
           print(f"\n{self.nome} ha appreso: {nuova_specialità}!")
      @staticmethod
      def info ():
        informazione="La classe Arrancar e il personaggio Ulquiorra arrivano dall'anime Bleach"
        return informazione        
 
class Mago(Pg):
      classe="Mago"
      tiro_colpire=0
      danno=0
      def __init__(self,nome,velocità,vita,CA,tecnica,dominio):
        super().__init__(nome,velocità,vita,CA,tecnica)
        self.dominio=dominio 
      @property        
      def Scheda_pg(self):
        scheda=f"\t\tClasse: {Mago.classe}\n\t\tTipo di magia: {self.dominio}\n"
        return super().Scheda_pg+scheda
      @property
      def mostra_dominio(self):
          return self.dominio
    
      def cambio_dominio(self,dom):         
          if dom in domini:
              setattr(self, "dominio", dom)
              print(f"\nDominio delle spell cambiato in {dom}")
          else:
              print("\nDominio non valido")
              
          
        
        
class Berserk(Pg):
      classe="Berserk"
      tiro_colpire=0
      danno=0
      def __init__(self,nome,velocità,vita,CA,tecnica):
        super().__init__(nome,velocità,vita,CA,tecnica)
        self.resistenza=0
        self.critico=False
      @property
      def Scheda_pg(self):
        scheda=f"\t\tClasse: {Berserk.classe}\n\t\tResistenza: {self.resistenza}\n\t\tCritico: {self.critico}\n"
        return super().Scheda_pg+scheda
      @property
      def colpo_critico(self):
        crit=randint(1,10)
        if crit == 10:
           setattr(self, "critico", True)
        else:
           setattr(self, "critico", False)
        return self.critico
      @property
      def attiva_resistenza(self):
        attivazione=randint(0,4)
        if attivazione > 2:
           resist=randint(1,10)
        else:
           resist=0
        setattr(self, "resistenza", 0)
        return resist
        

         
#print(f"personaggi in classi_mrpg: {personaggi}")  
        

