# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9/7/2020

@author: Alun Brain (Dr. Brain Stats)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import seaborn as sns
import statsmodels.api as sm
#import statsmodels.formula.api as sm
from statsmodels.tools.tools import add_constant
from statsmodels.stats.outliers_influence import variance_inflation_factor

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from tkinter import filedialog

import matplotlib 

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.figure import Figure


Tk().withdraw()


root = tk.Tk()
root.title("Python GUI - General LInear Model")

#900 (width)x 750 (height) is size of box,  +10+10 is position of box onscreen

root.geometry("990x750+30+30")
root.resizable(0, 0)
root.configure(bg='#49A')
#scroll box on top
scr = scrolledtext.ScrolledText(root, width=121, height=20, wrap=tk.WORD)
scr.grid(column=0, columnspan=10)

pd.set_option('display.max_columns', 500)

def getCSV():
    global df1
    
    import_file_path = filedialog.askopenfilename()
    df1 = pd.read_csv (import_file_path)

    combo1['values'] = list(df1)[0:]
    combo1.current(0)

    for i in list(df1)[0:]:
        combo2.insert(tk.END, i)
        
    scr.insert(tk.INSERT, "Data Details : ")
    scr.insert(tk.INSERT, '\n\n')
    scr.insert(tk.INSERT, df1.dtypes)
    scr.insert(tk.INSERT, '\n\n')


def create_window():
    window = tk.Toplevel(root)


def datadets():
    '''
    populate data details
    '''
   
    
    scr.insert(tk.INSERT, "Data Details : ")
    scr.insert(tk.INSERT, '\n\n')
    scr.insert(tk.INSERT, df1.dtypes)
    scr.insert(tk.INSERT, '\n\n')
    
    
def corrAll():
    '''
    Compute Correlation between all variables
    '''
    scr.insert(tk.INSERT, "Correlation between All : ")
    scr.insert(tk.INSERT, '\n\n')
    scr.insert(tk.INSERT, df1.corr())
    scr.insert(tk.INSERT, '\n\n')

def droplotscateg():
    for col in list(df1.select_dtypes(include=['object']).columns):
        if len(df1[col].unique()) >= 10:
            df1.drop(col,inplace=True,axis=1)
      # repopulate boxes            
   
    combo1['values'] = list(df1)[0:]
    combo1.current(0)
    
    combo2.delete(0, tk.END)
    for i in list(df1)[0:]:
        combo2.insert(tk.END, i) 
        

def onehotencoding():
    global df1
    df1 = pd.get_dummies(df1, drop_first=True)
     # repopulate boxes            
   
    combo1['values'] = list(df1)[0:]
    combo1.current(0)
    
    combo2.delete(0, tk.END)
    for i in list(df1)[0:]:
        combo2.insert(tk.END, i)   

def VIFall():
    '''
    VIF
    
    '''
    vifs = pd.Series(np.linalg.inv(df1.corr().values).diagonal(), index=df1.corr().index)
    
    scr.insert(tk.INSERT, "VIF between All : ")
    scr.insert(tk.INSERT, '\n\n')
    scr.insert(tk.INSERT, vifs)
    scr.insert(tk.INSERT, '\n\n')
    
    return vifs

def corr2():
    '''
    Compute Correlation between two variables
    '''
    val1 = combo1.get()
    values = [combo2.get(idx) for idx in combo2.curselection()]
    val2 = '+'.join(values)
    if(len(combo2.curselection()) == 1):
        scr.insert(tk.INSERT, "Correlation between " + val1 + " and " + val2 +
                   " : ")
        scr.insert(tk.INSERT, '\n\n')
        scr.insert(tk.INSERT, np.corrcoef(df1[val1], df1[val2]))
        scr.insert(tk.INSERT, '\n\n')
    else:
        scr.insert(tk.INSERT, 'Alert!, select only one Independent Variable')
        scr.insert(tk.INSERT, '\n\n')


def corr3():
    '''
    remove all correlated variables and repopulate boxes
    '''
    col_corr = set() # Set of all the names of deleted columns
    corr_matrix = df1.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (abs(corr_matrix.iloc[i, j]) >= 0.8)  and (corr_matrix.columns[j] not in col_corr):
                colname = corr_matrix.columns[i] # getting the name of column
                col_corr.add(colname)
                if colname in df1.columns:
                    del df1[colname] # deleting the column from the dataset
     # repopulate boxes            
   
    combo1['values'] = list(df1)[0:]
    combo1.current(0)
    
    combo2.delete(0, tk.END)
    for i in list(df1)[0:]:
        combo2.insert(tk.END, i)               

#    print(dataset)


    
#listbox.insert(END, newitem)
#result = sm.ols(formula="A ~ B + C", data=df).fit()
    
def RegAna():
    '''
    Compute Multiple Regression Model
    User select one Depedended Varaible and one or more Independent Variable(s)
    '''
    val1 = combo1.get()
    dep_var = val1.split(" ")
    values = [combo2.get(idx) for idx in combo2.curselection()]
    val2 = ','.join(values)
    ind_var = val2.split(",")
    if(val2 != ""):
        scr.insert(tk.INSERT, "Regression between " + val1 + " ~ " + val2 +
                   " : ")
        scr.insert(tk.INSERT, '\n\n')
      #  result = sm.OLS(df1[dep_var], add_constant(df1[ind_var])).fit()
       
        result = sm.OLS(df1[dep_var], df1[ind_var].assign(Intercept=1)).fit()
    #X = weekly[predictors].assign(Intercept=1)
        scr.insert(tk.INSERT, result.summary())
        scr.insert(tk.INSERT, '\n\n')
    else:
        scr.insert(tk.INSERT, 'Alert!, Select Independent Variable(s)')
        scr.insert(tk.INSERT, '\n\n')


