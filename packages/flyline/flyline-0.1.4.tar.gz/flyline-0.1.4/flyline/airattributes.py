from typing import TypedDict

from .schemas import AirAttribute, CabinClass


class AirAttributeFlightNumberRequestDataType(TypedDict):
    cabin_class: CabinClass
    carrier: str
    departure: str
    arrival: str
    departure_date: str
    flight_no: str


class SliceDeparture(TypedDict):
    code: str
    date: str


class SliceArrival(TypedDict):
    code: str


class SliceType(TypedDict):
    departure: SliceDeparture
    arrival: SliceArrival


class AirAttributeRouteRequestDataType(TypedDict):
    cabin_class: CabinClass
    slices: SliceType
    passengers: int


class AirAttributeAPI:
    async def get_airattributes_by_flight_number(self, data: dict) -> AirAttribute:
        url = f"{self.BASE_URL}/search/attributes/flight/"
        async with self.session.post(url, json=data) as response:
            res = await self.parse_response(response)
            return AirAttribute.from_json(res)

    async def get_airattributes_by_route(self, data: dict) -> AirAttribute:
        url = f"{self.BASE_URL}/search/attributes/route/"
        async with self.session.post(url, json=data) as response:
            res = await self.parse_response(response)
            return AirAttribute.from_json(res)
