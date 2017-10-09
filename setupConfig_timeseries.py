# -*- coding: utf-8 -*-
"""
Sets up the input data to process TIR data from Petit Nobressart using TSEB, DTD or OSEB 
"""
config_file = {
        
    'ModelMode'     : 'TSEB_PT',       # 'TSEB_PT' or 'OSEB'
    
    'SiteProps' : {
        'lat'       : 49.779242,    # Latitude
        'lon'       : 5.802408,     # Longitude
        'stdlon'    : 14.80,        # Standard longitude, central longitude of the 
                                    # Time zone of the site (degrees)
        'altitude'  : 380.0,        # (m) Altitude
        'zt'        : 2.41,         # (m) Measurement height temperature
        'zu'        : 2.41,         # (m), Measurement height wind
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
        'LAI'       : 1.2,          # Effective Leaf Area Index (m2/m2) 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value across the area
        'Fc'        : 0.8,          # Vegetation Fractional Cover 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value acroos the area
        'Hc'        : 0.15,         # Canopy height (m), 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value along the area
        'Wc'        : 1.0,          # Canopy height/with ratio (wc/hc) 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value along the area
        'Fg'        : 0.8,          # Green Fraction 
                                    # Optional, type either a full-path file or a 
                                    # Single value for a constant value along the area
        'xLAD'      : 1.0,          # Cambpbell 1990 leaf inclination distribution 
                                    # parameter:[x_LAD=1 for spherical LIDF, 
                                    # x_LAD=0 for vertical LIDF 
                                    # x_LAD=float(inf) for horzontal LIDF] 
        'leafWidth' : 0.02,          # leaf effective width (m)
        
        # Emissivities
        'emisVeg'   : 0.98,         # Leaf emissivity
        'emisSoil'  : 0.98,         # Soil emissivity
        
        # Canopy & soil spectral properties
        'rhovis'    : 0.07,         # rho_leaf_vis: visible reflectance 0.07
        'tauvis'    : 0.08,         # tau_leaf_vis: visible transmittance 0.08
        'rhonir'    : 0.40,         # rho_leaf_nir: NIR reflectance 0.32
        'taunir'    : 0.40,         # tau_leaf_nir: NIR transmittance 0.33
        'rsoilvis'  : 0.15,         # rsoilv: visible reflectance 0.15
        'rsoilnir'  : 0.30,         # rsoiln: NIR reflectance 0.25
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
        'CalcG'     : 0,            # switch to select soil heat flux measurment method
                                    # 0: Use a constant G, usually use G_Constant=0 
                                    #    to ignore the computation of G
                                    # 1: default, estimate G as a ratio of Rn_soil, 
                                    #    default G_ratio=0.35
                                    # 2: estimate G from Santanello and Friedl 
                                    #    with GAmp the maximum ration amplitude, 
                                    #    Gphase, the time shift between G and Rn 
                                    #    (hours) and Gshape the typical diurnal shape 
                                    #    (hours)
        'G_ratio'   : 0.35,         # estimate G as a ratio of Rn_soil
        'G_constant': 0.0,          # estimate G as a constant
        
        # estimate G from Santanello and Friedl
        'GAmp'      : 0.16,         # Gamp the maximum ration amplitude 
        'Gphase'    : 1.0,          # Gphase, the time shift between G and Rn (hours) 
        'Gshape'    : 24.0          # Gshape the typical diurnal shape (hours)
        },
        
    'PointTimeseriesInput' : {
        'InputFile' : '',
        'kB'        : 2.3           # kB value to correct the aerodynamic resistance
                                    # 'Kustas', 'Lhomme', or floar 2.3
        }}
            
