# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# USER INPUT -- Displaying the Top # (max) and Bottom # (min) of Player Goal Norms on Plot
inp = input("\n\nWhich Goal Results would you like to display on the plot? (All, Top, Bottom)\nNote: Only players with shot attempts over 25th percentile are considered.\n\nEnter option: ")

if inp == "Top":
    max = int(input("\n\nIndicate the # of Players you want to show for Top _ (for example: enter '3' for Top 3)?\nNote: Values only from 1-10 are acceptable.\n\nEnter value: "))
elif inp == "Bottom":
    min = int(input("\n\nIndicate the # of Players you want to show for Bottom _ (for example: enter '3' for Bottom 3)?\nNote: Values only from 1-10 are acceptable.\n\nEnter value: "))


# List of Name Corrections
NameCorr = {                    
    "Appa": "Paul's Dad",
    "KyungSoo": "Kyung Soo",
    "KChung": "Kevin Chung",
    "KCamal": "Kevin Camal"
    }

oldNames = list(NameCorr)                                   # old names from NameCorr dictionary
newNames = list(NameCorr.values())                          # new names from NameCorr dictionary


# Import CSV File containing Master Shot Data
data = pd.read_csv ('fullDataSet.csv')

p = np.unique(data.Player)                                  # distinct list of ALL players that played at least once (in string format)
nPlayers = len(p)                                           # total number of players in league

playersCorr = [p[i] for i in range(nPlayers)]               # initialize Corrected Player Name (for display) list to "players" list

# Replacing old names to display names
for j in range(len(oldNames)):
    for i in range(len(playersCorr)):
        if playersCorr[i] == oldNames[j]:
            playersCorr[i] = newNames[j]


# Calculating the Average of Video Numbers within All Game Footage (typically its 1-7, probably one or two of them are 1-8 or 2-8)
vNumAvg = np.average(data.VNum)



# Initialize all Arrays for For Loop
# Note: e = "early" = 1H = 1st Half, l = "late" = 2H = 2nd Half
colNames = ['1H Goals (eg)', '1H Attempts (ea)', '2H Goals (lg)', '2H Attempts (la)', 'Total Attempts (a)', 'Total Goals (g)', 'Norm of 1H and 2H Goals']
colLen = len(colNames)

eg, ea, lg, la, a, g, norm = (np.zeros(nPlayers) for i in range(colLen))


# Calculate the Following for Each Player
for i in range(nPlayers):
    eg[i] = sum((data.Player == p[i]) & (data.ShotResult == 'Y') & (data.VNum < vNumAvg))           # Total No. of Early Game (1H) Goals
    ea[i] = sum((data.Player == p[i]) & (data.VNum < vNumAvg))                                      # Total No. of Early Game (1H)Shot Attempts
    lg[i] = sum((data.Player == p[i]) & (data.ShotResult == 'Y') & (data.VNum > vNumAvg))           # Total No. of Late Game (2H) Goals
    la[i] = sum((data.Player == p[i]) & (data.VNum > vNumAvg))                                      # Total No. of Late Game (2H) Shot Attempts
    a[i] = sum((data.Player == p[i]))                                                               # Overall No. of Shot Attempts
    g[i] = sum((data.Player == p[i]) & (data.ShotResult == 'Y'))                                    # Overall No. of Goals
    norm[i] = np.sqrt(np.square(eg[i]) + np.square(lg[i]))                                          # Calculate norm of 1H Goals and 2H Goals


# Data Type Conversion to Integer Format for Arrays
eg = [int(i) for i in eg]
ea = [int(i) for i in ea]
lg = [int(i) for i in lg]
la = [int(i) for i in la]
a = [int(i) for i in a]
g = [int(i) for i in g]
norm = [int(i) for i in norm]


# Average Goal Percentages for Early Game [1H] (eavg) and Late Game [2H] (lavg) Goals
egavg = np.average(eg)
lgavg = np.average(lg)

