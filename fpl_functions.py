from datafetch.fetch_data import DataFetch
from dataformat.classes import Players
import pandas as pd

def create_team_list():
    a = DataFetch()
    b = a.get_current_fpl_info()
    player_info = b['elements']
    fixture_info = a.get_current_fixtures()

    players = Players(player_info, fixture_info)

    team_list = players.create_all_teams()  # list teams, where Arsenal = team_list[0], ... Wolves = team_list[-1]
    return team_list

def get_gameweek_data(gameweek_number):
    a = DataFetch()
    b = a.get_gameweek_info(gameweek_number)
    gameweek_info = b['elements']
    gameweek_df = pd.DataFrame(gameweek_info)
    ids = gameweek_df['id']
    stats = gameweek_df['stats']
    df = pd.DataFrame(stats.to_list())
    float_columns = ['ict_index', 'influence', 'creativity', 'threat']
    df[float_columns] = df[float_columns].astype(float)
    df.loc[:, 'id'] = ids.values
    df = df.sort_values('id', ascending=True)
    return df