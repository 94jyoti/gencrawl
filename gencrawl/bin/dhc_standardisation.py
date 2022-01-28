# python dhc_standardisation.py hca_output.jl hca_dir


import json
import csv
import sys
import os
from collections import defaultdict

input_file = sys.argv[1]
output_dir = sys.argv[2]
field_mapping = [("_profile_id", "Profile_id"), ("client_id", "DHC_ID"), ("website_id", "Domain_ID_(Forage_Internal)"),
				 ("website", "Domain_Name"), ("npi", "NPI"), ("raw_full_name", "Full_Name"), ("first_name", "First_Name"),
				 ("middle_name", "Middle_Name"), ("last_name", "Last_Name"), ("suffix", "Suffix"), ("designation", "Designation"),
				 ("speciality", "Specialty"), ("affiliation", "Affiliation"), ("practice_name", "Practice_Name"),
				 ("address_line_1", "Address_Line_1"), ("address_line_2", "Address_Line_2"), ("address_line_3", "Address_Line_3"),
				 ("city", "City"), ("state", "State"), ("zip", "Zip"), ("phone", "Phone"), ("fax", "Fax"), ("email", "Email_ID"),
				 ("search_url", "Search_Page_URL"), ("doctor_url", "Doctor_Page_URL"), ("comment", "qa_comment")]

fieldnames = [f[1] for f in field_mapping]
keys = [f[0] for f in field_mapping]

data = defaultdict(list)
for line in open(input_file):
	line = json.loads(line)
	dhc_id = line['client_id']
	data[dhc_id].append(line)

for dhc_id, items in data.items():
	filename = os.path.join(output_dir, str(dhc_id) + ".csv")
	with open(filename, 'w') as w:
		csv_writer = csv.DictWriter(w, fieldnames=fieldnames)
		csv_writer.writeheader()
		for item in items:
			if item.get("designation") and "," in item['designation']:
				item['designation'] = item['designation'].replace(", ", ",").replace(",", ", ")

			for key in ['phone', 'fax']:
				if item.get(key):
					val = item[key]
					val = val.strip("(").replace(") ", "-")
					item[key] = val

			item['zip'] = (item.get("zip") or '').split("-")[0]
			pincode = item['zip']
			if pincode and len(pincode) == 4:
				item['zip'] = '0{}'.format(item['zip'])

			row = {fieldnames[index]: item.get(key) for index, key in enumerate(keys)}
			csv_writer.writerow(row)



