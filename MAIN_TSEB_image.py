# -*- coding: utf-8 -*-
"""
Input configuration to run TSEB and OSEB for thermal imagery from 
Fendt, Germany, ScaleX field campaign 2016.
"""

# Imports
import pandas as pd
import timeit
import os, sys, glob
os.chdir(r'D:\Daten\Auswertung_Fendt_2016\PYTHON')
import fendt_utils
os.chdir(r'D:\Daten\Evaporation\Source_Codes\TwoSourceEnergyBalanceModel\pyTSEBmod')
from src.pyTSEB import PyTSEB
import tseb_utils
import pickle

############### Loading data ###############################################
 # Thermal imagery input folder
home = 'D:\Daten\Auswertung_Fendt_2016\TIR_Processing\Processing'
direct_in = os.path.join(home, 'model_inputs')
# Output folder for calculated fluxes
directOut = os.path.join(home, 'model_outputs')

# Loading config file
sys.path.append(home)
try:
    del CONFIG_FILE
except:
    pass
from setupConfig_Fendt import config_file as CONFIG_FILE

# Loading list of flights 
process_dates = fendt_utils.get_process_dates()
#
#process_dates = fendt_utils.create_prop_names(process_dates, 'LAI')
#process_dates = fendt_utils.create_prop_names(process_dates, 'FG')
#process_dates = fendt_utils.create_prop_names(process_dates, 'Hc')

# Loading EC data
met_data = fendt_utils.load_ECdata()
#process_dates = process_dates.loc[0, :]

############### Flight selection ############################################
for ind, val in process_dates.iterrows():
    print(ind)
    flightime, Imagery = fendt_utils.get_Imagery_flightime(process_dates, ind)
    if os.path.isfile(Imagery['outputFile']):
        f_no = len(glob.glob(Imagery['outputFile'][:-6] + '*_ancillary.tif')) + 1
        Imagery['outputFile'] = Imagery['outputFile'][:-4] + '_run%i' % f_no + '.tif'
    
    # Parse meteorological inputs into config file
    CONFIG_FILE = fendt_utils.parseMet(met_data, flightime, CONFIG_FILE)
    CONFIG_FILE = fendt_utils.parseImagery(Imagery, CONFIG_FILE)
    CONFIG_FILE = fendt_utils.get_veg_props(process_dates, ind, CONFIG_FILE)
    CONFIG_FILE = fendt_utils.get_res_dependency(process_dates, ind, CONFIG_FILE)
    
    if CONFIG_FILE['ModelMode'] == 'DTD':   
        if not os.path.isfile(os.path.join(direct_in, process_dates.iloc[0,0] + \
                                           '_LST_DTD.tif')):
            # Create LST_0 image from EC point surface temperature measurement
            tseb_utils.create_lst0(Imagery, met_data, flightime)
        Imagery['inputLST'] = os.path.join(direct_in, process_dates.iloc[0,0] + \
                                           '_LST_DTD.tif')
    
    ############### Resolution configuration ############################################
    CONFIG_FILE['resolution_dep']['flag'] = bool(process_dates.loc[ind, 'resolution_flag'])
    
    if (CONFIG_FILE['resolution_dep']['flag'] and 
        (CONFIG_FILE['resolution_dep']['level'] == 'dependent')): 
        
        inde_files = glob.glob(os.path.join(os.path.split(CONFIG_FILE['Imagery'][
                'outputFile'])[0], '*independent_vars.p'))
        if len(inde_files) > 1:
            print('Caution: There are more of one independent variable dataset' + \
                  'for this flight in the output folder. %s will be used.' % 
                  inde_files[-1])
        CONFIG_FILE['resolution_dep']['filepath'] = inde_files[-1]
            
    ############### Run function ################################################
    def RunTSEBFromConfigFile(config_file):
        # Open a log file in the working directory
        # Create a class instance from PyTSEB
        setup=PyTSEB()
        # Get the data from config file
        setup.GetDataTSEB(config_file, isImage=True)
        # Run model
        setup.RunTSEBLocalImage()
        return
        
    ############### Run & Evaluation ############################################
    start = timeit.default_timer()
    RunTSEBFromConfigFile(CONFIG_FILE)
    stop = timeit.default_timer()
    print('Runtime: ', stop - start )
    
    f = os.path.split(Imagery['outputFile'][:-4])[1]
    pickle.dump(CONFIG_FILE, open(os.path.join(home, 'config_files', f + \
                                               '_config.p'), 'wb'))
    model_fluxes = fendt_utils.evaluate_fluxes(Imagery['outputFile'], flightime, 
                                               style = 'half-hourly')
    pickle.dump(model_fluxes, open(Imagery['outputFile'][:-4] + '.p', 'wb'))
    

