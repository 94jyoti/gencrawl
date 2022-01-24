import csv
import json
import sys
from collections import defaultdict

un = {}
i = 0
for line in open(sys.argv[1]):
    line = json.loads(line)
    website = line['website']
    parent_config = line['parent_config']
    i += 1
    un[website+"_"+parent_config] = line

unn = defaultdict(list)
for line in un.values():
    website = line['website']
    unn[website].append(line)


fieldnames = ['website',  'doctor_url', 'raw_full_name', 'first_name', 'middle_name', 'last_name', 'designation',
              'affiliation',  'speciality', 'practice_name', 'address_line_1', 'address_line_2',
              'address_line_3', 'city', 'state', 'zip', 'phone', 'fax', 'address', 'parent_config']
with open(sys.argv[1].split(".")[0] + ".csv", "w") as w:
    csvwriter = csv.DictWriter(w, fieldnames=fieldnames)
    csvwriter.writeheader()
    for configs in unn.values():
        for config in configs:
            config = {k: v for k, v in config.items() if k in fieldnames}
            csvwriter.writerow(config)

        separator = {k: '' for k in fieldnames}
        csvwriter.writerow(separator)

