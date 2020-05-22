import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import fpl_functions as fpl_funcs
import utility_functions as utl_funcs


def create_data_frame():
    team_list = fpl_funcs.create_team_list()
    columns = [str(i) for i in range(0, len(team_list[0].fixtures_df.index) + 1)]
    columns[0] = 'Team'
    data = []
    temp_team = []
    for team in range(20):
        temp_team.append(team_list[team].name)
    for gameweek in range(20):
        team_info = team_list[gameweek]
        temp_data = [team_info.name]
        for team_idx in range(len(columns)-1):
            index_opp = team_info.fixtures_df['opponent_team'].index[team_idx]
            index_ah = team_info.fixtures_df['H/A'].index[team_idx]
            index_diff = team_info.fixtures_df['difficulty'].index[team_idx]
            opp = team_info.fixtures_df['opponent_team'][index_opp]
            ah = team_info.fixtures_df['H/A'][index_ah]
            diff = team_info.fixtures_df['difficulty'][index_diff]
            temp_data.append([utl_funcs.team_number_to_short_name(opp), ah, diff])
        data.append(temp_data)
    return pd.DataFrame(data=data, columns=columns)

def fixture_score_one_team(df, team_idx, GW_start, GW_end):
    score = 0
    team = df.loc[team_idx][0]
    upcoming_fixtures = np.empty(GW_end - GW_start + 1, dtype=object)
    upcoming_fixtures_score = np.empty(GW_end - GW_start + 1, dtype=int)
    for i in range(GW_start - 1, GW_end): 
        score += int(df.loc[team_idx][1:][i][2])
        if df.loc[team_idx][1:][i][1] == 'A':
            upcoming_fixtures[i - GW_start + 1] = df.loc[team_idx][1:][i][0].lower()
        if df.loc[team_idx][1:][i][1] == 'H':
            upcoming_fixtures[i - GW_start + 1] = df.loc[team_idx][1:][i][0].upper()
        upcoming_fixtures_score[i - GW_start + 1] = int(df.loc[team_idx][1:][i][2])
    return np.array([score, team, upcoming_fixtures, upcoming_fixtures_score])


def insertionsort(A):
    # sort an array according to its fixture score
    for i in range(A.size - 1):
        score = A[i + 1][0]
        team_array = A[i + 1]
        while i >= 0 and A[i][0] > score:
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = team_array
    return A

def best_games_future(df, GW_start, GW_end):
    number_of_teams = df.shape[0]
    # create an array with size of all teams, which will be sorted by score
    all_teams = np.empty(number_of_teams, dtype = object)
    for teams in range(0, number_of_teams):
        team = fixture_score_one_team(df, teams, GW_start, GW_end)
        all_teams[teams] = team
    # sort the list according to the score
    all_teams = insertionsort(all_teams)
    return all_teams

def compute_best_fixtures_one_team(df, GW_start, GW_end, team_idx, min_length):
    max_score = fixture_score_one_team(df, team_idx, GW_start, GW_end)[0] / (GW_end - GW_start)
    max_info = fixture_score_one_team(df, team_idx, GW_start, GW_end)
    for i in range(GW_start, GW_end):
        for j in range(i + 1, GW_end + 1):
            temp_score = fixture_score_one_team(df, team_idx, i, j)[0] / (j - i + 1)
            if temp_score <= max_score and (j - i + 1) >= min_length:
                if temp_score == max_score and len(fixture_score_one_team(df, team_idx, i, j)[2]) > len(max_info[2]):
                    max_info = fixture_score_one_team(df, team_idx, i, j)
                    max_score = temp_score
                if temp_score != max_score:
                    max_info = fixture_score_one_team(df, team_idx, i, j)
                    max_score = temp_score
    return max_info

