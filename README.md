This repository is a series of Jupyter notebooks that makes great use of the Pandas module to import .csv files containing past
storm/fire reports, rainfall, etc and outputs new .csv containing various data described below.

At NWS Austin/San Antonio Weather Forecast Office we defined our seasons to be as follows:

Winter: December, January, February

Spring: March, April, May

Summer: June, July, August

Fall: September, October, November

Storm reports (except Fire Weather) were gathered using the National Centers for Environmental Information's (NCEI) 
Storm Events Database: https://www.ncdc.noaa.gov/stormevents/

At this point, not all code is commented to explain my thoughts, but I intend to do so.

# Severe Weather

Code almost done, but not completely. Report Days is the only remaining indicator needed.

Selections in NCEI Storm Data: Hail, Lightning, Thunderstorm Wind, Tornado

Indicators: Total number of reports, number of report days, damages (adjusted to 2010), maximum hail size, maximum wind magnitude 
(non tornadic), maximum tornado width, total tornado path length, total rainfall (discussed below), fatalities, and injuries. 

A report day is defined to be 12Z - 12Z as overnight events are frequent and should be considered together. 

# River/ Flash Flooding

Code is still in progress.

Selections in NCEI Storm Data: Flash Flood, Flood

Combining river flooding and flash flooding may not always be applicable to every WFO. 

Indicators: Number of flash flood reports, number of days with a report, fatalities, injuries, damages (adjusted to 2010), total
rainfall (discussed below), maximum one day rainfall and two day rainfall (also discussed below), and number of times river 
gages went above moderate flood stage. 

In regards to river gages, 54 were selected on major rivers and creek throughout the CWA. 

# Fire Weather

Report dataset was obtained from the Texas Forestry Service. 

Indicators: Combined fire service and civilian fatalities, combined fire service and civilian injuries, acres burned, damages 
(adjusted to 2010), number of fires, number of days with a fire. 

In our dataset times were not given for the fire reports, so number of days with a fire were strictly by date.

# Winter Weather 

Code is currently still in process, but the beginning is uploaded. 

Seasons may be changed to October, November, December and January, February, March. 

Possible selections in NCEI Storm Data: Blizzard, Cold/Wind Chill, Extreme Cold/Wind Chill, Frost/Freeze, Heavy Snow, 
Lake-Effect Snow, Sleet, Winter Storm, Winter Weather

Possible indicators: Number of total reports (large amount of possibilities in NCEI Storm Database seen above), number of days 
with a report, fatalities, injuries, damages (adjusted to 2010), total snowfall, maximum one and two day snowfall, maximum wind
magnitude. 

Ice accumulations may also be useful indicators, if those measurements are available. 

# Rainfalls

There are multiple rainfall scripts uploaded. 

COOP Rainfall takes daily rainfall accumulations from COOP stations and outputs maximum one day and two day rainfall. 52 COOP 
stations were selected in an attempt to fully cover all counties in the CWA as well as have mutliple in metropolitan areas such 
as Austin and San Antonio. (Named COOP Rainfall Totals)

A script that reads in all .csv files containing local maxima from COOP stations and outputs the global maximum from these values
as well as the station this maximum was recorded at. This script is almost complete. (Named Maximum Rainfall)

LCRA Rainfall is used to estimated total rainfall throughout a given area using quadrangles created by the Lower Colorado River
Authority. 
They have collected rainfall data since 1940 and have monthly tables for rainfall and evaporation available at their website: 

http://www.twdb.texas.gov/surfacewater/conditions/evaporation/

We selected quadrangles that were over two-thirds covered by area in our county warning area (CWA). Output is rainfall estimations 
for our CWA area. (Named LCRA Rainfall)

Another possible method of estimating total rainfall is through use of climate divisions (CDs). Each state is divided into climate
divisions and total monthly and seasonal rainfall is calculated for each climate division in the National Weather Service's Local
Climate Analysis Tool (LCAT). A fraction of a CWA can be found inside of each CD then multiplied by the CD's rainfall and summed 
for all CDs of interest. 

# Snowfall

COOP Stations also record snowfall and snow depth, which could be useful for winter weather. However, snowfall measurements should 
be  made sure not to be related to severe weather days, as melted hail accumulations is recorded as snowfall (not sure if COOP 
stations do this but WFO's do). 


# Tropical Weather
