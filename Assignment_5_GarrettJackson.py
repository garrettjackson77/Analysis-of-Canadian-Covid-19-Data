#!/usr/bin/env python
# coding: utf-8

# In[85]:


import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys

class COVID19():
    def __init__(self):
        self.data=None
        self.dates=None
        self.provinces=None
        self.totals_per_province=0
        self.totals_per_day=0
        
    def read_data(self, filename):
        data=np.loadtxt(filename,delimiter='\t',dtype=str)
        self.dates=data[1:,0]
        self.dates=self.dates[::-1] # reverse order
        self.provinces=data[0,1:]
        self.data=np.array(data[1:,1:], dtype=int)
        self.data=self.data[::-1] # reverse order
        self.totals_per_province=self.data.sum(axis=0)
        self.totals_per_day=self.data.sum(axis=1)
        print('Loaded data with {0} days of {1} provinces.'.format(self.dates.size, self.provinces.size))
    
    def compute_correlations(self):
        """
        Computer correlations between provinces.
        """
        self.cors=np.zeros( (self.provinces.size,self.provinces.size) )
        self.pvalues=np.zeros( (self.provinces.size,self.provinces.size) )
        n=-1
        for c in range(len(self.provinces)):
            n=n+1
            x=self.data[:,c]
            i=0
            for c in range(len(self.provinces)):
                y=self.data[:,c]
                coeff,pval=stats.pearsonr(x,y)
                self.cors[n][i]=coeff
                self.pvalues[n][i]=pval
                i=i+1
    
    def plot(self):
        """
        Plot data.
        """
        fig,axs=plt.subplots(2,2)
        fig.set_size_inches(8,8)
        fig.tight_layout(pad=5)
        x=self.dates
        axs[0,0].plot(x,self.data[:,0], label='BC')                                                  
        axs[0,0].plot(x,self.data[:,1], label='AB')
        axs[0,0].plot(x,self.data[:,2], label='SK')
        axs[0,0].plot(x,self.data[:,3], label='MB')
        axs[0,0].plot(x,self.data[:,4], label='ON')
        axs[0,0].plot(x,self.data[:,5], label='OC')
        axs[0,0].plot(x,self.data[:,6], label='ATL')
        axs[0,0].plot(x,self.data[:,7], label='CRUISE')
        plt.setp(axs[0,0].get_xticklabels(), rotation=90, fontsize=7)
        axs[0,0].set_xlabel('Date')
        axs[0,0].set_ylabel('Number of Patients')
        axs[0,0].set_title('COVID-19 Infections Per Province')
        axs[0,0].legend()
        
        labels='BC','AB','SK','MB','ON','OC','ATL','CRUISE'
        percent=[self.totals_per_province[0]/sum(self.totals_per_province),self.totals_per_province[1]/sum(self.totals_per_province),
                 self.totals_per_province[2]/sum(self.totals_per_province),
                 self.totals_per_province[3]/sum(self.totals_per_province),self.totals_per_province[4]/sum(self.totals_per_province),
                 self.totals_per_province[5]/sum(self.totals_per_province),self.totals_per_province[6]/sum(self.totals_per_province),
                self.totals_per_province[7]/sum(self.totals_per_province)]
        explode=(0,0,0,0,0.1,0,0,0)
        axs[0,1].pie(percent,explode=explode,labels=labels, autopct='%.0f%%',shadow=True) 
        axs[0,1].set_title('Provincial Percentage of Total COVID-19 Cases')
        
        axs[1,0].bar(x, self.totals_per_day,color='orange')
        axs[1,0].set_xlabel('Date')
        axs[1,0].set_ylabel('Number of Patients')
        axs[1,0].set_title('Total COVID-19 Infections in Canada')
        plt.setp(axs[1,0].get_xticklabels(), rotation=90, fontsize=7)
        
        s=100*self.cors.flatten()
        i=0
        for x in range(len(self.provinces)):
            for y in range(len(self.provinces)):
                axs[1,1].scatter(self.provinces[x],self.provinces[y],s=s[i],c='blue')
                i=i+1
        axs[1,1].set_xlabel('Province')
        axs[1,1].set_ylabel('Province')
        plt.setp(axs[1,1].get_xticklabels(), rotation=90, fontsize=10)
        axs[1,1].set_title('COVID-19 Correlations Between Provinces')
    
        plt.savefig('COVID-19.pdf')


# In[86]:


c1=COVID19()
c1.read_data('./COVID-19_Canada_as_of_Mar162020.txt')


# In[87]:


# compute correlations among provinces
c1.compute_correlations()


# In[88]:


# plot
c1.plot()

