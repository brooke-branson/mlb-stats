import pytest
from unittest.mock import patch
import sys
from pathlib import Path
import pandas as pd
# Dynamically add the parent directory of the mlb-stats folder to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent / "mlb-stats"
sys.path.insert(0, str(ROOT_DIR))
from team import Team


@patch("team.statsapi.team_leaders")
@patch("team.statsapi.team_leader_data")
def test_leader_lookup_df_return(mock_leader_data, mock_leaders):

    mock_leaders.return_value = "Top HR leaders: 1. Player A - 40, 2. Player B - 35"
    mock_leader_data.return_value = [
        ["1", "Player A", "55"],
        ["2", "Player B", "55"]
    ]

    team = Team(name="Yankees", id=1, city="New York")

    result = team.leader_lookup(limit=10, df_return=True)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 3)  # 2 rows, 3 columns
    assert list(result.columns) == ["Rank", "Name", "Value"]
    assert result.iloc[0]["Name"] == "Player A"
    assert result.iloc[0]["Value"] == "55"


@patch("team.statsapi.team_leaders")
@patch("team.statsapi.team_leader_data")
def test_leader_lookup_stat_info(mock_leader_data, mock_leaders):

    mock_leaders.return_value = "Top HR leaders: 1. Player A - 40, 2. Player B - 35"
    mock_leader_data.return_value = [
        ["1", "Player A", "40"],
        ["2", "Player B", "35"]
    ]

    team = Team(name="Yankees", id=1, city="New York")

    result = team.leader_lookup(limit=2, df_return=False)

    assert isinstance(result, str)
    assert "Player A" in result
    assert "40" in result


@patch("team.statsapi.team_leaders")
@patch("team.statsapi.team_leader_data")
def test_leader_lookup_empty_data(mock_leader_data, mock_leaders):

    mock_leaders.return_value = "No leaders found."
    mock_leader_data.return_value = []

    team = Team(name="Yankees", id=1, city="New York")

    result = team.leader_lookup(limit=0, df_return=False)

    assert result == "No leaders found."


@patch("team.statsapi.boxscore")
@patch("team.statsapi.last_game")
def test_last_game_return(mock_lastgame_data, mock_boxscore_data):

    # Create the mock values to mimic the function
    mock_lastgame_data.return_value = {"gamePk": 123456}
    mock_boxscore_data.return_value = {
        "teams": {
            "home": {"team": {"name": "Yankees"}, "score": 5},
            "away": {"team": {"name": "Red Sox"}, "score": 3},
        }
    }

    # Create the object
    team = Team(name='Yankees', id=1, city='New York')

    # Create and check the results to match the return value
    result = team.last_game()

    assert result == {
        "teams": {
            "home": {"team": {"name": "Yankees"}, "score": 5},
            "away": {"team": {"name": "Red Sox"}, "score": 3},
        },
    }
