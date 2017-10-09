# -*- coding: utf-8 -*-
"""
Sets up the input data to process TIR data from Petit Nobressart using TSEB, DTD or OSEB 
"""
config_file = {
        
    'ModelMode'     : 'TSEB_PT',
    
    'SiteProps' : {
        'lat'       : 47.832912,    # Latitude
        'lon'       : 11.060705,    # Longitude
        'stdlon'    : 14.80,        # Standard longitude, central longitude of the 
                                    # Time zone of the site (degrees)
        'altitude'  : 594.0,        # (m) Altitude
        'zt'        : 3.52,         # (m) Measurement height temperature
        'zu'        : 3.52,         # (m), Measurement height wind
        'landCover' : 2.0,          # Primary land cover CROP=11, GRASS=2, SHRUB=5, 
                                    # CONIFER=4, BROADLEAVED=3
        },
        
    'Meteo'         : {
        'DOY'       : 180,
        'Time'      : 12.0,
        'Ta_0'      : 283.15,
        'Ta_1'      : 299.15,
        'u'         : 2.0,
        'p'         : 1000,
        'ea'        : 15.0,
        'Sdn'       : 800.0,
        'Ldn'       : '',
        },
            
    'SiteVegProps'  : {
        'LAI'       : 2.5,          # Effective Leaf Area Index (m2/m2) 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value across the area
        'Fc'        : 0.9,          # Vegetation Fractional Cover 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value acroos the area
        'Hc'        : 0.15,         # Canopy height (m), 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value along the area
        'Wc'        : 1.0,          # Canopy height/with ratio (wc/hc) 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value along the area
        'Fg'        : 0.9,          # Green Fraction 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value along the area
        'xLAD'      : 1.0,          # Cambpbell 1990 leaf inclination distribution 
                                    # parameter:[x_LAD=1 for spherical LIDF, 
                                    # x_LAD=0 for vertical LIDF 
                                    # x_LAD=float(inf) for horzontal LIDF] 
        'leafWidth' : 0.02,          # leaf effective width (m)
        
        # Emissivities
        'emisVeg'   : 0.97,         # Leaf emissivity
        'emisSoil'  : 0.99,         # Soil emissivity
        
        # Canopy & soil spectral properties
        'rhovis'    : 0.07,         # rho_leaf_vis: visible reflectance
        'tauvis'    : 0.08,         # tau_leaf_vis: visible transmittance
        'rhonir'    : 0.32,         # rho_leaf_nir: NIR reflectance
        'taunir'    : 0.33,         # tau_leaf_nir: NIR transmittance
        'rsoilvis'  : 0.15,         # rsoilv: visible reflectance
        'rsoilnir'  : 0.25,         # rsoiln: NIR reflectance
        },
                                   
           
    'AncProps' : {
        'maxAlphaPT': 1.26,         # Initial value for Priestley Taylor canopy transpiration
        'VZA'       : 0.0,          # View Zenith Angle (degrees) 
                                    # Optional, type either a full-path file or a 
                                    # single value for a constant value acroos the area
        'z0soil'    : 0.01,         # (m) Bare soil roughness length 
        'useMask'   : 0,            # Processing Mask (boolean) 
                                    # Optional, type a full-path file for processing 
                                    # only on non-masked pixels (all pixels with 
                                    # values > 0 in the mask image will be processed)         
        },
            
    'SHFinfo' : {
        'CalcG'     : 1,            # switch to select soil heat flux measurment method
                                    # 0: Use a constant G, usually use G_Constant=0 
                                    #    to ignore the computation of G
                                    # 1: default, estimate G as a ratio of Rn_soil, 
                                    #    default G_ratio=0.35
                                    # 2: estimate G from Santanello and Friedl 
                                    #    with GAmp the maximum ration amplitude, 
                                    #    Gphase, the time shift between G and Rn 
                                    #    (hours) and Gshape the typical diurnal shape 
                                    #    (hours)
        'G_ratio'   : 0.20,         # estimate G as a ratio of Rn_soil
        'G_constant': 0.0,          # estimate G as a constant
        
        # estimate G from Santanello and Friedl
        'GAmp'      : 0.12,         # Gamp the maximum ration amplitude 
        'Gphase'    : -3.0,          # Gphase, the time shift between G and Rn (hours) 
        'Gshape'    : 28.0          # Gshape the typical diurnal shape (hours)
        },
    
    'resolution_dep': {'flag'  : True,
                       'level' : 'dependent',
                       'filepath' : '' 
        },
                       
    'PointTimeseriesInput' : {
        'InputFile' : '',
        'kB'        : 2.3           # kB value to correct the aerodynamic resistance
                                    # 'Kustas', 'Lhomme', or float 2.3
        }}
            
