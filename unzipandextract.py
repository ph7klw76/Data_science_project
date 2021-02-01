import tarfile
import os
from rdkit import Chem
import lzma
import resultsFile

fname1 = '/scratch/woon/b3lyp_2017'
A = 'Compound_075275001_075300000'
B = '.tar.gz'
C = '.txt'
D = '.log'
fname = os.path.join(fname1, A+B)
tar = tarfile.open(fname, 'r:gz')
# tar.extractall()
# tar.close()
print('extraction success.')
path=os.path.join(fname1,A) 
arr1 = sorted(os.listdir(path))
# print(arr1)
print(len(arr1),' number of molecules')
savingfilepath=os.path.join(fname1, A+C)
for filename in arr1:
    mymoleculepath = os.path.join(path, filename)
    print(filename)
    path1 = mymoleculepath
#    print(path1,' path of my molecule')
    if os.path.isdir(path1):
#        print(path1, 'it is directory')
        ERROR = False
    else:
        ERROR = True
#    print(ERROR)
    if not ERROR:
        arrf = sorted(os.listdir(mymoleculepath))
        print(arrf)
        if len(arrf)==5:
            filepath_TD = os.path.join(path1, arrf[4])  # TDDFT
            tempTD=os.path.join(fname1, arrf[4]+D)
            filepath_HOMOLUMO = os.path.join(path1, arrf[1])  # HOMOLUMO
            tempHOMOLUMO=os.path.join(fname1, arrf[1]+D)
            filepath_SMILE = os.path.join(path1, arrf[2])  # molfile
            print(arrf[1])
            mydata=[]
#            print(filepath_SMILE,'SMILE')
            try:
                m = Chem.MolFromMolFile(filepath_SMILE)
                smile=str(Chem.MolToSmiles(m))
                salt=smile.find('.')
                if salt!=-1:
                    smile='An exception occurred'
            except: 
                smile='An exception occurred'
            if smile.find('occurred')>-1:
                file_SMILE_error=True
            else:
                file_SMILE_error=False
            print(filename,smile,'smile got error?',file_SMILE_error)
            try:
                with lzma.open(filepath_HOMOLUMO) as f, open(tempHOMOLUMO, 'wb') as fout:
                    file_content = f.read()
                    fout.write(file_content)
                    writefile_error=False
            except:
                writefile_error=True
            if writefile_error==False:
                try:
                    file_HOMOLUMO=resultsFile.getFile(tempHOMOLUMO) #
                    iter_Orbirtal=file_HOMOLUMO.virtual_mos[-1]+1
                    HOMO_index=round(file_HOMOLUMO.num_elec/2)-1
                    charge=file_HOMOLUMO.charge
                    multiplicity=file_HOMOLUMO.multiplicity
                    dipole=file_HOMOLUMO.dipole
                    energy=file_HOMOLUMO.energies
                    raw_orbital=str(file_HOMOLUMO.mo_sets)
                    structure=file_HOMOLUMO.geometry
                    result =raw_orbital.split(',')
                    orbital=[]
                    for i in range(iter_Orbirtal):
                        myresult=result[i]
                        myresult=myresult.split('\n')[0]
                        myresult=myresult.replace('UHFa','').replace('A','').replace('RHF','')
                        if i==0:
                           myresult=myresult.replace('{','').replace(':','').replace('[','').replace('\'','').strip()
                        if i==HOMO_index:
                           HOMO=myresult.strip()
                        if i==HOMO_index+1:
                           LUMO=myresult.strip()
                        myresult=myresult.strip() 
                        orbital.append(str(myresult))
                        file_HOMOLUMO_error=False
                except:
                    print('getfile extraction fail ',filepath_HOMOLUMO)
                    file_HOMOLUMO_error=True
                os.remove(tempHOMOLUMO)
            try:
                with lzma.open(filepath_TD) as f, open(tempTD, 'wb') as fout2:
                    file_content = f.read()
                    fout2.write(file_content) 
                    writefile_error2=False
            except:
                writefile_error2=True
            if writefile_error2==False:
                try:
                    with open(tempTD,'r') as file:
                        myline=100000000
                        for ii,line in enumerate(file):
                            if line.__contains__('SUMMARY OF TDDFT RESULTS'):
                                myline=ii
                            if myline+6>ii>myline+4:
                                newline=line.strip('\n')
                                newline=newline.split()
                                S1=newline[-5]
                                Osc=newline[-1]
                                file_TD_error=False                       
                except:
                    print('get S1 and osc fails ',filepath_TD)
                    file_TD_error=True
                os.remove(tempTD)
            if (file_TD_error==False) and (file_HOMOLUMO_error==False) and (file_SMILE_error==False) and(writefile_error==False) and (writefile_error2==False):
                print('HOMO=',HOMO,'HOMO=',LUMO,'S1=',S1,'osc=',Osc)
                print('\n')
                mydata=[filename,smile,multiplicity,charge, HOMO,LUMO,S1,Osc,dipole,energy,orbital,structure]
                datatosave=str(mydata)
                print(datatosave)
                with open(savingfilepath, 'a') as f3:
                    f3.write(datatosave)
                    f3.write('\n')
