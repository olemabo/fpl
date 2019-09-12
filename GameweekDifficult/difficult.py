import numpy as np
import pandas as pd


data  = pd.read_csv("difficulty.csv")
def createDataFrame(txt):
    data = pd.read_csv(txt)
    for i in range(1,data.shape[1]):
        for j in range(data.shape[0]):
            num = str(i)
            data[num][j] = data[num][j].split(" ")

    return pd.DataFrame(data = data)
	
df = createDataFrame("difficulty.csv") 
print(data.shape, "\n",  df)

def fixtureScore(df, GW_start, GW_end):
    begin = str(GW_start)
    print(begin)
    print(df[str(GW_start)], "here")
    Number_of_GW = GW_end - GW_start
    for GW in range(GW_start, GW_end + 1):
        #print(GW)
        #print(df)
        print(df[str(GW)])
    #print(df[])
    print(df.loc[df['Team'] == 'ARS'])
    print("w2",df.loc[0], "here2")
    ARS = df.loc[0][1:]
    score = 0
    # calc score for one single team
    for i in range(Number_of_GW + 1):
        score += int(ARS[i][2])
    print("score: ", score)
# return the score together with fixtures 
# return an array, first element is the team, second is score
# third is all fxtures

# one functon where all teams are evaluted and one where you specify
# which teams to check
def fixtureScoreOneTeam(df, Index, GW_start, GW_end):
    score = 0
    fixture = np.zeros(GW_end - GW_start + 1)
    print(df.loc[Index][1:][0][0].lower())
    for i in range(GW_end - GW_start + 1):
        score += int(df.loc[Index][1:][i][2])
    return score, df.loc[Index][0], fixture
print("calc score: ", fixtureScoreOneTeam(df, 1, 1, 3))
fixtureScore(df, 1, 2)

"""
print(data.shape, data['Team']=='ARS')
print(data_pd)
number_of_teams = data_pd.index[2] + 1
print("number of teams: ", number_of_teams)

print(data_pd['1'], data_pd['1'][0][4], data_pd.index)
print(data_pd['Team'][:], data['Team'][:])
# print by index smart to creat arrays
print(np.array(data_pd[data_pd.index==0]))
print(np.array(data_pd[data_pd['Team'] == 'ARS']))
print(data_pd[data_pd['Team'] == 'ARS'])
print(data_pd.loc[data_pd['Team'] == 'ARS'])
print("\n", np.array(data_pd.loc[[1,2]])[1,1:])
print("\n", np.array(np.array(data_pd.loc[[1,2]])[1,1:]).T.shape)
"""
