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

    def hr_leaders(self, limit=10):
        print(statsapi.team_leaders(teamId=self.id, leaderCategories="homeRuns", limit=limit))

