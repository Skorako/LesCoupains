import asyncio
import time
from typing import TYPE_CHECKING

import opengsq

if TYPE_CHECKING:
    from discordgsm.gamedig import GamedigResult


class Teamspeak3:
    def __init__(self, address: str, query_port: int, voice_port: int):
        self.address = address
        self.query_port = query_port
        self.voice_port = voice_port

    async def query(self):
        teamspeak3 = opengsq.Teamspeak3(self.address, self.query_port, self.voice_port, 10)
        start = time.time()
        info, clients, channels = await asyncio.gather(teamspeak3.get_info(), teamspeak3.get_clients(), teamspeak3.get_channels())
        ping = int((time.time() - start) * 1000)

        result: GamedigResult = {
            'name': info.get('virtualserver_name', ''),
            'map': '',
            'password': int(info.get('virtualserver_flag_password', '0')) == 1,
            'maxplayers': int(info.get('virtualserver_maxclients', '0')),
            'players': [{'name': player['client_nickname'], 'raw': player} for player in clients if player.get('client_type') == '0'],
            'bots': [],
            'connect': f'{self.address}:{self.query_port}',
            'ping': ping,
            'raw': {
                'info': info,
                'channels': channels
            }
        }

        return result


if __name__ == '__main__':
    async def main():
        teamspeak3 = Teamspeak3('199.231.233.138', 10011, 9987)
        print(await teamspeak3.query())

    asyncio.run(main())
