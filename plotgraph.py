import matplotlib.pyplot as plt
import numpy as np

plt_1 = plt.figure(figsize=(6, 6))

#f=open('E:/LS14soc-1.txt', 'r')
f=open('E:/LS141.txt', 'r')
for i,line in enumerate(f):
    line=line.strip('\n')
    print(line)
    E=line.split()[0]
    ST=line.split()[1]
    if float(E)<4.0:
        if ST[0]=='S':
            xpoints = np.array([0, 1])
            ypoints = np.array([E, E])
            plt.plot(xpoints,ypoints, color='blue')
            plt.text(1.05,E,ST)
            plt.text(-0.15,E,"%.2f" % float(E)+' eV',size=14)
        if ST[0]=='T':
            xpoints = np.array([2.5, 3.5])
            ypoints = np.array([E, E])
            plt.plot(xpoints,ypoints, color='green')
            plt.text(3.55,E,ST)
            plt.text(2.45,E,"%.2f" % float(E)+' eV',size=14)
plt.xlim(-0.15,4)
plt.ylabel('Energy (eV)',size=12)
plt.tick_params(left = False, right = False , labelleft = False ,
                labelbottom = False, bottom = False)
plt.savefig('E:/LS14soc-1.tiff', dpi=600)
plt.show()
