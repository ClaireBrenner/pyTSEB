#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Script to run TSEB/OSEB over a timeseries of point measurements
for the data set of Petit-Nobressart from summer 2015 collected during 
the CAOS field campaign.

To run the models two files have to be provided:
- Configuration file including location data, emissivity, spectral data,
     information on G computation method etc.
- Timeseries of meteorological and site specific properties 

The timeseries file is first written in this script for immediate use in the
models. (create_input)

To avoid overwritting of outputs, each run is numbered and the output, input 
as well as configuration file of each run are saved.
"""

import glob
import pickle
import os
import sys
import matplotlib.pyplot as plt
os.chdir('D:\\Daten\\Evaporation\\Source_Codes\\TwoSource' + \
         'EnergyBalanceModel\\pyTSEBmod')
from src.pyTSEB import PyTSEB

# Loading config file
home = r'D:\Daten\Auswertung_Feldarbeiten_Pt_Nobressart\PYTHON\Timeseries'
met_dir = r'D:\Daten\Auswertung_Feldarbeiten_Pt_Nobressart\PYTHON\Timeseries'
met_file = r'met_data_whole.csv'
g_file ='G_data_whole.csv'
ec_file = 'ec_data_whole.csv'

sys.path.append(home)
from setupConfig_PN_ts import config_file as CONFIG_FILE
import pn_ts_utils 
from evaluate_timeseries import Model_outputs
ec_corr_style = 'half-hourly'
pn_ts_utils.corr_ec(home, ec_file, style=ec_corr_style)            

# Get run label to avoid overwritting of data
F_NO = len(glob.glob(os.path.join(home, 'model_outputs', '*%s_run*.txt' % (
        CONFIG_FILE['ModelMode'][:4])))) + 1
# Name of the timeseries input file
if CONFIG_FILE['ModelMode'][:4] == 'TSEB':
    input_name = 'PN_Data_Timeseries_%s_run%i.txt' % (
            CONFIG_FILE['ModelMode'][:4], F_NO)
    output_name = 'PN_Output_Timeseries_%s_run%i.txt' % (
        CONFIG_FILE['ModelMode'][:4], F_NO)
elif CONFIG_FILE['ModelMode'][:4] == 'OSEB':
    kb_str = str(CONFIG_FILE['PointTimeseriesInput']['kB'])
    input_name = 'PN_Data_Timeseries_%s_kB_%s_run%i.txt' % (
            CONFIG_FILE['ModelMode'][:4], kb_str, F_NO)
    output_name = 'PN_Output_Timeseries_%s_kB_%s_run%i.txt' % (
        CONFIG_FILE['ModelMode'][:4], kb_str, F_NO)
    
# In the OSEB model G is calculated as fraction of Rn instead of Rn_soil and
# thus the fraction has to be reduced. It is set to 0.15.
if CONFIG_FILE['ModelMode'][:4] == 'OSEB':
    CONFIG_FILE['SHFinfo']['G_ratio'] = 0.15

# Vegetation information might be set as a scalar (valid for the whole time-
# series) or as an array of the length of the timeseries. I gathered 
# information about mowing and vegetation height for the field campaign and
# a created a timeseries of variable vegetation properties.
hc_values, lai_values, fg_values = pn_ts_utils.create_var_vegprops(
        met_dir=met_dir, met_file=met_file)

# Write timeseries input file
pn_ts_utils.create_input(met_dir, met_file, g_file, 
                         input_name, lai=lai_values, hc=hc_values, fg=fg_values, 
                         fc=0.9, wc=1.0)

# Write correct input name into the configuration file
CONFIG_FILE['PointTimeseriesInput']['InputFile'] = os.path.join(home,
           'model_inputs', input_name)
# Write correct output name into the configuration file
CONFIG_FILE['PointTimeseriesInput']['OutputFile'] = os.path.join(home,
           'model_outputs', output_name)

# Function to run the TSEB/OSEB model
def runTSEB_from_config_file(config_file):
    ''' Run the TSEB model'''
    # Open a log file in the working directory
    # Create a class instance from PyTSEB
    setup = PyTSEB()
    # Get the data from the widgets
    #configData=setup.parseInputConfig(configFile,isImage=False)
    setup.GetDataTSEB(config_file, isImage=False)
    setup.RunTSEBPointSeriesArray()
    return

# Run the model
runTSEB_from_config_file(CONFIG_FILE)

# Compare timeseries to EC data
model_data = Model_outputs(output_name)
model_data.plot_timeseries(style=ec_corr_style)

if model_data.modelName == 'TSEB':
    plt.savefig(os.path.join(home, 'plots','PN_Output_Timeseries_%s_run%i.png'
                                               % (CONFIG_FILE['ModelMode'][:4], 
                                                  F_NO)))
    # Save the configuration file
    pickle.dump(CONFIG_FILE, open(os.path.join(home,
                                           'config_files',
                                           'PN_Output_Timeseries_%s_run%i.p'
                                           % (CONFIG_FILE['ModelMode'][:4], 
                                              F_NO)), 'wb'))
    
elif model_data.modelName == 'OSEB':
    kb_str = str(CONFIG_FILE['PointTimeseriesInput']['kB'])
    plt.savefig(os.path.join(home, 'plots','PN_Output_Timeseries_%s_kB_%s_run%i.png'
                                               % (CONFIG_FILE['ModelMode'][:4], 
                                                  kb_str, F_NO)))
    # Save the configuration file
    pickle.dump(CONFIG_FILE, open(os.path.join(home,
                                           'config_files',
                                           'PN_Output_Timeseries_%s_kB_%s_run%i.p'
                                           % (CONFIG_FILE['ModelMode'][:4], 
                                              kb_str, F_NO)), 'wb'))
    
pn_ts_utils.add_plots(model_data, CONFIG_FILE, F_NO, home)


