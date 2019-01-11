#!/usr/bin/env python
"""
Field Data Analysis Library

Created : 11-01-2019
Last Modified : Fri 11 Jan 2019 02:42:04 PM EST
Created By : Enrique D. Angola

This library is designed to read mast data and perform user-defined analyses. It is purposedly designed to work
in conjunction with the well known Pandas library by transforming raw data into pandas dataframes and/or pandas 
time-series. This allows flexibility so that the main user is not restricted by the anlyses that have been coded
in this library.

The architecture of the library is divided in 4 main modules:
    - readers module: Contains reader objects for different sources of data.
    - filters module: Contains filter objects to generate filters for data.
    - analyses module: Contains analyses objects to compute different, coded analyses on data.
    - plotters module: Contains plotter objects to plot common graphics from coded analyses.

Currently supports:
- Anemometer analysis:
    - Scatter Ratio
    - Etc... 
- Vane analysis
- SymPro data reader
- Campbell data reader
- Classic filtering:
    - Ice
    - Wind speed
    - Best Sector

"""
