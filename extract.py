import sys
import pandas as pd

def main():
    # Get Player Stats
    df_1 = pd.read_json('https://api.overwatchleague.com/stats/players')
    print(df_1)
    df_1.to_json('owl_player_info.json')

    # Get all OWL Teams
    df_2 = pd.read_json('https://api.overwatchleague.com/v2/teams',lines=True)
    print(df_2)
    df_2.to_json('owl_teams.json')

    # Get OWL Rankings 
    df_3 = pd.read_json('https://api.overwatchleague.com/rankings', lines=True)
    print(df_3)
    df_3.to_json('owl_rankings.json')

if __name__ == '__main__':
    main()