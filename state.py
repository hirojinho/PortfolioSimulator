
import pypfopt
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from abc import abstractmethod
from scipy.optimize import minimize
from matplotlib.ticker import MaxNLocator

mpl.use('TkAgg')

class State:
    semana = 52
    
    def __init__(self, datos):
        self._datos = datos
        self._datos_returns = np.log(self._datos/self._datos.shift(1))
        self._datos_returns.dropna(inplace=True)
        self._normalized_series = (self._datos/self._datos.iloc[0])
        
    def stats(self): #print stats table
        self.calculate_stats()
        bar = []
        plt.subplots_adjust(hspace=.5,wspace=.5)
        for i in self._stats.columns:
            plt.subplot(321 + self._stats.columns.get_loc(i))
            # Colours - Choose the extreme colours of the colour map
            colours = ["#bbdefb", "#2196f3"]
            # Colormap - Build the colour maps
            cmap = mpl.colors.LinearSegmentedColormap.from_list("colour_map", colours, N=256)
            norm = mpl.colors.Normalize(self._stats.loc[:,i].min(), self._stats.loc[:,i].max()) # linearly normalizes data into the [0.0, 1.0] interval
            ax = plt.gca()
            # grid
            ax.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
            ax.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
            bar.append(ax.bar(self._stats.index,
                              self._stats.loc[:,i],
                              color = cmap(norm(self._stats.loc[:,i])),
                              width = 1,
                              zorder = 2,
                              align='edge'))
            # Reformat x-axis label and tick labels
            ax.set_xlabel('', fontsize=12, labelpad=10) # No need for an axis label
            ax.xaxis.set_label_position("bottom")
            ax.xaxis.set_major_formatter(lambda s, i : f'{s:,.0f}')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.xaxis.set_tick_params(pad=2, 
                                    labelbottom=True,
                                    bottom=True,
                                    labelsize=12,
                                    labelrotation=0)
            ax.set_xticks(self._stats.index, self._stats.index) # Map integers numbers from the series to labels list
            # Reformat y-axis
            ax.set_ylabel('Value',
                          fontsize=12,
                          labelpad=10)
            ax.yaxis.set_label_position("left")
            ax.yaxis.set_major_formatter(lambda s, i : f'{s:,.3f}')
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.yaxis.set_tick_params(pad=2, labeltop=False, labelbottom=True, bottom=False, labelsize=12)
            # Add label on top of each bar
            ax.bar_label(bar[-1], labels=[f'{e:,.3f}' for e in self._stats.loc[:,i]], padding=3, color='black', fontsize=8) 
            # Remove the spines
            ax.spines[['top','left','bottom']].set_visible(False)
            # Make the left spine thicker
            ax.spines['right'].set_linewidth(1.1)
            ax.set_title(i, pad=15)
            # Adjust the margins around the plot area
            plt.subplots_adjust(left=None,
                                bottom=0.2,
                                right=None,
                                top=0.85,
                                wspace=None,
                                hspace=None)
            # Set a white background
            ax.patch.set_facecolor('white')
        plt.show()
    
    def markowitz(self, risk_ret, value):
        rets = []
        vols = []
        opt_weight = []
        opt_par = float()
        for i in range(5000):
            weights = np.random.random(len(self.tab))
            weights /= np.sum(weights)
            rets.append(np.sum(self._datos_returns.mean()*weights)*self.semana)
            vols.append(np.sqrt(np.dot(weights.T, np.dot(self._datos_returns.cov()*self.semana, weights))))
            if risk_ret == 'Risk':
                if i == 0:
                    opt_par = rets[i]
                    opt_weight = weights
                if rets[-1] > opt_par and (0.99*value < vols[-1] < 1.01*value):
                    opt_weight = weights
                    opt_par = rets[-1]
            if risk_ret == 'Return':
                if i == 0:
                    opt_par = vols[i]
                    opt_weight = weights
                if vols[-1] < opt_par and (0.99*value < rets[-1] < 1.01*value):
                    opt_weight = weights
                    opt_par = vols[-1]
        rets = np.array(rets)
        vols = np.array(vols)
        plt.scatter(vols,
                    rets,
                    c = rets/vols,
                    marker = 'o',
                    cmap='coolwarm')
        plt.grid(True)
        plt.xlabel('expected volatility')
        plt.ylabel('expected return')
        plt.colorbar(label = 'Sharpe Ratio')
        plt.title('Monte Carlo Simulation Efficient Frontier')
        plt.figtext(0.15, 0.75,
                    'The optimal portfolio is \n {weights} \n with volatility {vol} \n and return {ret}'.format(
                    weights = opt_weight,
                    vol = np.sqrt(np.dot(opt_weight.T, np.dot(self._datos_returns.cov()*self.semana, opt_weight))),
                    ret = np.sum(self._datos_returns.mean()*opt_weight)*self.semana))
        plt.show()
    
    def risk_adj_sharpe(self):
        rets = []
        vols = []
        opt_weight = []
        opt_sharpe = float()
        for i in range(5000):
            weights = np.random.random(len(self.tab))
            weights /= np.sum(weights)
            rets.append(np.sum(self._datos_returns.mean()*weights)*self.semana)
            vols.append(np.sqrt(np.dot(weights.T, np.dot(self._datos_returns.cov()*self.semana, weights))))
            if i == 0:
                opt_sharpe = rets[-1]/vols[-1]
                opt_weight = weights 
            if opt_sharpe < rets[-1]/vols[-1]:
                opt_sharpe = rets[-1]/vols[-1]
                opt_weight = weights
        rets = np.array(rets)
        vols = np.array(vols)
        plt.scatter(vols,
                    rets,
                    c = rets/vols,
                    marker = 'o',
                    cmap='coolwarm')
        plt.grid(True)
        plt.xlabel('expected volatility')
        plt.ylabel('expected return')
        plt.colorbar(label = 'Sharpe Ratio')
        plt.title('Monte Carlo Simulation Efficient Frontier')
        plt.figtext(0.15, 0.75,
                    'The optimal portfolio is \n {weights} \n with volatility \n {vol}, \n return \n {ret}, \n and sharpe ratio of {sharpe}'.format(
                    weights = opt_weight,
                    vol = np.sqrt(np.dot(opt_weight.T, np.dot(self._datos_returns.cov()*self.semana, opt_weight))),
                    ret = np.sum(self._datos_returns.mean()*opt_weight)*self.semana,
                    sharpe = opt_sharpe))
        plt.show()
    
    def risk_parity(self):
        def _risk_budget_objective_error(weights, args):
            # The covariance matrix occupies the first position in the variable
            covariances = args[0]
            # The desired contribution of each asset to the portfolio risk occupies the
            # second position
            assets_risk_budget = args[1]
            # We convert the weights to a matrix
            weights = np.matrix(weights)
            # We calculate the risk of the weights distribution
            portfolio_risk = _allocation_risk(weights, covariances)
            # We calculate the contribution of each asset to the risk of the weights
            # distribution
            assets_risk_contribution = \
                _assets_risk_contribution_to_allocation_risk(weights, covariances)
            # We calculate the desired contribution of each asset to the risk of the
            # weights distribution
            assets_risk_target = \
                np.asmatrix(np.multiply(portfolio_risk, assets_risk_budget))
            # Error between the desired contribution and the calculated contribution of
            # each asset
            error = \
                sum(np.square(assets_risk_contribution - assets_risk_target.T))
            # It returns the calculated error
            return error
        def _allocation_risk(weights, covariances):
            # We calculate the risk of the weights distribution
            portfolio_risk = np.sqrt(np.dot(weights, np.dot(covariances, weights.T)))[0,0]
            # It returns the risk of the weights distribution
            return portfolio_risk
        def _assets_risk_contribution_to_allocation_risk(weights, covariances):
            # We calculate the risk of the weights distribution
            portfolio_risk = _allocation_risk(weights, covariances)
            # We calculate the contribution of each asset to the risk of the weights
            # distribution
            assets_risk_contribution = np.multiply(weights.T, np.dot(covariances, weights.T)) \
                / portfolio_risk
            # It returns the contribution of each asset to the risk of the weights
            # distribution
            return assets_risk_contribution
        def _get_risk_parity_weights(covariances, assets_risk_budget, initial_weights):
            # Restrictions to consider in the optimisation: only long positions whose
            # sum equals 100%
            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0},
                        {'type': 'ineq', 'fun': lambda x: x})
            # Optimisation process in scipy
            optimize_result = minimize(fun=_risk_budget_objective_error,
                                    x0=initial_weights,
                                    args=[covariances, assets_risk_budget],
                                    method='SLSQP',
                                    constraints=constraints,
                                    tol=1e-10,
                                    options={'disp': False})
            # Recover the weights from the optimised object
            weights = optimize_result.x
            # It returns the optimised weights
            return weights
        cov = self._datos_returns.cov()*self.semana
        assets_risk_budget = [1/self._datos.shape[1]]*self._datos.shape[1]
        init_weights = [1/self._datos.shape[1]]*self._datos.shape[1]
        # Optimisation process of weights
        weights = \
            _get_risk_parity_weights(cov, assets_risk_budget, init_weights)
        # Convert the weights to a pandas Series
        weights = pd.Series(weights, index=self._datos_returns.columns, name='weight')
        fig5 =plt.figure(figsize=(10,8))
        ax = plt.axes([0.1, 0.1, 0.8, 0.8])
        labels = list(self._datos.columns)
        explode = [0 + i/20 for i, col in enumerate(self._datos.columns)]
        plt.pie(weights,
                explode = explode,
                labels= labels,
                autopct= '%1.1f%%',
                startangle = 90,
                shadow=True)
        plt.title('Risk Parity Optimization',fontsize =14)
        plt.show()
    
    def black_litterman(self):
        weights = pd.Series(pypfopt.hierarchical_portfolio.HRPOpt(returns=self._datos_returns).optimize(),
                           index=self._datos_returns.columns,
                           name='weight')
        fig5 =plt.figure(figsize=(10,8))
        ax = plt.axes([0.1, 0.1, 0.8, 0.8])
        labels = list(self._datos.columns)
        explode = [0 + i/20 for i, col in enumerate(self._datos.columns)]
        plt.pie(weights,
                explode = explode,
                labels= labels,
                autopct= '%1.1f%%',
                startangle = 90,
                shadow=True)
        plt.title('Hierarchical Risk Parity Optimization',fontsize =14)
        plt.show()
        
    @abstractmethod
    def relative_performance(self) -> None:
        pass
        
    @abstractmethod
    def calculate_stats(self):
        pass
        
    @abstractmethod
    def compare(self) -> None:
        pass
    
    @abstractmethod
    def graph(self) -> None:
        pass
    
    @abstractmethod
    def dispersion(self) -> None:
        pass