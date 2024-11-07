import statsapi
from team import Team
import pandas as pd

"""
This works as the user interface, communicating with the Teams object to provide requested information from the API
"""

user_in = input("Team code? (abbrev. ex: sd): \n")

choice = statsapi.lookup_team(lookup_value=user_in)

if len(choice) == 1:
    print(f"The {choice[0]['name']} with the ID {choice[0]['id']}.\n")
    team_id = choice[0]['id']
else:
    print("Teams from that city are:\n")
    for team in choice:
        print(f"The {team['name']} with the ID {team['id']}.\n")

    team_id = input("What is the team ID you want to look at?\n")

choice = statsapi.lookup_team(lookup_value=team_id)[0]

# The meta end point for the leader types, used for reference.
# statsapi.meta(type="leagueLeaderTypes")

name = choice['name']
id = choice['id']
city = choice['locationName']

# Create the Team object using the team selected by the user. Initializes with name, id and City names.
user_team = Team(name, id, city)
user_team.hr_leaders()

