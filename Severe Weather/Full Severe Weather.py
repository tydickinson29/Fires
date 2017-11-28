#GOAL: To analyze severe weather storm reports for the creation
#of impact-based seasonal verification index
#INPUT: .csv file containing observed storm reports
#OUTPUT: Ranks of a 30-year climatology where 1 is the most impactful
#year and 30 is the least impactful year

#Authors: Ty Dickinson, Brian Tomiuk
#Additional collaborator: Justin Stipe



import pandas as pd
from collections import OrderedDict
#define an ordered dictionary to use if user wants output in csv
csvdict = OrderedDict()

#import the raw storm reports file and convert dates to a datetime format
Table = pd.read_csv('C:\Users\Ty Dickinson\Downloads\SevereStormsUpdated.csv', low_memory=False)
Table['BEGIN_DATE'] = pd.to_datetime(Table.BEGIN_DATE)

#adding new columns based on adjustments from existing columns
Table['Total_Damages'] = Table['DAMAGE_PROPERTY_NUM'] + Table['DAMAGE_CROPS_NUM']
Table['Z_Time'] = Table['BEGIN_TIME']
Table['Z_Day'] = Table['BEGIN_DATE']

pd.options.mode.chained_assignment = None

#ensuring that a blank cell is read as a 0 for later addition.
for i in range(0, len(Table.TOR_LENGTH)):
    if Table.TOR_LENGTH[i] == ' ':
        Table.TOR_LENGTH[i] = 0.0
for i in range(0, len(Table.TOR_WIDTH)):
    if Table.TOR_WIDTH[i] == ' ':
        Table.TOR_WIDTH[i] = 0.0
for i in range(0, len(Table.MAGNITUDE)):
    if Table.MAGNITUDE[i] == ' ':
        Table.MAGNITUDE[i] = 0.0
Table.fillna(value=0, inplace=True)

Table.TOR_LENGTH = Table.TOR_LENGTH.astype(float)
Table.TOR_WIDTH = Table.TOR_WIDTH.astype(float)
Table.DEATHS_DIRECT = Table.DEATHS_DIRECT.astype(int)
Table.INJURIES_DIRECT = Table.INJURIES_DIRECT.astype(int)
Table.MAGNITUDE = Table.MAGNITUDE.astype(float)
Table.BEGIN_TIME = Table.BEGIN_TIME.astype(int)

#converting CST to Z
for i in range(0, len(Table.BEGIN_TIME)):
    if Table.BEGIN_TIME[i] <= 1759:
        Table.Z_Time[i] = Table.BEGIN_TIME[i] + 600
        Table.Z_Day[i] = Table.BEGIN_DATE[i]
    else:
        Table.Z_Time[i] = (Table.BEGIN_TIME[i] + 600) - 2400
        Table.Z_Day[i] = Table.BEGIN_DATE[i] + pd.DateOffset(days=1)

#defining beginning and end dates
DateDJF1 = pd.to_datetime('12-01-1980')
DateDJF2 = pd.to_datetime('02-28-1981')
DateJFM1 = pd.to_datetime('01-01-1981')
DateJFM2 = pd.to_datetime('03-31-1981')
DateFMA1 = pd.to_datetime('02-01-1981')
DateFMA2 = pd.to_datetime('04-30-1981')
DateMAM1 = pd.to_datetime('03-01-1981')
DateMAM2 = pd.to_datetime('05-31-1981')
DateAMJ1 = pd.to_datetime('04-01-1981')
DateAMJ2 = pd.to_datetime('06-30-1981')
DateMJJ1 = pd.to_datetime('05-01-1981')
DateMJJ2 = pd.to_datetime('07-31-1981')
DateJJA1 = pd.to_datetime('06-01-1981')
DateJJA2 = pd.to_datetime('08-31-1981')
DateJAS1 = pd.to_datetime('07-01-1981')
DateJAS2 = pd.to_datetime('09-30-1981')
DateASO1 = pd.to_datetime('08-01-1981')
DateASO2 = pd.to_datetime('10-31-1981')
DateSON1 = pd.to_datetime('09-01-1981')
DateSON2 = pd.to_datetime('11-30-1981')
DateOND1 = pd.to_datetime('10-01-1981')
DateOND2 = pd.to_datetime('12-31-1981')
DateNDJ1 = pd.to_datetime('11-01-1981')
DateNDJ2 = pd.to_datetime('01-31-1982')

#The next block takes user input for the rolling 3 month periods
#they want to analyze. Months is a list containing possible
#good user inputs; request is a list that user input is put into

months = ['DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ',
         'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ']
