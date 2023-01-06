import matplotlib.pyplot as plt
import numpy as np

plt_1 = plt.figure(figsize=(6, 6))
f=open('E:/LS19.txt', 'r')
for i,line in enumerate(f):
    line=line.strip('\n')
    E=line.split()[0]
    S=line.split()[1]
    if S[0]=='S':
        xpoints = np.array([0, 1])
        ypoints = np.array([E, E])
        plt.plot(xpoints,ypoints, color='blue')
        plt.text(1.05,E,S)
        plt.text(-0.05,E,"%.3f" % float(E)+' eV')
    if S[0]=='T':
        xpoints = np.array([2.5, 3.5])
        ypoints = np.array([E, E])
        plt.plot(xpoints,ypoints, color='green')
        if S=='T6':
            print(S)
            plt.text(3.55,E,'    ,T6')
        if S!='T6':          
            plt.text(3.55,E,S)
        plt.text(2.45,E,"%.3f" % float(E)+' eV')
plt.xlim(-0.15,4)
plt.savefig('E:/LS19.png', dpi=300)
plt.show()
