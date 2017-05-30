# -*- coding: utf-8 -*-
"""
Utility functions for TSEB
"""
import gdal
import numpy as np
import pandas as pd

def create_lst0(Imagery, metData, flightime):
    ''' 
    Needed for TSEB in DTD mode in case that no Trad_0 image is available.
    This function creates a array of the size of LST with the surface temperature
    value from the EC data (homogeneous array)
    '''
    # Read LST information during day (Trad_1)
    in_im = Imagery['inputLST']
    fid=gdal.Open(in_im,gdal.GA_ReadOnly)
    lst = fid.GetRasterBand(1).ReadAsArray()
    prj = fid.GetProjection()
    geo = fid.GetGeoTransform()
    
    # Write point surface temperature value into array
    time = metData.loc[metData.index == flightime, :].index
    time_0 = pd.to_datetime(time.date[0]) + pd.Timedelta(5.5, unit = 'h')
    surf_temp = metData.loc[time_0, 'IR_TempC_Avg'] 
    lst_0 = np.zeros(lst.shape) + surf_temp
    lst_0[lst == -99] = -99
    
    # Write output
    rows,cols = np.shape(lst)
    driver = gdal.GetDriverByName('GTiff')
    fields = [lst, lst_0]
    nbands = len(fields)
    outfile = in_im.replace('lst.tif', 'lst_DTD.tif')
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
    



