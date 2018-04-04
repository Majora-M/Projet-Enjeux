import os
import inspect

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
    sets=[[0 for i in range(8)]]
    for line in file:
        if str(line)[0]=="\n":
            sets.append([0 for i in range(8)])
            i+=1
        elif str(line)[0]=="i" : sets[i][0]=int(''.join(ele for ele in line if ele.isdigit()))
        elif str(line)[0]=="l" :
            if i>=60:
                if i <=144:
                    sets[i][1]=1
                else:
                    sets[i][1]=2
        # originalement : le label str(line)[8:-1]
        elif str(line)[0]=="*" :
            if str(line)[1]=="C" and str(line)[2]==" "   : sets[i][2]=extract_percentage(str(line))
            elif str(line)[1]=="C" and str(line)[2]=="r" : sets[i][3]=extract_percentage(str(line))
            elif str(line)[1]=="N" and str(line)[2]==" " : sets[i][4]=extract_percentage(str(line))
            elif str(line)[1]=="N" and str(line)[2]=="a" : sets[i][5]=extract_percentage(str(line))
            elif str(line)[1]=="O"                       : sets[i][6]=extract_percentage(str(line))
            else                                         : sets[i][7]=extract_percentage(str(line))
    return sets[0:190]

def read_file3(file_name):
    file=open(file_name, "r")
    i=0
    sets=[[0 for i in range(5)]]
    for line in file:
        if str(line)[0]=="\n":
            sets.append([0 for i in range(5)])
            i+=1
        #if str(line)[0]=="i" : sets[i][0]=int(''.join(ele for ele in line if ele.isdigit()))
        if str(line)[0]=="l" :
            if i <=19:
                sets[i][1]=0
            elif i <=34:
                sets[i][1]=1
            else:
                sets[i][1]=2
        # originalement : le label str(line)[8:-1]
        elif str(line)[0]=="*" :
            if str(line)[1]=="C" : sets[i][2]=extract_percentage(str(line))
            if str(line)[1]=="N" : sets[i][3]=extract_percentage(str(line))
            if str(line)[1]=="O" : sets[i][4]=extract_percentage(str(line))
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
