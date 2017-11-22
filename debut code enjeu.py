import matplotlib.pyplot as plt
from random import *

# x : % d'élément chimique
# p : % de la longueur des sommets des trapèzes (plus p est grand plus les sommets sont larges)
# nb : nb de trapèzes
# L : liste des données brute
# n : nb d'éléments chimique considérés

def trapeze(x, p, nb):
    
    if nb == 1 :
        return [1]
    
    res = [0 for k in range(nb)]
    l1 = p/nb
    l2 = (100-p)/(nb-1)
    k = int(x/(l1+l2))
    
    if x - k*(l1+l2) < l1 :
        res[k] = 1
        return res
    
    else :
        a = x - k*(l1+l2)-l1
        res[k] = 1 - a/l2
        res[k+1] = a/l2
        return res

L=[0,0,70,20,10]

def histogramme(L, p, nb):    
                             
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

def rempli(k,l,C,n,nb):
        if k == 0 :
            C += [[l, randint(1,n)]]
        else:
            for i in range(nb): 
                rempli(k-1,[i]+l,C,n,nb)

def chromrandom(n, nb):
    C = []
    k = n
    rempli(k,[],C,n,nb)
    return C


    
