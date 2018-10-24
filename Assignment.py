path1="D:\\Users\\850037702\\Downloads\\retention_time.csv"
path2="D:\\Users\\850037702\\Downloads\\scans (1).csv"
import numpy as np
from scipy.optimize import curve_fit #copied from stackoverflow
from scipy import asarray as ar,exp  #copied from stackoverflow
import pylab as plb  #copied from stackoverflow
import matplotlib.pyplot as pt

file=open(path1)
lstOfScan=file.read().split("\n")
file.close()
lstMappingRows=open(path2).read().split("\n")



#This gaussian function copied from stackoverflow
def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))

#This  function finds the upper and lower bound and does a gaussian fit. Currently it is not working properly.Have some errors
def Find_Lower_UpperBound(x,y):
    xrows= [int(float(item)) for item in x]
    yrows= [int(float(item)) for item in y]
    
    lowweBound=min(zip(xrows,yrows))
    upperBound=max(zip(xrows,yrows))
    n = len(xrows)
     #Below code is referenced from stackoverflow
    mean = sum([a*b for a,b in zip(xrows,yrows)])/n
           
    sigma = sum([b*(a-mean) for a,b in zip(xrows,yrows)]^2)/n
    popt,pcov = curve_fit(gaus,xrows,yrows,p0=[1,mean,sigma])
    pt.plot(xrows,gaus(xrows,*popt),'ro:',label='fit')
    pt.show()





        
    
#this function will plot the graph and call another function for gaussian fit    
def PlotGraph():
    plottingXRows=[]
    plottingYRows=[]
    lstRows=MakeRT_IntensityPair(lstMappingRows)
    for item in lstRows:
        plottingXRows.append(item[0].replace("PT","").replace("S",""))
        plottingYRows.append(item[1])
    '''print(plottingXRows)
    print(plottingYRows)'''
    pt.plot(plottingYRows,plottingXRows)
    pt.show()
  
    Find_Lower_UpperBound(plottingYRows,plottingXRows)
        
        
    
    
    
   
    
#the input for this function will be the scan number and output will be the table containing m/z and intensity   
def MakeMappingTable(ScanList,MappingRows,ScanValue):
    IndexOfScan=ScanList.index(ScanValue)
    Table=MappingRows[IndexOfScan].split(",")
    nparray=np.array(Table)
    print(np.reshape(Table,(-1, 2)))

#this function will output retention time corresponding to all peaks having intensity greater than 10*e4  
def Filter_Intensity(nparray,ListofScan):
    lstFilter=[]
    for item in nparray:
        itemIndex=lstOfScan.index(item[0])
        for index,value in enumerate(ListofScan[itemIndex].split(",")):
            if index%2!=0:
                if float(value)>10000:
                    lstFilter.append(item[0])
                    break
    print(lstFilter)
    
    
    
 #this function will output a retention time and intensity pair table   
def MakeRT_IntensityPair(ListofScan):
    lstPairTable=[]
    Counter=-1
    for item in ListofScan:
        Counter+=1
        for index,value in enumerate(item.split(",")):
            if index%2==0:
                if float(value)>=128.0340 and float(value) <=128.0366:
                    lstPairTable.append([lstOfScan[Counter],value])
                    

    
    return lstPairTable
    
   
    
                    
        
        
        
    
    
MakeMappingTable(lstOfScan,lstMappingRows,"PT1.60056S")    
lstPairTable=MakeRT_IntensityPair(lstMappingRows)
nparray=np.array(lstPairTable)
Filter_Intensity(nparray,lstMappingRows)
PlotGraph()
    
    
 

 

