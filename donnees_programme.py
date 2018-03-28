n=6 #nombre d'éléments chimiques
nb=5 #nombre de termes d'une partition
nc=3 #nombre de classes
N=30 #nombre de chromosomes, taille de la population
nb_gen=50
taille_chromo=25
taille_while=50 #taille limite de certaines boucles while
elitisme=True

L_partitions=[[7,10,35,40,60,67,80,90],[4,11,26,30,40,50,60,70],[1.5,2.5,6,7.6,13.5,15.7,19.4,22],[3,10,30,40,50,60,70,80],[2,11.5,22.5,26,53,60,75,80],[4,7,30,40,50,60,70,80]]
#        partitions=[partition([25,34,43,52,61,70,79,90]),partition([6,8.5,12,14,23,36,40,60]),partition([2,8,25,34,43,52,61,70]),partition([0.5,0.9,1.1,2,10,20,30,40]),partition([0.5,0.9,1.1,2,10,20,30,40]),partition([0.5,0.9,1.1,2,10,20,30,40])]
partitions=L2part(L_partitions)

L_ex_danger=get_sets(10) # C,Cr,N,Na,0,S
L_ex_benigns=get_sets2(10) # C,Cr,N,Na,0,S
L_ex_bsimple=get_sets3(10) # C,O,N

LL=L_ex_benigns

L_classe=tri_classe(L_ex_benigns[380:],3)
L_ex=L_ex_benigns[380:]
L_test=L_ex_benigns[:380]

p_ajout=0.2
p_suppr=0.2
p_cat=0.1
p_statut=0.5
fit=fitness1

# pop=lanceur(N,nb_gen,p_suppr,p_cat,p_statut,p_ajout,n,nb,L_classe,L_ex,taille_chromo,taille_while,elitisme,fit)


### Améliorations :

# 1) Fonctions de partition ? Regarder histogramme et peaufiner. Passage en triangle ?

# 2) Fonction fitness : min/max c'est moyen quand même...

