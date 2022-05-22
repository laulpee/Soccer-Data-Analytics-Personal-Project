# Import Libraries
from cmath import nan
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as matp
import numpy as np
import math

shotloc = list(range(1,25))     # array of Shot Location Zones (1-24)
NameCorr = {                    # list of name corrections
    "Appa": "Paul's Dad",
    "KyungSoo": "Kyung Soo",
    "KChung": "Kevin Chung",
    "KCamal": "Kevin Camal"
    }

# Import CSV File containing Master Shot Data
data = pd.read_csv ('fullDataSet.csv')             # raw master data
loctemp = pd.read_csv ('fieldLocationMap.csv',header=None)    # array of (x,y) locations for each Shot Location Zone


# Define Functions
def nameCorrDisplayInput(data, NameCorr):
    oldNames = list(NameCorr)                                   # old names from NameCorr dictionary
    newNames = list(NameCorr.values())                          # new names from NameCorr dictionary

    players = np.unique(data.Player)                            # distinct list of ALL players that played at least once
    playersCorr = [players[i] for i in range(len(players))]     # initialize Corrected Player Name (for display) list to "players" list

    # Replacing old names to display names
    for j in range(len(oldNames)):
        for i in range(len(playersCorr)):
            if playersCorr[i] == oldNames[j]:
                playersCorr[i] = newNames[j]
    
    # Calculating highest # of columns for Name List Display
    for i in range(10):
        if len(playersCorr) % (i+1) == 0:
            pDisCol = i+1
            pDisRow = len(playersCorr)/(i+1)
    
    # Formatting Player List for Display
    pDis = np.reshape(playersCorr,(int(pDisRow), int(pDisCol)))    # reshaping player list for display
    ss = [[str(e) for e in row] for row in pDis]                   # converting names to strings
    lens = [max(map(len,col)) for col in zip(*ss)]                 # lengths of each column in name display list
    fmt = '\t\t'.join('{{:{}}}'.format(x) for x in lens)           # {:(length of col)} \t\t {:(length of col)}
    table = [fmt.format(*row) for row in ss]                       # combines format from previous line to the converted name list ss
    print("\nPlayer List in DataBase:\n")
    print('\n'.join(table))
    print("\n")

    # PLAYER INPUT BY USER
    pinput = input("Input Player Name (shown in list above): ")
    pinputDis = pinput                                             # set Display name to pinputDis. pinput will revert to oldName if applicable for analysis


    # Changing Inputted Display Name to Old Name for Analysis (i is the counter through Player List)
    i=0
    while i < len(players):
        if pinput == players[i]:
            break
        elif pinput == playersCorr[i]:
            for j in range(len(newNames)):
                if pinput == newNames[j]:
                    pinput = oldNames[j]
            break
        else:
            i += 1

    return players, playersCorr, oldNames, newNames, pinput, pinputDis, i
def dateDisplayInput(data, pinput):
    pdata = data[data.Player == pinput]                     # Extracted data from raw master data for Specified Player
    pdate = np.unique(pdata.DateText)                       # All game dates played by Specified Player
    
    # Game Dates played by Specified Player - displayed in list format
    for i in range(len(pdate)):
        if len(pdate) < 2:
            if i == 0:
                print(f"\nDates Played by Player: {pinputDis}\n\n{i+1}.   {pdate[i]}")
                print("\n")
        else:
            if i == 0:
                print(f"\nDates Played by Player: {pinputDis}\n\n{i+1}.   {pdate[i]}")
            elif i == len(pdate)-1:
                print(f"{i+1}.   {pdate[i]}\n")
            elif (i > 0) & (i < len(pdate)-1):
                print(f"{i+1}.   {pdate[i]}")

    # DATE INPUT BY USER
    dinput = input("Select Date from List Above (or Type 'All' to select All Dates): ")
    
    # Checking if inputted date matches any date on the list
    i=0
    while i < len(pdate):
        if dinput == pdate[i]:
            break
        else:
            i += 1

    return pdate, pinputDis, dinput, i
