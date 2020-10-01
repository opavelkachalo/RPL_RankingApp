import pandas as pd
from prettytable import PrettyTable

if __name__ == "__main__":
    data = pd.read_csv(r"data\RUS.csv")
else:
    data = pd.read_csv(r"src\data\RUS.csv")

# Useful features: points, wins, difference between scored and missed goals, scored goals number
# HG, AG, RES columns


def print_table(table_df):
    """Prints dataframe using PrettyTable() class"""
    table = PrettyTable()
    table.field_names = table_df.columns
    for i in range(len(table_df)):
        table.add_row(table_df.iloc[i, :])
    print(table)


def all_teams(season):
    """Prints all teams of season"""
    teams = data[(data.Season == season)].Home.unique()
    for i in teams:
        print(i)


def matches_of(team, season):
    """Returns all matches of a given team"""
    matches = data[(data.Season == season)]
    return matches[(matches.Home == team) | (matches.Away == team)].iloc[:, 2:10]


def matches_of_date(date):
    """Returns all matches, played on a given date"""
    return data[(data.Date == date)].iloc[:, 2:10]


class RankingTable:
    def __init__(self, season):
        self.data = data[data.Season == season]
        self.season = season
        self.teams = self.data["Home"].unique()
        self.goal_difference, self.scored = self.goal_difference()
        self.wins, self.draws, self.losses = self.wins_draws_losses()
        self.points = self.points()

        self.table = pd.DataFrame({"Team Name": self.teams,
                                   "Number Of Wins": self.wins,
                                   "Number Of Draws": self.draws,
                                   "Number Of Losses": self.losses,
                                   "Goal Difference": self.goal_difference,
                                   "Scored Goals": self.scored,
                                   "Points": self.points})

    def goal_difference(self):
        """Returns list of difference between scored and missed goals for each team"""
        scored = list(map(lambda team:
                          self.data[(self.data.Home == team)].loc[:, "HG"].sum() +
                          self.data[(self.data.Away == team)].loc[:, "AG"].sum(),
                          self.teams))

        missed = list(map(lambda team:
                          self.data[(self.data.Home == team)].loc[:, "AG"].sum() +
                          self.data[(self.data.Away == team)].loc[:, "HG"].sum(),
                          self.teams))

        return [scored[i] - missed[i] for i in range(len(self.teams))], scored

    def wins_draws_losses(self):
        """Returns lists of wins, draws and losses numbers for each team"""
        wins = [0 for _ in self.teams]
        draws = [0 for _ in self.teams]
        losses = [0 for _ in self.teams]

        for ind, team in enumerate(self.teams):
            try:
                wins[ind] = self.data[self.data.Home == team].Res.value_counts().H +\
                             self.data[self.data.Away == team].Res.value_counts().A
            except AttributeError:
                pass

            try:
                draws[ind] = self.data[(self.data.Home == team) | (self.data.Away == team)].Res.value_counts().D
            except AttributeError:
                pass

            try:
                losses[ind] = self.data[self.data.Home == team].Res.value_counts().A +\
                               self.data[self.data.Away == team].Res.value_counts().H
            except AttributeError:
                pass

        return wins, draws, losses

    def points(self):
        """Returns list of points for each team"""
        points = [0 for _ in self.teams]
        for i in range(len(points)):
            points[i] = self.wins[i] * 3 + self.draws[i]
        return points

    def rank(self):
        """Returns sorted ranking table of RPL teams"""
        self.table.sort_values(by=["Points", "Number Of Wins", "Goal Difference", "Scored Goals"],
                               ascending=False, inplace=True)
        self.table.index = range(len(self.table))

        # ranking places
        places = [1]
        for i in range(1, len(self.table)):
            if self.table.loc[i, "Points"] == self.table.loc[i - 1, "Points"] and \
                    self.table.loc[i, "Number Of Wins"] == self.table.loc[i - 1, "Number Of Wins"] and \
                    self.table.loc[i, "Goal Difference"] == self.table.loc[i - 1, "Goal Difference"] and \
                    self.table.loc[i, "Scored Goals"] == self.table.loc[i - 1, "Scored Goals"]:
                places.append(places[i - 1])
            else:
                places.append(places[i - 1] + 1)

        self.table["Ranking Place"] = places
        return self.table
