#!/bin/env/python
'''
## [Author]: @delta_kiloz
##-------------------------------------------------------------------------------------------------------------
## [Details]:
## This script was written based on Adam Khoo's Stock Trading Course level 2 (Market Snapper) and his
## momentum stock trading strategy that he describes in the course. The intent was to automate the use of
## the free FinViz website so that you're able to easily import the identified stocks into your trading
## platform's watchlist for future screening.
##-------------------------------------------------------------------------------------------------------------
## [Warning]:
## This script comes as-is with no promise of functionality or accuracy.  I strictly wrote it for personal use
## I have no plans to maintain updates, I did not write it to be efficient and in some cases you may find the
## functions may not produce the desired results so use at your own risk/discretion.
##-------------------------------------------------------------------------------------------------------------
## [Modification, Distribution, and Attribution]:
## You are free to modify and/or distribute this script as you wish.  I only ask that you maintain original
## author attribution and not attempt to sell it or incorporate it into any commercial offering.
##-------------------------------------------------------------------------------------------------------------
## [Prerequisite Requirements]:
## pip install rich
## pip install finvizlite
'''

import finvizlite as fl
from time import strftime
from time import sleep
from subprocess import Popen
from rich.console import Console
import os.path
import sys

# initialize the Console() class
console = Console()

console.print("[] Initiating FinViz Screener scraper.", style = "red")

# Formats the date string that will be appended to the end of the filename
timestr = strftime("_%Y%m%d")

# Base URL that will be used for scraping; URL was pulled after building the query directly
# from the FinViz website's Screener GUI. The screening criteria are as follows:
# Above 50 SMA; Above 200 SMA; Price > 2$; Avg Volume > 200k; ESP This Year > 10%; ESP qtr over qtr > 10%;
# Sales qtr over qtr > 10%; Current Volume > 200k.
df = fl.scrape("https://finviz.com/screener.ashx?v=111&f=fa_epsqoq_o10,fa_epsyoy_o10,fa_salesqoq_o10,sh_avgvol_o200,sh_curvol_o200,sh_price_o2,ta_sma200_pa,ta_sma50_pa")

# Formats hte filename and creates the .csv file the data will be written to
file = "High-Momo-Stocks" + timestr + ".csv"

# Check to see if the file already exists, that way it won't be over written. If it does exist, you need to either
# move or delte the file from the current directory so that the new file can be created and written to.
if os.path.isfile(file) == True:
    console.print("[] File already exists, please delete file then re-run the program.", style="red")
    sleep(0.05)
    sys.exit("[] Exiting program.")

# Notifying user what the .csv filename will be.
console.print("[]", style = "red")
console.print("[] Writing data to: ", file, style="red")
df.to_csv(file, mode="a", index=False)

# Because the webpage will only allow 20 rows to be viewed at a time with a free account, this
# will iterate through each page of 20 rows and will be returned from your original query. With
# each iteration, it will append the data to the same .csv file that was originall created.
count = 0
while (len(df.index) > 1):
    count = count + 2
    df = fl.scrape("https://finviz.com/screener.ashx?v=111&f=fa_epsqoq_o10,fa_epsyoy_o10,fa_salesqoq_o10,sh_avgvol_o200,sh_curvol_o200,sh_price_o2,ta_sma200_pa,ta_sma50_pa&r=" +str(count) + "1")

    # Prevents the last row from being written twice in the .csv file.
    if (len(df.index) < 2):
        break
    df.to_csv(file, mode="a", header=False, index=False)

console.print("[] Scraping completed!", style = "green")

# Open the .csv file in Excel to inspect the results.
Popen(file, shell=True)