def heatmap(shotloc, data, loc, dateInput):
    plocG = np.zeros(len(shotloc))
    plocS = np.zeros(len(shotloc))
    gPerc = np.zeros(len(shotloc))

    # Total Goals, Shots, Goal % for each Field Location for Specified Player
    for k in range(len(shotloc)):
        # Total Goals and Shots for ALL Dates
        if dateInput == "all":
            plocG[k] = data.query((f'Player == @pinput & ShotResult == "Y" & ShotLocation == @shotloc[{k}]'))['ShotResult'].count()
            plocS[k] = data.query((f'Player == @pinput & ShotLocation == @shotloc[{k}]'))['ShotResult'].count()
        # Total Goals and Shots for SPECIFIC Date
        elif dateInput == "spec":
            plocG[k] = data.query((f'Player == @pinput & ShotResult == "Y" & ShotLocation == @shotloc[{k}] & DateText == @dinput'))['ShotResult'].count()
            plocS[k] = data.query((f'Player == @pinput & ShotLocation == @shotloc[{k}] & DateText == @dinput'))['ShotResult'].count()

        # Goal % Calculation
        if ((plocG[k] == 0) & (plocS[k] == 0)) | math.isnan(gPerc[k]):
            gPerc[k] = 0
        else:
            gPerc[k] = plocG[k]/plocS[k]


    # Convert Goal, Shot values to String Type & Goal % to Percentage format
    plocG = [int(i) for i in plocG]
    plocS = [int(i) for i in plocS]
    gPerc = ["{:.0%}".format(i) for i in gPerc]
    
    # Establish (x,y) coordinates for each Field Location zone
    x = np.array(loc[:][1])
    y = np.array(loc[:][2])
    



    # PLOT heat map for shots & goals (scatter size = # of shots   |   colors = # of goals)
    plt.figure(figsize=(8,8))
    plt.scatter(x, y, s=np.multiply(plocS,30), c=plocG, cmap="Blues", edgecolors="Black", alpha=0.75)
    cbar=plt.colorbar()
    cbar.set_label('# of Goals Scored')

    # Echo Scatter Plot Design (decreasing alpha value - transparency)
    plt.scatter(x, y, s=np.multiply(plocS,50), c=plocG, cmap="Blues", edgecolors=None, alpha=0.25)
    plt.scatter(x, y, s=np.multiply(plocS,70), c=plocG, cmap="Blues", edgecolors=None, alpha=0.05)

    # Plotting the Goal % values at Field Location zones where # of shots > 0
    for j in range(len(shotloc)):
        if plocS[j] > 0:
            plt.text(x[j],y[j],gPerc[j], fontsize='small')
    

    # HARD CODED -- Field Lines created
    frect = matp.Rectangle((0,0),4,6,fill=False, color="black",linewidth=2)
    brect = matp.Rectangle((1,0),2,1,fill=False, color="black",linewidth=2)
    trect = matp.Rectangle((1,5),2,1,fill=False, color="black",linewidth=2)
    bgrect = matp.Rectangle((1.5,-0.25),1,0.25,fill=False, color="black",linewidth=2)
    tgrect = matp.Rectangle((1.5,6),1,0.25,fill=False, color="black",linewidth=2)

    # HARD CODED -- Grid for Field Location zones plotted
    q = 0           # initialize
    z = 0           # initialize
    a = 0.09        # alpha value (transparency)
    while z < 5:
        plt.vlines(x=z,ymin=0,ymax=6,colors="gray",linewidth=2,alpha=a)
        z += 1
    while q < 7:
        plt.hlines(y=q,xmin=0,xmax=4,colors="gray",linewidth=2,alpha=a)
        q += 1

    # Field Lines plotted
    plt.hlines(y=3,xmin=0,xmax=4,colors="black",linewidth=2)
    plt.gca().add_patch(frect)
    plt.gca().add_patch(brect)
    plt.gca().add_patch(trect)
    plt.gca().add_patch(bgrect)
    plt.gca().add_patch(tgrect)

    # HARD CODED -- Add Title, Player Name, Game Date and Notes onto Plot
    props = dict(facecolor='none',edgecolor='black',linewidth=0.5,pad=6)                # text box properties for main title
    plt.text(2,-0.8,"Note 1: Marker Size indicates # of Shots Attempted",ha='center')
    plt.text(2,-1.1,"Note 2: Goal Percentage in each Zone Shown",ha='center')
    plt.text(2,7.1,f"Heat Map for Goal & Shot Attempts (Player: {pinputDis})",weight="bold",bbox=props,ha='center')
    if dateInput == "all":
        plt.text(2,6.75,"Stats for All Games Played",weight="bold",ha='center')
    elif dateInput == "spec":
        plt.text(2,6.75,f"Stats for Game Date: {dinput}",weight="bold",ha='center')

    # HARD CODED -- Set x, y limits for plot and set aspect ratio
    plt.xlim(-0.4,4.4)
    plt.ylim(-0.3,6.3)
    plt.axis('off')
    plt.gca().set_aspect(aspect=0.85)

    # Add arrow indicating direction of play
    plt.arrow(-0.3,2.25,0,1.5,width=0.02,head_width=0.1,length_includes_head=True,color="black")


    heatmap = plt.show()
    return heatmap
