# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# USER INPUT -- Displaying the Top # (max) and Bottom # (min) of Player Goal% Norms on Plot
inp = input("\n\nWhich Goal % Results would you like to display on the plot? (All, Top, Bottom)\nNote: Only players with shot attempts over 25th percentile are considered.\n\nEnter option: ")

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



# Initialize all Arrays for For Loop
colNames = ['Close Goals (cg)', 'Close Attempts (ca)', 'Far Goals (fg)', 'Far Attempts (fa)', 'C Goal % (cPer)', 'F Goal % (fPer)', 'Total Goals (tg)', 'Total Attempts (ta)', 'Norm of C and F Goal %']
colLen = len(colNames)

cg, ca, fg, fa, cPer, fPer, tg, ta, norm = (np.zeros(nPlayers) for i in range(colLen))


# Calculate the Following for Each Player
for i in range(nPlayers):
    cg[i] = sum((data.Player == p[i]) & (data.ShotResult == 'Y') & (data.ShotLocation <= 24) & (data.ShotLocation >= 17))   # Total No. of Close Range Goals
    ca[i] = sum((data.Player == p[i]) & (data.ShotLocation <= 24) & (data.ShotLocation >= 17))                              # Total No. of Close Range Shot Attempts
    fg[i] = sum((data.Player == p[i]) & (data.ShotResult == 'Y') & (data.ShotLocation < 17))                                # Total No. of Far Range Goals
    fa[i] = sum((data.Player == p[i]) & (data.ShotLocation < 17))                                                           # Total No. of Far Range Shot Attempts
    tg[i] = sum((data.Player == p[i]) & (data.ShotResult == 'Y'))                                                           # Overall No. of Goals
    ta[i] = sum((data.Player == p[i]))                                                                                      # Overall No. of Shot Attempts

    np.seterr(invalid='ignore')                                         # ignore floating-point errors (errors due to very small numbers in division below)

    cPer[i] = cg[i] / ca[i]                                             # Goal Percentage for Close Range
    fPer[i] = fg[i] / fa[i]                                             # Goal Percentage for Far Range

    if math.isnan(cPer[i]):                                             # If Percentage is Nan, then set to 0
        cPer[i] = 0
        fPer[i] = 0

    norm[i] = np.sqrt(np.square(cPer[i]) + np.square(fPer[i]))          # Calculate norm of Close Range Goal % and Far Range Goal %



# Data Type Conversion to Integer Format for Goal & Shot Count Arrays
cg = [int(i) for i in cg]
ca = [int(i) for i in ca]
fg = [int(i) for i in fg]
fa = [int(i) for i in fa]
ta = [int(i) for i in ta]
tg = [int(i) for i in tg]

# Round Goal % and Norm Values to 2 Decimal Places
cPer = [round(i,2) for i in cPer]
fPer = [round(i,2) for i in fPer]
norm = [round(i,2) for i in norm]


# Average Goal Percentages for Close Range (cavg) and Far Range (favg) Goals
cavg = np.average(cPer)
favg = np.average(fPer)



# Finding 25th Percentile for Total Shot Attempts (This is to weed out players that have less shot attempts than the 25% mark of the overall league) -- for DISPLAY purposes
per25 = np.percentile(ta,25)


p25 = np.transpose([j for (i,j) in zip(ta,playersCorr) if i > per25])             # Array of Players with Shot Attempts over 25th percentile [CORRECTED NAMES]
norm25 = np.transpose([j for (i,j) in zip(ta,norm) if i > per25])                 # Array of Norms of Players with Shot Attempts over 25th percentile
cPer25 = np.transpose([j for (i,j) in zip(ta,cPer) if i > per25])                 # Array of Close-Range Goal % of Players with Shot Attempts over 25th percentile
fPer25 = np.transpose([j for (i,j) in zip(ta,fPer) if i > per25])                 # Array of Far-Range Goal % of Players with Shot Attempts over 25th percentile


# Note: Finding Top # and Bottom # within the Players that have Shot Attempts over 25th Percentile (ONLY IF ALL is not selected by user)
if inp == "Top":
    ind = np.argpartition(norm25,-max)[-max:]                                   # Finding the Indices of Players with Top # (max) Norm Values
elif inp == "Bottom":
    ind = np.argpartition(norm25,min)[:min]                                     # Finding the Indices of Players with Bottom # (min) Norm Values

ind_med = np.argpartition(norm25, len(norm25) // 2)[len(norm25) // 2]           # Finding the Index of Player with MEDIAN norm value





# SCATTER PLOT
plt.figure(figsize=(10,8.5))
plt.scatter(cPer, fPer, s=np.multiply(ta,3), c=tg, cmap = 'Blues', alpha=0.8, edgecolors='black')   # Plotting every Players' data point but only displaying Names over 25th Percentile


# If "All" is selected for input, display ALL player name data labels that have shot attempts over 25th percentile count
if inp == "All":
    for i in range(len(p25)):
        plt.text(cPer25[i],fPer25[i],p25[i],fontsize=9)
# If "Top" or "Bottom" is selected for input, display the corresponding player name data labels
else:
    for i in ind:
        plt.text(cPer25[i],fPer25[i],p25[i], fontsize=9)


# Plot Lines displaying the AVERAGE close-range and far-range goal percentages
h = plt.hlines(favg, xmin=-1, xmax=1, colors="black", linestyles='dashed', alpha=0.35)
v = plt.vlines(cavg, ymin=-1, ymax=1, colors="black", linestyles='dashed', alpha=0.35)


# Setting x-axis and y-axis limits
plt.xlim(-0.05,np.max(cPer)+0.05)
plt.ylim(-0.05,np.max(fPer)+0.05)


# Plot Color Bar for # of Goals Scored
cbar = plt.colorbar()
cbar.set_label('# of Goals Scored')


if inp == "All":
    plt.title(f'Far-Range vs Close-Range Goal Percentage\nDisplaying [{inp}] Players**',weight='semibold',pad=15)
elif inp == "Top":
    plt.title(f'Far-Range vs Close-Range Goal Percentage\nDisplaying Players** within [{inp} {max}] Overall Goal %',weight='semibold',pad=15)
elif inp == "Bottom":
    plt.title(f'Far-Range vs Close-Range Goal Percentage\nDisplaying Players** within [{inp} {min}] Overall Goal %',weight='semibold',pad=15)


plt.xlabel('Close-Range Goal Percentage')
plt.ylabel('Far-Range Goal Percentage')

plt.text(0.265,-0.14,'Note: Marker Size indicates Total Shot Attempts Taken', ha='center', va='center')
plt.text(0.265,-0.16,'Note **: Players with Shot Attempts over the 25th Percentile are Shown Only', ha='center', va='center')

plt.legend([h], ['Average'],loc='upper center', bbox_to_anchor=(0.5,-0.27))
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()