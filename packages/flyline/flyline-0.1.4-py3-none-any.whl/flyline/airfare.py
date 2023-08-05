from .schemas import AirFare

# from .types import AirFareRequest


class AirFareAPI:
    async def get_airfares(self, data: dict) -> AirFare:
        async with self.session.post(f"{self.BASE_URL}/flights/shop/", json=data) as response:
            res = await self.parse_response(response)
            return AirFare.from_json(res)