request = []
prompt = 'Enter the 3 month periods you want (only the first): '
x=1
while True:
    #initial user input;input is converted to capitals
    request.insert(0,str(raw_input(prompt)).upper())
    while True:
        #prompting user for additional 3 month periods
        request2 = str(raw_input('Any others? If none, type n/a ').upper())
        if request2 != 'N/A':
            #adds more periods into the list if the input is not n/a
            request.insert(x,request2)
            x += 1
            #continue makes the boolean stay True, nested while runs again
            continue
        else:
            #user inputs n/a, nested while statement breaks
            break
    try:
        for i in range(0,len(request)):
            #ensures user input matches possible 3 month periods
            y = months.index(request[i])
    except ValueError:
        #if entry is invalid, first while is run again
        print('One of the entries was not a valid 3 month period. Try again.')
        request = []
        continue
    else:
        #if all inputs are good, initial while is broken
        break

#prompting user asking if output should be printed or exported
outputq = '''Do you want the ranks printed or saved as a .csv?
          Type print or csv '''

while True:
    output = raw_input(outputq).upper()
    if output == 'PRINT':
        mode = 1
        break
    elif output == 'CSV':
        mode = 2
        break
    else:
        print('Invalid input. Type print or csv. ')
        continue

csvlist = []
csvlistname = []
#Overarching function to analyze storm reports
def Analysis(first, last, mode, name='DJF'):
    #Defining lists to use for each indicator
    Reports = []
    Death = []
    Injury = []
    Cost = []
    ReportDaysList = []
    TornadoWidth = []
    TornadoTrack = []
    HailMax = []
    WindMax = []


    #setting the index as date to use the df.loc expression
    df = Table.set_index(['BEGIN_DATE'])
    Count=0
    #while statements to cycle through seasons and calculate reports, report days, fatalities, injuries
    #damages, maximum hail size, maximum wind magnitude, maximum tornado width, and total tornado path length
    while Count <= 29:
        #filters whole table into only the parts between first and last dates
        x = df.loc[first:last]

        #filters the seasonal subset-table into data about the event types
        maxes = x.groupby(['EVENT_TYPE']).max()

        #the overall number of reports is just how many rows the table has
        Reports.insert(Count,len(x.index))

        #next few lines are simply sums of columns
        y = x.DEATHS_DIRECT.sum()
        Death.insert(Count,y)
        z = x.INJURIES_DIRECT.sum()
        Injury.insert(Count,z)
        a = x.TOR_LENGTH.sum()
        TornadoTrack.insert(Count,a)

        if not len(x.index) == 0 :
            #finds the max value as long as there are some reports
            b = max(x.TOR_WIDTH)
            TornadoWidth.insert(Count,b)
        else:
            TornadoWidth.insert(Count,0)
        c = x.Total_Damages.sum()
        Cost.insert(Count,c)

        #These try statements are for finding the maximum magnitude for wind and hail.
        #If there are no wind/hail reports, a KeyError is raised and then its value in the list is 0
        #If there are no reports for the season at all, the values are set at 0 in the else block
        try:
            if not len(x.index) == 0:
                d = maxes.MAGNITUDE['Hail']
                HailMax.insert(Count,d)
            else:
                HailMax.insert(Count,0)
        except KeyError:
            HailMax.insert(Count,0)

        try:
            if not len(x.index) == 0:
                d = maxes.MAGNITUDE['Thunderstorm Wind']
                WindMax.insert(Count,d)
            else:
                WindMax.insert(Count,0)
        except KeyError:
            WindMax.insert(Count,0)

        ReportDays = 1
        #nested if statements to calculate report days based on 12Z to 12Z the next day as 1 day
        if len(x.index) == 0:
            ReportDaysList.insert(Count, 0)
        else:
            for j in range(1, len(x.index)):
                if ((x.Z_Day[j] == x.Z_Day[j-1]) and ((x.Z_Time[j] < 1200) and (x.Z_Time[j-1] < 1200))):
                    continue
                elif ((x.Z_Day[j] == x.Z_Day[j-1]) and ((x.Z_Time[j] >= 1200) and (x.Z_Time[j-1] >= 1200))):
                    continue
                elif (x.Z_Day[j] == (x.Z_Day[j-1] + pd.DateOffset(days=1))) and ((x.Z_Time[j] < 1200) and (x.Z_Time[j-1] >= 1200)):
                    continue
                else:
                    ReportDays = ReportDays + 1
            ReportDaysList.insert(Count, ReportDays)
        if (last.is_leap_year) and (last.month == 2):
            last = last - pd.DateOffset(days=1)
        #adds a year to the end date range for the next cycle of the while statement
        first = first + pd.DateOffset(years=1)
        last = last + pd.DateOffset(years=1)
        #if the upcoming year is a leap year, add 1 day to account for Feb. 29
        if (last.is_leap_year) and (last.month == 2):
            last = last + pd.DateOffset(days=1)
        Count = Count + 1

    #Create dataframes for each list
    df1 = pd.DataFrame({name+' Reports': Reports})
    df2 = pd.DataFrame({name+' Report Days': ReportDaysList})
    df3 = pd.DataFrame({name+' Fatalities': Death})
    df4 = pd.DataFrame({name+' Injuries': Injury})
    df5 = pd.DataFrame({name+' Tornado Track': TornadoTrack})
    df6 = pd.DataFrame({name+' Damages': Cost})
    df7 = pd.DataFrame({name+' Largest Hail': HailMax})
    df8 = pd.DataFrame({name+' Strongest Wind': WindMax})
    df9 = pd.DataFrame({name+' Widest Tornado': TornadoWidth})

    #concatenate the dataframes together
    dftot = pd.concat([
        df1, df2, df3, df4,
        df5, df6, df7, df8, df9
        ], axis=1)

    #function used to make column of fatalities/injuries blend
    def blend(x,y):
        return x + (y/100.)

    #function to sum the indicators' ranks
    def Sum(a,b,c,d,e,f,g,h):
        return a+b+c+d+e+f+g+h

    #used to multiply inflation factor with unadjusted damages
    def multiply(x,y):
        return x*y

    #reads in the .csv containing 3 month inflation factors to 2010 levels
    #and then calls multiply to adjust damage figures
    def inflation(x, name='DJF'):
        inflator = pd.read_csv('C:\\Users\\Ty Dickinson\\Downloads\\InflationCalculator.csv')
        return multiply(inflator[name],x)

    #Creation of new columns in the dataframe with rank analysis
    #first line creates the blend with the .apply function acting to go row by row
    dftot['Fatalities Blend'] = dftot.apply(lambda x: blend(x[name+' Fatalities'], x[name+' Injuries']),axis=1)

    #calling the inflation function to make adjusted damages column
    dftot['Adjusted'] = inflation(dftot[name+' Damages'], name)

    #next 8 lines perform rank analysis on our 8 indicators
    dftot['Reports'] = dftot[name+' Reports'].rank(ascending=False)
    dftot['Days'] = dftot[name+' Report Days'].rank(ascending=False)
    dftot['Blend'] = dftot['Fatalities Blend'].rank(ascending=False)
    dftot['Damages'] = dftot['Adjusted'].rank(ascending=False)
    dftot['Track'] = dftot[name+' Tornado Track'].rank(ascending=False)
    dftot['Hail'] = dftot[name+' Largest Hail'].rank(ascending=False)
    dftot['Wind'] = dftot[name+' Strongest Wind'].rank(ascending=False)
    dftot['Width'] = dftot[name+' Widest Tornado'].rank(ascending=False)

    #making a new column; adds rank values of 8 indicators
    dftot['Sum'] = dftot.apply(lambda x: Sum(x['Reports'], x['Days'],
                                            x['Blend'], x['Damages'],
                                            x['Track'], x['Hail'], x['Wind'],
                                            x['Width']),axis=1)
    #rank analysis on indicator sums
    dftot['Rank'] = dftot['Sum'].rank()

    #sets index as climatology
    years = range(1981,2011)
    dftot = dftot.set_index([years])

    #end output dependent on what the user chose
    if mode == 1:
        print(name)
        print(dftot['Rank'])
    if mode == 2:
        csvlist.insert(i,dftot['Rank'])
        csvlistname.insert(i,name)
        if i == (len(request))-1:
            for m in range(0,len(request)):
                #creates the dictionary from the two lists of unknown sizes
                csvdict[csvlistname[m]] = (csvlist[m])
            finaloutput = pd.DataFrame(csvdict)
            finaloutput.to_csv('C:/Users/Ty Dickinson/Downloads/FullRanks.csv')
    return


