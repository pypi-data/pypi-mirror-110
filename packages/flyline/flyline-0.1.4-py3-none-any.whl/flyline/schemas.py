from dataclasses import dataclass
from dataclasses import fields as dataclass_fields
from datetime import datetime
from decimal import Decimal
from typing import Any, List, Literal, Optional, Union, get_args, get_origin

PassengerType = Literal["adult", "child", "infant"]
ServiceMetaType = Literal["checked", "carry_on"]
CabinClass = Literal["first", "business", "premium_economy", "economy"]


class FlylineBaseDataClass:
    @classmethod
    def from_json(cls, json_data: Union[dict, list]) -> Any:
        def convert_dict2dataclass(field_type, v):
            if hasattr(field_type, "from_json"):
                return field_type.from_json(v)
            elif field_type is Decimal:
                return Decimal(str(v))
            elif field_type is datetime:
                return datetime.fromisoformat(v)
            else:
                return v

        ret = []
        should_be_flatten = False
        if not isinstance(json_data, list):
            json_data = [json_data]
            should_be_flatten = True

        for ele_data in json_data:
            cdata = {}
            for field in dataclass_fields(cls):
                key = field.name
                value = ele_data.get(key, None)
                if value is not None:
                    if get_origin(field.type) is list:
                        cdata[key] = [convert_dict2dataclass(get_args(field.type)[0], item) for item in value]
                    else:
                        cdata[key] = convert_dict2dataclass(field.type, value)
                else:
                    cdata[key] = None
            ret.append(cls(**cdata))

        return ret[0] if should_be_flatten else ret


@dataclass(frozen=True)
class PaginationMeta(FlylineBaseDataClass):
    limit: int
    after: Optional[str] = None
    before: Optional[str] = None


# Basic & Air Resources Schemas
@dataclass(frozen=True)
class Aircraft(FlylineBaseDataClass):
    iata_code: str
    name: str


@dataclass(frozen=True)
class AircraftList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Aircraft]


@dataclass(frozen=True)
class Airline(FlylineBaseDataClass):
    iata_code: str
    name: str


@dataclass(frozen=True)
class AirlineList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Airline]


@dataclass(frozen=True)
class City(FlylineBaseDataClass):
    iata_code: str
    name: str
    iata_country_code: str


@dataclass(frozen=True)
class CityList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[City]


@dataclass(frozen=True)
class Airport(FlylineBaseDataClass):
    iata_code: str
    name: str
    iata_country_code: str
    latitude: Decimal
    longitude: Decimal
    icao_code: str
    time_zone: str
    city: City


@dataclass(frozen=True)
class AirportList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Airport]


@dataclass(frozen=True)
class SeatType(FlylineBaseDataClass):
    display_text: str
    pitch: str
    width: str


@dataclass(frozen=True)
class SeatTypeList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[SeatType]


@dataclass(frozen=True)
class SeatLayout(FlylineBaseDataClass):
    display_text: str


@dataclass(frozen=True)
class SeatLayoutList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[SeatLayout]


@dataclass(frozen=True)
class Food(FlylineBaseDataClass):
    display_text: str
    cost: str


@dataclass(frozen=True)
class FoodList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Food]


@dataclass(frozen=True)
class Beverage(FlylineBaseDataClass):
    display_text: str
    type: str
    alcoholic_cost: str
    nonalcoholic_cost: str


@dataclass(frozen=True)
class BeverageList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Beverage]


@dataclass(frozen=True)
class Entertainment(FlylineBaseDataClass):
    display_text: str


@dataclass(frozen=True)
class EntertainmentList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Entertainment]


@dataclass(frozen=True)
class Wifi(FlylineBaseDataClass):
    display_text: str
    quality: str
    cost: str


@dataclass(frozen=True)
class WifiList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Wifi]


@dataclass(frozen=True)
class Power(FlylineBaseDataClass):
    display_text: str
    multiple_at_seat: str
    usb_port: str
    power_outlet: str


@dataclass(frozen=True)
class PowerList(FlylineBaseDataClass):
    pagination: PaginationMeta
    data: List[Power]


# Air Fare Schemas
@dataclass(frozen=True)
class Passenger(FlylineBaseDataClass):
    id: str
    age: int
    type: PassengerType


@dataclass(frozen=True)
class SegmentBaggage(FlylineBaseDataClass):
    type: ServiceMetaType
    quantity: int


@dataclass(frozen=True)
class SegmentPassenger(FlylineBaseDataClass):
    passenger_id: str
    baggages: List[SegmentBaggage]


@dataclass(frozen=True)
class Segment(FlylineBaseDataClass):
    id: str
    aircraft: str
    origin: str
    origin_terminal: str
    departing_at: datetime
    destination: str
    destination_terminal: str
    arriving_at: datetime
    distance: int
    duration: str
    marketing_carrier: str
    marketing_carrier_flight_number: str
    operating_carrier: str
    operating_carrier_flight_number: str
    passengers: List[SegmentPassenger]


