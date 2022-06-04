import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

###############################
# Categorical data
###############################

# Task: Compare four categories of housing and their prices in two regions of the UK.

categoricalData = pd.read_csv("Data/Average-prices-Property-Type-2021-05_wrangled.csv")

# Date type converting & sorting
categoricalData["Date"] = pd.to_datetime(categoricalData["Date"])
categoricalData.sort_values(by="Date", ascending=True, inplace=True)
categoricalData.reset_index(inplace=True)
categoricalData = categoricalData.drop(["index"], axis=1)

# Data from 2020
dF2020 = categoricalData[categoricalData["Date"].dt.year == 2020]
dF2020 = dF2020.drop(["Date"], axis=1)

# Values from London sorted by average price
valsLondon = dF2020[dF2020["Region_Name"].str.contains("London")]
valsLondon = valsLondon.drop(["Region_Name"], axis=1)
valsLondon.sort_values(by="averagePrice", ascending=False, inplace=True)

# Values from Newcastle sorted by average price
valsNewcastle = dF2020[dF2020["Region_Name"].str.contains("Newcastle")]
valsNewcastle = valsNewcastle.drop(["Region_Name"], axis=1)
valsNewcastle.sort_values(by="averagePrice", ascending=False, inplace=True)

index = ['Detached', 'Semi Detached', 'Terraced', 'Flat']

###############################
# Numerical data
###############################

# Task: Compare the relationship between broadband upload and download speeds in all regions of the UK,
# demonstrate the strength of this relationship with a correlation calculation and a regression line.
# Highlight one or two regions that stand out that are of interest for you.

numericalData = pd.read_csv("Data/202006_fixed_laua_performance_wrangled.csv")

# Data with average values
averageDf = numericalData.drop(["medDown"], axis=1).drop(["medUpload"], axis=1)
# medDf = numericalData.drop(["averageDown"], axis=1).drop(["averageUpload"], axis=1)

# x - average download speed, y - average upload speed
avX = averageDf.averageDown
avY = averageDf.averageUpload

# mX = medDf.medDown
# mY = medDf.medUpload

# correlation coefficient
r = avX.corr(avY)

# Standard deviation
stdDown = avX.std()
stdUpload = avY.std()

# Mean
meanDown = avX.mean()
meanUpload = avY.mean()

###############################
# Time Series data / Financial
###############################

# Task: Demonstrate how a time series is presented, include at least one type of additional information
# that is of relevance to share trading decisions

financialData = pd.read_csv("Data/ftse_data_wrangled.csv")

# Date type converting
financialData["date"] = pd.to_datetime(financialData["date"])

# Taking data only from 2020
financialData = financialData[(financialData['date'] > '2020-01-01') & (financialData['date'] < '2020-12-31')]

# Data
openData = financialData.Open
highData = financialData.High
lowData = financialData.Low
closeData = financialData.Close

# Average line
y_mean = [closeData.mean()]*len(financialData.date)

################################################
# Pyplot
################################################
plt_x = 2
plt_y = 2

# Resolution: 1920x1080
plt.figure(num=None, figsize=(plt_x*8, plt_y*4.5), dpi=120, facecolor='w', edgecolor='k', tight_layout='true')

###############################
# House Pricing Graph
###############################
plt.subplot(plt_x, plt_y, 1)

w = 0.3
bar1 = [0, 1, 2, 3]
bar2 = [i+w for i in bar1]

plt.bar(bar1, valsLondon.averagePrice, w, label='London', color='#fc8d62')
plt.bar(bar2, valsNewcastle.averagePrice, w, label='Newcastle upon Tyne', color='#8da0cb')
plt.xticks(bar1, index)

plt.legend()
plt.ylabel("Value in British pounds GBP (1000s)", fontsize='11')
plt.xlabel("Housing categories", fontsize='11')
plt.title("Regional comparison of four housing categories \n by their price in the UK 2020", fontname="Times New Roman",
          fontsize=15, fontweight='bold')

# Y-axis formatter
plt.ylim(0, 1000000)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x*0.001), ',')))

plt.grid(which="major", axis='y', color='black',  alpha=0.1, linewidth=0.5, zorder=10)

###############################
# Broadband Data Graph
###############################
plt.subplot(plt_x, plt_y, 2)

# Limit for outliers detection
limitDown = stdDown * 2
limitUpload = stdUpload * 2

