import json
import sys
import os
# adding path to env variable
cdir = os.path.join(os.getcwd().split("gencrawl")[0], 'gencrawl')
sys.path.append(cdir)
from collections import OrderedDict
from gencrawl.util.statics import Statics
from gencrawl.util.utility import Utility

field_mapping_file = "nfn_field_mapping.csv"

if __name__ == "__main__":
    input_file = sys.argv[1]
    file_name, format = input_file.rsplit(".", 1)
    assert format in ["jl"]
    field_mapping_file = os.path.join(cdir, Statics.RES_DIR, field_mapping_file)
    field_mapping = []
    for row in Utility.read_csv(field_mapping_file):
        if row['value'].startswith('Temp '):
            break
        field_mapping.append(row['value'])

    for line in open(input_file):
        line = json.loads(line)
        for k in line:
            if k not in field_mapping:
                field_mapping.append(k)

    file_name = file_name + ".csv"
    data = []
    for line in open(input_file):
        line = json.loads(line)
        d = OrderedDict()
        for k in field_mapping:
            d[k] = line.get(k)
        data.append(d)

    Utility.write_csv(file_name, data, fieldnames=field_mapping)
    print("Output written to file - " + file_name)