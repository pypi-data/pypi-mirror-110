from typing import List

from .schemas import SeatMap


class AirSeatMapAPI:
    async def get_seat_map(self, carrier: str, aircraft: str) -> List[SeatMap]:
        data = {"carrier": carrier, "aircraft": aircraft}
        async with self.session.post(f"{self.BASE_URL}/seat-maps/", json=data) as response:
            res = await self.parse_response(response)
            return SeatMap.from_json(res)
