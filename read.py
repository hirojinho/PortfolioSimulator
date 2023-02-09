import pandas as pd
from tkinter import filedialog, messagebox
from individuals import Individuals
from allocation import portfolio
from state import State

class Context:
    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state):
        self._state = state
        self._state.context = self

class Reader:
    datos = None
    _per = None
    _comp = None
    # def __init__(self):
    #     self.datos = pd.read_excel('MasterAllocation.xlsx',sheet_name='Summary',index_col='Date')
        
    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Excel",
                                                            "*.xlsx*"),
                                                        ("all files",
                                                            "*.*")))
        # Change label contents
        if filename:
            filename = r"{}".format(filename)
            self.datos = pd.read_excel(filename,sheet_name='Summary',index_col='Date')
        self.context = Context(portfolio(self.datos, self._per))
        return filename
    
    def individual_graph(self):
        self.context.transition_to(Individuals(self.datos))
        self.context._state.graph()
    
    def individual_rel(self):
        self.context.transition_to(Individuals(self.datos))
        self.context._state.relative_performance()
        
    def individual_dis(self):
        self.context.transition_to(Individuals(self.datos))
        self.context._state.dispersion()
        
    def individual_comp(self):
        self.context.transition_to(Individuals(self.datos))
        self.context._state.calculate_stats()
        self.context._state.compare(self._comp[0], self._comp[1])
        
    def individual_stats(self):
        self.context.transition_to(Individuals(self.datos))
        self.context._state.stats()
        
    def allocation_graph(self):
        self.context.transition_to(portfolio(self.datos, self._per))
        self.context._state.graph()
        
    def allocation_dis(self):
        self.context.transition_to(portfolio(self.datos, self._per))
        self.context._state.dispersion()
        
    def allocation_comp(self, is_rebalancing, months=1, time_measure=1): 
        # time_measure is the space of time between one line of the sheet from another (time_measure=7 means weekly update)
        self.context.transition_to(portfolio(self.datos, self._per))
        if is_rebalancing:
            self.context._state.reb_compare(months=months, time_measure=time_measure)
        else:
            self.context._state.compare()
    
    def allocation_stats(self):
        self.context.transition_to(portfolio(self.datos, self._per))
        self.context._state.stats()
        
    def markowitz(self, gv):
        try:
            self.context._state.markowitz(gv._optimization_par.get(), float(gv._optimization_npar.get()))
        except ValueError:
            messagebox.showerror('Error in input',
                                "Please choose target risk or return")
    
    def risk_adjusted(self):
        self.context._state.risk_adj_sharpe()
        
    def risk_parity(self):
        self.context._state.risk_parity()
        
    def black_litterman(self):
        self.context._state.black_litterman()