mport numpy as np
import re
import os
import shutil
import time
import subprocess

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
            if i<20:   ####determine how many data you want
                dis=[]  # fresh array for new i
                m2=[] # index position for 2nd molecule in the gro file that are test
                xo1,yo1,zo1=atomic_position(filepath_data,i*3)
                xo2,yo2,zo2=atomic_position(filepath_data,i*3+1)
                xo3,yo3,zo3=atomic_position(filepath_data,i*3+2)
                if (9.0>xo1>1.0) and (9.0>yo1>1.0) and (9.0>zo1>1.0) and (9.0>xo2>1.0) and (9.0>yo2>1.0) and (9.0>zo2>1.0) and (9.0>xo3>1.0) and (9.0>yo3>1.0) and (9.0>zo3>1.0): #remove edge-effect
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
                        if float(mymin)<1.5:  # can change distance limit
                            f2.write(str(i+1)+','+str(m2[index])+','+str(mymin)+'\n')
    f2.close()

def crete_folder(my_folder):
    if not os.path.exists(str(my_folder)):
        os.makedirs(str(my_folder))          

def check_run_status():
    time.sleep(10)
    read_file=open('./automation.out') # jobname
    for i, line in enumerate(read_file):
        job_id=line.split()[3]
    check_status='squeue -h -j '+ str(job_id)
    process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    while output.__contains__(job_id):
        time.sleep(10)
        process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout 
    return True,job_id
         
filepath_gro='./md_0_1.gro'
no_of_atom=68

filepath_data_molecule='./pair.txt'
with open(filepath_data_molecule,'r') as f:
    avoidfirstindexreclaculation=[0]
    for i,line in enumerate(f):
        line=line.split(',')
        index_11=int(line[0])
        index_22=int(line[1])
        if i<2: # for testing and determine number of pairs calculated
            if index_11 !=avoidfirstindexreclaculation[-1]:
                calculate=True
            else:
                calculate=False
            avoidfirstindexreclaculation.append(index_11)
            my_folder='./pair_'+str(index_11)+'_'+str(index_22)
            crete_folder(my_folder)
            filepath_to_write=my_folder+'/single'+'_'+str(index_11)+'.gro'
            extract_molecule_pair(filepath_gro,filepath_to_write,no_of_atom,index_11,index_2=0)
            filename1='single'+'_'+str(index_11)+'.gro'
            filename2='single'+'_'+str(index_11)+'.pdb'
            shutil.copyfile('./convert.sh',my_folder+'/convert.sh')
            time.sleep(1)
            convert=open(my_folder+'/convert.sh', 'a')
            convert.write('gmx_mpi editconf -f '+my_folder+'/'+filename1+' -o '+my_folder+'/'+filename2+'\n')   
            filepath_to_write=my_folder+'/single'+'_'+str(index_22)+'.gro'
            extract_molecule_pair(filepath_gro,filepath_to_write,no_of_atom,index_22,index_2=0)
            filename1='single'+'_'+str(index_22)+'.gro'
            filename2='single'+'_'+str(index_22)+'.pdb'
            convert.write('gmx_mpi editconf -f '+my_folder+'/'+filename1+' -o '+my_folder+'/'+filename2+'\n')   
            filepath_to_write=my_folder+'/pair'+'_'+str(index_11)+'_'+str(index_22)+'.gro'
            extract_molecule_pair(filepath_gro,filepath_to_write,no_of_atom,index_11,index_2=index_22)  
            filename1='pair'+'_'+str(index_11)+'_'+str(index_22)+'.gro'
            filename2='pair'+'_'+str(index_11)+'_'+str(index_22)+'.pdb'
            convert.write('gmx_mpi editconf -f '+my_folder+'/'+filename1+' -o '+my_folder+'/'+filename2+'\n')
            convert.close()
            time.sleep(1)
            subprocess.run(['sbatch', my_folder+'/convert.sh'])
            done=check_run_status()
            time.sleep(5)
            file_to_read=my_folder+'/single'+'_'+str(index_11)+'.pdb'
            file_to_write=my_folder+'/single'+'_'+str(index_11)+'.com'
            convertpdb_gaussian(file_to_read,file_to_write,1)
            file_to_read=my_folder+'/single'+'_'+str(index_22)+'.pdb'
            file_to_write=my_folder+'/single'+'_'+str(index_22)+'.com'
            convertpdb_gaussian(file_to_read,file_to_write,1)
            file_to_read=my_folder+'/pair'+'_'+str(index_11)+'_'+str(index_22)+'.pdb'
            file_to_write=my_folder+'/pair'+'_'+str(index_11)+'_'+str(index_22)+'.com'
            convertpdb_gaussian(file_to_read,file_to_write,2)
            shutil.copyfile('./gaussian1.sh',my_folder+'/gaussian1.sh')
            time.sleep(1)
            gaussian=open(my_folder+'/gaussian1.sh', 'a')
            if calculate==True:
                crete_folder(my_folder+'/'+str(index_11))
                shutil.copyfile('./gaussian1.sh',my_folder+'/'+str(index_11)+'/gaussian1.sh')
                shutil.copyfile(my_folder+'/single'+'_'+str(index_11)+'.com',my_folder+'/'+str(index_11)+'/single'+'_'+str(index_11)+'.com')
                time.sleep(1)
                gaussian2=open(my_folder+'/'+str(index_11)+'/gaussian1.sh', 'a')
                gaussian2.write('g09 <single_'+str(index_11)+'.com>'+' single_'+str(index_11)+'.log'+'\n')
                gaussian2.close()
                workingdir=os.getcwd()
                os.chdir(workingdir+my_folder.strip('.')+'/'+str(index_11))
                print(os.getcwd())
            subprocess.run(['sbatch','./gaussian1.sh'])    
            gaussian.write('g09 <single_'+str(index_22)+'.com>'+' single_'+str(index_22)+'.log'+'\n')
            gaussian.write('g09 <pair_'+str(index_11)+'_'+str(index_22)+'.com>'+' pair_'+str(index_11)+'_'+str(index_22)+'.log'+'\n')
            gaussian.close()
            os.chdir(workingdir+my_folder.strip('.'))
            print(os.getcwd())
            subprocess.run(['sbatch','./gaussian1.sh'])     
            os.chdir(workingdir)
            print(os.getcwd())
