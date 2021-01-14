
import asyncio
import callofduty
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from callofduty import Mode, Platform, Title

load_dotenv(dotenv_path=".env")  # load env variables


class Warzone:
    def __init__(self, email, password):
        self.loop = asyncio.get_event_loop()
        self.email = email
        self.password = password
        self.client = None

    async def _initialize_client(self):
        self.client = await callofduty.Login(self.email, self.password)

    async def _fetch_lobby(self, username: str) -> tuple:
        if not self.client:
            await self._initialize_client()

        player = await self.client.GetPlayer(Platform.Activision, username)  # requires identifier
        current_match = (await player.matches(Title.ModernWarfare, Mode.Warzone, limit=1))[0]
        print(current_match.id)
        full_match = await self.client.GetFullMatch(Platform.Activision, Title.ModernWarfare, Mode.Warzone, current_match.id)

        start_time = datetime.fromtimestamp(full_match['allPlayers'][0]['utcStartSeconds'])
        print(start_time)

        player_stats = []
        for i in full_match['allPlayers']:
            player = {'kdRatio': i['playerStats']['kdRatio'],
                      'kills': i['playerStats']['kills'],
                      'deaths': i['playerStats']['deaths'],
                      'damageDone': i['playerStats']['damageDone'],
                      'team': i['player']['team'],
                      'player': i['player']['username']}
            player_stats.append(player)
        df = pd.DataFrame(player_stats).sort_values('damageDone', ascending=False).reset_index()
        return start_time, df

    async def post_game_stats(self, username: str, output_data=False):
        name = username.split('#')[0].lower().capitalize()
        start_time, df = await self._fetch_lobby(username)
        player = df[df['player'] == name]
        player_team = df[df['team'] == player['team'].iloc[0]]
        print(player_team)

        groups = df[['team', 'kdRatio', 'kills', 'deaths', 'damageDone']]\
            .groupby('team')\
            .mean()\
            .sort_values(by='kdRatio', ascending=False)\
            .reset_index()

        print(groups[groups['team'] == player['team'].iloc[0]])
        print(groups.head(5))

        if output_data:
            return start_time, player_team, groups
