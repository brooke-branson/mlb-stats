import statsapi
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from print_window import PrintWindow
import matplotlib.pyplot as plt

class Team:
    """
    Creates the team object which will contain all the information about specific playerts, leaders, games, and so on.
    """

    def __init__(self, name, id, city):
        """
        Initializes the team object by sending the ID to the mlb API, using info passed by the user.

        :param name: Team Full name
        :param id: Team unique ID for the API
        :param city: City of the team
        """
        self.name = name
        # self.nickname:
        self.id = id
        self.city = city

        # self.printer = PrintWindow()

    def help(self, type=None):
        """
        Quick call command to see the possible tags for stat calls

        :param help_reqeust: Type of tags you want to see:
        :return: print statement with related type tags for the meta endpoint call
        """

        meta_types = [
                'leagueLeaderTypes', 'awards', 'baseballStats', 'eventTypes', 'gameStatus', 'gameTypes',
                'hitTrajectories', 'jobTypes', 'languages', 'leagueLeaderTypes', 'logicalEvents', 'metrics',
                'pitchCodes', 'pitchTypes', 'platforms', 'positions', 'reviewReasons', 'rosterTypes', 'windDirection',
                'scheduleEventTypes', 'situationCodes', 'sky', 'standingsTypes', 'statGroups', 'statTypes'
        ]

        if type == None:
            print("Available meta tags are:\n")
            for type in meta_types:
                print(f'{type}.')
        else:
            return statsapi.meta(type=type)

    def leader_lookup(self, limit=10, plot=False, stat="homeRuns", df_return=False):
        """
        Prints a list of the HR Leaders based on the amount passed thru. Default is top 10

        :param limit: Default value = 10. How deep you want the list to be
                plot: Boolean. If set to True, will show a plot of the HR leaders, Defualt = False.
                df_return: If True, will return the data as a Pandas DF, instead of a printed statement.
        :return: Returns a usable Pandas DataFrame called hr_df
        """

        stat_info = statsapi.team_leaders(teamId=self.id, leaderCategories=stat, limit=limit)
        usable = statsapi.team_leader_data(teamId=self.id, leaderCategories=stat, limit=limit)

        names = []
        values = []

        for x in usable:
            names.append(x[1])
            try:
                values.append(int(x[2]))
            except:
                values.append(float(x[2]))
            finally:
                values.append(str(x[2]))

        hr_df = pd.DataFrame(usable, columns=['Rank', 'Name', 'Value'])

        if plot:
            plt.figure(figsize=(10, 5))  # Adjust figure size if needed
            plt.plot(names, values, marker='o')

            # Add text annotations for each point
            for i, (player, value) in enumerate(zip(names, values)):
                plt.text(i, value, player, ha='right', va='bottom', rotation=0, fontsize=11)

            plt.xlabel("Players")
            plt.ylabel(f"{type}")
            plt.xticks([])
            plt.yticks(list(range(0, max(values))))
            plt.title(f'{self.name} {type}')
            plt.show()

        print(stat_info)

        if df_return:
            return hr_df
        else:
            return stat_info

    def last_game(self):
        """
        Prints the info for the last game played by the team.

        :return:
        """
        self.printer.print(statsapi.boxscore(gamePk=statsapi.last_game(self.id)))

