# -*- coding: utf-8 -*-
"""
@author  gmking

This module is used to calculate the allocations and chains.
"""
from .Read_General import count_allo

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import curve_fit

 
def Allo_plot(name, compo, x_pos = 0, y_pos = 0, FORMAT = 'png', Path = ''):
    '''draw FRD plot of blocks and components

    ---Input
    1. name: str
        "XXX" (your file name without filename extension)

    2. compo: pd.daframe
        output of function info() or N_gram_info() in count.py
        you should get them from
        big, compo, block, longest = info(filename, encode)

    ---Parameters
    1. x_pos, y_pos : float
        (x_position, y_position) of your formula on FRD plot

    2. FORMAT: string
        The format of your plot. Most backends support png, pdf, ps, eps and svg. 
        else: just show plot instead of saving.
    
    3. Path: file path for saving picture
        Default: save at current document
        if Path == np.nan, no figure will be saved (just show it)
        else, the figure will be saved according to Path
    
    ---Output
        figure of allocation distribution
    
    ---Return
        Allo_fit: tuple (A, B), (str, str)
            fitting parameters of Allo(y') = (-A ln y' + B)^2
            They are saved as string to present significant figures
    '''
    Compo = compo.sort_values(by = '#allocations', ascending=False)
    reCompo = Compo.reset_index()

    #use OLS to get the fitting parameter
    #-----------------------------------------
    def allo(y, a, b):
        return (a * np.log(y) + b) ** 2

    popt, pcov = curve_fit(allo, compo['compoRank'], reCompo['#allocations'])
    #popt is the optimal values for the parameters (a,b)
    theo = allo(compo['compoRank'], *popt)
    fig, ax = plt.subplots()
    plt.plot(compo['compoRank'], theo, 'g--')
    plt.plot(reCompo['#allocations'], 'ro', label = 'compo', markersize = 4)
    
    #the following code deal with significant figures of fitting parameters
    #the tutor of significant figures: https://www.usna.edu/ChemDept/_files/documents/manual/apdxB.pdf
    #-----------------------------------------
    allo_dig = len(str(max(reCompo['#allocations'])))
    yp_dig = len(str(max(compo['compoRank']))) #ln(y) will have dig(y) +1 digits (dig(y) significant figures)
    a_dig = min(allo_dig, yp_dig +1) #significant figures of parameter a
    b_dig = a_dig #significant figures of parameter b
    
    # the fomat string is #.?g, where ? = significant figures
    # detail of the fomat string: https://bugs.python.org/issue32790
    # https://docs.python.org/3/tutorial/floatingpoint.html
    A = format(abs(popt[0]), '#.%dg' % a_dig)  # give a_dig significant digits
    B = format(popt[1], '#.%dg' % b_dig)  # give b_dig significant digits
    if 'e' in A: #make scientific notation more beautiful
        A_text = A.split('e')[0] + '\\times 10^{' + str(int(A.split('e')[1])) + '}'
    elif A[-1] == '.':
        A_text = A[:-1]
    else:
        A_text = A
    if 'e' in B: #make scientific notation more beautiful
        B_text = B.split('e')[0] + '\\times 10^{' + str(int(B.split('e')[1])) + '}'
    elif B[-1] == '.':
        B_text = B[:-1]
    else:
        B_text = B
        
    #a perfect solution to text wrap!!
    #https://stackoverflow.com/questions/2660319/putting-newline-in-matplotlib-label-with-tex-in-python
    parameters = (r"$\alpha=%s$"
                  "\n"
                 r"$\beta=%s$") % (A_text, B_text)    
    
    a = 1.5  #auto positioning for m = min(compo['compoRank']) = 1 always
    b = 2   #auto positioning for M = max(compo['compoRank'])
    xmid = max(compo['compoRank'])**(b/(a+b))  #exp([a*log(m)+b*log(M)]/[a+b]) = m^(a/[a+b]) * M^(b/[a+b])    
    ytop = max(reCompo['#allocations'])*5/7
    
    if x_pos != 0 and y_pos != 0:
        plt.text(x_pos, y_pos, parameters, fontsize=30)
    elif x_pos != 0 and y_pos == 0:
        plt.text(x_pos, ytop, parameters, fontsize=30)
    elif x_pos == 0 and y_pos != 0:
        plt.text(xmid, y_pos, parameters, fontsize=30)
    else:
        plt.text(xmid, ytop, parameters, fontsize=30)
    #-----------------------------------------
    plt.xlabel('Rank of component($y\prime$)', size = 20)
    plt.xscale('log')
    plt.ylabel('$Allo(y\prime)$', size = 20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    #https://stackoverflow.com/questions/6774086/why-is-my-xlabel-cut-off-in-my-matplotlib-plot
    plt.gcf().subplots_adjust(left = 0.17, bottom = 0.17)
    plt.title(name, fontsize = 20)
    try:
        if Path == '':
            fig.savefig('allocation_' + name + '.' + FORMAT, dpi = 500, format = FORMAT)
            plt.show()
        else:
            fig.savefig(Path + 'allocation_' + name + '.' + FORMAT, dpi = 500, format = FORMAT)
            plt.close()
    except:
        plt.show()
    
    Allo_fit = (A, B)
    return Allo_fit
        
def Chain_plot(name, block, x_pos = 0, y_pos = 0, FORMAT = 'png', Path = ''):
    '''draw allocation-rank plot 

    ---Input
    1. name: str
        "XXX" (your file name without filename extension)

    2. block: pd.daframe
        output of function info() or N_gram_info() in count.py
        you should get them from
        big, compo, block, longest = info(filename, encode)
    
    ---Parameters
    1. x_pos, y_pos : float
        (x_position, y_position) of your formula on FRD plot

    2. FORMAT: string
        The format of your plot. Most backends support png, pdf, ps, eps and svg. 
        else: just show plot instead of saving.
    
    3. Path: file path for saving picture
        Default: save at current document
        if Path == np.nan, no figure will be saved (just show it)
        else, the figure will be saved according to Path
    
    ---Output
        figure of chain distribution
    
    ---Return
        Chain_fit: tuple (A, B, U_Chain), (str, str, int)
            A, B are fitting parameters of Chain(x') = -A ln x' + B
            They are saved as string to present significant figures
            U_Chain denotes the the least upper bound of Chain
    '''
    Block = block.sort_values(by='#chains', ascending=False)
    reBlock = Block.reset_index()

    #use OLS to get the fitting parameter
    #-----------------------------------------
    def chain(x, a, b):
        return (a * np.log(x) + b)

    popt, pcov = curve_fit(chain, block['blockRank'], reBlock['#chains'])
    #popt is the optimal values for the parameters (a,b)
    theo = chain(block['blockRank'], *popt)
    fig, ax = plt.subplots()
    plt.plot(block['blockRank'], theo, 'g--')
    plt.plot(reBlock['#chains'], 'ro', label = 'block', markersize = 4)


    
    #the following code deal with significant figures of fitting parameters
    #the tutor of significant figures: https://www.usna.edu/ChemDept/_files/documents/manual/apdxB.pdf
    #-----------------------------------------
    chain_dig = len(str(max(reBlock['#chains'])))
    xp_dig = len(str(max(block['blockRank']))) #ln(x) will have dig(x) +1 digits (dig(x) significant figures)
    a_dig = min(chain_dig, xp_dig +1) #significant figures of parameter a
    b_dig = a_dig #significant figures of parameter b
    
    # the fomat string is #.?g, where ? = significant figures
    # detail of the fomat string: https://bugs.python.org/issue32790
    # https://docs.python.org/3/tutorial/floatingpoint.html
    A = format(abs(popt[0]), '#.%dg' % a_dig)  # give a_dig significant digits
    B = format(popt[1], '#.%dg' % b_dig)  # give b_dig significant digits
    if 'e' in A: #make scientific notation more beautiful
        A_text = A.split('e')[0] + '\\times 10^{' + str(int(A.split('e')[1])) + '}'
    elif A[-1] == '.':
        A_text = A[:-1]
    else:
        A_text = A
    if 'e' in B: #make scientific notation more beautiful
        B_text = B.split('e')[0] + '\\times 10^{' + str(int(B.split('e')[1])) + '}'
    elif B[-1] == '.':
        B_text = B[:-1]
    else:
        B_text = B
    
    #a perfect solution to text wrap!!
    #https://stackoverflow.com/questions/2660319/putting-newline-in-matplotlib-label-with-tex-in-python
    parameters = (r"$\gamma=%s$"
                  "\n"
                 r"$\omega=%s$") % (A_text, B_text)    
    
    a = 1.5  #auto positioning for m = min(compo['compoRank']) = 1 always
    b = 2   #auto positioning for M = max(compo['compoRank'])
    xmid = max(block['blockRank']) ** (b/(a+b))  #exp([a*log(m)+b*log(M)]/[a+b]) = m^(a/[a+b]) * M^(b/[a+b])
    ytop = max(reBlock['#chains'])*5/7
    
    if x_pos != 0 and y_pos != 0:
        plt.text(x_pos, y_pos, parameters, fontsize=30)
    elif x_pos != 0 and y_pos == 0:
        plt.text(x_pos, ytop, parameters, fontsize=30)
    elif x_pos == 0 and y_pos != 0:
        plt.text(xmid, y_pos, parameters, fontsize=30)
    else:
        plt.text(xmid, ytop, parameters, fontsize=30)
    #-----------------------------------------     
    plt.xlabel('Rank of block($x\prime$)', size = 20)
    plt.xscale('log')
    plt.ylabel('$Chain(x\prime)$', size = 20)
    ax.tick_params(axis='x', labelsize=15) 
    ax.tick_params(axis='y', labelsize=15)
    #https://stackoverflow.com/questions/6774086/why-is-my-xlabel-cut-off-in-my-matplotlib-plot
    plt.gcf().subplots_adjust(left = 0.17, bottom = 0.17)
    plt.title(name, fontsize = 20)
    try:
        if Path == '':
            fig.savefig('chain_' + name + '.' + FORMAT, dpi = 500, format = FORMAT)
            plt.show()
        else:
            fig.savefig(Path + 'chain_' + name + '.' + FORMAT, dpi = 500, format = FORMAT)
            plt.close()
    except:
        plt.show()
    
    Chain_fit = (A, B)
    U_Chain = max(reBlock['#chains'])
    return Chain_fit, U_Chain