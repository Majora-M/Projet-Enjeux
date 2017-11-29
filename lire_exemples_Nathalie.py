import os
import inspect

"""
## Notes

# Avant d'exécuter : vérifier que "lire_exemples_Nathalie.py" et le dossier
# "donnees" sont enregistres au meme endroit (ils doivent être à la même hauteur
# dans l'arborescence des fichiers

# Executer : dans pyzo, utiliser ctrl+shift+E ( sinon, dans le menu Run ->
# Run file as script )
# Le but est que le shell se place dans le dossier ou se trouvent
# "lire_exemples_Nathalie.py" et le dossier "donnees", pour pouvoir les lire
# correctement
"""

def extract_percentage(string):     
    """ argument : ligne du fichier .txt concernant un élément dans un exemple
        retourne : le pourcentage de cet élément dans l'exemple
    """
    ext=""
    for i in range(len(string)):
        if string[i]=="(":
            j=i+1
            while string[j]!=",":
                ext=ext+string[j]
                j+=1
    return float(ext)
    
def read_file(file_name, nc):
    """ argument : nom du fichier, nombre de classes 
        retourne : liste des exemples de ce fichier, triés par classe
            format  l_ex=[ [liste des exemples de classe 1], [liste des exemples de classe 2], ... ]
            ! cette liste est partielle, et ne comprend les exemples que d'un fichier .txt, voir get_L_ex
    """
    file=open(file_name, "r")
    i=0
    l_ex=[[] for i in range(nc)]
    ex_cour=[]
    for line in file:
        #générer un exemple, de format [ id(int), label(str), classe(int) ]
        if str(line)[0]=="\n":
            ex_cour.extend([C_pr, Cr_pr, N_pr, Na_pr, O_pr, S_pr])
            l_ex[ex_cour[2]-1].append(ex_cour)
            ex_cour=[]
        if str(line)[0]=="i" : ex_cour.append(int(''.join(ele for ele in line if ele.isdigit())))
        if str(line)[0]=="l" :
            ex_cour.append(str(line)[8:-1])
            # originalement : le label str(line)[8:-1]
            ex_cour.append(int(str(line)[8]))
        if str(line)[0]=="*" :
            if str(line)[1]=="C" and str(line)[2]==" " : C_pr = extract_percentage(str(line))
            if str(line)[1]=="C" and str(line)[2]=="r" : Cr_pr= extract_percentage(str(line))
            if str(line)[1]=="N" and str(line)[2]==" " : N_pr = extract_percentage(str(line))
            if str(line)[1]=="N" and str(line)[2]=="a" : Na_pr= extract_percentage(str(line))
            if str(line)[1]=="O"                       : O_pr = extract_percentage(str(line))
            if str(line)[1]=="S"                       : S_pr = extract_percentage(str(line))
    return l_ex

def get_L_ex(nb_files, nc):
    """ argument : nb de fichiers à lire, nb de classes
        retourne : liste des exemples, triés par classe
            format  L_ex=[ [liste des exemples de classe 1], [liste des exemples de classe 2], ... ]
            ! cette liste est totale, et comprend les exemples de tous les fichiers .txt, voir read_file
    """
    L_classes=[[] for i in range(nc)]
    L_ex=[]
    for i in range(1, nb_files+1):
        l_ex=read_file("donnees/Jeu drugs and explosives_15 "+str(i)+".txt", nc)
        for j in range(len(l_ex)):
            L_classes[j].extend(l_ex[j])
            L_ex.extend(l_ex[j])
    return L_classes, L_ex
    
def print_Ls(L_classes, L_ex, nc):
    """ Fonction de débeuguage
        la commenter dans le main
    """
    for i in range(nc):
        for j in range(len(L_classes[i])):
            print(L_classes[i][j])
            print(L_ex[i])

def main():
    # ici : n=6
    nc=2                            #nb de classes
    nb_files=10                     #nb de fichiers .txt dans lesquels ils faut lire
    L_classes, L_ex=get_L_ex(nb_files, nc)
    # print_Ls(L_classes, L_ex,nc)           #pour le débeuguage à garder commentée pour ne pas spammer
    
main()

