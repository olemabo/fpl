import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import fpl_functions as fpl_funcs
import utility_functions as utl_funcs
from datafetch.fetch_data import DataFetch
from tqdm import tqdm

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("gws", help="how many of the x-last gameweeks to consider", type=int)

if len(sys.argv[1:]) != 1:
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

def create_individual_players_list_by_attribute(player_index, attribute):
    # this is the bottleneck
    a = DataFetch()
    b = a.get_current_individual_players(player_index)
    his, fut = pd.DataFrame(b['history'])[attribute], 0
    return his, fut

def removeAccents(word):
    repl = {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a',
            'é': 'e', 'ê': 'e',
            'í': 'i', 'ï': 'i',
            'ó': 'o', 'ô': 'o', 'õ': 'o',
            'ú': 'u', 'ü': 'u', 'ö': 'ø', 'ö'.upper(): 'Ø'}

    new_word = ''.join([repl[c] if c in repl else c for c in word])
    return new_word

def create_index_to_player():
    team_list = fpl_funcs.create_team_list()
    f = open("player_to_index_dict.py", "w+")
    f.write("def player_idx_to_name(idx): \n")
    f.write("\tidx_to_name = { \n")
    for team in team_list:
        players = team.players_df['name']
        indexes = np.array(team.players_df['id'])
        for idx, player in enumerate(players):
            play = str(removeAccents(player))
            f.write("\t \t"+str(indexes[idx])+": "+'"'+str(play)+'",'+"\n")
    f.write("\t } \n")
    f.write("\treturn idx_to_name[idx]")
    f.close()

create_index_to_player()

def convert_name_to_idx(name):
    players = np.loadtxt('/home/ole/Dropbox/fpl/player_to_index.txt', dtype=str, delimiter=',')
    for player in players:
        if str(player[1]) == str(name):
            return int(player[0])
    return -1

def return_latest_I_C_T_ict(name, latest_gameweeks):
    player = convert_name_to_idx(name)
    invid_player_hist_df, no = create_individual_players_list(player)
    ict_sum = 0
    for i in invid_player_hist_df['ict_index'][-(latest_gameweeks):]:
        ict_sum +=float(i)
    return invid_player_hist_df[['minutes', 'bonus','saves', 'influence', 'creativity', 'threat', 'ict_index']][-(latest_gameweeks):], ict_sum, name

def return_latest_ict(name, latest_gameweeks, attribute):
    player = convert_name_to_idx(name)
    invid_player_hist_df, no = create_individual_players_list_by_attribute(player, attribute)
    #invid_player_hist_df, no = create_individual_players_list(player)
    #ict_values = invid_player_hist_df[attribute][-latest_gameweeks:]
    ict_values = invid_player_hist_df[-latest_gameweeks:]
    return ict_values, pd.to_numeric(ict_values).sum(axis=0)

def insertionsort(A):
    # sort an array according to its fixture score
    A = np.array(A)
    for j in range(1, A[1].size):
        score = A[1][j]
        team_array = A[1][j]
        team_array2 = A[0][j]
        i = j - 1
        while i >= 0 and float(A[1][i]) > float(score):
            A[0][i + 1] = A[0][i]
            A[1][i + 1] = A[1][i]
            i = i - 1
        A[1][i + 1] = team_array
        A[0][i + 1] = team_array2
        #if team_array2=="Barnes":
            #print(A, score, j, team_array2)
    return A

def find_max_ict(x_best, x_last, attribute):
    players = np.loadtxt('/home/ole/Dropbox/fpl/player_to_index.txt', dtype=str, delimiter=',')
    scores = np.zeros(x_best, dtype=float)
    names = np.empty(x_best, dtype=str)
    best = np.array((names, scores))
    for idx, name in tqdm(zip(players[:, 0], players[:, 1]), total=len(players[:, 0])):
        sum = return_latest_ict(name, x_last, attribute)[1] / x_last
        if sum > float(best[1, 0]):
            best[1, 0] = sum
            best[0, 0] = name
            best = insertionsort(best)
    return best


def write_to_file(attribute, x_last, num):
    gw =  create_individual_players_list(52)[0][['minutes']][-(x_last):].index[0]
    best = find_max_ict(num, x_last, attribute)
    f = open("/home/ole/Documents/fantasy/attribute_data/"+attribute+"/best_"+attribute+"_last_"+str(x_last)+".txt", "w+")
    f.write(attribute+" from last "+str(x_last)+ " gameweeks, "+"("+str(gw+1)+" to "+str(gw+x_last)+")"+"\n")
    for i in range(len(best[0])-1, 0, -1):
        f.write(str(best[0, i])+" "+str(round(float(best[1, i]), 2))+'\n')
    f.close()

def write_all_file(gw):
    write_to_file('ict_index', gw, 45)
    write_to_file('threat', gw, 45)
    write_to_file('influence', gw, 45)
    write_to_file('creativity', gw, 45)


def print_ict_info(list):
    for name in list:
        print(return_latest_I_C_T_ict(name, 4))

write_all_file(args.gws)

#names = ['Alli', 'Son']
#print_ict_info(names)
#print(return_latest_I_C_T_ict('Robertson', 4))
#print(return_latest_I_C_T_ict('Alexander-Arnold', 4))
#print(return_latest_I_C_T_ict('Zaha', 4))
#print(return_latest_I_C_T_ict('Guaita', 4))
#print(return_latest_I_C_T_ict('Lundstram', 4))
#there is a bug with players with same name
#best = find_max_ict(30, 4, 'ict_index')
#print("\n")
#for i in range(len(best[0])-1, 0, -1):
#    print(best[0, i], " ", best[1, i], i)
#print(best)


# liga ting
# attribute / points
# calc several attributes at the same time, ict, treat, influience u.z.w.
# calc attribute values depending on minutes playes