def goalLeagueGameAverages(data, players, dateInput):
    body = ['L', 'R', 'H']                                  # Body Types used for Shooting (L = Left Foot, R = Right Foot, H = Head)

    init = (len(players),len(body))                         # Set shape for Players (Row) x Body Type (Column) 2d array
    gTot=np.zeros(init)                                     # Initialize 2d array of Total Goal Count
    sTot=np.zeros(init)                                     # Initialize 2d array of Total Shot Attempt Count
    pTot = np.zeros(init)                                   # Initialize 2d array of Total Goal %

    # Total Goals, Shots for each Body Type for ALL Players
    for j in range(len(body)):
        for i in range(len(players)):
            # Total Goals and Shots for ALL Players & for ALL Dates
            if dateInput == "all":
                gTot[i,j] = data.query((f'Player == @players[{i}] & ShotResult == "Y" & Foot == @body[{j}]'))['ShotResult'].count()
                sTot[i,j] = data.query((f'Player == @players[{i}] & Foot == @body[{j}]'))['ShotResult'].count()
            # Total Goals and Shots for ALL Players & for Specified Date
            elif dateInput == "spec":
                gTot[i,j] = data.query((f'Player == @players[{i}] & ShotResult == "Y" & Foot == @body[{j}] & DateText == @dinput'))['ShotResult'].count()
                sTot[i,j] = data.query((f'Player == @players[{i}] & Foot == @body[{j}] & DateText == @dinput'))['ShotResult'].count()

    gTot = gTot.astype(int)                                 # convert Total Goal Count array to integer format
    sTot = sTot.astype(int)                                 # convert Total Shot Attempt Count array to integer format
    
    np.seterr(invalid='ignore')                             # ignore floating-point errors (errors due to very small numbers in division below)

    # Total Goal % for each Body Type for ALL Players
    for j in range(len(body)):
        for i in range(len(players)):
            pTot[i,j] = np.divide(gTot[i,j], sTot[i,j])


    OgTot = np.sum(gTot,axis=1)                             # Row of TOTAL Goals for each player in league (summing rows of L,R,H goals for each player)
    OgTotAVG = np.round(np.average(OgTot, axis=0),2)        # LEAGUE or GAME Average of GOAL COUNT (rounded to 2 decimal places)

    OsTot = np.sum(sTot,axis=1)                             # Row of TOTAL Shot Attempts for each player in league
    OsTotAVG = np.round(np.average(OsTot, axis=0),2)        # LEAGUE or GAME Average of SHOT ATTEMPT COUNT

    OpTot = [OgTot[i]/OsTot[i] for i in range(len(OgTot))]  # Row of OVERALL Goal % for each player in league
    OpTotAVG = "{:.2%}".format(np.nanmean(OpTot, axis=0))   # LEAGUE or GAME Average of GOAL % (formatted to 0.00% format)

    # Array of LEAGUE (all) or GAME (spec) Averages for (Goal Count, Shot Attempt Count, Goal %)
    OTotAVG = [OgTotAVG, OsTotAVG, OpTotAVG]                # used for stats display


    # Finding LEAGUE or GAME Averages for [LF, RF, H] for [Goal Count, Shot Attempt Count, Goal %]
    gTotAVG = np.round(np.mean(gTot, axis=0),2)          # Row of AVERAGE Goal Count for all body types
    sTotAVG = np.round(np.mean(sTot, axis=0),2)             # Row of AVERAGE Shot Attempt Count for all body types
    pTotAVG = np.nanmean(pTot,axis=0)                       # Calculate AVERAGE Goal % disregarding the NAN values (aka 0 shot attempts)
    pTotAVG = ["{:.0%}".format(pTotAVG[i]) for i in range(len(pTotAVG))]    # Row of AVERAGE Goal % formatted to [0%] format

    return gTotAVG, sTotAVG, pTotAVG, OTotAVG