#for loop to run the Analysis function however many times the user entered
#periods for; date range is specified and used as parameters for the function
#based on the input that is stored in the request list
for i in range(0,len(request)):
    if request[i] == 'DJF':
        begin = DateDJF1
        end = DateDJF2
        name = 'DJF'
    elif request[i] == 'JFM':
        begin = DateJFM1
        end = DateJFM2
        name = 'JFM'
    elif request[i] == 'FMA':
        begin = DateFMA1
        end = DateFMA2
        name = 'FMA'
    elif request[i] == 'MAM':
        begin = DateMAM1
        end = DateMAM2
        name = 'MAM'
    elif request[i] == 'AMJ':
        begin = DateAMJ1
        end = DateAMJ2
        name = 'AMJ'
    elif request[i] == 'MJJ':
        begin = DateMJJ1
        end = DateMJJ2
        name = 'MJJ'
    elif request[i] == 'JJA':
        begin = DateJJA1
        end = DateJJA2
        name = 'JJA'
    elif request[i] == 'JAS':
        begin = DateJAS1
        end = DateJAS2
        name = 'JAS'
    elif request[i] == 'ASO':
        begin = DateASO1
        end = DateASO2
        name = 'ASO'
    elif request[i] == 'SON':
        begin = DateSON1
        end = DateSON2
        name = 'SON'
    elif request[i] == 'OND':
        begin = DateOND1
        end = DateOND2
        name = 'OND'
    elif request[i] == 'NDJ':
        begin = DateNDJ1
        end = DateNDJ2
        name = 'NDJ'

    Analysis(begin,end,mode,name)
