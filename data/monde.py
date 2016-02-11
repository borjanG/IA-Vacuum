#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Generic python libs
from random import randrange, choice
from copy import deepcopy

#This code contains easter eggs.
__author__ = "Terral, Rodriguez, Geshkovski"
__date__ = "09.02.16"
__version__ = "0.3"

objetsStatiques = {100: ('aspirateur', '@'),
                   0: ('rien', ' '),
                   1: ('poussiere', ':')}

#Liste de cles
d = list(objetsStatiques.keys())

                          # ------------ #    
# ----------------------- # --- MONDE -- # --------------------------------------#
                          # ------------ #

class Monde(object):

  def __init__(self, a, l=1, c=2):
    """ Monde constructor """

    assert isinstance(a, Aspirateur), "Il faut un Stochy en parametre"
    assert type(l) == int and type(c) == int, "Il faut des entiers pour dimensions"
    
    self.__agent = a 
    self.__lignes = l
    self.__cols = c
    self.__table = [[0 for j in range(c)] for i in range(l)]
    # self.__table = [[choice(set(d) - set(100)) for j in range(c)] for i in range(l)]
    self.__posAgent = (0,0)
    self.__historique = []
    self.__perfGlobale = 0.0


  #Deepcopy car hash table & liste de listes
  # @property 
  # def objetsStatiques(self):
  #   return deepcopy(objetsStatiques)
  @property
  def table(self):
    # assert(self.__table.count(0)+self.__table.count(1) == self.__lignes*self.__cols)
    return deepcopy(self.__table)
  @property 
  def posAgent(self):
    #Shallow copy suffit
    return self.__posAgent[:]

  @property 
  def agent(self):
    return self.__agent 
  @property 
  def historique(self):
    return deepcopy(self.__historique)
  @property 
  def perfGlobale(self):
    return self.__perfGlobale

  def applyChoix(self, action):
    """ Mise a jour du monde et de la position de l'agent en fonction 
        de son choix """

    if action == "Gauche":
      if 0 < self.posAgent[1]:
        if self.table[self.posAgent[0]][self.posAgent[1]-1] == 2:
          pass
        else:
          self.__posAgent = (self.posAgent[0], self.posAgent[1]-1)
      else:
        pass

    if action == "Droite":
      if self.__cols -1 > self.posAgent[1]:
        if self.table[self.posAgent[0]][self.posAgent[1]+1] == 2:
          pass
        else:
          self.__posAgent = (self.posAgent[0], self.posAgent[1]+1)
      else:
        pass

    if action == "Aspirer":
      if self.table[self.posAgent[0]][self.posAgent[1]] == 1:
        self.__table[self.posAgent[0]][self.posAgent[1]] = 0
      else:
        pass

    return 0.

  # /!\ A MODIF.
  def getPerception(self, capteurs = []):
    """ Recuperation des valeurs dans les cases 
        disponibles au aspirateur par ses capteurs """
    assert isinstance(capteurs, list)

    i = self.posAgent[0]
    j = self.posAgent[1]

    seer = [(i-1,j), (i-1,j+1), (i,j+1), (i+1,j+1), (i+1,j),
            (i+1,j-1), (i,j-1), (i-1,j-1), (i,j)]

    oracle = []
    for flash in capteurs:
      x = seer[flash][0]
      y = seer[flash][1]
      if 0 <= x < len(self.table) and 0 <= y < len(self.table[0]):
        oracle.append(self.table[x][y])
      else:
        oracle.append(-1)

    return oracle

  def __str__(self):
    """ Generic string method
        Unicode:
        \u2550: ═ ; \u2564: ╤
        \u2500: ─ ; \u253C: ┼
        \u2567: ╧ ; \u2554: ╔
        \u2557: ╗ ; \u2551: ║
        \u255A: ╚ ; \u255D: ╝
    """

    tab = []
    key = max(objetsStatiques.keys()) #Pas plus de 100 keys qd meme

    #Genere le tableau
    for i in range(len(self.table)):
      tab.append([])
      for j in range(len(self.table[0])):
        tab[i].append(objetsStatiques[self.table[i][j]][1])
    tab[self.posAgent[0]][self.posAgent[1]] += objetsStatiques[key][1]
    # tab[self.posAgent[0]][self.posAgent[1]] = objetsStatiques[key][1]

    l = len(tab)
    c = len(tab[0])
    _=[]

    #Strings utiles
    _head = "\u2550"*3 + "\u2564"
    _mid = "\u2500"*3 + "\u253C"
    _foot = "\u2550"*3 + "\u2567"

    header = "\u2554" +_head*(c-1) + "\u2550"*3 + "\u2557"
    middle = "\u2551" +_mid*(c-1) + "\u2500"*3 + "\u2551"
    footer = "\u255A" +_foot*(c-1) + "\u2550"*3 + "\u255D"

    #Header
    _.append(header)

    #Middle
    #Ligne 0
    _elt = "\u2551" + "%3s" %(tab[0][0]) #Premier element
    if c > 1:
      for j in range(1, c):
        _elt += "\u2502" + "%3s" %(tab[0][j])
    _elt += "\u2551"
    _.append(_elt)

    #Autres lignes (s'il y en a)
    if l > 1:
      for i in range(1, l):
        _.append(middle)
        _elt = "\u2551" + "%3s" %(tab[i][0]) #ligne i col 0
        if c > 1:                  #autres cols s'il y en a
          for j in range(1, c):
            _elt += "\u2502" + "%3s" %(tab[i][j])
        _elt += "\u2551"
        _.append(_elt)

    #Footer      
    _.append(footer)
    
    return "\n".join(_)

  def step(self):
    """ Ce qui se passe ~ un etat """

    percept = self.getPerception(self.agent.capteurs)
    choix = self.agent.getDecision(percept)
    self.__historique.append(((self.table, self.posAgent), choix))
    self.agent.setReward(self.applyChoix(choix))
    self.updateWorld()
    
  def simulation(self, n = 42):
    """ Execution de n etats et evolue le monde """
    # assert n == 2*len(self.table), "2*taille du monde pour n!"

    self.initialisation()
    # print(self)

    while self.agent.vivant and n > 0:
      self.step()
      # print(self)
      # print("A fait : ",self.historique)
      n-=1

    # self.__historique = []
    self.agent.setReward(self.perfGlobale)
    return self.perfGlobale 

  def initialisation(self):
    """ Initialisation du monde """
    self.__posAgent = (randrange(self.__lignes), randrange(self.__cols))
    
    self.__table = [[randrange(len(objetsStatiques)-1)
                              for j in range(self.__cols)]
                              for i in range(self.__lignes)]

  def updateWorld(self):
    """ Mise a jour aleatoire du monde dynamique """
    #Agit sur table 
    pass

                          # ------------ #    
