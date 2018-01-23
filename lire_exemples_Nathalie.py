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
    ext=""
    for i in range(len(string)):
        if string[i]=="(":
            j=i+1
            while string[j]!=",":
                ext=ext+string[j]
                j+=1
    return float(ext)
    
def read_file(file_name):
    file=open(file_name, "r")
    i=0
    sets=[[]]
    for line in file:
        if str(line)[0]=="\n":
            sets.append([])
            i+=1
        if str(line)[0]=="i" : sets[i].append(int(''.join(ele for ele in line if ele.isdigit())))
        if str(line)[0]=="l" : sets[i].append(1)
        # originalement : le label str(line)[8:-1]
        if str(line)[0]=="*" :
            if str(line)[1]=="C" and str(line)[2]==" " : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="C" and str(line)[2]=="r" : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="N" and str(line)[2]==" " : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="N" and str(line)[2]=="a" : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="O"                       : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="S"                       : sets[i].append(extract_percentage(str(line)))
    return sets[0:130]

def read_file2(file_name):
    file=open(file_name, "r")
    i=0
    sets=[[]]
    for line in file:
        if str(line)[0]=="\n":
            sets.append([])
            i+=1
        if str(line)[0]=="i" : sets[i].append(int(''.join(ele for ele in line if ele.isdigit())))
        if str(line)[0]=="l" :
            if i <=59:
                sets[i].append(0)
            elif i <=144:
                sets[i].append(1)
            else:
                sets[i].append(2)
        # originalement : le label str(line)[8:-1]
        if str(line)[0]=="*" :
            if str(line)[1]=="C" and str(line)[2]==" " : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="C" and str(line)[2]=="r" : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="N" and str(line)[2]==" " : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="N" and str(line)[2]=="a" : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="O"                       : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="S"                       : sets[i].append(extract_percentage(str(line)))
    return sets[0:190]

def read_file3(file_name):
    file=open(file_name, "r")
    i=0
    sets=[[]]
    for line in file:
        if str(line)[0]=="\n":
            sets.append([])
            i+=1
        if str(line)[0]=="i" : sets[i].append(int(''.join(ele for ele in line if ele.isdigit())))
        if str(line)[0]=="l" :
            if i <=19:
                sets[i].append(0)
            elif i <=34:
                sets[i].append(1)
            else:
                sets[i].append(2)
        # originalement : le label str(line)[8:-1]
        if str(line)[0]=="*" :
            if str(line)[1]=="C" : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="0" : sets[i].append(extract_percentage(str(line)))
            if str(line)[1]=="N" : sets[i].append(extract_percentage(str(line)))
    return sets[0:190]

def tri_classe(L,nb_classe):
    R=[[] for i in range(nb_classe)]
    for ex in L:
        R[ex[1]].append(ex)
    return R

def get_sets(nb_files):
    Sets=[]
    for i in range(1, nb_files+1):
        Sets=Sets+read_file("donnees/Jeu drugs and explosives_15 "+str(i)+".txt")
    return Sets

def get_sets2(nb_files):
    Sets=[]
    for i in range(1, nb_files+1):
        Sets=Sets+read_file2("donnees/Jeu drugs, explosives, benigns_15 "+str(i)+".txt")
    return Sets

def get_sets3(nb_files):
    Sets=[]
    for i in range(1, nb_files+1):
        Sets=Sets+read_file3("donnees/Jeu drugs, explosives, benigns_simple_15 "+str(i)+".txt")
    return Sets


