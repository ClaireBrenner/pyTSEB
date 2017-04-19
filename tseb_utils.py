# -*- coding: utf-8 -*-
"""
Utility functions for TSEB
"""
import gdal
import numpy as np
import pandas as pd
import sys

# Import met_utils
sys.path.append('D:\Daten\Evaporation\PYTHON')
import met_utils

def createLST0(Imagery, metData, flightime):
    ''' 
    Needed for TSEB in DTD mode in case that no Trad_0 image is available.
    This function creates a array of the size of LST with the surface temperature
    value from the EC data (homogeneous array)
    '''
    # Read LST information during day (Trad_1)
    in_im = Imagery['inputLST']
    fid=gdal.Open(in_im,gdal.GA_ReadOnly)
    LST = fid.GetRasterBand(1).ReadAsArray()
    prj = fid.GetProjection()
    geo = fid.GetGeoTransform()
    
    # Write point surface temperature value into array
    time = metData.loc[metData.index == flightime, :].index
    time_0 = pd.to_datetime(time.date[0]) + pd.Timedelta(5.5, unit = 'h')
    surf_temp = metData.loc[time_0, 'IR_TempC_Avg'] 
    LST_0 = np.zeros(LST.shape) + surf_temp
    LST_0[LST == -99] = -99
    
    # Write output
    rows,cols = np.shape(LST)
    driver = gdal.GetDriverByName('GTiff')
    fields = [LST, LST_0]
    nbands = len(fields)
    outfile = in_im.replace('LST.tif', 'LST_DTD.tif')
    ds = driver.Create(outfile, cols, rows, nbands, gdal.GDT_Float32)
    ds.SetGeoTransform(geo)
    ds.SetProjection(prj)
    for i,field in enumerate(fields):
        band=ds.GetRasterBand(i+1)
        band.SetNoDataValue(0)
        band.WriteArray(field)
        band.FlushCache()
    ds.FlushCache()
    del ds
    

def parseMet(metData, flightime, config_file):
    '''
    Parse meteorological data during flightime into the config_file.
    '''
    time = metData.loc[metData.index == flightime, :].index
    DOY = int(metData.loc[metData.index == flightime, :].index.dayofyear)          
    decTime = time.hour + float(time.minute)/60 + float(time.second)/3600
    Ta_1 = metData.loc[flightime, 'airtemp_Avg'] + 273.15
    Sdn = metData.loc[flightime, 'SR_In_Avg'] 
    Ldn = metData.loc[flightime, 'IR_InCo_Avg'] 
    u = metData.loc[flightime, 'u'] 
    p = metData.loc[flightime, 'airpressure_Avg'] 
    ea = met_utils.get_ea_fromRH(metData.loc[flightime, 'relhumidity_Avg'], Ta_1 - 273.15)
    
    if config_file['ModelMode'] == 'DTD':
        time_0 = pd.to_datetime(time.date[0]) + pd.Timedelta(5.5, unit = 'h')
        Ta_0 = metData.loc[time_0, 'airtemp_Avg'] + 273.15
        config_file['Ta_0'] = Ta_0
              
    config_file['Meteo']['DOY'] = DOY
    config_file['Meteo']['Time'] = decTime[0]
    config_file['Meteo']['Ta_1'] = Ta_1
    config_file['Meteo']['u'] = u
    config_file['Meteo']['p'] = p
    config_file['Meteo']['ea'] = ea
    config_file['Meteo']['Sdn'] = Sdn
    config_file['Meteo']['Ldn'] = Ldn
    return config_file