# ----------------------- # --- AGENT -- # --------------------------------------------------------#
                          # ------------ #

class Aspirateur(object):
  """ Aspirateur constructor """

  def __init__(self, capteurs = [], actions = ['Gauche', 'Droite', 'Aspirer']):
    assert isinstance(capteurs, list) and set(capteurs).issubset(set(range(9))) and len(set(capteurs)) == len(capteurs), "I'm blind!"
    assert isinstance(actions, (list, tuple)) 
    #Les sets c'est trop fort en python yep.

    self.__vivant = True
    self.__capteurs = capteurs
    self.__actions = actions
    self.__reward = 0

  @property 
  def vivant(self):
    return self.__vivant

  @property 
  def capteurs(self):
    return self.__capteurs 

  @property 
  def actions(self):
    return self.__actions

  def getDecision(self, percept = []):
    """ Renvoie une action en accord avec l'etat de l'environnement """
    assert set(percept).issubset(set(d).union([-1])), "I'm blind!"

    index = randrange(len(self.actions))
    action = self.actions[index]
    return action 

  def getEvaluation(self):
    """ Recupere l'evaluation """
    return 0.

  def setReward(self, reward):
    """ Associe une recompense au aspirateur """

    assert isinstance(reward, (float, int)), ' Stochy veut un nombre!'
    self.__reward = reward

  def getLastReward(self):
    return self.__reward

                          # ------------- #
# ----------------------- # --- FILLES -- # --------------------------------------------------------# 
                          # ------------- #

class AspiClairvoyant(Aspirateur):
  """ Aspirateur qui voit le contenu de sa propre case """

  def __init__(self, capteurs = [8], actions = ['Gauche', 'Droite', 'Aspirer']):
    super().__init__(capteurs, actions)

  def getDecision(self, percept = []):
    """ Renvoie une action en accord avec l'etat de l'environnement """
    assert set(percept).issubset(set(d).union([-1])), "I'm blind!"
    
    if percept[0] == 1:
      #Much ado about nothing
      action = self.actions[self.actions.index('Aspirer')]
    else:
      choix = list(set(actions)-{'Aspirer'})
      action = choice(choix) 

    return action

class AspiVoyant(Aspirateur):
  """ Aspirateur qui aspire la salete uniquement """

  def __init__(self, capteurs = [8,2], actions = ['Gauche', 'Droite', 'Aspirer']):
    super().__init__(capteurs, actions)

  # /!\ A MODIF.
  def getDecision(self, percept = []):
    """ Renvoie une action en accord avec l'etat de l'environnement """
    assert set(percept).issubset(set(d).union([-1])), "I'm blind!"
  
    if len(percept) == 1:
      if percept[0] == 1:
        #Much ado about nothing
        action = self.actions[self.actions.index('Aspirer')]
      else:
        choix = list(set(actions)-{'Aspirer'})
        action = choice(choix) 
    else:
      if percept[self.capteurs.index(8)] == 1:
        action = 'Aspirer'
      else:
        if percept == [0, 1]:
          action = 'Droite'
        #Si jamais double gauche retour a droite
        else:
          action = 'Gauche'
    return action