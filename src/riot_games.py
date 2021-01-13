
import os
import requests
import riotwatcher
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")  # load env variables


class DataDragon:
    def __init__(self, region='na1', language='en_US'):

        self.lol = riotwatcher.LolWatcher(os.getenv('RIOT_API_KEY'))
        self.language = language
        self.url = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/{query}'

        self.region = region
        self.version = self.lol.data_dragon.versions_for_region(region=self.region)['v']
        self.manifest = self.lol.data_dragon.champions(version=self.version, full=False)['data']
        self.champions = [v['name'] for _, v in self.manifest.items()]

    def get_champion_cool_down(self, champion: str) -> dict:
        query = f'champion/{champion}.json'
        response = requests.get(self.url.format(version=self.version, language=self.language, query=query)).json()['data']
        spells = zip(['q', 'w', 'e', 'r'], response[champion]['spells'])

        cooldowns = {k: v['cooldownBurn'] for k, v in spells}
        return cooldowns


if __name__ == '__main__':
    d = DataDragon().get_champion_cool_down('Aatrox')