def goalPlayerStats(data):
    body = ['L', 'R', 'H']                                  # Body Types used for Shooting (L = Left Foot, R = Right Foot, H = Head)

    gTot=np.zeros(len(body))                                # Initialize array of Total Goal Count
    sTot=np.zeros(len(body))                                # Initialize array of Total Shot Attempt Count
    pTot = np.zeros(len(body))                              # Initialize 2d array of Total Goal %

    # Total Goals, Shots for each Body Type for Specified Player
    for j in range(len(body)):
        # Total Goals and Shots for Specified Player & for ALL Dates
        if dateInput == "all":
            gTot[j] = data.query((f'Player == @pinput & ShotResult == "Y" & Foot == @body[{j}]'))['ShotResult'].count()
            sTot[j] = data.query((f'Player == @pinput & Foot == @body[{j}]'))['ShotResult'].count()
        # Total Goals and Shots for Specified Player & for Specified Date
        elif dateInput == "spec":
            gTot[j] = data.query((f'Player == @pinput & ShotResult == "Y" & Foot == @body[{j}] & DateText == @dinput'))['ShotResult'].count()
            sTot[j] = data.query((f'Player == @pinput & Foot == @body[{j}] & DateText == @dinput'))['ShotResult'].count()

    gTot = gTot.astype(int)                                 # convert Total Goal Count array to integer format
    sTot = sTot.astype(int)                                 # convert Total Shot Attempt Count array to integer format
    
    np.seterr(invalid='ignore')                             # ignore floating-point errors (errors due to very small numbers in division below)

    # Total Goal % for each Body Type for Specified Player
    for j in range(len(body)):
            pTot[j] = np.divide(gTot[j], sTot[j])

    # Format Goal % array into [0%] format for non-NAN values only (NAN values are left as is)
    pTotPerc = ["{:.0%}".format(pTot[i]) if (not math.isnan(pTot[i])) else pTot[i] for i in range(len(pTot))]
    
    return gTot, sTot, pTot, pTotPerc
