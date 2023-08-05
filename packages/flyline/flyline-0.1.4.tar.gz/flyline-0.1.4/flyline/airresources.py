from typing import Any, Dict, List, Optional, Tuple, Union

from .errors import FlylinePayloadError
from .schemas import (
    Aircraft,
    AircraftList,
    Airline,
    AirlineList,
    Airport,
    AirportList,
    Beverage,
    BeverageList,
    CabinClassMapping,
    City,
    CityList,
    Entertainment,
    EntertainmentList,
    Food,
    FoodList,
    PaginationMeta,
    Power,
    PowerList,
    SeatLayout,
    SeatLayoutList,
    SeatType,
    SeatTypeList,
    Wifi,
    WifiList,
)

Resource = Union[Aircraft, Airline, Airport, Beverage, City, Entertainment, Food, Power, SeatType, SeatLayout, Wifi]


class AirResourcesAPI:
    async def _get_resources(self, _class: Any, endpoint: str) -> Tuple[PaginationMeta, List[Resource]]:
        async with self.session.get(f"{self.BASE_URL}/{endpoint}/") as response:
            res = await self.parse_response(response)
            try:
                pagination_meta = res["meta"]
                data = res["data"]
            except KeyError:
                raise FlylinePayloadError()
            else:
                return PaginationMeta.from_json(pagination_meta), _class.from_json(data)

    async def _get_resource(self, _class: Any, endpoint: str, code: str) -> Optional[Resource]:
        async with self.session.get(f"{self.BASE_URL}/{endpoint}/{code}/") as response:
            res = await self.parse_response(response)
            try:
                data = res["data"]
            except KeyError:
                raise FlylinePayloadError()
            return _class.from_json(data)

    async def get_aircrafts(self) -> AircraftList:
        res = await self._get_resources(_class=Aircraft, endpoint="aircraft")
        return AircraftList(pagination=res[0], data=res[1])

    async def get_aircraft(self, iata_code: str) -> Optional[Aircraft]:
        return await self._get_resource(_class=Aircraft, endpoint="aircraft", code=iata_code)

    async def get_airlines(self) -> AirlineList:
        res = await self._get_resources(_class=Airline, endpoint="airlines")
        return AirlineList(pagination=res[0], data=res[1])

    async def get_airline(self, iata_code: str) -> Airline:
        return await self._get_resource(_class=Airline, endpoint="airlines", code=iata_code)

    async def get_airports(self) -> AirportList:
        res = await self._get_resources(_class=Airport, endpoint="airports")
        return AirportList(pagination=res[0], data=res[1])

    async def get_airport(self, iata_code: str) -> Optional[Airport]:
        return await self._get_resource(_class=Airport, endpoint="airports", code=iata_code)

    async def get_airports_by_city(self, city_iata_code: str) -> List[Airport]:
        async with self.session.get(f"{self.BASE_URL}/cities/{city_iata_code}/airports/") as response:
            res = await self.parse_response(response)
            return Airport.from_json(res.get("data", []))

    async def get_cities(self) -> CityList:
        res = await self._get_resources(_class=City, endpoint="cities")
        return CityList(pagination=res[0], data=res[1])

    async def get_city(self, iata_code: str) -> Optional[City]:
        return await self._get_resource(_class=City, endpoint="cities", code=iata_code)

    async def get_cabin_class_mapping(
        self, carrier: Optional[str] = None, cabin_class: Optional[str] = None
    ) -> Dict[str, List[CabinClassMapping]]:
        params = {}
        if carrier:
            params["carrier"] = carrier
        if cabin_class:
            params["cabin_class"] = cabin_class

        async with self.session.get(f"{self.BASE_URL}/cabin-booking/", params=params) as response:
            res = await self.parse_response(response)
            return {carrier: CabinClassMapping.from_json(data) for carrier, data in res.items()}

    async def get_seat_types(self) -> SeatTypeList:
        res = await self._get_resources(_class=SeatType, endpoint="seats")
        return SeatTypeList(pagination=res[0], data=res[1])

    async def get_seat_layouts(self) -> SeatLayoutList:
        res = await self._get_resources(_class=SeatLayout, endpoint="layouts")
        return SeatLayoutList(pagination=res[0], data=res[1])

    async def get_foods(self) -> FoodList:
        res = await self._get_resources(_class=Food, endpoint="foods")
        return FoodList(pagination=res[0], data=res[1])

    async def get_beverages(self) -> BeverageList:
        res = await self._get_resources(_class=Beverage, endpoint="beverages")
        return BeverageList(pagination=res[0], data=res[1])

    async def get_entertainments(self) -> EntertainmentList:
        res = await self._get_resources(_class=Entertainment, endpoint="entertainments")
        return EntertainmentList(pagination=res[0], data=res[1])

    async def get_wifis(self) -> WifiList:
        res = await self._get_resources(_class=Wifi, endpoint="wifis")
        return WifiList(pagination=res[0], data=res[1])

    async def get_powers(self) -> PowerList:
        res = await self._get_resources(_class=Power, endpoint="powers")
        return PowerList(pagination=res[0], data=res[1])
