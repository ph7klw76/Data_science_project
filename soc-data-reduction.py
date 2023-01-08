"""
Created on Fri Jan  6 20:27:21 2023

@author: User
"""
import numpy as np

dataT=[]
dataS=[]
f=open('E:/LS19-1.txt', 'r')
f2=open('E:/LS19soc-1.txt', 'r')
f3=open('E:/LS19soccaluation.txt', 'w')
for i,line in enumerate(f):
    line=line.strip('\n')
    E=line.split()[0]
    S=line.split()[1]
    if S[0]=='S':
       dataS.append(E)
    if S[0]=='T':
       dataT.append(E)
       
Hbar=6.5821E-16  
KbT=25.7*0.001
lamda=0.25 #assume
def krisc(Hso,dE): #in eV
    Hso=0.000123981*Hso # convert cm-1 to eV
    if dE+lamda<0: # exp is 1
        k=2*np.pi*np.power(Hso,2)
    else:
        k=2*np.pi*np.power(Hso,2)*np.exp(-1*(np.power((dE+lamda),2)/4*lamda)/KbT)
    k=k/(Hbar*np.sqrt(4*np.pi*lamda*KbT))
    return k


# S0=['S0']    
# T1=['T1','T2']
# S1=['S1','S2']
# T2=['T3','T4']
# S2=['S3','S4']
# T3=['T5','T6']
# T4=['T7']
# T5=['T8','T9']
# T6=['T10']
# S3=['S5','S6','S7','S8','S9','S10']
# groupS=[S0,S1,S2,S3]
# groupT=[T1,T2,T3,T4,T5,T6]
# data=f2.readlines()
# n=len(data)
# Sn=len(groupS)
# Tn=len(groupT)
# calculation=[]

# for Tnn in range(Tn):
#     for i in range(n):
#         S=data[i].split()[0]
#         T=data[i].split()[1]
#         Hso=float(data[i].split()[2])
#         if S in groupS[4]:
#             if T in groupT[Tnn]:
#                 calculation.append(Hso**2)
#     c=np.sqrt(sum(calculation))
#     print('S4',' T'+str(Tnn+1),c)
#     calculation=[]
            
    
            # print(S,T,Hso)
            
            
            
for i,line in enumerate(f2):
    line=line.strip('\n').split()
    S=int(line[0][1])
    T=int(line[1][1])
    S=float(dataS[S-1]) 
    T=float(dataT[T-1])
    dE=S-T #activated positive
    Hso=float(line[2])
    k=krisc(Hso,dE)
    if -0.1<dE<0.1:
        print(line[0],line[1],1/k, dE)
