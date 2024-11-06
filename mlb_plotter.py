import statsapi

# sched = statsapi.schedule(start_date='07/01/2018',end_date='07/31/2018',team=143,opponent=121)
team_name = input("Team code? (abbrev. ex: sd): \n")

teams = statsapi.lookup_team(lookup_value=team_name)

if len(teams) == 1:
    print(f"The {teams[0]['name']} with the ID {teams[0]['id']}.\n")
else:
    print("Teams from that city are:\n")
    for team in teams:
        print(f"The {team['name']} with the ID {team['id']}.\n")
