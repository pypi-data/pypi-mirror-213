from typing import Optional

from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession


class JumpGate(WaypointType):
    def __init__(self, waypoint: str, session: AutoTradersSession, data=None):
        self.faction_symbol: Optional[str] = ""
        self.jump_range: Optional[int] = None
        super().__init__(waypoint, "jump-gate", session, data)

    def update(self, data: dict = None):
        if data is None:
            data = self.get()["data"]
        self.jump_range = data["jumpRange"]
        if "factionSymbol" in data:
            self.faction_symbol = data["factionSymbol"]
