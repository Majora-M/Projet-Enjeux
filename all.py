import numpy as np
import matplotlib.pyplot as plt
from random import *
from math import *
import os
from copy import *
import time
import lire_donnees as lire
import ecrire_donnees as ecrire

## Fonctions d'appartenance et partitions

def mu(a,b,c,d): # Fonction d'appartance trapèze repérée par les points a,b,c,d
    def f(x):
        if x<a or x>d:
            return 0
        if x<b:
            return (x-a)/(b-a)
        if x>c:
            return (d-x)/(d-c)
        return 1
    return f

def partition(l): #Renvoie la fonction de partition repéré par les points d'abcisses contenus dans l
    def f(x):
        return [mu(0,0,l[0],l[1])(x)]+[mu(l[2*i],l[2*i+1],l[2*i+2],l[2*i+3])(x) for i in range((len(l)+2)//2-2)] + [mu(l[-2],l[-1],100,100)(x)]
    return f

def L2part(l): # Transforme un ensemble de listes de la forme précedente en un ensemble de partitions 
    return [partition(i) for i in l]

## Fonctions de tracé

def trace_repere(xmax,ymax):
    plt.plot([0,0],[-ymax/20,ymax*1.1],'k')
    plt.plot([-xmax/20,xmax],[0,0],'k')
    plt.plot([0,xmax],[ymax,ymax],'--k')

def trace_mu(a,b,c,d):
    trace_repere(100,1)
    plt.plot([0,a,b,c,d,100],[0,0,1,1,0,0])

def trace_mu_simple(a,b,c,d): #Sans répéter le tracé des abcisses/ordonnées 
    plt.plot([0,a,b,c,d,100],[0,0,1,1,0,0])

def trace_partition(l): #On doit avoir len(l)=2n-2 avec n=nombre de fonctions mu
    trace_repere(100,1)
    trace_mu_simple(0,0,l[0],l[1])
    for i in range((len(l)+2)//2-2):
        trace_mu_simple(l[2*i],l[2*i+1],l[2*i+2],l[2*i+3])
    trace_mu_simple(l[-2],l[-1],100,100)
    
## Création vecteur et individu
    
def vecteur_aleatoire(n): # Crée un vecteur aléatoire de taille n normalisé
    L=[random() for i in range(n)]
    total=sum(L)
    return [i*100/total for i in L]
    
def classe_dominante(x,parti): # Pour x, pourcentage pour un élément chimique et sa partition parti, renvoie la classe dominante de x
    l=parti(x)
    maxi,k=0,0
    for i in range(len(l)):
        if l[i]>maxi:
            maxi=l[i]
            k=i
    return k

def suppr_doublons(l): # Supprime les doublons de l
    res=[]
    for i in l:
        if not i in res:
            res+=[i]
    return res

def creer_regle(exemple,n,partitions): # Crée une règle adaptée pour l'exemple
    return [  [1,classe_dominante(exemple[k+2],partitions[k])] for k in range(n)]+[exemple[1]]

def creer_indi(liste_of_exemples,n,partitions): # Crée un individu adapté pour la liste d'exemple
    return suppr_doublons([creer_regle(x,n,partitions) for x in liste_of_exemples ])


## Opérateurs mutation et croisement de règles


def muter_ajout(indi,liste_ex,p_ajout,n,taille_while,partitions): # Peut ajouter une règle
    p=random()
    if p<=p_ajout:
        ajout=creer_regle(choice(liste_ex),n,partitions)
        i=0
        while ajout in indi and i<taille_while:
            ajout=creer_regle(choice(liste_ex),n,partitions)
            i+=1
        if i<taille_while:
            indi+=[ajout]
            return True
    return False


def muter_suppr(indi,p_suppr): # Peut supprimer une règle
    p=random()
    if p<=p_suppr:
        k=randint(0,len(indi)-1)
        indi.remove(indi[k])
        return True
    return False


def muter_cat(indi,p_cat,nb,taille_while): # Peut changer la catégorie d'une prémisse (passer de 'peu de' à 'beaucoup de')
    p=random()
    if p<=p_cat:
        l=deepcopy(indi)
        i_boucle=0
        fini=False 
        while not fini and i_boucle<taille_while:
            i = randint(0,len(indi)-1)
            P=choice(l[i][:-1])
            if P[1]==0:
                P[1]=1
            else:
                if P[1]==(nb-1):
                    P[1]-=1
                else:
                    P[1]+=2*randint(0,1)-1
            if (not l[i] in indi[:i]+indi[(i+1):] ):
                fini=True
            else:
                l=deepcopy(indi)
                i_boucle+=1
        if i<taille_while:
            indi[i]=l[i]
            return True
    return False


def muter_statut(indi,p_statut,n,taille_while): # Peut activer ou désactiver une prémisse
    p=random()
    if p<=p_statut:  #muter l'individu
        i_boucle=0
        nouveau = False
        t=len(indi)
        while i_boucle<taille_while and not nouveau:
            k=randint(0,t-1)
            regle=deepcopy(indi[k])   #on choisit une regle a muter
            j=randint(0,n-1)
            regle[j][0]=1-regle[j][0]
            if not regle in indi:
                nouveau=True
            i_boucle+=1
        if nouveau:
            indi[k]=regle
            return True
    return False


def croiser_indi(indi1,indi2): # Croisement entre deux individus
    c1=deepcopy(indi1)
    c2=deepcopy(indi2)
    indi_fils=[]
    for regle in c1:
        if regle in c2:
            indi_fils.append(regle)
            c1.remove(regle)
            c2.remove(regle)
    n1=len(c1)
    n2=len(c2)
    shuffle(c1)
    shuffle(c2)
    indi_fils+=c1[:n1//2]+c2[n2//2:]
    return(indi_fils)


## Fonction Fitness

def fitness(indi, liste_ex,n,len_ex,nc,partitions): # Fitness avec le min et le max. Marche toujours. Calcul de l'écart à la réalité
    note=0
    def test(indi,ex,n,partitions):
        ccl=[]
        for regle in indi:
            certitude=1
            for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
                if regle[i][0]:
                    certitude= min(certitude,((partitions[i])(ex[i+2]) [regle[i][1]]))   #partitions variable globale, liste de fonctions
            if not certitude == 0:
                ccl.append([certitude, regle[-1]])
        return(ccl)
    def score(ccl,exemple,nc):
        R=[[0,i] for i in range(nc)]
        for i in ccl:
            R[i[1]][0]=max(R[i[1]][0],i[0])
        s=0
        for i in R:
            if i[1]==exemple[1]:
                s+=1-i[0]
            else:
                s+=i[0]
        return 1-s/nc
    for ex in liste_ex:
        note+=score(test(indi,ex,n,partitions),ex,nc)
    return(note/len_ex)

def fitness1(indi, liste_ex,n,len_ex,nc,partitions): #Marche pas toujours : + et x. Les prémisses doivent toujours être activées pour marcher
    note=0
    def test(indi,ex,n,partitions):
        ccl=[]
        for regle in indi:
            certitude=1
            for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
                if regle[i][0]:
                    certitude= certitude*(partitions[i](ex[i+2])[regle[i][1]])   #partitions variable globale, liste de fonctions
            if not certitude == 0:
                ccl.append([certitude, regle[-1]])
        return(ccl)
    def score(ccl,exemple,nc):
        R=[[0,i] for i in range(nc)]
        for i in ccl:
            R[i[1]][0]=R[i[1]][0]+i[0]
        s=0
        for i in R:
            if i[1]==exemple[1]:
                s+=1-i[0]
            else:
                s+=i[0]
        return 1-s/nc
    for ex in liste_ex:
        note+=score(test(indi,ex,n,partitions),ex,nc)
    return(note/len_ex)

def liste_fit(pop,fit,liste_ex,n,len_ex,nc,partitions): # Calcul de la liste de l'ensemble des individus de la population
    return [fit(pop[i],liste_ex,n,len_ex,nc,partitions) for i in range(len(pop))]



## Algo génétique

def creer_population(N,n,liste_ex,taille_indi,partitions): # Crée une pop de taille N selon la liste d'exemples
    pop=[]
    for i in range(N):
        L=deepcopy(liste_ex)
        shuffle(L)
        pop+=[creer_indi(L[:taille_indi],n,partitions)]
    return pop


def selection(Pop,N): # Sélection des N meilleurs individus
    aux=deepcopy(sorted(Pop, key=lambda tup: tup[1]))
    Pop=aux[(len(Pop)-N):]
    return Pop


def croiser_population(Pop,N): # Croisement de la pop de taille N
    shuffle(Pop)
    pop_ajout=[croiser_indi(Pop[0][0],Pop[-1][0])]
    for i in range(N-1):
        pop_ajout+=[croiser_indi(Pop[i][0],Pop[i+1][0])]
    Pop+=[[i,-1] for i in pop_ajout]

def croiser_population1(Pop,N): # Idem mais en fonction de la fitness
    proportion=[]
    k=0
    s=sum([i[1] for i in Pop])
    for i in Pop:
        proportion+=[k]*(ceil(100*i[1]/s))
        k+=1
    for i in range(N):
        j,k=choice(proportion),choice(proportion)
        indi=croiser_indi(Pop[j][0],Pop[k][0])
        Pop+=[[indi,-1]]

def muter_pop(Pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,nc,liste_ex,taille_while,N,len_ex,partitions,fit): # Mutation de toute la population
    for i in range(2*N):
        indi=deepcopy(Pop[i][0])
        same = not muter_ajout(indi,liste_ex,p_ajout,n,taille_while,partitions)       #L_classe est une variable globale
        same = same and not muter_suppr(indi,p_suppr)
        for j in range(len(indi)):
            same = same and not muter_cat(indi,p_cat,nb,taille_while)
            same = same and not muter_statut(indi,p_statut,n,taille_while)
        if (not same) or (Pop[i][1]==-1):
            Pop[i]=[indi,fit(indi, liste_ex,n,len_ex,nc,partitions)] # Si on ne connaît pas la fitness de indi, on la calcule

def muter_pop1(Pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,nc,liste_ex,taille_while,N,len_ex,partitions,fit): # Idem mais pas de mutation de statut
    for i in range(2*N):
        indi=deepcopy(Pop[i][0])
        same = not muter_ajout(indi,liste_ex,p_ajout,n,taille_while,partitions)       #L_classe est une variable globale
        same = same and not muter_suppr(indi,p_suppr)
        for j in range(len(indi)):
            same = same and not muter_cat(indi,p_cat,nb,taille_while)
        if (not same) or (Pop[i][1]==-1):
            Pop[i]=[indi,fit(indi, liste_ex,n,len_ex,nc,partitions)]

## ccl_tri

def ccl_tri(indi,exemple,n,nc,partitions): # Tri les conclusions apportées par les règles selon min et max
    ccl=[]
    for regle in indi:
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
    
def ccl_tri1(indi,exemple,n,nc,partitions): # Tri les conclusions apportées par les règles selon x et +
    ccl=[]
    for regle in indi:
        certitude=1
        for i in range(n):                                       #n variable globale, nbre d'éléments chimiques
            if regle[i][0]:
                certitude= certitude*(partitions[i](exemple[i+2]) [regle[i][1]])   #partitions variable globale, liste de fonctions
        if not certitude ==0:
            ccl.append([certitude, regle[-1]])
    R=[0 for i in range(nc)]
    for i in ccl:
        R[i[1]]=R[i[1]]+i[0]
    return R   

def taux_bc(indi,liste_test,n,nc,partitions,f_ccl_tri): # Calcul du taux de bonne classification
    t=0
    t1=0
    for ex in liste_test:
        l=f_ccl_tri(indi,ex,n,nc,partitions)
        k=ex[1]
        a,b=l[k],max( l[:k]+l[(k+1):] )
        if a>b:
            t+=1
            t1+=1
        elif a==b:
            t+=0.5
    length = len(liste_test)
    tbc_ns = t/length*100
    tbc_s  = t1/length*100
    print('Taux de bonne classification :',tbc_ns,'%','(non stricte) ;',tbc_s,'%','(stricte)')
    print('')
    return tbc_ns,tbc_s

## Lanceur

def lanceur(N,n,nb,nc,nb_gen,p_suppr,p_cat,p_statut,p_ajout,taille_indi,taille_while,liste_ex,len_ex,partitions,cat_partitions,elitisme,fit,f_croisement,f_mutation,f_selection,l_indi,f_ccl_tri):
    debut=time.time()
    pop=creer_population(N-len(l_indi),n,liste_ex,taille_indi,partitions)+l_indi
    l_fit=liste_fit(pop,fit,liste_ex,n,len_ex,nc,partitions)
    Pop=[ [pop[i],l_fit[i]] for i in range(N)]
    Pop=sorted(Pop, key=lambda tup: tup[1])
    X=[0]
    Y_max=[Pop[-1][1]]
    Y_moy=[sum([i[1] for i in Pop])/N]
    Y_min=[Pop[0][1]]
    print('Initialisation')
    for i in range(1,nb_gen+1):
        debut_gen=time.time()
        if elitisme:
            indi_f_elite=Pop[-1]
        f_croisement(Pop,N)
        f_mutation(Pop,p_suppr,p_cat,p_statut,p_ajout,n,nb,nc,liste_ex,taille_while,N,len_ex,partitions,fit)
        if elitisme:
            Pop+=[indi_f_elite]
        Pop=f_selection(Pop,N)
        X.append(i)
        Y_max.append(Pop[-1][1])
        Y_moy.append(sum([i[1] for i in Pop])/N)
        Y_min.append(Pop[0][1])
        fin_gen=time.time()
        print('Génération',i,'/',nb_gen,'--- Temps restant approximatif :',int((fin_gen-debut_gen)*(nb_gen-i)),'s')
    fin=time.time()
    trace_repere(nb_gen,1)
    plt.plot(X,Y_max,'g',label="max")
    plt.plot(X,Y_moy,'b',label="moy")
    plt.plot(X,Y_min,'r',label="min")
    plt.xlabel('Nombre de génération')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()
    
    str_fit             = fit.__name__
    str_f_croisement    = f_croisement.__name__
    str_f_mutation      = f_mutation.__name__
    str_f_selection     = f_selection.__name__
    
    
    tps_calc    = fin-debut
    fit_max     = Y_max[-1]
    fit_moy     = Y_moy[-1]
    fit_min     = Y_min[-1]
    print('')
    print('Durée du calcul :',int(tps_calc),'secondes')
    print('')
    print('Calcul des fitness :')
    print('Fit max :',fit_max)
    print('Fit moyenne :',fit_moy)
    print('Fit min :',fit_min)
    print('')
    
    tbc_ns,tbc_s = taux_bc(Pop[-1][0],liste_test,n,nc,partitions,f_ccl_tri)
    # retourner le liste des parametres utilises et resultats de calcul
    # N,n,nb,nc,nb_gen,p_suppr,p_cat,p_statut,p_ajout,taille_indi,taille_while,partitions,elitisme,fit,f_croisement,f_mutation,f_selection,l_indi,    tps_calc,fit_max,fit_moy,fit_min,tbc_ns,tbc_s
    l_resultats=[N,n,nb,nc,nb_gen,p_suppr,p_cat,p_statut,p_ajout,taille_indi,taille_while,cat_partitions,elitisme,str_fit,str_f_croisement,str_f_mutation,str_f_selection,len(l_indi),tps_calc,fit_max,fit_moy,fit_min,tbc_ns,tbc_s]
    return Pop,l_resultats

## Finalisation 

def epure(indi,fit,liste_ex,n,len_ex,nc,partitions): # À faire à la fin du programme, pour enlever les règles inutiles d'un indi
    R=[]
    i=0
    while i<len(indi):
        if fit(indi[:i]+indi[(i+1):],liste_ex,n,len_ex,nc,partitions)<fit(indi,liste_ex,n,len_ex,nc,partitions):
            R.append(indi[i])
            i+=1
        else:
            indi=indi[:i]+indi[(i+1):]
    return R

l_resultats_tot=[]










## Paramètres

N=2
n=6 ##
nb=5 ##
nc=3 ##
nb_gen=10
    
p_ajout=0.2
p_suppr=0.2
p_cat=0.2
p_statut=0.2
    
taille_indi=5
taille_while=5

alpha = 0.5 # taille de la liste d'exemple d'entraînement sur la taille de la liste d'exemple totale

L_ex_danger  = lire.get_sets(10) # C,Cr,N,Na,0,S     ##
L_ex_benigns = lire.get_sets2(10) # C,Cr,N,Na,0,S   ##
L_ex_bsimple = lire.get_sets3(10) # C,O,N           ##

LL=L_ex_benigns
length=len(LL) ##

liste_ex=LL[(int(alpha*length)):]    ##
len_ex=len(liste_ex)                 ##
liste_test=LL[:(int(alpha*length))]  ##
    
L_partitions=[[7,10,35,40,60,67,80,90],[4,11,26,30,40,50,60,70],[1.5,2.5,6,7.6,13.5,15.7,19.4,22],[3,10,30,40,50,60,70,80],[2,11.5,22.5,26,53,60,75,80],[4,7,30,40,50,60,70,80]] ##
partitions      = L2part(L_partitions)  ##
cat_partitions = 'trapeze_1'

elitisme        = True
fit             = fitness
f_croisement    = croiser_population1
f_mutation      = muter_pop
f_selection     = selection
    
l_indi=[]

f_ccl_tri=ccl_tri

Pop,l_resultats=lanceur(N,n,nb,nc,nb_gen,p_suppr,p_cat,p_statut,p_ajout,taille_indi,taille_while,liste_ex,len_ex,partitions,cat_partitions,elitisme,fit,f_croisement,f_mutation,f_selection,l_indi,f_ccl_tri) ##

l_resultats_tot.append(l_resultats)

ecrire.overwrite_file("resultats/testfile.txt", l_resultats_tot)
#ecrire.write_file("resultats/testfile.txt", l_resultats_tot)
    
print("############") ##
print("exiting main") ##
