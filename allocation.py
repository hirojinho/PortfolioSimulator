import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
import math
from matplotlib import patheffects
from state import State

matplotlib.use('TkAgg')

class portfolio(State):
    _sliders = []
    tab = pd.DataFrame() #dataframe com os valores de alocação
    
    def __init__(self, datos, percentages):
        super().__init__(datos)
        self.allocate(percentages)
        self._normalized_series1 = self._normalized_series.copy()
        self._normalized_series1['Port1'] = self._normalized_series.mul(self.tab['Port1'].values,axis=1).sum(axis=1)
        self._normalized_series1['Port2'] = self._normalized_series.mul(self.tab['Port2'].values,axis=1).sum(axis=1)
        
    def rebalancing(self, months, time_measure):
        # rebalanceando o portfolio 1
        partial_per1 = self._normalized_series[list(self._datos.columns)].mul(self.tab.Port1.values,axis=1)
        new_nor = partial_per1.copy()
        for i in range(math.ceil(len(self._normalized_series.index)/math.floor(30*months/time_measure))):
            try:
                multiplier = new_nor.iloc[i*math.floor(30*months/time_measure)].sum()
                for j in range(math.floor(months*30/time_measure)):
                    new_nor.iloc[i*math.floor(30*months/time_measure)+j] = (partial_per1.iloc[i*math.floor(30*months/time_measure)+j]/partial_per1.iloc[i*math.floor(30*months/time_measure)])*multiplier
            except IndexError:
                pass
        partial_per1 = new_nor.mul(self.tab['Port1'].values,axis=1)
        self._reb_series = new_nor.copy()
        self._reb_series['Port1'] = new_nor.mul(self.tab['Port1'].values,axis=1).sum(axis=1)
        # rebalanceando o portfolio 2
        partial_per2 = self._normalized_series[list(self._datos.columns)].mul(self.tab.Port2.values,axis=1)
        new_nor = partial_per2.copy()
        n=0
        for i in range(math.ceil(len(self._normalized_series.index)/math.floor(30*months/time_measure))):
            try:
                multiplier = new_nor.iloc[i*math.floor(30*months/time_measure)].sum()
                for j in range(math.floor(months*30/time_measure)):
                    new_nor.iloc[i*math.floor(30*months/time_measure)+j] = (partial_per2.iloc[i*math.floor(30*months/time_measure)+j]/partial_per2.iloc[i*math.floor(30*months/time_measure)])*multiplier
            except IndexError:
                pass
        partial_per2 = new_nor.mul(self.tab['Port2'].values,axis=1)
        self._reb_series['Port2'] = new_nor.mul(self.tab['Port2'].values,axis=1).sum(axis=1)
        
    def calculate_stats(self):
        self._stats = pd.DataFrame()
        self._stats.index = ['Port1', 'Port2']
        self._stats['Expected Returns(%)'] = [np.sum(self._datos_returns.mean()* self.tab.Port1)* self.semana*100,
                                              np.sum(self._datos_returns.mean()* self.tab.Port2)* self.semana*100]
        self._stats['Annualized Volatility(%)'] = [np.sqrt(np.dot(self.tab.Port1.T,np.dot(self._datos_returns.cov()*self.semana,self.tab.Port1)))*100,
                                                   np.sqrt(np.dot(self.tab.Port2.T,np.dot(self._datos_returns.cov()*self.semana,self.tab.Port2)))*100]
        self._stats['Sharpe Ratio'] = self._stats['Expected Returns(%)']/self._stats['Annualized Volatility(%)']
    
    def allocate(self, percentages): #determine the percentage from each portfolio
        self.tab = pd.DataFrame(data = percentages,
                            index=list(self._datos.columns),
                            columns =['Port1','Port2'])
        
    def graph(self): #plots the pizza distribution of each portfolio
        fig5 =plt.figure(figsize=(10,8))
        ax = plt.axes([0.1, 0.1, 0.8, 0.8])
        labels = list(self._datos.columns)
        explode = [0 + i/20 for i, col in enumerate(self._datos.columns)]
        plt.subplot(121)
        plt.pie(self.tab['Port2'],
                explode = explode,
                labels= labels,
                autopct= '%1.1f%%',
                startangle = 90,
                shadow=True)
        plt.title('Portfolio 2',fontsize =14)
        plt.subplot(122)
        plt.pie(self.tab['Port1'],
                explode = explode,
                labels= labels,
                autopct= '%1.1f%%',
                startangle = 67,
                shadow= True)
        plt.title('Portfolio 1',fontsize =14)

        plt.show()
        
    def compare(self): #historical series of each normalized portfolio
        fig6 =plt.figure(figsize=(14,10))
        ax = plt.gca()
        ax.plot(self._normalized_series1[['Port1','Port2']])

        title_text_obj = plt.title("Historical Performance Including Custom Portfolios Normalized",
                                    fontsize = 18,
                                    verticalalignment = 'bottom')
        title_text_obj.set_path_effects([patheffects.withSimplePatchShadow()])
        pe = patheffects.withSimplePatchShadow(offset = (1, -1),
                                                shadow_rgbFace = (1,0,0),
                                                alpha = 0.8)
        xlabel_obj = plt.xlabel('Dates', fontsize = 16)
        ylabel_obj = plt.ylabel('Asset Price Evolution', fontsize = 16)
        #('AGG','SPY','QQQ','EMB','GLD')
        ax.legend(('Portfolio 1', 'Portfolio 2'),fontsize = 12)
        #ax.annotate('EM Portfolio provides \nhigher risk adjusted return',('2018-04-30',1.4),xycoords = 'data',xytext =('2013-08-30',1.4),arrowprops =dict(arrowstyle ='->'),fontsize=14)
        plt.show()
        
    def reb_compare(self, months, time_measure): #historical series of each normalized portfolio
        fig6 =plt.figure(figsize=(14,10))
        ax = plt.gca()
        self.rebalancing(months, time_measure)
        ax.plot(self._reb_series[['Port1','Port2']])
        title_text_obj = plt.title("Historical Performance Including Custom Portfolios Normalized Rebalanced",
                                    fontsize = 18,
                                    verticalalignment = 'bottom')
        title_text_obj.set_path_effects([patheffects.withSimplePatchShadow()])
        pe = patheffects.withSimplePatchShadow(offset = (1, -1),
                                                shadow_rgbFace = (1,0,0),
                                                alpha = 0.8)
        xlabel_obj = plt.xlabel('Dates', fontsize = 16)
        ylabel_obj = plt.ylabel('Asset Price Evolution', fontsize = 16)
        #('AGG','SPY','QQQ','EMB','GLD')
        ax.legend(('Portfolio 1', 'Portfolio 2'),fontsize = 12)
        #ax.annotate('EM Portfolio provides \nhigher risk adjusted return',('2018-04-30',1.4),xycoords = 'data',xytext =('2013-08-30',1.4),arrowprops =dict(arrowstyle ='->'),fontsize=14)
        plt.show()
        
    def dispersion(self):
        binsnumber = 35
        fig7, ax = plt.subplots(figsize=(14,10))
        plt.subplots_adjust(hspace=.4,wspace=.4) # it adds space in between plots
        plt.subplot(121)
        ax = plt.gca()
        ax.hist(self._normalized_series1['Port1'],
                bins=binsnumber, color='steelblue',
                density = True,
                alpha = 0.5,
                histtype ='stepfilled',
                edgecolor ='red')
        sigma, mu = self._normalized_series1['Port1'].std(),self._normalized_series1['Port1'].mean() # mean and standard deviation
        s = np.random.normal(mu, sigma, 1000)
        count, bins, ignored = plt.hist(s, binsnumber, density=True, alpha = 0.1)
        ax.plot(bins,
                1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
                linewidth=1.5,
                color='r')
        ax.annotate('Skewness: {}\n\nKurtosis: {}'.format(round(self._normalized_series1['Port1'].skew(),2),
                                round(self._normalized_series1['Port1'].kurtosis(),2)),
                                xy=(10,20),
                                xycoords = 'axes points',
                                xytext =(20,360),
                                fontsize=14)
        ax.set_xlabel('Values')
        ax.set_ylabel('Frequency')
        ax.set_title('Portolio 1')
        plt.subplot(122)
        ax1 = plt.gca()
        ax1.hist(self._normalized_series1['Port2'],
                bins=binsnumber, color='steelblue',
                density = True,
                alpha = 0.5,
                histtype ='stepfilled',
                edgecolor ='red')
        sigma, mu = self._normalized_series1['Port2'].std(),self._normalized_series1['Port2'].mean() # mean and standard deviation
        s = np.random.normal(mu, sigma, 1000)
        count, bins, ignored = plt.hist(s, binsnumber, density=True, alpha = 0.1)
        ax1.plot(bins,
                 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
                 linewidth=1.5,
                 color='r')
        ax1.annotate('Skewness: {}\n\nKurtosis: {}'.format(round(self._normalized_series1['Port2'].skew(),2),
                                round(self._normalized_series1['Port2'].kurtosis(),2)),
                                xy=(10,20),
                                xycoords = 'axes points',
                                xytext =(20,360),
                                fontsize=14)
        ax1.set_xlabel('Values')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Portfolio 2')
        plt.show()