def resPlot():
    '''
    Draw Residual Plot
    '''
    val1 = combo1.get()
    dep_var = val1.split(" ")
    values = [combo2.get(idx) for idx in combo2.curselection()]
    val2 = ','.join(values)
    ind_var = val2.split(",")
    if(val2 != ""):
        scr.insert(tk.INSERT, '\n\n')
        result = sm.OLS(df1[dep_var], df1[ind_var].assign(Intercept=1)).fit()
        pred_val = result.fittedvalues.copy()
        true_val = df1[val1]
        residual = true_val - pred_val
        fig, ax = plt.subplots(1, 1)
        ax.scatter(pred_val, residual)
        plt.title("Residual Plot - Residual V/S Fitted")
       
        plt.show()
        scr.insert(tk.INSERT, '\n\n')
    else:
        scr.insert(tk.INSERT, 'Alert!, Select Independent Variable(s)')
        scr.insert(tk.INSERT, '\n\n')


def probPlot():
    '''
    Draw Probability Plot
    '''
    val1 = combo1.get()
    dep_var = val1.split(" ")
    values = [combo2.get(idx) for idx in combo2.curselection()]
    val2 = ','.join(values)
    ind_var = val2.split(",")
    if(val2 != ""):
        scr.insert(tk.INSERT, '\n\n')
       # result = sm.OLS(df1[dep_var], add_constant(df1[ind_var])).fit()
        result = sm.OLS(df1[dep_var], df1[ind_var].assign(Intercept=1)).fit()
        pred_val = result.fittedvalues.copy()
        true_val = df1[val1]
        residual = true_val - pred_val
        fig, ax = plt.subplots(1, 1)
        stats.probplot(residual, plot=ax, fit=True)
        plt.title("Probability Plot")
        plt.show()
        scr.insert(tk.INSERT, '\n\n')
    else:
        scr.insert(tk.INSERT, 'Alert!, Select Independent Variable(s)')
        scr.insert(tk.INSERT, '\n\n')


def scatterPlot():
    '''
    Draw Scatter Plot
    '''
    val1 = combo1.get()
    dep_var = val1.split(" ")
    values = [combo2.get(idx) for idx in combo2.curselection()]
    val2 = ','.join(values)
    ind_var = val2.split(",")
    if(len(combo2.curselection()) > 0 and len(combo2.curselection()) < 5):
        scr.insert(tk.INSERT, '\n\n')
        sns.pairplot(df1, x_vars=ind_var, y_vars=dep_var, height=7, aspect=0.7,
                     kind='reg')
        plt.show()
        scr.insert(tk.INSERT, '\n\n')
    else:
        scr.insert(tk.INSERT, 'Alert!, Maximum Three Independent Variables')
        scr.insert(tk.INSERT, '\n\n')

# import data

browseButton_CSV = ttk.Button(root, text="  -----  Import CSV File  ----    ", command=getCSV)
browseButton_CSV.grid(row=1, column=1,  pady=10)


datadetsx = ttk.Button(root, text="  -Data Details    ", command=datadets)
datadetsx.grid(row=1, column=4,  pady=10)

# Combo Box - 1
lbl_sel1 = ttk.Label(root, text="Select Target Variable").grid(row=2, column=0)
ch1 = tk.StringVar()
combo1 = ttk.Combobox(root, width=12, textvariable=ch1)
combo1.grid(row=2, column=1)


# Combo Box - 2

lbl_sel2 = ttk.Label(root, text="Select Independend Variable").grid(row=2, column=2, padx=(10))
ch2 = tk.StringVar()

#frame = Frame(root)

frame = Frame(root)
frame.grid(column=3, row=2)

combo2 = Listbox(frame, width=20, height=6, selectmode=tk.MULTIPLE)
combo2.grid(column=4, row=2, sticky='w')

scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=combo2.yview)
#ns makes it fill the side of the frame
scrollbar.grid(column=5, row=2, sticky='ns')

combo2.config(yscrollcommand=scrollbar.set)



reg_btn = ttk.Button(root, text="  REGRESSION  ", command=RegAna)
reg_btn.grid(row=2, column=5, pady=10)

corr2_btn = ttk.Button(root, text="Correlation between Two", command=corr2)
corr2_btn.grid(row=7, column=0)


corrAll_btn = ttk.Button(root, text="Correlation Between All", command=corrAll)
corrAll_btn.grid(row=7, column=1)

VIF_btn = ttk.Button(root, text="VIF", command=VIFall)
VIF_btn.grid(row=7, column=2)



corr3_btn = ttk.Button(root, text="Remove Correlated Vars", command=corr3)
corr3_btn.grid(row=9, column=1, pady=20)

drop_btn = ttk.Button(root, text="Drop it like it's hot", command=droplotscateg)
drop_btn.grid(row=9, column=2, pady=20)


onehot_btn = ttk.Button(root, text="One Hot Encoding", command=onehotencoding)
onehot_btn.grid(row=9, column=3, pady=20)



scatter_btn = ttk.Button(root, text="Scatter Plot (Max. 4 Pairs)",
                         command=scatterPlot)
scatter_btn.grid(row=10, column=2, pady=10)

resPlot_btn = ttk.Button(root, text="Residual Plots",
                         command=resPlot)
resPlot_btn.grid(row=10, column=3, pady=10)

probPlot_btn = ttk.Button(root, text="Probability Plot", command=probPlot)
probPlot_btn.grid(row=10, column=5, pady=10)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


exit_btn = ttk.Button(root, text="Exit", command=_quit)
exit_btn.grid(row=12, column=5, padx=10, pady=30)

root.mainloop()

