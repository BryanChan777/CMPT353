import sys
import urllib
import urllib.request
import os
import json, csv, collections
import argparse
import pandas as pd
## Some code was taken from https://github.com/TianyangZhan/OverwatchLeaguePredictor/blob/master/owl.py 
## as we needed a way to parse the json file retrieved by the api into a csv file 

class OwlData:

    def __init__ (self):
        self.teamdata = {}
        self.playerdata = {}
        self.table = [{}]
        self.schedule = []
        self.stage = ""
        self.week = ""


    def to_dict(self):
        teams = []
        for i in range(len(self.teamdata["data"])):
            temp = {}
            temp["name"] = self.teamdata["data"][i]["name"]
            temp["abbr"] = self.teamdata["data"][i]["abbreviatedName"]
            temp["matchWin"] = self.teamdata["data"][i]["league"]["matchWin"]
            temp["matchLoss"] = self.teamdata["data"][i]["league"]["matchLoss"]
            temp["matchDraw"] = self.teamdata["data"][i]["league"]["matchDraw"]
            temp["gameWin"] = self.teamdata["data"][i]["league"]["gameWin"]
            temp["gameLoss"] = self.teamdata["data"][i]["league"]["gameLoss"]
            temp["gameTie"] = self.teamdata["data"][i]["league"]["gameTie"]
            
            #stats for offense
            temp["dpsK/D"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][0] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][1]
            temp["dpsUlt/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][3] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]
            temp["dpsHeroDamage/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][5] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]            
            temp["dpsFinalBlows/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][6] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]            
            #stats for tank
            if 'tank' in self.playerdata[int(self.teamdata["data"][i]["id"])]:
                temp["tankK/D"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][0] / self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][1]
                temp["tankUlt/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][3] / self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][4]
                temp["tankHeroDamage/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][5] / self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][4]
                temp["tankFinalBlows/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][6] / self.playerdata[int(self.teamdata["data"][i]["id"])]["tank"][4]
            else: #use offense stats if no tank players
                temp["tankK/D"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][0] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][1]
                temp["tankUlt/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][3] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]
                temp["tankHeroDamage/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][5] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]
                temp["tankFinalBlows/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][6] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]
            #stats for support
            if 'support' in self.playerdata[int(self.teamdata["data"][i]["id"])]:
                temp["supportHealing"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["support"][2] / self.playerdata[int(self.teamdata["data"][i]["id"])]["support"][4]
                temp["supportUlt/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["support"][3] / self.playerdata[int(self.teamdata["data"][i]["id"])]["support"][4]
            else: #use offense stats if no support players
                temp["supportHealing"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][2] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]
                temp["supportUlt/10mins"] = self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][3] / self.playerdata[int(self.teamdata["data"][i]["id"])]["offense"][4]
                
            teams.append(temp)
        self.table = teams

    def playerstats_todict(self):
        players=[]
        url = urllib.request.urlopen("https://api.overwatchleague.com/stats/players?stage_id=regular_season")
        data = json.loads(url.read().decode())
        for i in range(len(data["data"])):
            temp = {}
            temp["playerId"] = data["data"][i]["playerId"]
            temp["teamId"] = data["data"][i]["teamId"]
            temp["role"] = data["data"][i]["role"]
            temp["name"] = data["data"][i]["name"]
            temp["team"] = data["data"][i]["team"]
            temp["eliminations_avg_per_10m"] = data["data"][i]["eliminations_avg_per_10m"]
            temp["deaths_avg_per_10m"]= data["data"][i]["deaths_avg_per_10m"]
            temp["healing_avg_per_10m"] = data["data"][i]["healing_avg_per_10m"]
            temp["ultimates_earned_avg_per_10m"]= data["data"][i]["ultimates_earned_avg_per_10m"]
            temp["hero_damage_avg_per_10m"]= data["data"][i]["hero_damage_avg_per_10m"]
            temp["final_blows_avg_per_10m"]= data["data"][i]["final_blows_avg_per_10m"]
            temp["time_played_total"]= data["data"][i]["time_played_total"]

            players.append(temp)
        self.playerstable = players


    def get_teamdata(self):
        url = urllib.request.urlopen("https://api.overwatchleague.com/v2/standings?locale=en_US")
        teamdata = json.loads(url.read().decode())
        self.teamdata = teamdata


    def get_playerdata(self):
        url = urllib.request.urlopen("https://api.overwatchleague.com/stats/players?stage_id=regular_season")
        data = json.loads(url.read().decode())
        hashmap = {}
        for i in range(len(data["data"])):
            if not data["data"][i]["teamId"] in hashmap:
                hashmap[data["data"][i]["teamId"]] = {}
            if not data["data"][i]["role"] in hashmap[data["data"][i]["teamId"]]:
                hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]] = [0,0,0,0,0,0,0]

            hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]][0] += data["data"][i]["eliminations_avg_per_10m"]
            hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]][1] += data["data"][i]["deaths_avg_per_10m"]
            hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]][2] += data["data"][i]["healing_avg_per_10m"]
            hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]][3] += data["data"][i]["ultimates_earned_avg_per_10m"]
            hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]][5] += data["data"][i]["hero_damage_avg_per_10m"]
            hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]][6] += data["data"][i]["final_blows_avg_per_10m"]
            #total player count
            if data["data"][i]["eliminations_avg_per_10m"]:
                hashmap[data["data"][i]["teamId"]][data["data"][i]["role"]][4] += 1
        self.playerdata = hashmap

    def save_to_file(self,fileName):
        colname = self.table[0].keys()
        try:
            with open(fileName, 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=colname)
                dict_writer.writeheader()
                dict_writer.writerows(self.table)
        except IOError:
            print("I/O error")

    def playerstats_save_to_file(self,fileName):
        colname = self.playerstable[0].keys()
        try:
            with open(fileName, 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=colname)
                dict_writer.writeheader()
                dict_writer.writerows(self.playerstable)
        except IOError:
            print("I/O error")

    def read_from_file(self,fileName):
        with open(fileName) as f:
            content = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
        self.table = content
    
def main():
#     # Get Player Stats
#     df_1 = pd.read_json('https://api.overwatchleague.com/stats/players')
#     print(df_1)
#     for col in df_1.columns:
#         print(col)
#     df_1.to_json('owl_player_info.json')

#     # Get all OWL Teams
#     df_2 = pd.read_json('https://api.overwatchleague.com/v2/teams',lines=True)
#     print(df_2)
#     df_2.to_json('owl_teams.json')

#     # Get OWL Rankings 
#     df_3 = pd.read_json('https://api.overwatchleague.com/rankings', lines=True)
#     print(df_3)
#     df_3.to_json('owl_rankings.json')
    owl = OwlData()
    file = "owl_data.csv"
    file2 = "owl_playerstats.csv"
    owl.get_playerdata()
    owl.get_teamdata()
    owl.to_dict()
    owl.save_to_file(file)

    owl.playerstats_todict()
    owl.playerstats_save_to_file(file2)

    #owl.get_schedule(1,1)
    df = pd.read_csv('owl_data.csv')
    df2 = pd.read_csv('owl_playerstats.csv')
    print(df)
    print(df2)


if __name__ == '__main__':
    main()