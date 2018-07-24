#!/usr/bin/env python3

import json
from syncplay import version

f = open('bintray.json', 'r')
data = json.load(f)

data['version']['name'] = 'v' + version

g = open('bintray.json', 'w')
json.dump(data, g, indent=4)
