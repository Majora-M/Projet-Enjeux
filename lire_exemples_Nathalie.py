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
    sets=[[[],[],[],[],[],[],[],[]]]
    for line in file:
        if str(line)[0]=="\n":
            sets.append([[],[],[],[],[],[],[],[]])
            i+=1
        if str(line)[0]=="i" : sets[i][0]=int(''.join(ele for ele in line if ele.isdigit()))
        if str(line)[0]=="l" : sets[i][1]=1
        # originalement : le label str(line)[8:-1]
        if str(line)[0]=="*" :
            if str(line)[1]=="C" and str(line)[2]==" " : sets[i][2]=extract_percentage(str(line))
            if str(line)[1]=="C" and str(line)[2]=="r" : sets[i][3]=extract_percentage(str(line))
            if str(line)[1]=="N" and str(line)[2]==" " : sets[i][4]=extract_percentage(str(line))
            if str(line)[1]=="N" and str(line)[2]=="a" : sets[i][5]=extract_percentage(str(line))
            if str(line)[1]=="O"                       : sets[i][6]=extract_percentage(str(line))
            if str(line)[1]=="S"                       : sets[i][7]=extract_percentage(str(line))
    return sets

def get_sets(nb_files):
    Sets=[]
    for i in range(1, nb_files+1):
        Sets.append(read_file("donnees/Jeu drugs and explosives_15 "+str(i)+".txt"))
        print("Set", i, "is of length", len(Sets[i-1]))
    return Sets

def main():
    # ici : n=6
    nb_files=10
    Sets=get_sets(nb_files)
    print(Sets[0][:3])
    
main()