def visualize_one_teams_fixtures(df, GW_start, GW_end, team_index):
    info = fixture_score_one_team(df, team_index, GW_start, GW_end)
    diff = info[3]
    print(info)
    # info should be a list of objects 
    x_len, y_len = GW_end-GW_start+1, 1
    fig, ax = plt.subplots(1,1)
    # add x-axis 
    gameweeks = np.empty([x_len], dtype=object)
    for j, i in enumerate(np.arange(GW_start, GW_end + 1)):
        gameweeks[j] = 'GW' + ' ' + str(i)
    # plot values for each pixel
    for j in range(x_len):
            text = ax.text(j, 0, info[2][j], ha="center", va="center", color="black")
    cmap = colors.ListedColormap(["lime", "lightgrey", "lightcoral", "red"])
    img = plt.imshow([diff], cmap=cmap)
    ax.set_xticks(np.arange(x_len))
    ax.set_xticklabels(gameweeks)
    ax.set_yticks(np.arange(y_len))
    print(info[1])
    #ax.set_yticklabels(info[1])
    ax.set_yticklabels(np.array([utl_funcs.team_number_to_name(team_index+1)], dtype=object))
    fig.tight_layout()
    ax.set_title("Fixture plan from GW %i to GW %i" %(GW_start, GW_end))
    plt.show()

def visualize_fixtures(df, GW_start, GW_end):
    info = np.empty(df.shape[0], dtype=object)
    diff = np.empty([df.shape[0], GW_end - GW_start + 1], dtype=int)
    for i in range(df.shape[0]):
        info[i] = fixture_score_one_team(df, i, GW_start, GW_end)
        diff[i] = info[i][3]
    # info should be a list of objects 
    x_len, y_len = GW_end-GW_start+1, df.shape[0]
    fig, ax = plt.subplots(1,1)
    
    # add x-axis
    gameweeks = np.empty([x_len], dtype=object)
    for j, i in enumerate(np.arange(GW_start, GW_end + 1)):
        gameweeks[j] = 'GW' + ' ' + str(i)
        gameweeks[j] = str(i)

    # add y-axis
    team = np.empty([y_len+1], dtype=object)
    for i in range(y_len):
        team[i+1] = info[i][1]

    # plot values for each pixel
    for i in range(y_len):
        for j in range(x_len):
            text = ax.text(j, i, info[i][2][j], ha="center", va="center", color="black")
    cmap = colors.ListedColormap(["lime","lightgrey", "lightcoral", "red"])

    #cmap = colors.ListedColormap(["lime", "forestgreen", "lightgrey", "lightcoral", "red"])
    plt.imshow(np.array(diff), cmap=cmap)
    ax.set_xticks(np.arange(x_len))
    ax.set_xticklabels(gameweeks)
    ax.set_yticks(np.arange(y_len))
    ax.set_yticklabels(team[1:])
    ax.set_ylim(-0.5, y_len - 0.5)
    fig.tight_layout()
    ax.set_title("Fixture plan from GW %i to GW %i" %(GW_start, GW_end))
    plt.show()

def get_ICT(name):
    team_list = fpl_funcs.create_team_list()
    number_of_teams = len(team_list)
    for temp_team in team_list:
        temp_players = temp_team.players_df
        if np.sum(temp_players['name'] == name):
            player = temp_players[temp_players['name'] == name]
            team = temp_team
            break
    print(team.name, " \n ", player)

def get_players():
    team_list = fpl_funcs.create_team_list()
    Arsenal = team_list[0]
    print(Arsenal.players_df)
    print(team_list[1].players_df)

#get_players()
#get_ICT('Pukki')
#for i in best_games_future(create_data_frame(), 12, 20):
#    print(i[1], " score : ", i[0])
#print(best_games_future(create_data_frame(), 20, 24))
#visualize_one_teams_fixtures(create_data_frame(), 12, 20, 17-1)
#visualize_one_teams_fixtures(create_data_frame(), 12, 20, 11-1)
#print(create_data_frame())

#visualize_fixtures(create_data_frame(), 14, 28)
visualize_fixtures(create_data_frame(), 17, 25)
