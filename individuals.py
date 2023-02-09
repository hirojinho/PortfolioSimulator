
import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib
from state import State
from matplotlib import patheffects

matplotlib.use('TkAgg')

class Individuals(State):
    def calculate_stats(self):
        self._stats = pd.DataFrame()
        self._stats['Annualized Returns(%)'] = self._datos_returns.mean() * self.semana *100
        self._stats['Annualized Volatility(%)'] = self._datos_returns.std() * np.sqrt(self.semana)*100
        self._stats['Sharpe Ratio'] = self._stats['Annualized Returns(%)']/self._stats['Annualized Volatility(%)']
    
    def graph(self): #plots the historical series for each asset
        plt.subplots_adjust(hspace=.5,wspace=.5) # it adds space in between plots
        for column in self._datos:
            plt.subplot(321 + self._datos.columns.get_loc(column))
            ax = plt.gca()
            ax.plot(self._datos[column], color = tuple(np.random.uniform(0, 1, [1, 3])[0]))
            ax.set_xlabel('Dates',fontsize=14)
            ax.set_ylabel('Price',fontsize =14)
            ax.set_title(column)
        plt.show()
        
    def relative_performance(self): #Normalizes each asset series
        fig2 =plt.figure(figsize=(14,10))
        plt.plot(self._normalized_series)
        title_text_obj = plt.title("Historical Performance Normalized", fontsize = 18,
                                verticalalignment = 'bottom')
        title_text_obj.set_path_effects([patheffects.withSimplePatchShadow()])
        pe = patheffects.withSimplePatchShadow(offset = (1, -1), shadow_rgbFace = (1,0,0),
                                            alpha = 0.8)
        xlabel_obj = plt.xlabel('Dates', fontsize = 16)
        ylabel_obj = plt.ylabel('Asset Price Evolution', fontsize = 16)
        #('AGG','SPY','QQQ','EMB','GLD')
        plt.legend(list(self._datos.columns),fontsize = 16)
        plt.show()
    
    def dispersion(self): #the dispersion of each asset in camparison with normal distribution
        binsnumber = 35
        fig3, ax = plt.subplots(figsize=(14,10))
        plt.subplots_adjust(hspace=.4,wspace=.4) # it adds space in between plots
        for column in self._datos_returns:
            plt.subplot(321 + self._datos_returns.columns.get_loc(column))
            ax = plt.gca()

            ax.hist(self._datos_returns[column], bins=binsnumber, color='steelblue', density = True,
                    alpha = 0.5, histtype ='stepfilled',edgecolor ='red' )

            sigma, mu = self._datos_returns[column].std(),self._datos_returns[column].mean() # mean and standard deviation
            s = np.random.normal(mu, sigma, 1000)
            count, bins, ignored = plt.hist(s, binsnumber, density=True, alpha = 0.1)
            ax.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=1.5, color='r')
            ax.annotate('Skewness: {}\n\nKurtosis: {}'.format(round(self._datos_returns[column].skew(),2),round(self._datos_returns[column].kurtosis(),2)),
                        xy=(10,20),xycoords = 'axes points',xytext =(20,60),fontsize=12)
            ax.set_xlabel('Values')
            ax.set_ylabel('Frequency')
            ax.set_title(column)
        plt.show()
    
    def compare(self, column1, column2): #distribution of returns from two distinct assets
        fig4 = plt.figure(figsize=(14,10))
        sns.distplot(self._datos_returns[column1])
        sns.distplot(self._datos_returns[column2])
        plt.legend((column1,column2),fontsize = 12)

        # anotate an important value
        plt.annotate('{} Sharpe: {}\n{} Sharpe: {}'.format(
                    column1,
                    round(self._stats.loc[column1,'Sharpe Ratio'],2),
                    column2,
                    round(self._stats.loc[column2,'Sharpe Ratio'],2)),
                    xy=(-.01,40),
                    xycoords = 'data',
                    xytext =(-.07, 50),
                    fontsize=16)
        plt.title(column1 + ' vs ' + column2,fontsize=18)
        plt.xlabel('Returns Distribution', fontsize= 14)
        plt.ylabel('Frequency',fontsize=14)
        plt.show()