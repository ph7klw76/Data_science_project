from rdkit import Chem
from rdkit.ML.Descriptors import MoleculeDescriptors
from rdkit.Chem import Descriptors
from padelpy import from_smiles
import re
import time

nms=[x[0] for x in Descriptors._descList]
print('\n')
calc = MoleculeDescriptors.MolecularDescriptorCalculator(nms)
f=open('/scratch/woon/b3lyp_2017/datasmile2.txt')
for i, line in enumerate(f):
    mydes=[]
    mylist=[]
    line=line.split(',')
    number=str(line[0])
    print(number)
    line=line[1]
    m = Chem.MolFromSmiles(line)
    try:
        time.sleep(1)
        des= from_smiles(line,fingerprints=True,timeout=180)
        des=str(des).split(',')
        for ii in range(len(des)):
            b=des[ii].split(',')
            b=des[ii].strip('[').strip(']')
            b=re.sub('[^.,a-zA-Z0-9 \n\.]', '', b)
            b=b.replace('[',' ')
            b=b.replace(']',' ')
            b=b.strip()
            b=b.split(' ')
            mylist.append(b[0])
            try:
                b=b[1]
            except:
                b=''
            if bool(b)==True:
                mydes.append(float(b))
            if bool(b)==False:
                mydes.append('NA')
    # print(len(mylist))
            a=calc.CalcDescriptors(m)
            a=str(a)
            a=a.replace('(', '')
            a=a.replace(')', '')
            line=str(line)
            towrite=str(number+','+line.strip(' ').strip('\n')+','+a+','+str(mydes))
            with open('/scratch/woon/b3lyp_2017/book4.csv', 'a') as mydata:
                mydata.write(towrite+'\n')
    except:
        time.sleep(3)
