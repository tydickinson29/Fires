This is the folder dedicated to severe weather, the most analyzed of the hazards here.

Script 'Severe Weather' was the first one written and only analyzes the initial
seasons of DJF, MAM, ASO, and SON.

Script 'Rolling 3 Month Severe Weather' is simply the initial script expanded
to account for all 3 month periods. The end output of these scripts is a .csv
containing all of the indicators' raw values for each season of each year.

Script 'Full Severe Weather' does all of the analysis. In the beginning, we used
Excel to perform get the ranks of the indicators and thus the years. This script
adds on to the previous scripts and the end output is the final ranks to divide
into terciles. This output can either be printed or exported to a .csv; the user
will be prompted to input the seasons they want as well as the format of the
output.
