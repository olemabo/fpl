from datafetch.fetch_data import DataFetch
import utility_functions as utl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def league(league_id):
    a = DataFetch()
    b = a.get_current_league(league_id)
    league_name = b['league']['name']
    member_info = pd.DataFrame(data=b['standings']['results'])
    member_names = member_info['entry_name']
    df = pd.DataFrame()
    for i in range(len(member_info)):
        mem_info = (a.get_current_member(member_info['entry'][i]))
        total_points = pd.DataFrame(mem_info['current'])['total_points']
        total_points = pd.DataFrame({member_names[i]: total_points})
        df = pd.concat([df, total_points], axis=1)

    ax = plt.gca()
    for idx, team_name in enumerate(member_names):
        df.plot(marker='.', linestyle='-', y=member_names[idx], ax=ax)
    plt.xlabel('GW')
    plt.ylabel('Points')
    plt.show()

def plot_one_player(player_id):
    a = DataFetch()
    b = a.get_current_member(player_id)
    data = b['current']
    print(b)
    total_points = pd.DataFrame(b['current'])['total_points']
    total_rank = pd.DataFrame(b['current'])['overall_rank']
    gw = pd.DataFrame(b['current'])['event']
    plt.loglog(gw[1:], total_rank[1:])
    plt.show()

def magnus_place():
    team_id = 1908330
    a = DataFetch()
    b = a.get_current_member(team_id)
    data = b['current']
    last_gameweek = int(pd.DataFrame(data)['event'].tail(1))
    team_info = a.get_current_ind_team(team_id, last_gameweek)
    players = pd.DataFrame(team_info['picks'])
    for i in range(players.index.stop):
        if players['position'][i] == 12:
            print('\n Bench: ')
        player_id = players['element'][i]
        if players['is_captain'][i] == True:
            print(utl.player_idx_to_name(player_id)+ " (c)")
        elif players['is_vice_captain'][i] == True:
            print(utl.player_idx_to_name(player_id)+ " (vc)")
        else:
            print(utl.player_idx_to_name(player_id))
    print('\n') 
    team_info = a.get_current_individual_players(1908330)
    total_points = pd.DataFrame(b['current'])['total_points']
    total_rank = pd.DataFrame(b['current'])['overall_rank']
    return total_rank[len(total_rank)-1]

def places(league_id):
    a = DataFetch()
    b = a.get_current_member(league_id)
    data = b['current']
    total_points = pd.DataFrame(b['current'])['total_points']
    total_rank = pd.DataFrame(b['current'])['overall_rank']
    print(np.array(total_rank), " hw ")
    plt.plot(total_rank)
    plt.show()
    return total_rank[len(total_rank)-1]
tuva = 1670428
tor = 27207

#places(tuva)

place = magnus_place()
print("magnus is one " + str(place) + " place")
#698446 fysmat
#58349 bolla
#league(58349)
#plot_one_player(1908330)
#print(return_latest_ict('Salah', 9))
#https://fantasy.premierleague.com/api/leagues-h2h/X/standings/
