import os
import inspect

"""
Forme de la liste :
    n               int     Nombre d'éléments chimiques        
    nb              int     Nombre 
    nc              int     Nombre de classes
    N               int     Nombre d'individus (fixe)
    nb_gen          int     Nombre de générations
    taille_chromo   int     Taille du chromosome
    taille_while    int     Compteur sécurité des boucles while
    elitisme        bool    Activation de l'élistisme

"""  
    
def write_file(file_name, list):
    file=open(file_name, "w")
    file.write("n,nb,nc,N,nb_gen,taille_chromo,taille_while,elitisme"+"\n")
    for i in range(len(list)):
        for j in range(len(list[0])):
            file.write(str(list[i][j])+",")
        file.write("\n")
    file.close()
    
#write_file("resultats/testfile.txt", [[1,2,3,4],[2,3,4,5]])
  