def pieChart(data, gTotAll, sTotAll, gTotAVG, sTotAVG, pTotAVG, pTotPerc, pdate, OTotAVG):
    type = ['L', 'R', 'H']                                 # Body Types used for Shooting (L = Left Foot, R = Right Foot, H = Head)
    shotResult = ['G', 'Y', 'B', 'N']                      # Shot Results (G = Goal, Y = OnTarget but no goal, B = Blocked by non-keeper, N = Off Target)

    init = (len(type), len(shotResult))                    # Set shape for Body Type (Row) x Shot Result (Column) 2d array
    mat = np.zeros(init)                                   # Initialize 2d array of Body Type x Shot Result for Specified Player
    matPerc = np.zeros(init)                               # Initialize 2d array of Shot Result Percentages for each Body Type (used for Pie Chart display below)

    # Body Type (L,R,H) x Shot Result (G,Y,N,B) 2d Array for Specified Player
    for i in range(len(type)):
        for j in range(len(shotResult)):
            # Array for Specified Player & for ALL Dates
            if dateInput == "all":
                mat[i,j] = data.query((f'Player == @pinput & Foot == @type[{i}] & OnOffTarget == @shotResult[{j}]'))['ShotResult'].count()
            # Array for Specified Player & for Specified Date
            elif dateInput == "spec":
                mat[i,j] = data.query((f'Player == @pinput & Foot == @type[{i}] & OnOffTarget == @shotResult[{j}] & DateText == @dinput'))['ShotResult'].count()

    # TOTAL Shot Attempt Count for each Body Type [L, R, H] -- used to calculate matPerc below
    typesums = np.sum(mat,axis=1)

    # Shot Result Percentages for each Body Type 2d Array for Specified Player
    for i in range(len(type)):
        for j in range(len(shotResult)):
            matPerc[i,j] = np.divide(mat[i,j],typesums[i])*100

    mat = mat.astype(int)                                   # convert array to integer format


    # OVERALL Goal/Shot Stats (for Pie Chart in Top Right)
    Omat = [sum(x) for x in zip(*mat)]                      # Row of TOTAL Shot Attempts for each Shot Result Type [G, Y, B, N] for Specified Player
    OmatTot = np.sum(Omat)                                  # TOTAL Shot Attempts (1 value) for Specified Player
    OmatPerc = np.divide(Omat,OmatTot)                      # OVERALL Shot Result Percentages for each Shot Result type [G, Y, B, N]
    
    Ostats = [Omat[0], OmatTot, "{:.0%}".format(Omat[0]/OmatTot)]   # OVERALL Goals, Shot Attempts, Goal % for OVERALL Goal/Shot Stats Table
    Ostatsmat = np.transpose([Ostats,OTotAVG])                      # Ostats combined with Array for OVERALL Goal/Shot Stats for LEAGUE or GAME Average (OTotAVG called from goalLeagueGameAverages function)

    # Splitting matPerc to respective body type
    matPercL = matPerc[0,:]                                 # Shot Result Percentages [G, Y, B, N] for Left Foot
    matPercR = matPerc[1,:]                                 # Shot Result Percentages [G, Y, B, N] for Right Foot
    matPercH = matPerc[2,:]                                 # Shot Result Percentages [G, Y, B, N] for Head

    
    # Data Compilation for Stats Table Display Prep
    # Compiled Stats Results for [Goal, Shot, Goal %] (row) x Body Type (col) 3x3 Array
    playerStats = np.vstack((gTotAll,sTotAll,pTotPerc))     # Stats for Specified Player
    leagueStats = np.vstack((gTotAVG,sTotAVG,pTotAVG))      # Stats for Entire League or Entire Game

    # Combine playerStats array and leagueStats array together to create separate Stats arrays for each Body Type
    matLRH = [[[playerStats[i,j], leagueStats[i,j]] for i in range(len(type))] for j in range(len(type))]
    
    Lstats = matLRH[0]                                      # Left Foot Goal Stats for Player & League/Game
    Rstats = matLRH[1]                                      # Right Foot Goal Stats for Player & League/Game
    Hstats = matLRH[2]                                      # Head Foot Goal Stats for Player & League/Game

    # List of Game Dates for Specified Player -- converted from ROW (pdate) to COLUMN (pdateCol) for display purposes
    pdateCol = [[pdate[i] for j in range(1)] for i in range(len(pdate))]


    
    
    # MANUAL INPUTS for Pie Chart Graphics
    labels = ['Goals', 'On Target', 'Blocked', 'Off Target']    # Labels for Shot Result Percentage section of Pie Chart
    colors = ('#2980B9', '#7FB3D5','#D4E6F1', '#EAF2F8')        # Colors for Shot Result Percentage section of Pie Chart
    explode = (0.1,0,0,0)                                       # Explode value for Pie Chart sections [G, Y, B, N] -- only G is exploded out of chart

    # MANUAL INPUTS for Stats Table - Row and Column Titles
    if dateInput == "all":
        tCol = [f'Player: {pinputDis}', 'League Average']       # Column Headers: Player Name & Average for LEAGUE (All Games)
    elif dateInput == "spec":
        tCol = [f'Player: {pinputDis}', 'Game Average']         # Column Headers: Player Name & Average for GAME-wide (Specified Date)
    tRow = ['Goals', 'Shots', 'Goal %']                         # Row Headers: Goals & Shots & Goal %




    # Create SubPlots -- MANUAL INPUT on figure size and padding
    fig, ax = plt.subplots(2,3,figsize=(12,9))
    fig.tight_layout(pad=4)


    # MAIN TITLE for Figure -- MANUAL INPUTS
    props = dict(facecolor='#154360',edgecolor='black',linewidth=1,pad=12)                # text box properties for main title
    fig.text(0.3445,0.95,f'(Player: {pinputDis})   Detailed Goal & Shot Statistics',ha='center',va='center',fontsize=12,weight='semibold',bbox=props,color='white')

    if dateInput == "all":
        fig.text(0.3425,0.9,"Stats for All Games Played",weight="bold",ha='center',va='center',fontsize=11)
    elif dateInput == "spec":
        fig.text(0.3425,0.9,f"Stats for Game Date: {dinput}",weight="bold",ha='center',va='center',fontsize=11)


    # Table for All Games Played -- MANUAL INPUTS
    ax[0,0].axis('off')
    tableD = ax[0,0].table(pdateCol, rowLoc = 'center', rowLabels=range(1,len(pdate)+1), colLabels=["Game Date"], loc='center', cellLoc='center',bbox=[0.03,0.14,0.35,0.5],edges='open')
    tableD.set_fontsize(9)
    tableD.scale(0.3,1.2)
    headerD = ax[0,0].table(cellText=[['Games Played']],loc='center',bbox=[0,0.67,0.335,0.1],cellLoc='center')
    headerD.set_fontsize(9)

    
    # Stats Table for OVERALL Goals & Shots Stats
    ax[0,1].axis('off')
    tableO = ax[0,1].table(Ostatsmat, rowLoc = 'center', rowLabels=tRow, colLabels=tCol, loc='center', cellLoc='center',bbox=[-0.3,0.1,1.15,0.5])
    tableO.set_fontsize(20)
    tableO.scale(1,2.5)
    headerO = ax[0,1].table(cellText=[['Overall Goal Statistics']],loc='center',bbox=[-0.718,0.65,1.632,0.1],cellLoc='center',edges='open')
    headerO.set_fontsize(12)

    # Pie Chart for OVERALL Goals & Shots Results
    ax[0,2].pie(OmatPerc,autopct='%1.0f%%',labels=labels,explode=explode,colors=colors,radius=1.1,
                wedgeprops={"edgecolor" : "black",
                            'linewidth' : 2})
    ax[0,2].set_title("Overall Shot Results",fontweight="bold",pad=20)


    # Pie Chart & Stats Table for LEFT FOOT Shot Results
    if Lstats[1][0] == '0':     # if total shot attempts is 0, then gray out pie chart with N/A text
        ax[1,0].pie([100],autopct='N/A',pctdistance=0,colors=["gray"],radius=0.9,
                    wedgeprops={"edgecolor" : "black",
                                'linewidth' : 2})
    else:
        ax[1,0].pie(matPercL,autopct='%1.0f%%',labels=labels,explode=explode,colors=colors,radius=0.9,
                    wedgeprops={"edgecolor" : "black",
                                'linewidth' : 2})
    ax[1,0].set_title("Shot Results with Left Foot",fontweight="bold")
    tableL = ax[1,0].table(Lstats,loc='bottom',rowLabels=tRow, colLabels=tCol,cellLoc='center',bbox=[0.205,-0.32,0.8,0.3])
    tableL.set_fontsize(10)
    tableL.scale(0.8,1.5)

    
    # Pie Chart & Stats Table for RIGHT FOOT Shot Results
    if Rstats[1][0] == '0':     # if total shot attempts is 0, then gray out pie chart with N/A text
        ax[1,1].pie([100],autopct='N/A',pctdistance=0,colors=["gray"],radius=0.9,
                    wedgeprops={"edgecolor" : "black",
                                'linewidth' : 2})
    else:
        ax[1,1].pie(matPercR,autopct='%1.0f%%',labels=labels,explode=explode,colors=colors,radius=0.9,
                    wedgeprops={"edgecolor" : "black",
                                'linewidth' : 2})
    ax[1,1].set_title("Shot Results with Right Foot",fontweight="bold")
    tableR = ax[1,1].table(Rstats,loc='bottom',rowLabels=tRow, colLabels=tCol,cellLoc='center',bbox=[0.205,-0.32,0.8,0.3])
    tableR.set_fontsize(10)
    tableR.scale(0.8,1.5)


    # Pie Chart & Stats Table for HEAD Shot Results
    if Hstats[1][0] == '0':     # if total shot attempts is 0, then gray out pie chart with N/A text
        ax[1,2].pie([100],autopct='N/A',pctdistance=0,colors=["gray"],radius=0.9,
                    wedgeprops={"edgecolor" : "black",
                                'linewidth' : 2})
    else:
        ax[1,2].pie(matPercH,autopct='%1.0f%%',labels=labels,explode=explode,colors=colors,radius=0.9,
                wedgeprops={"edgecolor" : "black",
                            'linewidth' : 2})
    ax[1,2].set_title("Shot Results with Head",fontweight="bold")
    tableH = ax[1,2].table(Hstats,loc='bottom',rowLabels=tRow, colLabels=tCol,cellLoc='center',bbox=[0.205,-0.32,0.8,0.3])
    tableH.set_fontsize(10)
    tableH.scale(0.8,1.5)

    
    statsDash = plt.show()
    return statsDash