@dataclass(frozen=True)
class Slice(FlylineBaseDataClass):
    origin: str
    destination: str
    duration: str
    segments: List[Segment]


@dataclass(frozen=True)
class FareRulesTicketing(FlylineBaseDataClass):
    endorsements: List[str]


@dataclass(frozen=True)
class FareRules(FlylineBaseDataClass):
    refundable: bool
    corporate: bool
    change_fee: bool
    cancel_fee: bool
    cancellation_change_fees: str
    seat_selection: str
    boarding_zone: str
    points_mileage: str
    ticketing: FareRulesTicketing


@dataclass(frozen=True)
class FareSegmentCabinAmenities(FlylineBaseDataClass):
    food: Food
    beverage: Beverage
    entertainment: Entertainment
    wifi: Wifi
    power: Power


@dataclass(frozen=True)
class FareSegmentCabinAttributes(FlylineBaseDataClass):
    seat_attributes: SeatType
    seat_layout: SeatLayout


@dataclass(frozen=True)
class FareSegment(FlylineBaseDataClass):
    segment_id: str
    cabin_amenities: FareSegmentCabinAmenities
    cabin_attributes: FareSegmentCabinAttributes


@dataclass(frozen=True)
class Fare(FlylineBaseDataClass):
    cabin_class: str
    cabin_name: str
    fare_class: str
    fare_name: str
    fare_basis_code: str
    fare_type: str
    fare_rules: FareRules
    segments: List[FareSegment]
    passengers: List[str]


@dataclass(frozen=True)
class Offer(FlylineBaseDataClass):
    id: str
    base_amount: Decimal
    base_currency: str
    tax_amount: Decimal
    tax_currency: str
    total_amount: Decimal
    total_currency: str
    passengers: List[Passenger]
    owner: str
    slices: List[Slice]
    fares: List[Fare]
    expires_at: datetime
    ticket_time_limit: datetime
    max_connections: int


@dataclass(frozen=True)
class AirFare(FlylineBaseDataClass):
    live_mode: bool
    count: int
    airports: List[Airport]
    aircraft: List[Aircraft]
    carriers: List[Airline]
    offers: List[Offer]


# Air Attribute API Schema
@dataclass(frozen=True)
class TripAttributeSegment(FlylineBaseDataClass):
    origin: str
    destination: str
    aircraft: str
    flight_no: str
    cabin_amenities: FareSegmentCabinAmenities
    cabin_attributes: FareSegmentCabinAttributes


@dataclass(frozen=True)
class FareAttribute(FlylineBaseDataClass):
    baggage_rules: str
    cancellation_change_fees: str
    seat_selection: str
    boarding_zone: str
    points_mileage: str


@dataclass(frozen=True)
class AirlineWithFareAttribute(FlylineBaseDataClass):
    iata_code: str
    name: str
    fare_attributes: FareAttribute


@dataclass(frozen=True)
class AirAttribute(FlylineBaseDataClass):
    cabin_class: CabinClass
    carriers: List[AirlineWithFareAttribute]
    airports: List[Airport]
    aircraft: List[Aircraft]
    trip_attributes: List[List[TripAttributeSegment]]


# Schedule API Schemas
@dataclass(frozen=True)
class ScheduleDeparture(FlylineBaseDataClass):
    airport_code: str
    city: str
    country_code: str
    time_scheduled: datetime
    time_expected: Optional[datetime] = None
    time_actual: Optional[datetime] = None
    terminal: Optional[str] = None


@dataclass(frozen=True)
class ScheduleArrival(FlylineBaseDataClass):
    airport_code: str
    city: str
    country_code: str
    time_scheduled: datetime
    time_expected: Optional[datetime] = None
    time_actual: Optional[datetime] = None
    terminal: Optional[str] = None


@dataclass(frozen=True)
class Schedule(FlylineBaseDataClass):
    flight_status: str
    flight_no: str
    aircraft: str
    distance: int
    departure: ScheduleDeparture
    arrival: ScheduleArrival


# Seat Map API Schemas
@dataclass(frozen=True)
class Seat(FlylineBaseDataClass):
    designator: str
    description: str
    position_type: str


@dataclass(frozen=True)
class SeatMapByClass(FlylineBaseDataClass):
    seat_count: int
    cabin_class: str
    data: List[Seat]


@dataclass(frozen=True)
class SeatMap(FlylineBaseDataClass):
    display_text: str
    airline_code: str
    airline_name: str
    aircraft_code: str
    # seat_map: str
    # seat_map_key: str
    overview: str
    seats: List[SeatMapByClass]
    traveler_photos: Optional[List[str]] = None


@dataclass(frozen=True)
class CabinClassMapping(FlylineBaseDataClass):
    carrier: str
    cabin_class: str
    cabin_class_code: str
    fare_class_codes: List[str]
