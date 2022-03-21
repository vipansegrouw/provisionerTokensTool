from typing import List

from gw2api import GuildWars2Client


class GW2Client:
    def gw2_client(self):
        return GuildWars2Client()

    def get_prices_from_api(self, ids: List[int] = None):
        return self.gw2_client().commerceprices.get(ids=ids)

