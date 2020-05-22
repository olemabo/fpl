from datafetch.fetch_data import DataFetch
import utility_functions as utl
import matplotlib.pyplot as plt
import json
import pandas as pd
import requests
import webbrowser
import numpy as np
from selenium import webdriver
import time
import subprocess
from tqdm import tqdm
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("player", help="player to check", type=str)
parser.add_argument("top_x", help="check top x fpl teams", type=int)
parser.add_argument("google", help="open on google or not", type=int)

if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()
args = parser.parse_args()

def open_internet_page(x_top_50):
    web_global_league = 'https://fantasy.premierleague.com/api/leagues-classic/314/standings/?phase=1&page_new_entries=1&page_standings=X'
    for i in tqdm(range(x_top_50)):
        string = web_global_league.replace('X', str(i+1))
        p = subprocess.Popen(["google-chrome", string])
        #webbrowser.open_new_tab(web_global_league.replace('X', str(i+1)))
        time.sleep(1)
        p.kill()

def dataFetch(num):
    web_global_league = 'https://fantasy.premierleague.com/api/leagues-classic/314/standings/?phase=1&page_new_entries=1&page_standings=X'
    #webbrowser.open_new_tab(web_global_league.replace('X', str(num)))
    r = requests.get(web_global_league.replace('X', str(num)))
    jsonResponse = r.json()
    return jsonResponse

def find_ids(top_x_players):
    x_top_50 = top_x_players // 50
    id_s = []
    web_global_league = 'https://fantasy.premierleague.com/api/leagues-classic/314/standings/?phase=1&page_new_entries=1&page_standings=X'
    #open_internet_page(x_top_50)
    for i in range(x_top_50):
        data = dataFetch(i+1)
        #print(i)
        ############################
        # this can be remove when alleready done
        #string = web_global_league.replace('X', str(i+1))
        #p = subprocess.Popen(["google-chrome", string])
        #time.sleep(0.6)
        #data = dataFetch(i+1)
        #p.kill()
        ############################
        data_pd = pd.DataFrame(data['standings'])
        for j in range(50):
            id_s.append(data_pd['results'][j]['entry'])
    return id_s

def convert_name_to_idx(name):
    players = np.loadtxt('/home/ole/Dropbox/fpl/player_to_index.txt', dtype=str, delimiter=',')
    for player in players:
        if str(player[1]) == str(name):
            return int(player[0])
    return -1

def check_player(player, top_x_players, google):
    if google:
        open_internet_page(top_x_players // 50)
    id_s = find_ids(top_x_players)
    a = DataFetch()
    last_gameweek = int(pd.DataFrame(a.get_current_member(id_s[0])['current'])['event'].tail(1))
    check_player_idx = convert_name_to_idx(player)
    is_in, is_not, is_captain = 0, 0, 0
    for i in tqdm(range(top_x_players)):
        team_info = a.get_current_ind_team(id_s[i], last_gameweek)
        players = pd.DataFrame(team_info['picks'])['element']
        #print(pd.DataFrame(team_info['picks']))
        captain = pd.DataFrame(team_info['picks'])
        captain_idx = captain.loc[captain['is_captain'] == 1]['element'] 
        is_player_in_team = players.isin([str(check_player_idx)])
        if is_player_in_team.sum() >= 1:
            is_in += 1
            if check_player_idx == int(captain_idx):
                is_captain += 1
        else:
            is_not += 1
    fig1, ax1 = plt.subplots()
    population = [is_in-is_captain, is_captain, is_not]
    print(population)
    labels = [player, 'Captain','Not ' + player]
    colors = ['limegreen', 'forestgreen', 'red']
    output, label, color = [], [], []
    for idx, i in enumerate(population):
        if i != 0:
            output.append(i)
            color.append(colors[idx])
            label.append(labels[idx])
    print(output,label)
    ax1.pie(output, labels=label, autopct='%1.1f%%', colors=color) 
    ax1.set_title('Top '+str(is_in+is_not)+' fpl managers')
    print("writing to directory: " + str(last_gameweek))
    plt.savefig("/home/ole/Dropbox/fpl/global_plot/"+str(last_gameweek)+"/"+str(player)+"_"+str(top_x_players)+".png")
    plt.show()
    

check_player(args.player, args.top_x, args.google)

