from typing import List, Optional

from .schemas import Schedule


class AirScheduleAPI:
    async def get_schedules_by_flight_number(self, airline: str, date: str, flight_number: str) -> Optional[Schedule]:
        data = {
            "airline": airline,
            "date": date,
            "flight_number": flight_number,
        }
        async with self.session.post(f"{self.BASE_URL}/schedule-flight/", json=data) as response:
            res = await self.parse_response(response)
            if "message" in res:
                return None
            return Schedule.from_json(res)

    async def get_schedules_by_route(
        self, airline: str, origin: str, destination: str, date: str
    ) -> Optional[List[Schedule]]:
        data = {
            "airline": airline,
            "origin": origin,
            "destination": destination,
            "date": date,
        }
        async with self.session.post(f"{self.BASE_URL}/schedule/", json=data) as response:
            res = await self.parse_response(response)
            if "message" in res:
                return None
            return Schedule.from_json(res)
