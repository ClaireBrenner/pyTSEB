#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Script to run TSEB over a timeseries of point measurements

Created on Dec 29 2015
@author: Hector Nieto

Modified on Jan 13 2016
@author: Hector Nieto

"""

import time
import os, sys
os.chdir('D:\Daten\Evaporation\Source_Codes\TwoSourceEnergyBalanceModel\pyTSEBmod')
from src.pyTSEB import PyTSEB

# Loading config file
dir1 = r'D:\Daten\Auswertung_Feldarbeiten_Pt_Nobressart\PYTHON\Timeseries'
sys.path.append(dir1)
from setupConfig_PN_ts import config_file


def RunTSEBFromConfigFile(config_file):
    # Open a log file in the working directory
    # Create a class instance from PyTSEB
    setup=PyTSEB()
    # Get the data from the widgets
    #configData=setup.parseInputConfig(configFile,isImage=False)
    setup.GetDataTSEB(config_file,isImage=False)
    setup.RunTSEBPointSeriesArray()
    return

config_file['PointTimeseriesInput']['InputFile'] = os.path.join(dir1, 'PN_Data_Timeseries_TSEB2.txt')
config_file['PointTimeseriesInput']['OutputFile'] = os.path.join(dir1, 'PN_Output_Timeseries_TSEB.txt')

RunTSEBFromConfigFile(config_file)
