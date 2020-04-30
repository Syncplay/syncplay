#!/usr/bin/env python3

import json
from syncplay import version

bintrayFileName = 'bintray.json'

f = open(bintrayFileName, 'r')
data = json.load(f)

data['version']['name'] = 'v' + version

g = open(bintrayFileName, 'w')
json.dump(data, g, indent=4)
