#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Input configuration to run TSEB and OSEB for thermal imagery from 
Fendt, Germany, ScaleX field campaign 2016.
"""

import time
from src.pyTSEB import PyTSEB


configFile='Config_LocalImage.txt'

def RunTSEBFromConfigFile(configFile):
    # Open a log file in the working directory
    # Create a class instance from PyTSEB
    setup=PyTSEB()
    # Get the data from the widgets
    configData=setup.parseInputConfig(configFile,isImage=True)
    setup.GetDataTSEB(configData,isImage=True)
    setup.RunTSEBLocalImage()
    return

if __name__=='__main__':
    import sys
    args=sys.argv
    if len(args)>1:
        configFile=args[1]
    print('Run pyTSEB with configuration file = '+str(configFile))
    RunTSEBFromConfigFile(configFile)
