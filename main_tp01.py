from corrige_tp01 import Aspirateur_KB, World, KB, Rule, objetsStatiques
import numpy as np # pour faire des stats simples
# from monde import AspiVoyant

def test_performance(w,n,nb=10):
    """
        w: le monde qui fait la simulation
        n: la durée d'une simulation
        nb: le nombre total de simulation
        
        ATTENTION: compteurs est un dictionnaire que j'ai ajouté à Aspirateur_KB et qui est réinitialisé
        à chaque simulation, il est rempli dans Aspirateur_KB.getDecision
    """
    res={}
    # assert isinstance(w,World),"World instance required"
    _resultat={'agent': [], 'world': [], }
    for i in range(nb):
        # print("simulation %02d" % (i+1))
        w.simulation(n)
        # print(w.agent.compteurs)
        _resultat['agent'].append(w.agent.getEvaluation())
        _resultat['world'].append(w.perfGlobale)
        # print("eval agent {0[agent]} vs perf globale {0[world]}".format(_resultat))
        # print(w) ; print("table: {0.table} posAgent is {0.posAgent}".format(w))
        # print(w.agent.knowledge)
        # print("Historique")
        for i,((t,p),a) in enumerate(w.historique):
            pass
            # print("%02d: table %s position %s action %s" % (i,t,p,a))
        # print("_"*23)
    _evalAgent = {'v':np.array( _resultat['agent'] ), 'name':"Evaluation Agent"}
    _globalPerf = { 'v': np.array( _resultat['world'] ), 'name': "Performance Globale"}
    for data in (_evalAgent,_globalPerf):
        # print("statistiques",data['name'])
        arr = data['v']
        # print("moyenne", round(np.mean( arr ),3))
        # print("mediane", round(np.median( arr ),3) )
        # print("minimum", round(np.min( arr ),3))
        # print("maximum", round(np.max( arr ),3))
        # print("EcT", round(np.std( arr ),3))
        #ajout:
        res[data['name']]=round(np.mean( arr ),3)
    # print(res)
    return res
    

def build_base():
    """ exemple pour 2 capteurs [8,2] """
    _maBase = KB()
    _obj = [ _ for _ in objetsStatiques if 0<= _ < 100 ] # objets possibles
    _objBord = _obj[:] # Obligatoire si on ne veut pas que _obj subisse la modification suivante
    _objBord.append(-1) # objets possibles + bord du monde (erreur)
    # Aspirer si 1 en 8
    for x in _objBord:
        _maBase.add( Rule([1,x],'Aspirer',.2) )
    # Aller à Droite si 0 en 8, n'importe en 2
    for x in _obj:
        _maBase.add( Rule([0,x],'Droite',.1) )
    # Aller à Gauche si n'importe quoi en 8 et -1 en 2
    for x in _obj:
        if x!= 1: _maBase.add( Rule([x,-1], 'Gauche', .1) )
    return _maBase
    
