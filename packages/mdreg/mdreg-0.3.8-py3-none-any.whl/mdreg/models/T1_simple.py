""" 
@author: Steven Sourbron 
T1-MOLLI model fit  
2022  
Messroghli DR, Radjenovic A, Kozerke S, Higgins DM, Sivananthan MU, Ridgway JP. 
Modified Look-Locker inversion recovery (MOLLI) for high-resolution T1 mapping of the heart. 
Magn Reson Med. 2004 Jul;52(1):141-6. doi: 10.1002/mrm.20110. PMID: 15236377. 
"""

import numpy as np
from scipy.optimize import curve_fit

def pars():
    return ['S0', 'alpha', 'T1']

def bounds():
    lower = [0, 0, 1.0] 
    upper = [5000, 3000, 3000.0]
    return lower, upper


def func(TI, a,b, T1):
    """ exponential function for T1-fitting.
    Args
    ----
    x (numpy.ndarray): Inversion times (TI) in the T1-mapping sequence as input for the signal model fit.    
    
    Returns
    -------
    a, b, T1 (numpy.ndarray): signal model fitted parameters.  
    """

    return np.abs(a - b * np.exp(-TI/T1)) 


def main(images, TI):
    """ main function that performs the T2*-map signal model-fit for input 2D image at multiple time-points (TEs).
    Args
    ----
    images (numpy.ndarray): input image at all time-series (i.e. at each TE time) with shape [x-dim*y-dim, total time-series].  
    t (list): list containing time points of exponential.  
    Returns
    -------
    fit (numpy.ndarray): signal model fit per pixel for whole image with shape [x-dim*y-dim, total time-series].  
    par (numpy.ndarray): output signal model fit parameters 'S' and 'R' stored in a single nd-array with shape [2, x-dim*y-dim].      
    """

    TI = np.array(TI)
    shape = np.shape(images)
    par = np.empty((shape[0], 3)) # pixels should be first for consistency
    fit = np.empty(shape)

    for x in range(shape[0]):

        signal = images[x,:]
        p0 = [687.0, 1329.0, 1500.0]
        try:
            par[x,:], _ = curve_fit(func, 
                xdata = TI, 
                ydata = signal, 
                p0 = p0, 
                bounds = ([0, 0, 1.0], [5000, 2000, 3000.0]), 
                method = 'trf', 
                maxfev = 500, 
            )
        except RuntimeError: #optimum not found.
            par[x,:] = p0

        fit[x,:] = func(TI, par[x,0], par[x,1], par[x,2])
        par[x,2] = par[x,2] * (np.divide(par[x,1], par[x,0], out=np.zeros_like(par[x,1]), where=par[x,0]!=0) - 1) #calculate real T1 from apparent T1
        if par[x,2] > 3000:
            par[x,2] = 3000
        if par[x,2] <0:
            par[x,2] = 0
        
    return fit, par