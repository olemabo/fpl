import numpy as np
import pandas as pd

import utility_functions as util_funcs


class Team:
    """
        Class of a team
    """
    def __init__(self, team_number, players_df, fixtures_df):
        """
            Initialize object
        :param team_number: Based on alphabetical order -> Arsenal = 1, ..., Wolves = 20
        :param players_df: DataFrame containing information about the players on the team
        :param fixtures_df: DataFrame providing information about gameweeks, opponents, difficulty and H/A.
        """
        self.team_number = team_number
        self.name = util_funcs.team_number_to_name(self.team_number)
        self.players_df = players_df
        self.fixtures_df = fixtures_df


class Fixtures:
    """
        Class of Fixtures
    """
    def __init__(self, fixtures_information):
        """
            Initialize object
        :param fixtures_information: list of dictionaries with fixture information
        """
        df = pd.DataFrame(fixtures_information)
        features = ['event', 'team_h', 'team_h_difficulty', 'team_a', 'team_a_difficulty']
        final_features = ['gameweek', 'opponent_team', 'difficulty', 'H/A']
        new_name = {'event': 'gameweek'}
        df = df[features]
        df = df.rename(columns=new_name)
        self.list_teams = []
        # loop through each team and get fixture information
        for i in range(df['team_h'].min(), df['team_h'].max()+1):
            temp = pd.DataFrame()
            home_matches = df[df['team_h'] == i].copy()
            home_matches.loc[:, 'difficulty'] = home_matches['team_h_difficulty']
            home_matches.loc[:, 'opponent_team'] = home_matches['team_a']
            home_matches.loc[:, 'H/A'] = ['H'] * 19
            away_matches = df[df['team_a'] == i].copy()
            away_matches.loc[:, 'difficulty'] = away_matches['team_a_difficulty']
            away_matches.loc[:, 'opponent_team'] = away_matches['team_h']
            away_matches.loc[:, 'H/A'] = ['A'] * 19
            temp = temp.append(home_matches[final_features])
            temp = temp.append(away_matches[final_features])
            temp = temp.sort_values('gameweek', ascending=True)
            self.list_teams.append(temp)


class Players:
    """
        Class of FPL players.
    """
    def __init__(self, information_players, fixtures_information):
        """
            Initialize object
        :param information_players: list of dictionaries with information about players
        :param fixtures_information: list of dictionaries with fixture information
        """
        df = pd.DataFrame(information_players)
        float_columns = ['form', 'points_per_game', 'selected_by_percent']  # ensure float from strings
        df[float_columns] = df[float_columns].astype(float)
        length_news = df['news'].str.len()
        df.loc[:, 'fitness'] = length_news.values == 0  # create boolean for fitness/available players
        new_names = {'web_name': 'name', 'now_cost': 'price', 'selected_by_percent': 'selection',
                     'element_type': 'position'}  # new and better names for columns
        df = df.rename(columns=new_names)
        # decide attributes to keep
        attributes_to_use = ['name', 'price', 'team', 'total_points', 'points_per_game', 'minutes', 'form',
                             'clean_sheets', 'assists', 'goals_scored', 'selection', 'position', 'fitness', 'id']
        self.df = df[attributes_to_use]
        self.fixtures = Fixtures(fixtures_information)

    def get_attribute_from_all_players(self, attribute):
        if attribute not in self.df.keys():
            print(f'Attribute {attribute} does not exist for a player!')
            exit(1)
        return self.df[attribute]

    def create_all_teams(self):
        list_of_teams_df = [x for _, x in self.df.groupby('team')]
        team_list = []
        for i in range(len(list_of_teams_df)):
            team = Team(list_of_teams_df[i]['team'].values[0], list_of_teams_df[i], self.fixtures.list_teams[i])
            team_list.append(team)
        return team_list


class Squad:
    # TODO: this has not been tested and is not ready for use... Yet!
    """
        Class of a selected squad with 15 players to be used in FPL
    """
    def __init__(self, players_df):
        """
            Initialize object
        :param players_df: DataFrame containing information about the players on the squad
        """
        self.players_df = players_df
        self.max_price = 1000
        self.number_of_goalkeepers = 2
        self.number_of_defenders = 5
        self.number_of_midfielders = 5
        self.number_of_attackers = 3
        self.positions_sum = self.number_of_goalkeepers*1 + self.number_of_defenders*2 + \
                             self.number_of_midfielders*3 + self.number_of_attackers*4

    def validate_squad(self):
        prices = self.players_df['price'].values
        positions = self.players_df['position'].values
        total_cost_squad = np.sum(prices)
        below_check = total_cost_squad <= self.max_price
        sum_of_positions = np.sum(positions)
        position_check = sum_of_positions == self.positions_sum
        if below_check*position_check == 1:
            return True
        else:
            return False
