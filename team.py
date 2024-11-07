import statsapi
import pandas as pd

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
            statsapi.meta(type=type)

    def hr_leaders(self, limit=10):
        """
        Prints a list of the HR Leaders based on the amount passed thru. Default is top 10

        :param limit: Default value = 10. How deep you want the list to be

        :return: Returns a usable Pandas DataFrame called hr_df
        """

        hr_info = statsapi.team_leaders(teamId=self.id, leaderCategories="homeRuns", limit=limit)

        usable = statsapi.team_leader_data(teamId=self.id, leaderCategories='homeRuns', limit=limit)

        hr_df = pd.DataFrame(usable, columns=['Rank', 'Name', 'Value'])

        print(hr_info)

        return hr_df