# Finding 25th Percentile for Total Shot Attempts (This is to weed out players that have less shot attempts than the 25% mark of the overall league) -- for DISPLAY purposes
per25 = np.percentile(a,25)



p25 = np.transpose([j for (i,j) in zip(a,playersCorr) if i > per25])       # Array of Players with Shot Attempts over 25th percentile [CORRECTED NAMES]
norm25 = np.transpose([j for (i,j) in zip(a,norm) if i > per25])           # Array of Norms of Players with Shot Attempts over 25th percentile
eg25 = np.transpose([j for (i,j) in zip(a,eg) if i > per25])            # Array of Early-Game (1H) Goals of Players with Shot Attempts over 25th percentile
lg25 = np.transpose([j for (i,j) in zip(a,lg) if i > per25])            # Array of Late-Game (2H) Goal % of Players with Shot Attempts over 25th percentile


# Note: Finding Top # and Bottom # within the Players that have Shot Attempts over 25th Percentile (ONLY IF ALL is not selected by user)
if inp == "Top":
    ind = np.argpartition(norm25,-max)[-max:]                                   # Finding the Indices of Players with Top # (max) Norm Values
elif inp == "Bottom":
    ind = np.argpartition(norm25,min)[:min]                                     # Finding the Indices of Players with Bottom # (min) Norm Values

ind_med = np.argpartition(norm25, len(norm25) // 2)[len(norm25) // 2]           # Finding the Index of Player with MEDIAN norm value



# SCATTER PLOT
plt.figure(figsize=(15,9))
plt.scatter(eg, lg, s=np.multiply(a,3), c=g, cmap = 'Blues', alpha=0.8, edgecolors='black')     # Plotting every Players' data point but only displaying Names over 25th Percentile


# If "All" is selected for input, display ALL player name data labels that have shot attempts over 25th percentile count
if inp == "All":
    for i in range(len(p25)):
        plt.text(eg25[i],lg25[i],p25[i],fontsize=9)
# If "Top" or "Bottom" is selected for input, display the corresponding player name data labels
else:
    for i in ind:
        plt.text(eg25[i],lg25[i],p25[i], fontsize=9)



# Plot Lines displaying the AVERAGE early game (1H) and late game (2H) goal counts
h = plt.hlines(lgavg,xmin=-5, xmax=np.max(eg)+5, colors="black", linestyles='dashed', alpha=0.35)
v = plt.vlines(egavg,ymin=-5, ymax=np.max(lg)+5, colors="black", linestyles='dashed', alpha=0.35)


# Setting x-axis and y-axis limits
plt.xlim(-3,np.max(eg)+3)
plt.ylim(-3,np.max(lg)+3)
plt.xticks(np.arange(0,np.max(eg)+3,5))

# Plot Color Bar for # of Goals Scored
cbar = plt.colorbar()
cbar.set_label('# of Goals Scored')


if inp == "All":
    plt.title(f'1st-Half vs 2nd-Half Goal Impact\nDisplaying [{inp}] Players**',weight='semibold',pad=15)
elif inp == "Top":
    plt.title(f'1st-Half vs 2nd-Half Goal Impact\nDisplaying Players** within [{inp} {max}] Overall Goal %',weight='semibold',pad=15)
elif inp == "Bottom":
    plt.title(f'1st-Half vs 2nd-Half Goal Impact\nDisplaying Players** within [{inp} {min}] Overall Goal %',weight='semibold',pad=15)


plt.xlabel('1st-Half Goals')
plt.ylabel('2nd-Half Goals')

plt.text(20.5,-7,'Note: Marker Size indicates Total Shot Attempts Taken', ha='center', va='center', fontsize=12)
plt.text(20.5,-8.2,'Note **: Players with Shot Attempts over the 25th Percentile are Shown Only', ha='center', va='center', fontsize=12)

plt.legend([h], ['Average'],loc='upper center', bbox_to_anchor=(0.5,-0.25), fontsize=12)
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()