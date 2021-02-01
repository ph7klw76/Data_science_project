import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("time_series_covid19_confirmed_global.csv") #cumulative cases
print(data) #print the 0 to 9 rows of dataframe
country=data['Country/Region']
state=data['Province/State']


total_cols=len(data.axes[1])
date=[data.columns[4+i] for i in range(total_cols-4)]

todrop=[]
for i in range(len(data)):
    if pd.isna(state[i]):
        co=data.at[i, date[total_cols-5]]
        if co<2000:
            todrop.append(i)
        
listofcountry=[]
for item in country:
        if item not in listofcountry:
            listofcountry.append(item)   
for i in todrop:
    print(country[i])
    listofcountry.remove(country[i])   
         


def findcountryrow(c):
    counting=[]
    for count, i in enumerate(country):
        if i==c and pd.isna(state[count]):
            counting.append(count)
            break
        elif i==c:
            counting.append(count)                               
    return counting

def countrydailyinfection(c,i):
    mycountry=findcountryrow(c)
    mydata=0
    for ii in mycountry:
        if i==0:
            mydata+=data.at[ii, date[i]] # select based on country and date
        else:
            mydata+=data.at[ii, date[i]]-data.at[ii, date[i-1]]
    return mydata

def average10days(c):
    average=[]
    for i in range(len(date)-10):
        mylist=[(countrydailyinfection(c,ii)) for ii in range(0+i,10+i)]
        mylist=sum(np.asarray(mylist))
        average.append(mylist/10)
    return average

x=[data.columns[4+i+10] for i in range(total_cols-4-10)]


        
newx=[i+1 for i in range(len(x))]

from scipy.optimize import curve_fit

def myfilter(x):
  if x > 1:
    return x

def filtereddata(c):
    y=[]
    mydata = filter(myfilter,average10days(c))
    for i in mydata:
        y.append(i)
    yy=np.asarray(y) 
    newx=[i+1 for i in range(len(yy))]
    return newx,yy

def intergration(func):
    y_0=func[0]
    newx=len(func)
    y_n=func[newx-1]
    y=0
    for i in range(newx-2):
        y+=2*func[i+1]
    return (y_0+y_n+y)*0.5

def normalizeddata(c):
    newx, yy=filtereddata(c)
    area=intergration(yy)    
    maxdata=np.argmax(yy)
    maxdata2=max(yy)
    newx=[i-maxdata for i in range(len(yy))]
    maxdata=len(yy)-maxdata
    newx=np.asarray(newx)
    return newx,yy/area, maxdata,maxdata2

def Gaussian(x,u,sigma):
    a=sigma*np.sqrt(2*np.pi)
    b=np.exp(-0.5*((x-u)/sigma)**2)
    return b/a

def fitting(func,x,y):
    popt, pcov = curve_fit(func, x, y)                                                              
    predicted=func(x, *popt) 
    r=np.corrcoef(y, predicted)
    r2=r[0][1]**2
    return popt, r2

def fittingparameter(listofcountry):
    returndata=[]
    for i in range(len(listofcountry)):
        mydata=normalizeddata(listofcountry[i])
        popt,r2=fitting(Gaussian,mydata[0],mydata[1])
        u, sigma=popt
        cou=listofcountry[i]
        returndata.append([cou,u,sigma,r2, mydata[2], mydata[3]])
    return returndata
i=0  
c1,sigma1,r21, maxvalu=[],[],[],[]  
for coun,u,sigma,r2, peak, maxvalue in fittingparameter(listofcountry):
    if peak >1:
        print(i," country=",coun, " sigma=",round(sigma,3), " r=",round(r2,3))
        c1.append(coun)
        sigma1.append(sigma)
        r21.append(r2)
        maxvalu.append(maxvalue)
    i+=1




plt.hist(sigma1, bins=10, density=True)
plt.title('Probalility versus one sigma: a measure of how long Covid-19 patient is infectious')
plt.ylabel('Probability')
plt.xlabel('standard deviation (days)')

fig, ax = plt.subplots()
ax.scatter(sigma1, r21)
plt.ylabel('correlation coeffient')
plt.xlabel('standard deviation of Gaussian Curve')
plt.title('Gaussian fitting for countries which pass the peaks for more than 10 days')

for i, txt in enumerate(c1):
    ax.annotate(txt, (sigma1[i], r21[i]))   
    