# Thresholds
min_thresholdDown = meanDown - limitDown
max_thresholdDown = meanDown + limitDown

min_thresholdUpload = meanUpload - limitUpload
max_thresholdUpload = meanUpload + limitUpload

# Scatter plot & marking outliers
check = 0
for x, y in zip(avX, avY):
    color = '#8da0cb'
    label = None
    if not min_thresholdDown <= x <= max_thresholdDown:
        color = '#fc8d62'
        label = 'Outstanding regions'
        check += 1
    elif not min_thresholdUpload <= y <= max_thresholdUpload:
        color = '#fc8d62'
        label = 'Outstanding regions'
        check += 1

    plt.scatter(x, y, color=color, label=label if check == 1 else "")


plt.grid(which="major", axis='y', color='black',  alpha=0.1, linewidth=0.5, zorder=0)

# Regression line
gradient, intercept = np.polyfit(avX, avY, 1)
plt.plot(avX, gradient*avX + intercept, zorder=30, color="#1f78b4", label="Regression line")

# 45 degree line
plt.axline([1, 1], [2, 2], linestyle=(0, (1, 3)), color="black", alpha=0.2)

# Limits
plt.xlim(-1, 170)
plt.ylim(-1, 170)

plt.legend(loc='best')
plt.xlabel("Average download speed (Mbit/s)", fontsize='11')
plt.ylabel("Average upload speed (Mbit/s)", fontsize='11')
plt.title("Correlation of broadband upload and download speeds \n in all regions of the UK, " + "r = "
          + "{:2.2f}".format(r), fontname="Times New Roman", fontsize=15, fontweight='bold')

###############################
# Financial Data Graph
###############################
plt.subplot(plt_x, plt_y, 3)

# Bollinger bands
sma = closeData.rolling(7).mean()
std = closeData.rolling(7).std()

# Calculate top and bottom band
bollUp = sma + std * 2.0
bollDown = sma - std * 2.0

# Mean
plt.plot(financialData.date, y_mean, label='Mean', linestyle='-.', color='black', alpha=0.3)

# Top and Bottom bands
plt.plot(financialData.date, bollUp, linestyle="--", color="#66c2a5", label="Top band")
plt.plot(financialData.date, bollDown, linestyle="--", color="#fc8d62", label="Bottom band")

# Close Price
plt.plot(financialData.date, closeData, color='#1f78b4', label="Close price")

plt.grid(which="major", axis='y', color='black',  alpha=0.1, linewidth=0.5, zorder=0)
plt.grid(which="major", axis='x', color='black',  alpha=0.1, linewidth=0.5, zorder=0)

# Y-axis formatter
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

plt.legend(loc='best')
plt.xlabel("Date & Time", fontsize='11')
plt.ylabel("Price of stock", fontsize='11')
plt.title("FTSE 100 Closing Price \n along with auxiliary Bollinger bands in 2020",
          fontname="Times New Roman", fontsize=15, fontweight='bold')

###############################
# Narrative
###############################
plt.subplot(plt_x, plt_y, 4)

plt.text(0.02, 0.15, 'I. \n In the first graph we can see that real estate prices in the capital of Great Britain are much '
                    '\n higher than in the distant northern city of Newcastle. We can also see a sequence of prices, \n '
                    'independent of the region, among the types of housing, where the order goes from the \n most '
                    'expensive type of "Detached" and in turn: "Semi Detached", "Terraced", "Flat". \n\nII.\n'
                    ' Based on the second top graph, we can conclude that the correlation between download \n '
                    'and upload speeds across regions of the UK is weak. There are regions where the speeds \n '
                    'differ significantly from each other. However, despite the prominent areas, in most cases, \n '
                    'the speeds tend to move and increase depending on each other. \n\nIII. \n '
                    'By looking at the last chart, we can say that after the start of the global pandemic in 2020, \n '
                    'the UK suffered some financial losses, but by the end of the year, the market was able to \n '
                    'stabilize and began to grow slightly.'
                    '', fontsize=10)
plt.title("Narrative",  fontname="Times New Roman", fontsize=15,  fontweight='bold')
plt.tick_params(
    axis='both',
    which='both',
    bottom=False,
    left=False,
    top=False,
    labelbottom=False,
    labelleft=False
)

# Image export
plt.savefig('Coursework.png')

plt.show()
