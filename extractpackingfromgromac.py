import numpy as np
import re

def finddistance(x1,y1,z1,x2,y2,z2):
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def centerofmolecule(filepath,S1,S2,N1,no_atom,filepath_data):
    with open(filepath,'r') as f:
        with open(filepath_data, 'w') as f2:
            for i,line in enumerate(f):
                ii=(i-1)//no_atom
                if i==S1+1+ii*no_atom:
                    lineS1=line
                    f2.write(lineS1)
                if i==S2+1+ii*no_atom:
                    lineS2=line  
                    f2.write(lineS2)
                if i==N1+1+ii*no_atom:
                    lineN1=line
                    f2.write(lineN1)
        f2.close()

def atomic_position(filepath_data,which_line):
    with open(filepath_data, 'r') as f:
        for i,line in enumerate(f):
            if i==which_line:
                line=line.split()
                z=float(line[-4:-3][0])
                y=float(line[-5:-4][0])
                x=float(line[-6:-5][0])
        return x,y,z
def nth_shortest(dis,n):   
    s = set(dis)
    mymin=sorted(s)[n]
    indexes = [i for i,x in enumerate(dis) if x ==mymin ]
    return indexes[0], mymin

def extract_molecule_pair(file_to_read,file_to_write,no_of_atom,index_1,index_2=0):
        with open(file_to_read, 'r') as f:
            with open(file_to_write,'w') as f2:
                f2.write('extracted molecule'+'\n')
                if index_2!=0:
                    f2.write(str(no_of_atom*2)+'\n')
                if index_2==0:
                    f2.write(str(no_of_atom*1)+'\n')
                for i,line in enumerate(f):
                    if i>1:
                        line2=line.split()[0]
                        line2=line2.split('D')[0] #molecular dependent
                        if line2==str(index_1):
                            f2.write(line)
                        if index_2!=0:
                            if line2==str(index_2):
                                f2.write(line)
                f2.write('   0.00000   0.00000   0.00000')
                f2.close()
            f.close()
            
def convertpdb_gaussian(file_to_read,file_to_write,job_type):
    unique_elemment=[]
    with open(file_to_read, 'r') as f:
        with open(file_to_write,'w') as f2:
            f2.write('%mem=15GB'+'\n'+'%nprocshared=8'+'\n')
            if job_type==1:
                f2.write('# Def2SVP nosymm punch(MO)'+'\n'+'# scf=(direct,nosymm)'+'\n')
                f2.write('\n'+'type 1'+'\n'+'\n'+'0 1'+'\n')
                for i,line in enumerate(f):
                    if i>1:
                        line=line.split()
                        try:
                            element=line[2]
                            element=re.split('(\d+)', element)[0]
                            unique_elemment.append(element)
                            z=line[-3:-2][0]
                            y=line[-4:-3][0]
                            x=line[-5:-4][0]
                            f2.write(str(element)+'    '+str(x)+'    '+str(y)+'    '+str(z)+'\n')
                        except:
                            None
                myset=list(set(unique_elemment))
                f2.write('\n')
                for ele in myset:
                    f2.write(str(ele)+' ')
                f2.write('0'+'\n')
                f2.write('Def2SVP'+'\n')
                f2.write('****')
                f2.close()
            if job_type==2:
                f2.write('#  gen guess=huckel nosymm pop=nboread'+'\n'+'# scf=(direct,nosymm)'+'\n')
                f2.write('\n'+'type 2'+'\n'+'\n'+'0 1'+'\n')
                for i,line in enumerate(f):
                    if i>1:
                        line=line.split()
                        try:
                            element=line[2]
                            element=re.split('(\d+)', element)[0]
                            unique_elemment.append(element)
                            z=line[-3:-2][0]
                            y=line[-4:-3][0]
                            x=line[-5:-4][0]
                            f2.write(str(element)+'    '+str(x)+'    '+str(y)+'    '+str(z)+'\n')
                        except:
                            None
                myset=list(set(unique_elemment))
                f2.write('\n')
                for ele in myset:
                    f2.write(str(ele)+' ')
                f2.write('0'+'\n')
                f2.write('Def2SVP'+'\n')
                f2.write('****'+'\n'+'\n')
                f2.write('$NBO SAO=w53 FAO=W54 $END')
                f2.close()
################important to rename Fork'    

def pair_of_molecule_with_distance(filepath_gro,no_of_atom,filepath_data,filepath_towrite_pair,n1,n2,n3):
    centerofmolecule(filepath_gro,n1,n2,n3,no_of_atom,filepath_data)          
    with open(filepath_towrite_pair, 'w') as f2:
        for i in range(1095):
            if i<1000:   ####determine how many data you want
                dis=[]  # fresh array for new i
                m2=[] # index position for 2nd molecule in the gro file that are test
                xo1,yo1,zo1=atomic_position(filepath_data,i*3)
                xo2,yo2,zo2=atomic_position(filepath_data,i*3+1)
                xo3,yo3,zo3=atomic_position(filepath_data,i*3+2)
                if (8.0>xo1>2.0) and (8.0>yo1>2.0) and (8.0>zo1>2.0) and (8.0>xo2>2.0) and (8.0>yo2>2.0) and (8.0>zo2>2.0) and (8.0>xo3>2.0) and (8.0>yo3>2.0) and (8.0>zo3>2.0): #remove edge-effect
                    #print(xo1,xo2,xo3)
                    for ii in range(1095):  # 1095 depends on the how many molecule in the system 
                        if i!=ii:
                            distance=0
                            for iii in range(3):
                                x2,y2,z2=atomic_position(filepath_data,ii*3+iii)
                                 #print(xo1,xo2,xo3,x2,y2,z2) # molecular pair to be tested the distance
        #                        print(x2,y2,z2,iii)
                                distanceo1= finddistance(xo1,yo1,zo1,x2,y2,z2)
                                distanceo2= finddistance(xo2,yo2,zo2,x2,y2,z2)
                                distanceo3= finddistance(xo3,yo3,zo3,x2,y2,z2)
                                distance +=(distanceo1+distanceo2+distanceo3)/3
                            distance=distance/3
        #                    print(distance)
                            m2.append(ii+1)
                            dis.append(distance)  #dis[0] is the second molecule
                    for n in range(20):
                        index, mymin= nth_shortest(dis,n)
                        if float(mymin)<1.2:  # can change distance limit
                            f2.write(str(i+1)+','+str(m2[index])+','+str(mymin)+'\n')
    f2.close()

filepath_gro='./md_0_1.gro'
no_of_atom=68
n1=35
n2=60
n3=28
filepath_data='./data.txt'
filepath_towrite_pair='./pair.txt'


pair_of_molecule_with_distance(filepath_gro,no_of_atom,filepath_data,filepath_towrite_pair,n1,n2,n3)
