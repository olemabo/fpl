from datafetch.fetch_data import DataFetch
import utility_functions as utl
import argparse
import sys
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument("team_id_arg", help="Compare your team with cup opponentole: 1119029 tor: 27207", type=int)


if len(sys.argv[1:]) == 0:
    parser.print_help()
    # parser.print_usage() # for just the usage line
    parser.exit()
args = parser.parse_args()

def import_cup_opponent(player_id):
    a = DataFetch()
    b = a.get_current_cup(player_id)
    opponent = pd.DataFrame(b['cup_matches'])
    gw = len(pd.DataFrame(a.get_current_member(player_id)['current']))
    if len(opponent) == 0:
        print("Not in the cup anymore, did not qualify")
        return -1, -1, -1
    elif 15+len(opponent) > gw or 15+len(opponent) < gw-1:
        if len(opponent) == 1:
            print("Not in the cup anymore, lasted "+str(len(opponent))+ " round")    
        else:
            print("Not in the cup anymore, lasted "+str(len(opponent))+" rounds")
        return -1, -1, -1
    your_team_name = opponent['entry_1_name'][0]
    opponent_id, opponent_name = opponent['entry_1_entry'][opponent.index.stop-1], opponent['entry_1_name'][opponent.index.stop-1]
    if opponent_id == player_id:
        opponent_id, opponent_name = opponent['entry_2_entry'][opponent.index.stop - 1], opponent['entry_2_name'][
            opponent.index.stop - 1]
    return opponent_id, opponent_name, your_team_name

def fpl_gameweek_team(team_id):
    a = DataFetch()
    b = a.get_current_member(team_id)
    data = b['current']
    last_gameweek = int(pd.DataFrame(data)['event'].tail(1))
    team_info = a.get_current_ind_team(team_id, last_gameweek)
    players = pd.DataFrame(team_info['picks'])
    return players

def compare_with_cup_opponent(player_id):
    your_id = player_id
    opponent_id, opponent_name, your_name = import_cup_opponent(player_id)
    if opponent_id == -1:
        return -1, -1, -1, -1
    opponent_team = fpl_gameweek_team(opponent_id)
    your_team = fpl_gameweek_team(your_id)
    return your_team, opponent_team, your_name, opponent_name

def print_comparison(player_id):
    your_team, opponent_team, your_name, opponent_name = compare_with_cup_opponent(player_id)
    if opponent_name == -1:
        return 0
    cap_you = utl.player_idx_to_name(int(your_team.loc[your_team['is_captain'] == 1]['element'])) 
    cap_opp = utl.player_idx_to_name(int(opponent_team.loc[opponent_team['is_captain'] == 1]['element'])) 
    print(your_name+'\t \t \t'+opponent_name)
    print(cap_you+'\t \t \t \t'+cap_opp)
    print('\n')
    for i in range(your_team.index.stop):
        if your_team['position'][i] == 12:
            print('\n Bench: ')
        player_id_opponent = opponent_team['element'][i]
        player_id_you = your_team['element'][i]
        if player_id_opponent == int(your_team.loc[your_team['is_captain'] == 1]['element']):
            extra_you = 'c'
        if player_id_opponent == int(opponent_team.loc[opponent_team['is_captain'] == 1]['element']):
            extra_opp = 'c'
        if len(utl.player_idx_to_name(player_id_you)) <= 4:
            print(utl.player_idx_to_name(player_id_you)+'\t \t \t \t'+utl.player_idx_to_name(player_id_opponent))
        elif len(utl.player_idx_to_name(player_id_you)) < 8:
            print(utl.player_idx_to_name(player_id_you)+'\t \t \t \t '+utl.player_idx_to_name(player_id_opponent))
        elif len(utl.player_idx_to_name(player_id_you)) <= 12:
            print(utl.player_idx_to_name(player_id_you)+'\t \t \t'+utl.player_idx_to_name(player_id_opponent))
        else:
            print(utl.player_idx_to_name(player_id_you)+'\t \t  '+utl.player_idx_to_name(player_id_opponent))
    print('\n')

team_tor = 27207
team_ole = 1119029
print_comparison(team_ole)
print_comparison(args.team_id_arg)
#file = open("player_to_index_dict.txt", "r")
#import numpy as np
#load = np.loadtxt("player_to_index.txt", skiprows=1, )
#print(load)
