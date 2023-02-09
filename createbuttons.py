from tkinter import *
import customtkinter
from sys import exit

class Create_buttons():
    inputs = []
    
    def initial_page(self, mainframe, gv):
        self.label_file_explorer = customtkinter.CTkLabel(mainframe,
                            text = "Portfolio Simulator",
                            font=customtkinter.CTkFont(size=30, weight="bold"))
        self.button_explore = customtkinter.CTkButton(mainframe,
                                text = "Browse Files",
                                command = gv.explore_button)
        self.button_exit = customtkinter.CTkButton(mainframe,
                                text = "Exit",
                                command = exit)
        self.label_file_explorer.grid(column = 1, row = 1)
        self.button_explore.grid(column = 1, row = 2)
        self.button_exit.grid(column = 1,row = 3)
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.columnconfigure(2, weight=1)
        mainframe.rowconfigure(1, weight=1)
        mainframe.rowconfigure(2, weight=1)
        mainframe.rowconfigure(3, weight=1)
        
    def update_buttons(self, gv):
        self.label_file_explorer['text'] = gv._reader.browseFiles() + ' selected'
        self.button_explore.configure(state="disabled")
        
    def explore_buttons(self, per_frame, gv, reg):
        def set_inputs():  
            for i in self.inputs:
                i.destroy()
            self.inputs = []
            if gv._optimization_type.get() == 'Markowitz':
                self.inputs.append(customtkinter.CTkLabel(optimization_type_frame2,
                    text='Markowitz Parameters'))
                self.inputs.append(customtkinter.CTkRadioButton(optimization_type_frame2,
                    text='Give Risk',
                    variable=gv._optimization_par,
                    value='Risk'))
                self.inputs.append(customtkinter.CTkRadioButton(optimization_type_frame2,
                    text='Give Return',
                    variable=gv._optimization_par,
                    value='Return'))
                self.inputs.append(customtkinter.CTkEntry(optimization_type_frame2,
                                             textvariable=gv._optimization_npar,
                                             width=120))
                self.inputs[0].grid(row=1, column=0)
                for i in range(1, 4):
                    self.inputs[i].grid(row=2, column=i-1)
        # create frames
        weights_frame0 = customtkinter.CTkFrame(per_frame, fg_color='orange')
        weights_frame1 = customtkinter.CTkFrame(weights_frame0, fg_color='orange')
        optimization_type_frame0 = customtkinter.CTkFrame(per_frame, fg_color='#67ADFF')
        optimization_type_frame1 = customtkinter.CTkFrame(optimization_type_frame0, fg_color='orange')
        optimization_type_frame2 = customtkinter.CTkFrame(optimization_type_frame1, fg_color='orange')
        # create button to start calculations
        self.button_start = customtkinter.CTkButton(weights_frame0,
                                text='Go',
                                command = gv.go_button)
        self.button_start.grid(column = 0,row = 2)
        # enumerate to each asset/portfolio (verbose? yeah, but whatever)
        for n, i in enumerate(gv._reader.datos.columns): 
            # the text box to input percentages
            gv.str_var[0].append(StringVar())
            gv.str_var[0][n].trace('w', gv.limit_size)
            gv.str_var[1].append(StringVar())
            gv.str_var[1][n].trace('w', gv.limit_size)
            gv.text[0].append(customtkinter.CTkEntry(weights_frame1,
                                width=45,
                                textvariable=gv.str_var[0][n]))
            gv.text[1].append(customtkinter.CTkEntry(weights_frame1,
                                width=45,
                                textvariable=gv.str_var[1][n]))
            gv.text[0][n].grid(column = 1+n, row = 1)
            gv.text[1][n].grid(column = 1+n, row = 2)
            gv.text[0][n].configure(validate="key", validatecommand=(reg, '%P'))
            gv.text[1][n].configure(validate="key", validatecommand=(reg, '%P'))
            # the check buttons to decide which two assets to compare
            gv._to_compare_bool.append(BooleanVar())
            gv.assets.append(customtkinter.CTkCheckBox(weights_frame1,
                                        text=i,
                                        variable=gv._to_compare_bool[n],
                                        onvalue=True,
                                        offvalue=False))
            gv.assets[n].grid(column = 1+n, row = 0, sticky=S)
            weights_frame1.columnconfigure(1+n, weight=1)
        port1=customtkinter.CTkLabel(weights_frame1, text='Portfolio 1')
        port2=customtkinter.CTkLabel(weights_frame1, text='Portfolio 2')
        port1.grid(column = 0, row = 1)
        port2.grid(column = 0, row = 2)
        # button to offer markowitz optimization
        self.mark_option = customtkinter.CTkRadioButton(optimization_type_frame2,
                                    text='Markowitz',
                                    variable=gv._optimization_type,
                                    value='Markowitz',
                                    command = set_inputs)
        self.mark_option.grid(row = 0,
                            column = 0)
        # button to offer risk adjusted optimization
        self.risk_adj_option = customtkinter.CTkRadioButton(optimization_type_frame2,
                                    text='Risk Adjusted',
                                    variable=gv._optimization_type,
                                    value='Risk Adjusted',
                                    command = set_inputs)
        self.risk_adj_option.grid(row = 0,
                            column = 1)
        # button to offer risk parity optimization
        self.risk_parity = customtkinter.CTkRadioButton(optimization_type_frame2,
                                    text='Risk Parity',
                                    variable=gv._optimization_type,
                                    value='Risk Parity',
                                    command = set_inputs)
        self.risk_parity.grid(row = 0,
                            column = 2)
        # button to offer black-litterman optimization
        self.black_litterman = customtkinter.CTkRadioButton(optimization_type_frame2,
                                    text='Hierarchical Risk',
                                    variable=gv._optimization_type,
                                    value='Hierarchical Risk',
                                    command = set_inputs)
        self.black_litterman.grid(row = 0,
                            column = 3)
        # button to start the optimization
        self.optimize_button = customtkinter.CTkButton(optimization_type_frame1,
                                    text='Optimize',
                                    command = gv.optimization)
        self.optimize_button.grid(row = 2,
                            column = 0)
        # titles
        title_weights = customtkinter.CTkLabel(weights_frame0,
                                                text='Assign weights to each asset',
                                                font=customtkinter.CTkFont(size=30, weight="bold"))
        title_optimize = customtkinter.CTkLabel(optimization_type_frame1,
                                                text='Choose one optimization',
                                                font=customtkinter.CTkFont(size=30, weight="bold"))
        title_weights.grid(row=0, column=0)
        title_optimize.grid(row=0, column=0)
        # grid all the frames
        weights_frame0.grid(column=0, row=0)
        weights_frame1.grid(column=0, row=1)
        optimization_type_frame0.grid(column=0, row=1)
        optimization_type_frame1.grid(column=1, row=0)
        optimization_type_frame2.grid(column=0, row=1)
        # configure rows and columns
        # nb
        per_frame.columnconfigure(0, weight=1)
        per_frame.rowconfigure(0, weight=1)
        per_frame.rowconfigure(1, weight=1)
        # weights_frame0
        weights_frame0.columnconfigure(0, weight=1)
        weights_frame0.rowconfigure(0, weight=1)
        # weights_frame1 is configured in the loop
        # opt_frame0
        weights_frame0.columnconfigure(0, weight=1)
        weights_frame0.columnconfigure(1, weight=1)
        weights_frame0.columnconfigure(2, weight=1)
        weights_frame0.rowconfigure(0, weight=1)
        # opt_frame1
        weights_frame0.columnconfigure(0, weight=1)
        weights_frame0.rowconfigure(0, weight=1)
        for child in optimization_type_frame1.winfo_children():
            child.grid_configure(padx=10, pady=10)
        for child in weights_frame0.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def options_to_plot(self, opt_frame, gv):
        def activate_time():
            if gv._reb_bool.get():
                self.time_text.configure(state='normal')
                self.time_day.configure(state='normal')
                self.time_week.configure(state='normal')
                self.time_months.configure(state='normal')
            else:
                self.time_text.configure(state='disabled')
                self.time_day.configure(state='disabled')
                self.time_week.configure(state='disabled')
                self.time_months.configure(state='disabled')     
        def choose_rebalancing():
            if gv._reb_bool.get():
                gv._reader.allocation_comp(gv._reb_bool.get(),
                                        months=gv.months.get(),
                                        time_measure=gv._time_frame.get())
            else:
                gv._reader.allocation_comp(gv._reb_bool.get())
        # create frames
        bt_frame0 = customtkinter.CTkFrame(opt_frame, fg_color="#67ADFF")
        bt_frame1 = customtkinter.CTkFrame(bt_frame0, fg_color="orange")
        bt_frame2 = customtkinter.CTkFrame(bt_frame0, fg_color="orange")
        reb_frame0 = customtkinter.CTkFrame(opt_frame, fg_color="orange")
        bt_frame0.configure(width=400)
        bt_frame1.configure(width=400)
        bt_frame2.configure(width=400)
        reb_frame0.configure(width=400)
        # plot individual performance
        self.button_in_graph = customtkinter.CTkButton(bt_frame1,
                                            text='Plot individual performance',
                                            command = gv._reader.individual_graph)
        # relative performance
        self.button_in_rel = customtkinter.CTkButton(bt_frame1,
                                text='Individual relative',
                                command = gv._reader.individual_rel)
        # dispersion individual
        self.button_in_dis = customtkinter.CTkButton(bt_frame1,
                                text='Individual dispersion',
                                command = gv._reader.individual_dis)
        # individual comparison
        self.button_in_comp = customtkinter.CTkButton(bt_frame1,
                                text='Individual comparison',
                                command = gv._reader.individual_comp)
        # individual comparison
        self.button_in_stats = customtkinter.CTkButton(bt_frame1,
                                text='Individual statistics',
                                command = gv._reader.individual_stats)
        # allocation percentages
        self.button_allo_graph = customtkinter.CTkButton(bt_frame2,
                                text='Portfolio graph',
                                command = gv._reader.allocation_graph)
        # portfolio dispersion
        self.button_allo_dis = customtkinter.CTkButton(bt_frame2,
                                text='Portfolio dispersion',
                                command = gv._reader.allocation_dis)
        # portfolio performance
        self.button_allo_comp = customtkinter.CTkButton(bt_frame2,
                                text='Portfolio comparison',
                                command = choose_rebalancing)
        #portfolio stats
        self.button_allo_stats = customtkinter.CTkButton(bt_frame2,
                                text='Portfolio statistics',
                                command = gv._reader.allocation_stats)
        title_in = customtkinter.CTkLabel(bt_frame1,
                                                text='Plot individuals stats',
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        title_allo = customtkinter.CTkLabel(bt_frame2,
                                                text='Plot portfolio stats',
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        # grid for individuals
        title_in.grid(column=0, row=0)
        self.button_in_graph.grid(column=0, row=1)
        self.button_in_rel.grid(column=0, row=2)
        self.button_in_dis.grid(column=0, row=3)
        self.button_in_comp.grid(column=0, row=4)
        self.button_in_stats.grid(column=0, row=5)
        # grid for portfolios
        title_allo.grid(row=0, column=0)
        self.button_allo_graph.grid(column=0, row=1)
        self.button_allo_dis.grid(column=0, row=2)
        self.button_allo_comp.grid(column=0, row=3)
        self.button_allo_stats.grid(column=0, row=4)
        distribution = customtkinter.CTkLabel(reb_frame0,
                    text = str(gv.allocation),
                    width = 100)
        # rebalancing button
        check_reb = customtkinter.CTkCheckBox(reb_frame0,
                                    text = 'Rebalancing',
                                    variable=gv._reb_bool,
                                    onvalue=True,
                                    offvalue=False,
                                    command=activate_time)
        title_months_reb = customtkinter.CTkLabel(reb_frame0,
                                                text='Months to rebalance',
                                                font=customtkinter.CTkFont(size=18, weight="bold"))
        self.time_text = customtkinter.CTkEntry(reb_frame0,
                width=45,
                textvariable=gv.months,
                placeholder_text = "Months")
        title_span_reb = customtkinter.CTkLabel(reb_frame0,
                                                text='Interval between lines',
                                                font=customtkinter.CTkFont(size=12, weight="bold"))
        self.time_day = customtkinter.CTkRadioButton(reb_frame0,
                                    text='Days',
                                    variable=gv._time_frame,
                                    value=1)
        self.time_week = customtkinter.CTkRadioButton(reb_frame0,
                                    text='Weeks',
                                    variable=gv._time_frame,
                                    value=7)
        self.time_months = customtkinter.CTkRadioButton(reb_frame0,
                                    text='Months',
                                    variable=gv._time_frame,
                                    value=30)
        # grid for rebalancing
        check_reb.grid(column=0, row=0, sticky=W)
        title_months_reb.grid(column=0, row=1, sticky=W)
        self.time_text.grid(column=0, row=2, sticky=W)
        title_span_reb.grid(column=0, row=3, sticky=W)
        self.time_day.grid(column=0, row=4, sticky=W)
        self.time_week.grid(column=0, row=5, sticky=W)
        self.time_months.grid(column=0, row=6, sticky=W)
        distribution.grid(column=0, row=7, sticky=W)
        # grid the frames
        bt_frame0.grid(row=0, column=0, sticky='ns')
        bt_frame1.grid(row=0, column=0, sticky='ns')
        bt_frame2.grid(row=0, column=1, sticky='ns')
        reb_frame0.grid(row=0, column=1, sticky='ns')
        # configure frames
        # nb
        opt_frame.columnconfigure(0, weight=1)
        opt_frame.columnconfigure(1, weight=1)
        opt_frame.rowconfigure(0, weight=1)
        # bt_frame0
        bt_frame0.columnconfigure(0, weight=1)
        bt_frame0.columnconfigure(1, weight=1)
        bt_frame0.rowconfigure(0, weight=1)
        # bt_frame1
        bt_frame1.rowconfigure(0, weight=1)
        bt_frame1.rowconfigure(1, weight=1)
        bt_frame1.rowconfigure(2, weight=1)
        bt_frame1.rowconfigure(3, weight=1)
        bt_frame1.rowconfigure(4, weight=1)
        bt_frame1.rowconfigure(5, weight=1)
        # bt_frame2
        bt_frame2.rowconfigure(0, weight=1)
        bt_frame2.rowconfigure(1, weight=1)
        bt_frame2.rowconfigure(2, weight=1)
        bt_frame2.rowconfigure(3, weight=1)
        bt_frame2.rowconfigure(4, weight=1)
        self.time_day.configure(state='disabled')
        self.time_week.configure(state='disabled')
        self.time_months.configure(state='disabled')
        self.time_text.configure(state='disabled')
        # reb_frame0
        reb_frame0.rowconfigure(0, weight=1)
        reb_frame0.rowconfigure(1, weight=1)
        reb_frame0.rowconfigure(2, weight=1)
        reb_frame0.rowconfigure(3, weight=1)
        reb_frame0.rowconfigure(4, weight=1)
        reb_frame0.rowconfigure(5, weight=1)
        reb_frame0.rowconfigure(6, weight=1)
        reb_frame0.rowconfigure(7, weight=1)
        # add padding
        for child in bt_frame1.winfo_children():
            child.grid_configure(padx=10, pady=10)
        for child in bt_frame2.winfo_children():
            child.grid_configure(padx=10, pady=10)
        for child in reb_frame0.winfo_children():
            child.grid_configure(padx=10, pady=10)