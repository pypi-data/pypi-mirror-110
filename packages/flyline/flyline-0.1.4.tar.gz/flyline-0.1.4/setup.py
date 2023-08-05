# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flyline']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'flyline',
    'version': '0.1.4',
    'description': 'Flyline Client Libraray',
    'long_description': '# flyline_python\nFlyline Python Library\n\n## Install\n```python\npip install flyline\n```\n\n## Getting Started\n\n```python\nimport asyncio\nfrom flyline import FlylineClient\n\nasync def main():\n    key = \'test_***\'\n    async with FlylineClient(key=key) as client:\n        data = {\n            "cabin_class": "economy",\n            "slices": [\n                {\n                    "departure": {"code": "DFW", "date": "2021-06-12"},\n                    "arrival": {"code": "LAX"}\n                }\n            ],\n            "passengers": [{"age": 27}],\n        }\n        seat_map = await client.get_airfares(data=data)\n        print(seat_map)\n\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\n## Endpoints\n### AirFare API\n```python\n    client.get_airfares()\n```\n\n### AirAttribute API\n```python\n    client.get_airattributes_by_flight_number()\n    client.get_airattributes_by_route()\n```\n\n### AirSchedule API\n```python\n    client.get_schedules_by_flight_number()\n    client.get_schedules_by_route()\n\n```\n\n### AirSeatMap API\n```python\n    client.get_seat_map()\n```\n\n### AirResources API\n```python\n    client.get_aircrafts()\n    client.get_aircraft()\n    client.get_airlines()\n    client.get_airline()\n    client.get_airports()\n    client.get_airport()\n    client.get_airports_by_city()\n    client.get_cities()\n    client.get_city()\n    client.get_cabin_class_mapping()\n    client.get_seat_types()\n    client.get_seat_layouts()\n    client.get_foods()\n    client.get_beverages()\n    client.get_entertainments()\n    client.get_wifis()\n    client.get_powers()\n```\n',
    'author': 'Flyline Development Team',
    'author_email': 'development@flyline.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
