This repository is a series of Jupyter notebooks that makes great use of the Pandas module to import .csv files containing past
storm/fire reports, rainfall, etc and outputs new .csv containing various data described below. It should be noted that parts of
the scripts written here can be written in shorter, more efficient ways, most likely. But, the data that was output was the data
we were needing, so the scripts did the job. This readme is divided into two sections: Information regarding the research 
methods, various weather and climate events, etc. and a section describing a few essential lines of code utilized.

# Background Info, Research Methods, and More
At NWS Austin/San Antonio Weather Forecast Office we defined our seasons to be as follows:

Winter: December, January, February

Spring: March, April, May

Summer: June, July, August

Fall: September, October, November

Storm reports (except Fire Weather) were gathered using the National Centers for Environmental Information's (NCEI) 
[Storm Events Database](https://www.ncdc.noaa.gov/stormevents/).

A report day is defined to be 12Z - 12Z as overnight events are frequent and should be considered together. 


## Severe Weather

Selections in NCEI Storm Data: Hail, Lightning, Thunderstorm Wind, Tornado

Indicators: Total number of reports, number of report days, damages (adjusted to 2010), maximum hail size, maximum wind magnitude 
(non tornadic), maximum tornado width, total tornado path length, total rainfall (discussed below), fatalities, and injuries. 



## River/ Flash Flooding

Selections in NCEI Storm Data: Flash Flood, Flood

Combining river flooding and flash flooding may not always be applicable to every WFO. 

Indicators: Number of flash flood reports, number of days with a report, fatalities, injuries, damages (adjusted to 2010), total
rainfall (discussed below), maximum one day rainfall and two day rainfall (also discussed below), and number of times river 
gages went above moderate flood stage. 

In regards to river gages, 54 were selected on major rivers and creek throughout the CWA. 

The main flooding script will output: reports, report days, fatalities, injuries, and damages. The rainfall data is discussed below
and the number of times river gages went above moderate was gathered by hand through AWIPS.


## Fire Weather

Report dataset was obtained from the Texas Fire Marshal's Office. 

Indicators: Combined fire service and civilian fatalities, combined fire service and civilian injuries, acres burned, damages 
(adjusted to 2010), number of fires, number of days with a fire. 

In our dataset times were not given for the fire reports, so number of days with a fire were strictly by date.

Any controlled burning or prescribed burn that did not have a fatality, injury, associated cost, or acres burned listed.


## Winter Weather 

Seasons may be changed to October, November, December and January, February, March. 

Code is written with original seasons in mind but can easily be modified. 

Possible selections in NCEI Storm Data: Blizzard, Cold/Wind Chill, Extreme Cold/Wind Chill, Frost/Freeze, Heavy Snow, 
Lake-Effect Snow, Sleet, Winter Storm, Winter Weather

Possible indicators: Number of total reports (large amount of possibilities in NCEI Storm Database seen above), number of days 
with a report, fatalities, injuries, damages (adjusted to 2010), total snowfall, maximum one and two day snowfall, maximum wind
magnitude. 

Ice accumulations may also be useful indicators, if those measurements are available. 


## Rainfalls

There are multiple rainfall scripts uploaded. 

COOP Rainfall takes daily rainfall accumulations from COOP stations and outputs maximum one day and two day rainfall. 52 COOP 
stations were selected in an attempt to fully cover all counties in the CWA as well as have mutliple in metropolitan areas such 
as Austin and San Antonio. (Named COOP Rainfall Totals)

A script that reads in all .csv files containing local maxima from COOP stations and outputs the global maximum from these values
as well as the station this maximum was recorded at. This script is almost complete. (Named Maximum Rainfall)

LCRA Rainfall is used to estimated total rainfall throughout a given area using quadrangles created by the Lower Colorado River
Authority. 
They have collected rainfall data since 1940 and have monthly tables for rainfall and evaporation available at their 
[website](http://www.twdb.texas.gov/surfacewater/conditions/evaporation/)

We selected quadrangles that were over two-thirds covered by area in our county warning area (CWA). Output is rainfall estimations 
for our CWA area. (Named LCRA Rainfall)

Quadrangles used in calculation for our CWA:
- 709
- 710
- 807
- 808
- 809
- 810
- 908

Quadrangles used elsewhere:
- 606
- 607
- 706
- 707
- 708
- 811
- 910
- 1010

Another possible method of estimating total rainfall is through use of climate divisions (CDs). Each state is divided into climate
divisions and total monthly and seasonal rainfall is calculated for each climate division in the National Weather Service's Local
Climate Analysis Tool (LCAT). A fraction of a CWA can be found inside of each CD then multiplied by the CD's rainfall and summed 
for all CDs of interest. 


LCRA vs. CD is a script that I wrote before doing a Wilcoxon Signed Ranks Test to determine if there is a statistically significant
difference between gathering rainfall accumulations using LCRA 1 degree latitude by 1 degree longitude quadrangles or by using 
the Climate Divisions.This test was done at the 95% significance level, was a two-tailed test, and used a large sample
approximation.

## Snowfall

COOP Stations also record snowfall and snow depth, which could be useful for winter weather. However, snowfall measurements should 
be  made sure not to be related to severe weather days, as melted hail accumulations is recorded as snowfall.

## Tropical Weather


# Some Code Explanations

The Pandas module is a very powerful, yet easy to use, module for data analysis using tabular data. All of the data used in 
this research was either in tabular format directly from a URL or imported in from an existing .csv file. Output is also in .csv
format which can easily be converted to .xlsx for further analysis, such as statistics. Below I will briefly discuss a few 
lines of code I utilized very often. Pandas documentation is also very accessible and helpful through a simple Google search.

## Reading in a .csv file
```
Table = pd.read_csv('C:\Users\Ty Dickinson\Downloads\SevereStormsUpdated.csv', low_memory=False)
Table['BEGIN_DATE'] = pd.to_datetime(Table.BEGIN_DATE)
```

The first line sets the .csv file from the specified path as a variable called Table. By doing this, you can easily call
specific columns of data, like in line 2 where I access the column labeled BEGIN_DATE. 
This second line converts that whole column from the default datatype object to a Pandas datatype called datetime. This is an
amazing function and allows dates to easily be analyzed later. This conversion is very powerful as Pandas can automatically 
recognize the format of the date (and time, if it is in the same column) regardless if it uses slashes or dashes. 

## Separating the Entire Table into Seasons
```
df = Table.set_index(['BEGIN_DATE'])
Date1 = '12-01-1980'
Date2 = '02-28-1981'
Date1 = pd.to_datetime(Date1)
Date2 = pd.to_datetime(Date2)
x = df.loc[Date1:Date2]
```

By default, when tabular data is read into the program, it in indexed from 0 to n-1, where n is the number of rows in the original
file. The first line above sets the index to instead be the BEGIN_DATE column. This allows me to use the .loc function. Dates 1 
and 2 are defined and converted to a datetime format to be used in the .loc. The last line sets the variable x to be the portion
of the file that is between those two dates (both dates are included). 

## Running the Script Through Seasons for Several Years
```
WinterCount = 0
while WinterCount <= 30:
    x = df.loc[Date1:Date2]
    if Date2.is_leap_year:
        Date2 = Date2 - pd.DateOffset(days=1)
    Date1 = Date1 + pd.DateOffset(years=1)
    Date2 = Date2 + pd.DateOffset(years=1)
    if Date2.is_leap_year:
        Date2 = Date2 + pd.DateOffset(days=1)
    WinterCount = WinterCount + 1
```

The While statement is set while WinterCount is less than or equal to 30, for all the winter seasons of interest in our 
time period. 
pd.DateOffset is used in lines 6 and 7 to add one year to Dates 1 and 2 so that the next time the while statement runs, 
the boundaries are Dec. 1981 and Feb. 1982 instead of 1980 and 1981, respectively. 
Pandas has a very helpful function called is_leap_year that looks at the year of a date and will return True or False if the
year is a leap year or is not a leap year. Line 8 says that if Date 2 is a leap year (so, if True was returned) then to 
add 1 day (line9) so that Feb. 29 is not missed. Lines 4 and 5 do the same but after all the calculations are made based on
the data in the file so that adding a year to Date 2 does not return an error (cannot have a Feb. 29 in a non-leap year).

## Creating a Pandas Dataframe and Exporting to a .csv 
```
df1 = pd.DataFrame({'Winter Reports': WinterReports})
df2 = pd.DataFrame({'Spring Reports': SpringReports})
df3 = pd.DataFrame({'Summer Reports': SummerReports})
df4 = pd.DataFrame({'Fall Reports': FallReports})
dftot = pd.concat([df1, df2, df3, df4], axis=1)
dftot.to_csv('Severe Weather Impacts.csv')
```

A Pandas dataframe is a 2-Dimensional data structure. I like to think of them as parts of a spreadsheet. 
The first four lines create dataframes based on lists created earlier in the script (WinterReports, Spring Reports, etc) and
also give them a column header name in quotes ('Winter Reports'). pd.concat concatenates the dataframes together into columns
(axis=1 concatenates them into columns; axis=0 would concatenate them into rows). 
Finally, this large dataframe is then exported to a .csv that can be downloaded and is titles Severe Weather Impacts.csv
