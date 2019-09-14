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

# one functon where all teams are evaluted and one where you specify
# which teams to check

def fixture_score_single_team(df, Index, GW_start, GW_end):
    score = 0
    fixture = np.empty(GW_end - GW_start + 1, dtype=object)
    for i in range(GW_start - 1, GW_end): 
        score += int(df.loc[Index][1:][i][2])
        if df.loc[Index][1:][i][1] == 'A':
            fixture[i - GW_start + 1] = df.loc[Index][1:][i][0].lower()
        if df.loc[Index][1:][i][1] == 'H':
            fixture[i - GW_start + 1] = df.loc[Index][1:][i][0].upper()
    return np.array([score, df.loc[Index][0], fixture])


def best_games_future(df, GW_start, GW_end, best_teams):
    number_of_teams = df.shape[0]
    print("number of teams: ", number_of_teams)
    print("from gameweek %i to %i " %(GW_start, GW_end))
    print("Score: Team: Fixtures: ")
    # create an array with size of all teams, which will be sorted by score
    all_teams = np.empty(number_of_teams, dtype = object)
    for teams in range(0, number_of_teams):
        team = fixture_score_single_team(df, teams, GW_start, GW_end)
        print(team[0], " ", team[1], " ", team[2])
        # maybe create a dataframe with score team and fixtures
        all_teams[teams] = team
    # sort the list according to the score
    all_teams = insertionsort(all_teams)
    print("\n Best %i teams with fixtures from GW %i to %i" %(best_teams, GW_start, GW_end))
    for i in range(best_teams):
        print(all_teams[i])
    
def insertionsort(A):
    for i in range(A.size - 1):
        key = A[i + 1][0]
        key2 = A[i + 1]
        while i >= 0 and A[i][0] > key:
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = key2
    return A

best_games_future(df, 2, 5, 3)

#print("calc score: ", fixtureScoreOneTeam(df, 1, 1, 3))
#fixtureScore(df, 1, 3)
#print(fixtureScoreOneTeam(df, 0, 1, 3))




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
