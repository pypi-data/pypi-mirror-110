from . import (
    AirAttributeAPI,
    AirFareAPI,
    AirResourcesAPI,
    AirScheduleAPI,
    AirSeatMapAPI,
    FlylineBaseClient,
)


class FlylineClient(AirFareAPI, AirSeatMapAPI, AirAttributeAPI, AirScheduleAPI, AirResourcesAPI, FlylineBaseClient):
    pass
