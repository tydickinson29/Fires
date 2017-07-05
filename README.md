This repository is a series of Jupyter notebooks that makes great use of the Pandas module to import .csv files containing past storm/fire reports, rainfall, etc and outputs new .csv containing various data described below.

At NWS Austin/San Antonio Weather Forecast Office we defined our seasons to be as follows:

Winter: December, January, February

Spring: March, April, May

Summer: June, July, August

Fall: September, October, November

# Severe Weather

Code is still in progress.

Impacts: Total number of reports, number of report days, damages (adjusted to 2010), maximum hail size, maximum wind magnitude (non-tornadic), maximum tornado width, total tornado path length, total rainfall, fatalities, and injuries. 

A report day is defined to be 12Z - 12Z as overnight events are frequent and should be considered together. 

# Fires

Impacts: Combined fire service and civilian fatalities, combined fire service and civilian injuries, acres burned, damages (adjusted to 2010), number of fires, number of days with a fire. 

In our dataset times were not given for the fire reports, so number of days with a fire were strictly by date.

# Winter Weather 

Code is currently still in process, but the beginning is uploaded. 

Seasons may be changed to October, November, December and January, February, March. 

# Rainfalls

There are multiple rainfall scripts uploaded. COOP Rainfall takes daily rainfall accumulations from COOP stations and outputs maximum one day and two day rainfall. 

LCRA Rainfall is used to estimated total rainfall throughout a given area using quadrangles created by the Lower Colorado River Authority. 
They have collected rainfall data since 1940 and have monthly tables for rainfall and evaporation available at their website: 

http://www.twdb.texas.gov/surfacewater/conditions/evaporation/

We selected quadrangles that were over two-thirds covered by area in our county warning area (CWA). Output is rainfall estimations for our CWA area.
