import numpy as np
import matplotlib.pyplot as plt
from random import *
from math import *
import os
import inspect

## Données globales



n=6
partitions=[]
p_ajout=0
p_suppr=0
p_cat=0
p_statut=0
N=10
list_ex_danger=[]
list_ex_non_danger=[]
list_ex=[]

## Fonctions d'appartenance

def mu(a,b,c,d):
    def f(x):
        if x<a or x>d:
            return 0
        if x<b:
            return (x-a)/(b-a)
        if x>c:
            return (d-x)/(d-c)
        return 1
    return f

def trace_repere(xmax,ymax):
    plt.plot([0,0],[-ymax/20,ymax*1.1],'k')
    plt.plot([-xmax/20,xmax],[0,0],'k')
    plt.plot([0,xmax],[ymax,ymax],'--k')

def trace_mu(a,b,c,d):
    trace_repere(100,1)
    plt.plot([0,a,b,c,d,100],[0,0,1,1,0,0])

def trace_mu_simple(a,b,c,d): #Sans répéter le tracé des abcisses/ordonnées 
    plt.plot([0,a,b,c,d,100],[0,0,1,1,0,0])

def partition(l):
    def f(x):
        return [mu(0,0,l[0],l[1])(x)]+[mu(l[2*i],l[2*i+1],l[2*i+2],l[2*i+3])(x) for i in range((len(l)+2)//2-2)] + [mu(l[-2],l[-1],100,100)(x)]
    return f

def trace_partition(l): #On doit avoir len(l)=2n-2 avec n=nombre de fonctions mu
    trace_repere(100,1)
    trace_mu_simple(0,0,l[0],l[1])
    for i in range((len(l)+2)//2-2):
        trace_mu_simple(l[2*i],l[2*i+1],l[2*i+2],l[2*i+3])
    trace_mu_simple(l[-2],l[-1],100,100)

## Histogrammes

def histogramme_par_categorie(L, p, nb):    
    n = len(L)-2
    l = []
    for i in range(2,n+2):
        l += [L[i]]
    k = (nb+1)*n 
    X = []
    for i in range(n):
        res = trapeze(l[i], p, nb)
        for j in range(nb):
            for y in range(int(res[j]*100)+1):  # +1 permet de distinguer les éléments
                X += [100*(i*(nb+1)+j)/k]
                
    z = plt.hist(X, k-1)
    plt.show()

def histogramme(L,nombre_pics):
    a=100/(2*nombre_pics)
    length=len(L)
    X=np.linspace(a,100-a,nombre_pics)
    Y=[ sum([ mu(x-a,x-a,x+a,x+a)(i)/(2*a*length) for i in L]) for x in X]
    trace_repere(100,max(Y))
    plt.plot(X,Y,'o',ls='--')

# exemple : histogramme([random()*100 for i in range(5000)],200)

def f(X): # Pas important...
    return [(x-50)**3/50**3*50+50 for x in X]

## Création vecteur et chromosome
    
def vecteur_aleatoire(n):
    L=[random() for i in range(n)]
    total=sum(L)
    return [i*100/total for i in L]
    
def classe_dominante(x,parti): # Pour x, pourcentage pour un élément chimique et parti sa partition associée, renvoie la catégorie dominante de x
    l=parti(x)
    maxi,k=0,0
    for i in range(len(l)):
        if l[i]>maxi:
            maxi=l[i]
            k=i
    return k

def creer_gene(exemple): # Crée un gène adapté pour l'exemple
    n=len(vecteur)
    return [  [1,classe_dominante(vecteur[k+2],partitions[k])] for k in range(n)]+[exemple[1]]

# exemple : creer_gene([10,95,80,79],[partition([20,80]),partition([10,15,60,90]),partition([56,59]),partition([11,50,70,90])],1)

def creer_chromosome(liste_of_exemples):
    return [creer_gene(x) for x in list_of_exemples ]

## Fonctions d'évolution de la population

def muter_ajout(chromo,exemple):
    p=random()
    if p<=p_ajout:
        chromo+=creer_gene(exemple)

def muter_suppr(chromo):
    p=random()
    if p<=p_suppr:
        k=randint(0,n-1)
        chromo=chromo[:k]+chromo[(k+1):]

def muter_cat(chromo):
    p=random()
    if p<=p_cat:
        i = randint(0,len(chromo)-1)
        j=randint(0,n-1)
        s=randint(0,1)
        P=chromo[i][j]
        if s:
            if P[1]<nb-1:
                P[1]+=1
        else:
            if P[1]>0:
                P[1]-=1

def muter_statut(chromo):
    p=random()
    if p>=p_statut:  #muter le chromosome
        k=randint(0,len(chromo)-1)
        gen=chromo[k]   #on choisit un gène a muter
        j=randint(0,n-1)
        gen[j][0]=(gen[j][0]-1)**2
        

def croiser_chromo(chromo1,chromo2):
    c1=chromo1[:]
    c2=chromo2[:]
    chromo_fils=[]
    for regle in c1:
        if regle in c2:
            chromo_fils.append(regle)
            c1.remove(regle)
            c2.remove(regle)
    n1=len(c1)
    n2=len(c2)
    rd.shuffle(c1)
    rd.shuffle(c2)
    chromo_fils+=c1[:n1//2]+n2[n2//2:]
    return(chromo_fils)


## Fonction Fitness

def test(chromo, ex):
    ccl=[]
    for regle in chromo:
        certitude=1
        for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
            if regle[i][0]:
                certitude*= (partitions[i])(ex[i+2]) [regle[i][1]]   #partitions variable globale, liste de fonctions
        if certitude!=0:
            ccl.append(certitude, regle[-1])
    ccl.sort()
    return(ccl)


def score(ccl,ex):
    if ex[1]==1:
        note=ccl[-1][0]
    else:
        note=1-ccl[-1][0]
    return(note)

def fitness(chromo, list_ex):
    note=0
    N=len(litse_ex)
    for ex in list_ex:
        note+=score(test(chromo,ex),ex)
    return(note/N)


## Algo génétique

def creer_population(N):
    return creer_chromosome(list_ex_danger.shuffle[:N]) 

def selection(pop_ini):
    m=len(pop_ini)
    score=[(fct(pop_ini[i]),i) for i in range(m)]
    score.sort()                                                #attention, classe du plus petit au plus grand
    pop_fin=[pop_ini[score[i][1]] for i in range(m//2,m)]
    return(pop_fin)

def croiser_population(pop):
    rd.shuffle(pop)
    m=len(pop)
    pop+=[croiser_chromo(pop[i],pop[i+1]) for i in range(m-1)]
    pop+=croiser_chromo(pop[0],pop_ini[m-1])

def muter_pop(pop):
    for chromo in pop:
        muter_ajout(chromo,list_ex_danger[randint(0,len(list_ex_danger)-1)])       #list_ex_danger est une variable globale
        muter_suppr(chromo)
        for i in range(len(chromo)):
            muter_cat(chromo)
            muter_statut(chromo)

def algo_gen(m, nb_gen):
    pop=creer_population(m)
    for i in range(nb_gen):
        croiser_population(pop)
        muter_pop(pop)
        pop=selection(pop)
    return(pop[0])

