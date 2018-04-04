import os
import inspect

"""
lanceur(N,n,nb,nc,nb_gen,p_suppr,p_cat,p_statut,p_ajout,taille_indi,taille_while,liste_ex,len_ex,partitions,elitisme,fit,f_croisement,f_mutation,f_selection,l_indi)

Forme de la liste :
    N               int     Nombre d'individus (fixe)
    n               int     Nombre d'éléments chimiques        
    nb              int     Nombre 
    nc              int     Nombre de classes
    nb_gen          int     Nombre de générations
    p_suppr         float   Probabilité de supprimer une règle
    p_cat           float   Probabilité de muter la catégorie
    p_statut        float   Probabilité de muter l'activation (statut)
    p_ajout         float   Probabilité d'ajouter une nouvelle règle
    taille_indi     int     Nombre de règles des id à l'initialisation
    taille_while    int     Compteur sécurité des boucles while
    partitions      str/f   Type de partition
    elitisme        bool    Activation de l'élistisme
    fit             str/funcType de fitness utilisé
    f_croisement    str/f   Type de croisement
    f_mutation      str/f   Type de mutation
    f_selection     str/f   Type de sélection
    l_indi          bool    Si on initialise la liste d'individus 
    
    tps_calc
    fit_max
    fit_moy
    fit_min
    tbc_ns
    tbc_s

"""  
    
def overwrite_file(file_name, list):
    file=open(file_name, "w")
    file.write("N,n,nb,nc,nb_gen,p_suppr,p_cat,p_statut,p_ajout,taille_indi,taille_while,partitions,elitisme,fit,f_croisement,f_mutation,f_selection,l_indi,    tps_calc,fit_max,fit_moy,fit_min,tbc_ns,tbc_s"+"\n")
    for i in range(len(list)):
        for j in range(len(list[0])):
            file.write(str(list[i][j])+",")
        file.write("\n")
    file.close()
    
def write_file(file_name, list):
    file=open(file_name,"a")
    for i in range(len(list)):
        for j in range(len(list[0])):
            file.write(str(list[i][j])+",")
        file.write("\n")
    file.close()
  

