#!/usr/bin/python3
# -*- coding: utf-8 -*-

__usage__ = "tp01"
__author__ = "mmc, Terral, Rodriguez, Geshkovski"
__date__ = "28.02.16"
__version__ = "0.3"

#Custom py libs
from monde import objetsStatiques, Aspirateur, Monde
from briques import Rule, KB
#Generic py libs
import copy
from random import choice, random
# import collections
objetsStatiques[-1] = ('erreur','?')

class Aspirateur_KB(Aspirateur):
    """ 4 paramètres
        probaExploitation: pas de valeur par défaut
        lCap: valeur par défaut []
        lAct: valeur par défaut la liste des 3 actions Gauche Droite Aspirer
        learn: valeur par défaut False (pas d'apprentissage)
    """
    def __init__(self, probaExploitation, lCap=[], lAct="Gauche Droite Aspirer".split(), learn=False):
        super(Aspirateur_KB,self).__init__(lCap,lAct)

        assert 0 <= probaExploitation <= 1, "Probability expected"
        assert isinstance(learn, bool), "Boolean expected got %s" % type(learn)
        
        self.__knowbase = KB()     # base de données vide
        self.__probaExploitation = probaExploitation
        self.__learn = learn
        self.__lastAction = None  # dernière action choisie
        self.__lastPercept = None # dernier percept reçu
        # self.compteurs = collections.OrderedDict()
        self.compteurs = {'alea': 0, 'exploitation' : 0, 'total' : 0, 'exploration': 0}
        
    @property
    def apprentissage(self): return self.__learn
    @apprentissage.setter
    def apprentissage(self, v):
        assert isinstance(v, bool), "pas bool."
        self.__learn = v    
    @property
    def knowledge(self): return copy.deepcopy(self.__knowbase)
    @knowledge.setter
    def knowledge(self, v):
        assert isinstance(v, KB), "pas KB"
        self.__knowbase = v   
    @property
    def probaExploitation(self): return self.__probaExploitation
    
    # def getEvaluation(self): 
    #     # super().getEvaluation()
    #     return (self.nettoyage+1)/(len(self.knowledge)+1)
        
    def getDecision(self, percepts):
        assert isinstance(percepts,(list,tuple)), "%s should be list or tuple" % percepts
        assert len(percepts) == len(self.capteurs), "percepts and capteurs do not match"
        assert all([x in objetsStatiques for x in percepts]), "bad percepts %s" % percepts

        self.__lastPercept = percepts
        rule_lst = self.__knowbase.find(percepts)

        if len(rule_lst) == 0:
            action = choice(self.actions)
            self.compteurs['alea'] += 1
        else:
            base_actions = [regle.conclusion for regle in rule_lst]
            notbase_actions = list(set(self.actions) - set(base_actions))
            best_rule = max(rule_lst, key = lambda rule: rule.scoreMoyen)
            r = random()
            if r < self.probaExploitation:
                action = best_rule.conclusion
                self.compteurs['exploitation'] += 1
            else:
                num = rule_lst.index(best_rule)
                other_rules = rule_lst[:num] + rule_lst[(num+1):]
                if len(other_rules) !=0:
                    _ = choice(other_rules)
                    action = _.conclusion
                    if _.scoreMoyen < 0 and len(notbase_actions) != 0:
                        action = choice(notbase_actions)
                else:
                    action = choice(notbase_actions)
                self.compteurs['exploration'] += 1 

        self.compteurs['total'] += 1
        self.__lastAction = action
        return self.__lastAction
        
    def setReward(self, value):
        super(Aspirateur_KB,self).setReward(value)
        if self.apprentissage:
            r = Rule(self.__lastPercept, self.__lastAction, value)
            _ = self.knowledge
            _.add(r)
            self.knowledge = _
              
class World(Monde):
    """ constructeur avec 3 paramètres, syntaxe identique au constructeur de Monde """
    def __init__(self,agent, nbLignes=1, nbColonnes=2):
        super(World,self).__init__(agent,nbLignes,nbColonnes)
        self.__cols = nbColonnes
        self.__lignes = nbLignes
    
    def initialisation(self):
        super(World,self).initialisation()
        self._passage = [[0 for j in range(len(self.table[0]))] for i in range(len(self.table))]
        i,j = self.posAgent
        self._passage[i][j] = 1
        self.agent.nettoyage = 0
        
    def getPerception(self,capteurs):
        """ informe l'agent en fonction des capteurs """

        delta = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (0,0)]
        res = []
        for x in capteurs:
            nx = self.posAgent[0] + delta[x][0]
            ny = self.posAgent[1] + delta[x][1]
            if self.__lignes > nx >= 0 and self.__cols > ny >= 0: 
                res.append(self.table[nx][ny])
            else: 
                res.append(-1)
        return res   
 
    def applyChoix(self, choix):
        """ modifie table & posAgent en fonction de choix """

        dx = self.posAgent[0]
        dy = self.posAgent[1]
        score = 0

        if choix == 'Aspirer':
            if self.table[dx][dy] == 1:
                self._table[dx][dy] = 0
                self.agent.nettoyage += 1
                score = 2
            else: score = 0
        else:
            if choix == 'Gauche':
                if dy > 0: 
                    self._posAgent = (dx, dy-1)
                    score = 1
                else: score = -1
            elif choix == 'Droite':
                if dy < self.__cols-1: 
                    self._posAgent = (dx, dy+1)
                    score = 1
                else: score = -1

        i, j = self.posAgent
        self._passage[i][j] += 1  
        return score
        
    @property
    def perfGlobale(self):
        #Charlotte
        # compteur=0
        # for elem in self._passage:
        #     for x in elem:
        #         if x >= 3: compteur+=1
        # return self.agent.nettoyage - compteur

        #Borjan
        T = 0
        for i in range(len(self._passage)):
            T += len(list(filter(lambda x: x>2, self._passage[i])))
        return self.agent.nettoyage - T

