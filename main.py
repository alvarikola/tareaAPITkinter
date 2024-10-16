from collections import namedtuple
from json import JSONEncoder

import requests
import json
from types import SimpleNamespace
import dimensions
from dimensions import Dimensions


class ProductEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def customProductDecoder(producto):
    return namedtuple("X", producto.keys())(*producto.values())

URL = "https://dummyjson.com/products"
response = requests.get(URL)
producto = response.json()
productoJSON = json.dumps(producto, indent = 4, cls = ProductEncoder)
print('Solicitud exitosa')
print('Data:', response.json())


# data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

x = json.loads(response.json(), object_hook= customProductDecoder)
print(x.products[0].title)
# print(x.name, x.hometown.name, x.hometown.id)