# Display CORRECTED List of Player Names for Selection and ASK FOR NAME INPUT
players, playersCorr, oldNames, newNames, pinput, pinputDis, i = nameCorrDisplayInput(data, NameCorr)



# If Name Input doesn't match any name, print Error. Else, go forward w/ analysis
if i == len(players):
    print("Error: Inputted Player Name is Not Available")
else:
    pdate, pinputDis, dinput, i = dateDisplayInput(data,pinput)         # Display List of Game Dates Played by Specified Player and Ask for Date Input

    if dinput == "All":                                                 # If user inputs "All", this will set code to analyze stats for all games played by player
        dateInput = "all"
    elif i < len(pdate):
        dateInput = "spec"                                              # If user inputs a specific date, this will set code to analyze stats for the specific game
    else:
        print("Error: Inputted Date is Not Available")                  # If input does not match game date string, then prompt error message


    # Data Analysis for Heat Map of Goals, Shots, Goal % for each Field Location Zones
    heatmapAll = heatmap(shotloc, data, loctemp, dateInput)


    # Data Analysis for Calculating Goal, Shot, Goal % Stats for each Body Type for Specified Player (used for Stats Dashboard)
    gTot, sTot, pTot, pTotPerc = goalPlayerStats(data)


    # Data Analysis for Calculating Goal, Shot, Goal % Stats for each Body Type for Entire League or Game-wide (used for Stats Dashboard)
    gTotAVG, sTotAVG, pTotAVG, OTotAVG = goalLeagueGameAverages(data, players, dateInput)


    # Compile Data Analysis Results and Present Goal, Shot, Goal % Results using Pie Charts and Tables
    statsDash = pieChart(data, gTot, sTot, gTotAVG, sTotAVG, pTotAVG, pTotPerc, pdate, OTotAVG)