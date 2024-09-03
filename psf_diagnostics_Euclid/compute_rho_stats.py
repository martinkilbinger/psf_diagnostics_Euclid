# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: sp_validation
#     language: python
#     name: python3
# ---

import os
import sys
import glob

import itertools
import numpy as np
import matplotlib.pylab as plt

from cs_util import args

from shear_psf_leakage.rho_tau_stat import RhoStat

# +
# Set parameters from file or user input
class dummy(object):
    def __init__(self):
        
        self._params = {
            "in_dir_base": ".",
            "title": None,
        }

obj = dummy()
params_upd = args.read_param_script("params_rho.py", obj._params, verbose=True)
for key in params_upd:
    obj._params[key] = params_upd[key]

default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_cycle = itertools.cycle(default_colors)
col = next(color_cycle)

coord_units = "deg"
theta_min = 0.1
theta_max = 250
sep_units = "arcmin"
nbins = 20

# ## Set up                                                                     
TreeCorrConfig = {                                                           
    'ra_units': coord_units,                                                    
    'dec_units': coord_units,                                                   
    'min_sep': theta_min,                                                       
    'max_sep': theta_max,                                                       
    'sep_units': sep_units,                                                     
    'nbins': nbins,                                                             
    'var_method':'bootstrap',                                                   
}
# -

rho_stat_handler = RhoStat(                                                     
    output=obj._params["in_dir_base"],
    treecorr_config=TreeCorrConfig,                                          
    verbose=True
)

# +
filenames = []
colors = []
patches = []

input = "../data/test/Euclid_rho_input.fits"
path = f"rho_stats_id.fits"
if os.path.exists(f"{obj._params['in_dir_base']}/{path}"):
    print(f"Reading rho stats {obj._params['in_dir_base']}/{path}...")
    rho_stat_handler.load_rho_stats(path)
    filenames.append(path) 
    colors.append('blue')
    patches.append('test_euclid') #Hardcoded for now
else:
    print(
        f"File rho stats {obj._params['in_dir_base']}/{path} not found, computing the rho_stats..."
    )
    rho_stat_handler.build_cat_to_compute_rho(input, catalog_id='test_euclid', square_size=True)
    rho_stat_handler.compute_rho_stats('test_euclid', filename=path)
    filenames.append(path)
    colors.append('blue') #Hardcoded for now
    patches.append('test_euclid') #Same here
# -

# Create plot                                                                   
rho_stat_handler.plot_rho_stats(                                                
    filenames,                                                                  
    colors,                                                                     
    patches,                                                                   
    abs=True,                                                                  
    savefig='rho_stats.png',                                                    
    legend="outside",
)
