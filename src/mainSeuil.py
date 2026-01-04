import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

############ fonction fermeture transitive ##############

def fermeture_transitive(M):
    M_transitive = np.matrix.copy(M)
    taille = np.shape(M)[0]
    for element in range (0,taille):
        precedant = []
        suivant = []
        
        #Obtention des suivants :
        for suiv in range(0,taille):
            if M_transitive[element][suiv] == 1:
                suivant.append(suiv)

        #Obtention des précédants
        for prec in range(0,taille):
            if M_transitive[prec][element] == 1 :
                precedant.append(prec)

        for p in precedant:
            for s in suivant:
                M_transitive[p][s] = 1
                
    return M_transitive

############ Test de forte connexité avec fermeture transitive ##############

def fc(M):
    M_transitive = fermeture_transitive(M)
    return np.all(M_transitive) 


M = np.array([
    [1, 1, 1, 1, 1],
    [0, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0]
])


if fc(M): print("Le graphe données par la matrice M non pondéré est fortement connexe")


############ Test de forte connexité pour un graphe avec p=50% de flèches ##############

def graphe(n, a, b):  #génére un graphe de taille n
    return rand.randint(a, b, (n, n))

def test_stat_fc(n):
    nb_connexe = 0
    for k in range (500):
        if fc(graphe(n,0,2)) == True :
            nb_connexe += 1
                  
    return (nb_connexe*100) / 500

def etude_statistique():
    n = 2
    while test_stat_fc(n) < 99:
        n+=1
    return n

print(f"l'affirmation ''Lorsqu’on teste cette fonction fc(M) sur des matrices de taille n avec n grand(500), avec une proportion p = 50% de 1 (et 50% de 0), on obtient presque toujours un graphe fortement connexe'' est vrai a partir d'un graphe de taille {etude_statistique()}")

############ Détermination du seuil de forte connexité ##############

def graphe2(n, p):
    return rand.binomial(1, p, (n,n))

def seuil(n):
    i = 0
    p = (n-i) / n 
    while test_stat_fc2(n,p) >= 99 and p > 0.1:
        i += 1
        p = (n-i)/n
    return p

def test_stat_fc2(n,p):
    nb_connexe = 0
    for k in range (50):
        if fc(graphe2(n,p)) == True :
            nb_connexe += 1
            
    return (nb_connexe*100) / 50

def rep_graph_seuil():
    effx = []
    valx = []
    for n in range (10,50):
        effx.append(seuil(n))
        valx.append(n)
    plt.figure(figsize=[6,6])
    
    plt.loglog(valx, effx, linestyle='-', marker='o', color='r', label="Courbe log-log")
    
    plt.title("Proportion de flèches par taille(n) pour être fortement connexe")
    plt.xlabel("Taille (n)")
    plt.ylabel("Proportion de flèches (seuil)")
    plt.legend()
    plt.show()

