import numpy as np
import matplotlib.pyplot as plt
from random import *
from math import *
import os
import inspect
from copy import *
import time

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
#f associe à un élément x la liste de ses degrés d'appartenance aux domaines définis par l

def trace_partition(l): #On doit avoir len(l)=2n-2 avec n=nombre de fonctions mu
    trace_repere(100,1)
    trace_mu_simple(0,0,l[0],l[1])
    for i in range((len(l)+2)//2-2):
        trace_mu_simple(l[2*i],l[2*i+1],l[2*i+2],l[2*i+3])
    trace_mu_simple(l[-2],l[-1],100,100)

def L2part(L):
    return [partition(l) for l in L]
#l contient les listes caractérisant les partitions de chaque élément
#L2part contient donc toutes les fonctions partitions

## Histogrammes

def histogramme_par_categorie(L, p, nb):    
    n = len(L)-2
    l=list(L[2:n+2])
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

def histogramme_commun(L,nombre_pics,couleur,lon):
    a=100/(2*nombre_pics)
    X=np.linspace(a,100-a,nombre_pics)
    Y=[ sum([ mu(x-a,x-a,x+a,x+a)(i)/(2*a*lon) for i in L]) for x in X]
    trace_repere(100,max(Y))
    plt.plot(X,Y,couleur)

def trace_histo(LL,k):
    lon=len(LL)
    histogramme_commun([i[2+k] for i in LL],100,'k',lon)
    histogramme_commun([i[2+k] for i in LL if i[1]==0],100,'g',lon)
    histogramme_commun([i[2+k] for i in LL if i[1]==2],100,'r',lon)
    histogramme_commun([i[2+k] for i in LL if i[1]==1],100,'b',lon)

# trace_partition(L[1])
# histo_element_normalise(l,1,100)

## Création vecteur et chromosome
#un vecteur contient des pourcentages, pas des chiffres bruts    
def vecteur_aleatoire(n):
    L=[random() for i in range(n)]
    total=sum(L)
    return [i*100/total for i in L]
    
def classe_dominante(x,parti): # x est un pourcentage d'élément chimique, parti la partition associée à l'élément,la fonction renvoie le terme auquel x appartient le plus
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

def creer_chromosome(liste_of_exemples,n): #n n'est pas le nombre d'éléments chimiques
    return suppr_doublons([creer_gene(x,n) for x in liste_of_exemples ])


## Fonctions d'évolution de la population

def muter_ajout(chromo,L_classe,p_ajout,n,taille_while): # Peut ajouter un gène
    p=random()
    if p<=p_ajout:
        ajout=creer_gene(choice(choice(L_classe)),n)
        i=0
        while ajout in chromo and i<taille_while:
            ajout=creer_gene(choice(choice(L_classe)),n)
            i+=1
        if i<taille_while:
            chromo+=[ajout]

def muter_suppr(chromo,p_suppr): # Peut supprimer un gène
    p=random()
    if p<=p_suppr:
        k=randint(0,len(chromo)-1)
        chromo.remove(chromo[k])


def muter_cat(chromo,p_cat,nb,taille_while): # Peut modifier une variable linguistique d'un gène (passage de 'peu de' à 'beaucoup de')
    p=random()
    if p<=p_cat:
        l=deepcopy(chromo)
        i_boucle=0
        fin=True
        while fin and i_boucle<taille_while:
            i = randint(0,len(chromo)-1)
            prémisse=choice(l[i][:-1])
            if prémisse[1]==0:
                prémisse[1]=1
            else:
                if prémisse[1]==(nb-1):
                    prémisse[1]-=1
                else:
                    prémisse[1]+=2*randint(0,1)-1
            if (not l[i] in chromo[:i]+chromo[(i+1):] ):
                fin=False
            else:
                l=deepcopy(chromo)
                i_boucle+=1
        if i<taille_while:
            chromo[i]=l[i]


def muter_statut(chromo,p_statut,n,taille_while): #Peut activer ou désactiver une prémisse
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

""" ## X et +, ne marche pas !!!
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
"""

def test(chromo,exemple,n):
    ccl=[]
    for regle in chromo:
        certitude=1
        for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
            if regle[i][0]:
                certitude= min(certitude,((partitions[i])(exemple[i+2]) [regle[i][1]]))   #partitions variable globale, liste de fonctions
        if certitude!=0:
            ccl.append([certitude, regle[-1]])
    return(ccl)

def score(ccl,exemple):
    ll=[ i[0] for i in ccl if i[1]==exemple[1]]
    if ll:
        return(max([ i[0] for i in ccl if i[1]==exemple[1]]))
    return 0

def fitness(chromo, L_test,n):
    note=0
    longueur=len(L_test)
    for ex in L_test:
        note+=score(test(chromo,ex,n),ex)
    return(note/longueur)

##

def test1(chromo,exemple,n):
    ccl=[]
    for regle in chromo:
        certitude=1
        for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
            if regle[i][0]:
                certitude= min(certitude,((partitions[i])(exemple[i+2]) [regle[i][1]]))   #partitions variable globale, liste de fonctions
        if not certitude ==0:
            ccl.append([certitude, regle[-1]])
    return(ccl)

def score1(ccl,exemple,nc):
    R=[[0,i] for i in range(nc)]
    for i in ccl:
        R[i[1]][0]=max(R[i[1]][0],i[0])
    s=0
    for i in R:
        if i[1]==exemple[1]:
            s+=i[0]
        else:
            s-=i[0]/(nc-1)
    return s

def ccl_tri(chromo,exemple,n,nc):
    ccl=[]
    for regle in chromo:
        certitude=1
        for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
            if regle[i][0]:
                certitude= min(certitude,((partitions[i])(exemple[i+2]) [regle[i][1]]))   #partitions variable globale, liste de fonctions
        if not certitude ==0:
            ccl.append([certitude, regle[-1]])
    R=[0 for i in range(nc)]
    for i in ccl:
        R[i[1]]=max(R[i[1]],i[0])
    return R

def fitness1(chromo, L_ex,n):
    note=0
    longueur=len(L_ex)
    for ex in L_ex:
        note+=score1(test(chromo,ex,n),ex,nc)
    return(note/longueur)

def score2(ccl,exemple,nc):
    R=[[0,i] for i in range(nc)]
    for i in ccl:
        R[i[1]][0]=max(R[i[1]][0],i[0])
    erreur=0
    for i in R:
        if i[1]==exemple[1]:
            erreur+=1-i[0]
        else:
            erreur+=i[0]
    return 1-erreur/nc

def fitness2(chromo, L_ex,n): # Calcule l'écart à la réalité : à utiliser pour le moment
    note=0
    longueur=len(L_ex)
    for ex in L_ex:
        note+=score2(test(chromo,ex,n),ex,nc)
    return(note/longueur)

def moy(l,N):
    return sum(l)/N

def liste_fit(pop,fit,L_ex,n):
    return [fit(pop[i],L_ex,n) for i in range(len(pop))]

##


def fitness_pop(pop,L_ex,n,fit): # Calcul de la fitness max
    return max([fit(i,L_ex,n) for i in pop])
    
def fitness_pop_min(pop,L_ex,n,fit): # """ min
    return min([fit(i,L_test,n) for i in pop])  
    
def fitness_pop_moy(pop,L_ex,n,fit,N): # """ moyenne
    return sum([fit(i,L_ex,n) for i in pop])/N

## Algo génétique

def creer_population(N,n,L_ex,taille_chromo):
    pop=[]
    L=deepcopy(L_ex)
    for i in range(N):
        shuffle(L)
        pop+=[creer_chromosome(L[:taille_chromo],n)]
    return pop

def selection(pop_ini,L_ex,n,fit): 
    m=len(pop_ini)
    l_couple=[(fit(pop_ini[i],L_ex,n),i) for i in range(m)]
    l_couple.sort()                                                #attention, classe du plus petit au plus grand
    return([pop_ini[l_couple[i][1]] for i in range(m//2,m)])

def selection1(pop_ini,L_ex,n,fit): # Sélection proportionnelle à la fitness des individus
    m=len(pop_ini)
    l_fit=[(fit(pop_ini[i],L_ex,n),i) for i in range(m)]
    l_fit.sort()                                                #attention, classe du plus petit au plus grand
    return([pop_ini[l_fit[i][1]] for i in range(m//2,m)],[ i[0] for i in l_fit[(m//2+1):]])

'''
def tirer_chromo(l):                                # l=[(x,s)] où x sont des individus et s leur score
    score_total=sum(l[i][1] for i in range (len(l)))
    l0=[l[0][1]/score_total]
    for i in range(len(l)-1):
        l0.append(l[i+1][1]/score_total+l0[i])
    r=random()
    i=0
    while l0[i]<r:
        i+=1
    return(l[i][0])

def croiser_population(pop): 
    l=[(pop[i],fct(pop[i])) for i in range(len(pop))]
    for i in range(len(pop)):
        pop.append(croiser_chromo(tirer_chromo(l),tirer_chromo(l)))
'''


def croiser_population(pop):
    shuffle(pop)
    longueur=len(pop)
    pop+=[croiser_chromo(pop[0],pop[-1])]
    for i in range(longueur-1):
        pop+=[croiser_chromo(pop[i],pop[i+1])]

def croiser_population1(pop,l_fit): #Croisement proportionnel à la fitness
    proportion=[]
    k=0
    s=sum(l_fit)
    for i in l_fit:
        proportion+=[k for j in range(ceil(100*i/s))]
        k+=1
    for i in range(len(pop)):
        i,j=choice(proportion),choice(proportion)
        pop+=[croiser_chromo(pop[i],pop[j])]

def muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while):
    for chromo in pop:
        muter_ajout(chromo,L_classe,p_ajout,n,taille_while)       #L_classe est une variable globale
        muter_suppr(chromo,p_suppr)
        for i in range(len(chromo)):
            muter_cat(chromo,p_cat,nb,taille_while)
            muter_statut(chromo,p_statut,n,taille_while)

def epure(chromo,fit,L_ex,n): # à utiliser à la fin du programme pour enelever les règles inutiles d'un individu
    R=[]
    i=0
    while i<len(chromo):
        if fit(chromo[:i]+chromo[(i+1):],L_ex,n)<fit(chromo,L_ex,n):
            R.append(chromo[i])
            i+=1
        else:
            chromo=chromo[:i]+chromo[(i+1):]
    return R

''' # Sans élitisme

def algo_gen(N, nb_gen,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,L_ex,L_test,taille_chromo,taille_while):
    pop=creer_population(N,n,L_ex,taille_chromo)
    for i in range(nb_gen):
        croiser_population(pop)
        muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
        pop=selection(pop,L_test,n)
    return(pop)

def trace_fitness(N, nb_gen,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,L_ex,L_test,taille_chromo,taille_while):
    pop=creer_population(N,n,L_ex,taille_chromo)
    X=[0]
    Y_max=[fitness_pop(pop,L_test,n)]
    Y_moy=[fitness_pop_moy(pop,L_test,n,N)]
    Y_min=[fitness_pop_min(pop,L_test,n)]
    for i in range(nb_gen):
        croiser_population(pop)
        muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
        pop=selection(pop,L_test,n)
        X.append(X[-1]+1)
        Y_max.append(fitness_pop(pop,L_test,n))
        Y_moy.append(fitness_pop_moy(pop,L_test,n,N))
        Y_min.append(fitness_pop_min(pop,L_test,n))
    trace_repere(nb_gen,1)
    plt.plot(X,Y_max,'g',label="max")
    plt.plot(X,Y_moy,'b',label="moy")
    plt.plot(X,Y_min,'r',label="min")
    plt.xlabel('Nombre de génération')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()

'''

def lanceur(N, nb_gen,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,L_ex,taille_chromo,taille_while,elitisme,fit,l_indi):
    debut=time.time()
    pop=creer_population(N-len(l_indi),n,L_ex,taille_chromo)+l_indi
    X=[0]
    l_fit=liste_fit(pop,fit,L_ex,n)
    Y_max=[max(l_fit)]
    Y_moy=[moy(l_fit,N)]
    Y_min=[min(l_fit)]
    print(0)
    if elitisme:
        indice=l_fit.index(max(l_fit))
        indi=deepcopy(pop[indice])
        croiser_population(pop)
        muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
        pop,l_fit=selection1(pop+[indi],L_ex,n,fit)
        pop=pop[1:]
        X.append(X[-1]+1)
        Y_max.append(max(l_fit))
        Y_moy.append(moy(l_fit,N))
        Y_min.append(min(l_fit))
        print(1)
        for i in range(nb_gen-1):
            indi=deepcopy(pop[-1])
            croiser_population1(pop,l_fit)
            muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
            pop,l_fit=selection1(pop+[indi],L_ex,n,fit)
            pop=pop[1:]
            X.append(X[-1]+1)
            Y_max.append(max(l_fit))
            Y_moy.append(moy(l_fit,N))
            Y_min.append(min(l_fit))
            print(2+i)
    else:
        croiser_population(pop)
        muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
        pop,l_fit=selection(pop,L_ex,n,fit)
        X.append(X[-1]+1)
        Y_max.append(max(l_fit))
        Y_moy.append(moy(l_fit,N))
        Y_min.append(min(l_fit))
        print(1)
        for i in range(nb_gen-1):
            croiser_population1(pop,l_fit)
            muter_pop(pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,taille_while)
            pop,l_fit=selection1(pop,L_ex,n,fit)
            X.append(X[-1]+1)
            Y_max.append(max(l_fit))
            Y_moy.append(moy(l_fit,N))
            Y_min.append(min(l_fit))
            print(2+i)
    fin=time.time()
    trace_repere(nb_gen,1)
    plt.plot(X,Y_max,'g',label="max")
    plt.plot(X,Y_moy,'b',label="moy")
    plt.plot(X,Y_min,'r',label="min")
    plt.xlabel('Nombre de génération')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()
    print(fin-debut,Y_max[-1],Y_moy[-1],Y_min[-1])
    return pop

def taux_bc(chromo,L_test,n,nc): # Calcule le taux de bonne classification
    t=0
    t1=0
    for ex in L_test:
        l=ccl_tri(chromo,ex,n,nc)
        k=ex[1]
        a,b=l[k],max( l[:k]+l[(k+1):] )
        if a>b:
            t+=1
            t1+=1
        elif a==b:
            t+=0.5
    length=len(L_test)
    return t/length*100,t1/length*100
