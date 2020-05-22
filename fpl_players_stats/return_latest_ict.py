import numpy as np
import pandas as pd
import fpl_functions as fpl_funcs
import utility_functions as utl_funcs
from datafetch.fetch_data import DataFetch
from tqdm import tqdm
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("x_latest", help="Check ICT for x latest rounds", type=int)
parser.add_argument("name", help="Name of fpl player", type=str)

if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()
args = parser.parse_args()
print(args)

def create_individual_players_list(player_index):
    # this is the bottleneck
    a = DataFetch()
    b = a.get_current_individual_players(player_index)
    player_info_history = b['history']
    player_info_future = b['fixtures']
    player_history_df = pd.DataFrame(player_info_history)
    player_future_df = pd.DataFrame(player_info_future)
    attributes = ["element", "fixture","opponent_team","total_points","was_home","kickoff_time","team_h_score","team_a_score","round","minutes","goals_scored","assists","clean_sheets","goals_conceded","own_goals",\
                  "penalties_saved", "penalties_missed","yellow_cards","red_cards","saves","bonus","bps","influence","creativity","threat","ict_index","value","transfers_balance","selected","transfers_in","transfers_out"]
    return player_history_df, player_future_df

def convert_name_to_idx(name):
    players = np.loadtxt('/home/ole/Dropbox/fpl/player_to_index.txt', dtype=str, delimiter=',')
    for player in players:
        if str(player[1]) == str(name):
            return int(player[0])
    return -1

def create_individual_players_list_by_attribute(player_index, attribute):
    # this is the bottleneck
    a = DataFetch()
    b = a.get_current_individual_players(player_index)
    his, fut = pd.DataFrame(b['history'])[attribute], 0
    return his, fut

def return_latest_ict(name, latest_gameweeks, attribute):
    player = convert_name_to_idx(name)
    invid_player_hist_df, no = create_individual_players_list_by_attribute(player, attribute)
    ict_values = invid_player_hist_df[-latest_gameweeks:]
    return ict_values, pd.to_numeric(ict_values).sum(axis=0)

def return_latest_I_C_T_ict(name, latest_gameweeks):
    player = convert_name_to_idx(name)
    invid_player_hist_df, no = create_individual_players_list(player)
    ict_sum = 0
    for i in invid_player_hist_df['ict_index'][-(latest_gameweeks):]:
        ict_sum +=float(i)
    return invid_player_hist_df[['minutes', 'goals_scored','assists', 'clean_sheets', 'saves', 'bonus', 'influence', 'creativity', 'threat', 'ict_index']][-(latest_gameweeks):], ict_sum, name

info = return_latest_I_C_T_ict(args.name, args.x_latest)
print(info[0], '\n total ict: ', round(float(info[1]),2), '\n avg ict: ',  round(float(info[1]/args.x_latest), 2), '\n player: ', info[2])
