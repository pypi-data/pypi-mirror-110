from typing import List, Literal, TypedDict

CabinClass = Literal["first", "business", "premium_economy", "economy", "basic_ecnomoy"]


class AirFareRequestSlice(TypedDict):
    pass


class AirFareRequestPassenger(TypedDict):
    pass


class AirFareRequestMaxPrice(TypedDict):
    price: str
    currency: str


class AirFareRequestCorporateAccount(TypedDict):
    pass


class AirFareRequest(TypedDict):
    cabin_class: CabinClass
    slices: List[AirFareRequestSlice]
    passengers: List[AirFareRequestPassenger]
    max_price: AirFareRequestMaxPrice
    permitted_carriers: List[str]
    sort_by: str
    corporate_accounts: List[AirFareRequestCorporateAccount]
