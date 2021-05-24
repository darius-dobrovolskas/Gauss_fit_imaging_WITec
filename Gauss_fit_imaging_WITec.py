# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:44:06 2020

@author: dd
version: 1.1

Reads fitted parameters from txt files and plots as 2d images. 
Saves each parameter as 2d matrix to file (if needed).
Parameters automatically reshaped to a square image (n*n).
Extreme outliers are imputed as mean values.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#load data
data_folder = 'C:\\DARBAI\\Binning test\\InGaN\\'
raw = pd.read_csv(data_folder + 'fitted_values.txt')
binned = pd.read_csv(data_folder + 'fitted_values_binned.txt')

raw.drop('y0', axis=1, inplace=True)
binned.drop('y0', axis=1, inplace=True)

columns = raw.columns

n = int(np.sqrt(len(raw['amp1'])))   #length of a square side for raw images 
m = int(np.sqrt(len(binned['amp1'])))#length of a square side for binned images 

# raw.boxplot(['amp1', 'x01', 'w1'])   

#impute extreme outliers as mean values
for i, column in enumerate(columns):
    column = [column]
    mean = raw[column].values.mean()
    for x in column:
        q75,q25 = np.percentile(raw.loc[:,x],[75,25])
        intr_qr = q75-q25
         
        max = q25+(10*intr_qr)
        min = q25-(10*intr_qr)
                
        print(round(mean,2))
        raw.loc[raw[x] < min,x] = round(mean,2)
        raw.loc[raw[x] > max,x] = round(mean,2)

#loop for images
for i, column in enumerate(columns):
    param_raw = raw[column]
    param_raw = param_raw.values.reshape(n, n)
    param_bin = binned[column]
    param_bin = param_bin.values.reshape(m, m)        
    
    #plot raw parameters
    fig1, axs1 = plt.subplots(figsize=(6,6))
    im1 = axs1.imshow(param_raw, interpolation=None) 
                # vmin=param_raw.flatten().mean()-3*param_raw.flatten().std(),
                # vmax=param_raw.flatten().mean()+3*param_raw.flatten().std())
    cbar1 = fig1.colorbar(im1, fraction=0.046, pad=0.04)
    cbar1.set_label('{}'.format(column))
    axs1.set_title('Raw data, {}'.format(column))
    axs1.set_xlabel('Pixel number')
    axs1.set_ylabel('Pixel number')
    #plot binned parameters
    fig2, axs2 = plt.subplots(figsize=(6,6))
    im2 = axs2.imshow(param_bin, interpolation=None) 
                # vmin=param_bin.flatten().mean()-3*param_bin.flatten().std(),
                # vmax=param_bin.flatten().mean()+3*param_bin.flatten().std())
    cbar2 = fig2.colorbar(im2, fraction=0.046, pad=0.04)
    cbar2.set_label('{}'.format(column))
    axs2.set_title('Binned data, {}'.format(column))
    axs2.set_xlabel('Pixel number')
    axs2.set_ylabel('Pixel number')

plt.show()
  
    #save each param as 2d matrix to file
    # np.savetxt(data_folder + '{}_2d_raw.txt'.format(column), param_raw)