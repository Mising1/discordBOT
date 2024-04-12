import requests
from dotenv import load_dotenv
import os

load_dotenv()

class RiotAPI:
    def __init__(self, api_key, puuid):
        self.api_key = api_key
        self.puuid = puuid
        self.matches = []
        self.toTxt = []

    def get_match_ids(self):
        api_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?startTime=1709251200&type=ranked&start=0&count=8&api_key={self.api_key}"
        self.gry = requests.get(api_url).json()
        return self.gry

    def get_match_data(self, match_ids):
        api_url = "https://europe.api.riotgames.com/lol/match/v5/matches/"
        for i in match_ids:
            self.matches += requests.get(api_url + i + "?api_key=" + self.api_key).json()['info']["participants"]

    def count_wins_and_losses(self):
        i = 0
        for one in self.matches:
            if one["puuid"] == self.puuid:
                if one["win"] == True:
                    self.toTxt.append(self.gry[i]+": win")
                    i += 1
                else:
                    self.toTxt.append(self.gry[i]+": lose")
                    i += 1

    def print_results(self):
        f = open("gry.txt", "a")
        tab = self.read_results()
        for i in self.toTxt:
            if i not in tab:
                f.write(i + "\n")
        f.close()

    def read_results(self):
        f = open("gry.txt", "r")
        tab = f.readlines()
        tab = [x.strip() for x in tab]
        f.close()
        return tab


def main():
    api = RiotAPI(os.getenv("RIOT_API_KEY"), "jCAc2hNySnG-cjBWS8_gJeIuFzqVf7rKtBc0uPwP7u1r_6fW0k5wQXQOjmMRe-S0xDttchdtQsNbbg")
    match_ids = api.get_match_ids()
    api.get_match_data(match_ids)
    api.count_wins_and_losses()
    api.print_results()
    win = 0
    lose = 0
    for i in api.read_results():
        if "win" in i:
            win += 1
        else:
            lose += 1
    return win, lose
