import numpy as np
import matplotlib.pyplot as plt
from random import *
from math import *
import os
import inspect
from copy import *

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
    plt.plot(X,Y,'k')

def histogramme_normalise(L,nombre_pics):
    a=100/(2*nombre_pics)
    length=len(L)
    X=np.linspace(a,100-a,nombre_pics)
    Y=[ sum([ mu(x-a,x-a,x+a,x+a)(i)/(2*a*length) for i in L]) for x in X]
    trace_repere(100,1)
    maxi=max(Y)
    plt.plot(X,[y/maxi for y in Y],'--k')

# exemple : histogramme([random()*100 for i in range(5000)],200)
    
def histo_element(l,k,nombre_pics):
    histogramme([x[k+2] for x in l],nombre_pics)

def histo_element_normalise(l,k,nombre_pics):
    histogramme_normalise([x[k+2] for x in l],nombre_pics)

# trace_partition(L[1])
# histo_element_normalise(l,1,100)

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


def creer_gene(exemple,n): # Crée un gène adapté pour l'exemple
    return [  [1,classe_dominante(exemple[k+2],partitions[k])] for k in range(n)]+[exemple[1]]

# exemple : creer_gene([10,95,80,79],1)

def suppr_doublons(l):
    res=[]
    for i in l:
        if not i in res:
            res+=[i]
    return res

def creer_chromosome(liste_of_exemples,n):
    return suppr_doublons([creer_gene(x,n) for x in liste_of_exemples ])


## Fonctions d'évolution de la population

def muter_ajout(chromo,L_classe,p_ajout,n,taille_while):
    p=random()
    if p<=p_ajout:
        ajout=creer_gene(choice(choice(L_classe)),n)
        i=0
        while ajout in chromo and i<taille_while:
            ajout=creer_gene(choice(choice(L_classe)),n)
            i+=1
        if i<taille_while:
            chromo+=[ajout]

def muter_suppr(chromo,p_suppr): 
    p=random()
    if p<=p_suppr:
        k=randint(0,len(chromo)-1)
        chromo.remove(chromo[k])


def muter_cat(chromo,p_cat,nb,taille_while):
    p=random()
    if p<=p_cat:
        l=deepcopy(chromo)
        i_boucle=0
        fin=True
        while fin and i_boucle<taille_while:
            i = randint(0,len(chromo)-1)
            P=choice(l[i][:-1])
            if P[1]==0:
                P[1]=1
            else:
                if P[1]==(nb-1):
                    P[1]-=1
                else:
                    P[1]+=2*randint(0,1)-1
            if (not l[i] in chromo[:i]+chromo[(i+1):] ):
                fin=False
            else:
                l=deepcopy(chromo)
                i_boucle+=1
        chromo[i]=l[i]


def muter_statut(chromo,p_statut,n,taille_while):
    p=random()
    if p<=p_statut:  #muter le chromosome
        i_boucle=0
        nouveau = False
        t=len(chromo)
        while i_boucle<taille_while and not nouveau:
            k=randint(0,t-1)
            gen=deepcopy(chromo[k])   #on choisit un gène a muter
            j=randint(0,n-1)
            gen[j][0]=1-gen[j][0]
            if not gen in chromo:
                nouveau=True
            i_boucle+=1
        if nouveau:
            chromo[k]=gen


def croiser_chromo(chromo1,chromo2):
    c1=deepcopy(chromo1)
    c2=deepcopy(chromo2)
    chromo_fils=[]
    for regle in c1:
        if regle in c2:
            chromo_fils.append(regle)
            c1.remove(regle)
            c2.remove(regle)
    n1=len(c1)
    n2=len(c2)
    shuffle(c1)
    shuffle(c2)
    chromo_fils+=c1[:n1//2]+c2[n2//2:]
    return(chromo_fils)


## Fonction Fitness

def test(chromo,exemple,n):
    ccl=[]
    for regle in chromo:
        certitude=1
        for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
            if regle[i][0]:
                certitude*= (partitions[i])(exemple[i+2]) [regle[i][1]]   #partitions variable globale, liste de fonctions
        if certitude!=0:
            ccl.append([certitude, regle[-1]])
    return(ccl)


def score(ccl,exemple):
    return(sum([ i[0] for i in ccl if i[1]==exemple[1]]))

def fitness(chromo, L_test,n):
    note=0
    longueur=len(L_test)
    for ex in L_test:
        note+=score(test(chromo,ex,n),ex)
    return(note/longueur)

def fitness_pop(pop,L_test,n):
    return max([fitness(i,L_test,n) for i in pop])

## Algo génétique

def creer_population(N,n,L_ex,taille_chromo):
    pop=[]
    for i in range(N):
        L=deepcopy(L_ex)
        shuffle(L)
        pop+=[creer_chromosome(L[:taille_chromo],n)]
    return pop

def selection(pop_ini,L_test,n): 
    m=len(pop_ini)
    l_couple=[(fitness(pop_ini[i],L_test,n),i) for i in range(m)]
    l_couple.sort()                                                #attention, classe du plus petit au plus grand
    return([pop_ini[l_couple[i][1]] for i in range(m//2,m)])

#def tirer_chromo(l):                                # l=[(x,s)] où x sont des individus et s leur score
#    score_total=sum(l[i][1] for i in range (len(l)))
#    l0=[l[0][1]/score_total]
#    for i in range(len(l)-1):
#        l0.append(l[i+1][1]/score_total+l0[i])
#    r=random()
#    i=0
#    while l0[i]<r:
#        i+=1
#    return(l[i][0])

#def croiser_population(pop): 
#    l=[(pop[i],fct(pop[i])) for i in range(len(pop))]
#    for i in range(len(pop)):
#        pop.append(croiser_chromo(tirer_chromo(l),tirer_chromo(l)))

def croiser_population(pop):
    shuffle(pop)
    longueur=len(pop)
    pop+=[croiser_chromo(pop[0],pop[-1])]
    for i in range(longueur-1):
        pop+=[croiser_chromo(pop[i],pop[i+1])]


def muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while):
    for chromo in pop:
        muter_ajout(chromo,L_classe,p_ajout,n,taille_while)       #L_classe est une variable globale
        muter_suppr(chromo,p_suppr)
        for i in range(len(chromo)):
            muter_cat(chromo,p_cat,nb,taille_while)
            muter_statut(chromo,p_statut,n,taille_while)

def algo_gen(N, nb_gen,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,L_ex,L_test,taille_chromo,taille_while):
    pop=creer_population(N,n,L_ex,taille_chromo)
    for i in range(nb_gen):
        croiser_population(pop)
        muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
        pop=selection(pop,L_test,n)
    return(pop[-1])

def trace_fitness(N, nb_gen,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,L_ex,L_test,taille_chromo,taille_while):
    pop=creer_population(N,n,L_ex,taille_chromo)
    X=[0]
    Y=[fitness_pop(pop,L_test,n)]
    for i in range(nb_gen):
        croiser_population(pop)
        muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
        pop=selection(pop,L_test,n)
        X.append(X[-1]+1)
        Y.append(fitness_pop(pop,L_test,n))
    trace_repere(nb_gen,1)
    plt.plot(X,Y)
    plt.show()


