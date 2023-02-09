from read import Reader
from tkinter import *
from tkinter import messagebox
from createbuttons import Create_buttons
import customtkinter

class Events():
    def __init__(self):
        self.root = customtkinter.CTk(fg_color="white")
        self.root.geometry(f"{825}x{435}")
        self.root.resizable(False, False)
        customtkinter.set_appearance_mode("Light")
        self.assets = []
        self.compare = []
        self._to_compare_bool = []
        self.text = [[],[]]
        self.str_var =[[],[]] # used to trace each textbox entry and limit its character size
        self.allocation = [[],[]]
        self._reader = Reader()
        self.months = IntVar()
        self._time_frame = IntVar()
        self._reb_bool = BooleanVar()
        self._optimization_par = StringVar()
        self._optimization_type = StringVar()
        self._optimization_npar = StringVar()
        self._button_creator = Create_buttons()
        self.nb = customtkinter.CTkTabview(self.root, fg_color='#67ADFF')
        self.reg = self.root.register(self.callback_validation)
        # now let's configure
        self.root.title("Choose a file")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.nb.grid(column=0, row=0, sticky=(N, W, E, S))
        self.nb.add('Start Page')
        self._button_creator.initial_page(self.nb.tab("Start Page"), self)
    
    def callback_validation(self, input):
        try:
            if float(input) <= 1:
                return True
            else:
                return False
        except ValueError:
            if input == '':
                return True
            elif input == ".":
                return True
            return False
        
    def choose_comparison(self):
        comp = []
        for n, i in enumerate(self._to_compare_bool):
            if i.get():
                comp.append(self._reader.datos.columns[n])
        return comp
            
    def limit_size(self, *args):
        value = [[v.get() for v in i] for i in self.str_var]
        for (i, row) in enumerate(value):
            for (j, col) in enumerate(row):
                self.str_var[i][j].set(value[i][j][:4]) if len(col) > 4 else None
                
    def optimization(self):
        if self._optimization_type.get() == 'Markowitz':
            self._reader.markowitz(self)
        elif self._optimization_type.get() == 'Risk Adjusted':
            self._reader.risk_adjusted()
        elif self._optimization_type.get() == 'Risk Parity':
            self._reader.risk_parity()
        elif self._optimization_type.get() == 'Hierarchical Risk':
            self._reader.black_litterman()
        else:
            messagebox.showerror('Error in selection',
                                "Please select an optimization type")
            
    def explore_button(self):
        try:
            self._button_creator.update_buttons(self)
            self.nb.add("Portfolio Composition")
            self._button_creator.explore_buttons(self.nb.tab("Portfolio Composition"), self, self.reg)
            for child in self.nb.tab("Portfolio Composition").winfo_children():
                child.grid_configure(padx=5, pady=5)
        except AttributeError:
            messagebox.showerror('Error in input',
                                "Please choose a .xlsx file")
            
    def go_button(self):
        try:
            self.allocation = [[],[]]
            for txt, txt1 in zip(self.text[0], self.text[1]):
                self.allocation[0].append(float(txt.get()))
                self.allocation[1].append(float(txt1.get()))
        except ValueError:
            messagebox.showerror('Error in Input',
                                'One of the entries is not a number')
        else:
            if abs(1 - sum(self.allocation[0])) < 10**-3 and abs(1 - sum(self.allocation[1])) < 10**-3:
                self._reader._comp = self.choose_comparison()
                if len(self._reader._comp) == 2:
                    self._reader._per = list(map(list, zip(*self.allocation)))
                    # individual graph button
                    self.nb.add("Plot Assets Graphs")
                    self._button_creator.options_to_plot(self.nb.tab("Plot Assets Graphs"), self)
                else:
                    messagebox.showerror('Error in Input',
                                    'Please, select two assets to compare')
            else:
                print(self.allocation)
                messagebox.showerror('Error in Input',
                                    'The sum of one of the portfolios is not one')
        
if __name__ == "__main__":
    gv = Events()
    gv.root.mainloop()