if __name__ == "__main__":
    import pylab as py 
    import matplotlib.pyplot as plot 

    # input("Aléatoire")
    # a = Aspirateur_KB(.7)
    # w = World(a)
    # test_performance(w,4)
    # input("Apprenant")
    # b = Aspirateur_KB(0.75,[8,2],learn=True)
    # w = World(b)
    # test_performance(w,4)
    # input("Base forcée")
    # c = Aspirateur_KB(0.7,[8,2])
    # c.knowledge = build_base()
    # w = World( c )
    # test_performance(w,4)

    #Stochy
    a = Aspirateur_KB(.7)
    nb_cols=40
    mondes = [World(a, 1, i) for i in range(1, nb_cols)]
    eval_monde = list()
    eval_agent = list()
    for monde in mondes:
        dico=test_performance(monde,2*len(monde.table[0]),10)
        eval_monde.append(dico['Performance Globale'])
        eval_agent.append(dico['Evaluation Agent'])
    # py.plot(list(range(1, nb_cols)), eval_monde, "Red", label='Stochy')
    py.plot(list(range(1, nb_cols)), eval_agent, "Red", label='Stochy')


    #Learny
    a = Aspirateur_KB(0.75,[8,2],learn=True)
    mondes = [World(a, 1, i) for i in range(1, nb_cols)]
    eval_monde = list()
    eval_agent = list()
    for monde in mondes:
        a.knowledge = KB()
        dico = test_performance(monde,2*len(monde.table[0]),10)
        eval_monde.append(dico['Performance Globale'])
        eval_agent.append(dico['Evaluation Agent'])
    # py.plot(list(range(1, nb_cols)), eval_monde, "Blue", label='Learny')
    py.plot(list(range(1, nb_cols)), eval_agent, "Blue", label='Learny')


    #Deter
    a = Aspirateur_KB(0.75,[8,2],learn=False)
    mondes = [World(a, 1, i) for i in range(1, nb_cols)]
    eval_monde = list()
    eval_agent = list()
    for monde in mondes:
        a.knowledge = build_base()
        dico = test_performance(monde, 2*len(monde.table[0]),10)
        eval_monde.append(dico['Performance Globale'])
        eval_agent.append(dico['Evaluation Agent'])
    # py.plot(list(range(1, nb_cols)), eval_monde, "green", label='Base forced')
    py.plot(list(range(1, nb_cols)), eval_agent, "green", label='Base forced')
    

    py.legend(loc='upper left')
    py.xlabel("Taille du monde (nombre de colonnes)")
    py.ylabel("Performance")
    # py.title("Nouvelle cover des Arctic Monkeys")
    py.title("Point de vue agent : (getEval -> Original)")
    plot.show()


    # #deter
    # a = AspiVoyant([8,2])
    # nb_cols=40
    # mondes = [World(a, 1, i) for i in range(1, nb_cols)]
    # eval_monde = list()
    # eval_agent=list()
    # for monde in mondes:
    #     dico=test_performance(monde,2*len(monde.table[0]),10)
    #     # print(dico)
    #     eval_monde.append(dico['Performance Globale'])
    #     eval_agent.append(dico['Evaluation Agent'])
    # # py.plot(list(range(1, nb_cols)), eval_monde, "Purple", label='Performance Globale')
    # py.plot(list(range(1, nb_cols)), eval_agent, "orange", label='Evaluation Agent deter nous 1')
    # py.legend(loc='lower right')
    # py.xlabel("Taille du monde (nombre de colonnes)")
    # py.ylabel("Performance")

    # mondes = [World(a, 1, i) for i in range(1, nb_cols)]
    # eval_monde = list()
    # eval_agent=list()
    # for monde in mondes:
    #     dico=test_performance(monde,2*len(monde.table[0]),10)
    #     # print(dico)
    #     eval_monde.append(dico['Performance Globale'])
    #     eval_agent.append(dico['Evaluation Agent'])
    # # py.plot(list(range(1, nb_cols)), eval_monde, "Purple", label='Performance Globale')
    # py.plot(list(range(1, nb_cols)), eval_agent, "brown", label='Evaluation Agent deter nous 2')
    # py.legend(loc='lower right')
    # py.xlabel("Taille du monde (nombre de colonnes)")
    # py.ylabel("Performance")


    # mondes = [World(a, 1, i) for i in range(1, 20)]
    # ord = list()
    # for monde in mondes:
    # # monde.simulation(2*len(monde.table[0]))
    #     ord.append(monde.simulation(2*len(monde.table[0])))
    # coeff = linregress(list(range(1, 20)), ord)
    # _a = coeff[0]
    # _b = coeff[1]
    # ordo = list()
    # for i in range(1, 20):
    #     ordo.append(_a*i + _b)

    # py.plot(list(range(1, 20)), ordo, "Green")
    # py.xlabel("Taille du monde (nombre de colonnes)")
    # # py.ylabel("#Cases avec poussiere debut / #Cases avec poussiere fin")
    # # py.ylabel("#Pieces netoyees - #de cases ou il passe 3+ fois")
    # py.title("Aspi v1 (Deter)")
    # plot.show()
    
