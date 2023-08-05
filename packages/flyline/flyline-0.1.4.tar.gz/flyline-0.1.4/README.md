# flyline_python
Flyline Python Library

## Install
```python
pip install flyline
```

## Getting Started

```python
import asyncio
from flyline import FlylineClient

async def main():
    key = 'test_***'
    async with FlylineClient(key=key) as client:
        data = {
            "cabin_class": "economy",
            "slices": [
                {
                    "departure": {"code": "DFW", "date": "2021-06-12"},
                    "arrival": {"code": "LAX"}
                }
            ],
            "passengers": [{"age": 27}],
        }
        seat_map = await client.get_airfares(data=data)
        print(seat_map)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Endpoints
### AirFare API
```python
    client.get_airfares()
```

### AirAttribute API
```python
    client.get_airattributes_by_flight_number()
    client.get_airattributes_by_route()
```

### AirSchedule API
```python
    client.get_schedules_by_flight_number()
    client.get_schedules_by_route()

```

### AirSeatMap API
```python
    client.get_seat_map()
```

### AirResources API
```python
    client.get_aircrafts()
    client.get_aircraft()
    client.get_airlines()
    client.get_airline()
    client.get_airports()
    client.get_airport()
    client.get_airports_by_city()
    client.get_cities()
    client.get_city()
    client.get_cabin_class_mapping()
    client.get_seat_types()
    client.get_seat_layouts()
    client.get_foods()
    client.get_beverages()
    client.get_entertainments()
    client.get_wifis()
    client.get_powers()
```
