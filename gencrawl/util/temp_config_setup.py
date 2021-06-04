import requests
import csv
from io import BytesIO
import codecs
import json
import os

GOOGLE_LINK = "https://docs.google.com/spreadsheets/u/1/d/1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw/export?format=csv&id=1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw&gid=0"


class TempConfig:

    def download_csv_file(self, url):
        response = requests.get(url)
        print(response)
        buffer = BytesIO(response.content)
        decoder = codecs.getreader('utf-8')
        return list(csv.DictReader(decoder(buffer, errors='strict')))

    def get_config_map(self, rows):
        configs = []
        rows = [r for r in rows if r['Field_Names']]
        rows = [rows[i: i+5] for i in range(0, len(rows), 5)]
        for row in rows:
            if row[0].pop("create_fresh_configs") != "1":
                print(f"Skipping configs for {row[0]['website']}")
                continue

            config = dict()
            for r in row:
                c = r.pop("Field_Names")
                config[c] = r
            configs.append(config)
        return configs

    def create_configs(self, configs):
        parsed_config_list = {}
        parsed_config = dict()
        for config in configs:
            xpaths = config.get("xpaths")
            cleanups = config.get("cleanups")
            return_types = config.get("return_type")
            selectors = config.get("selector")
            comments = config.get("comments")

            parsed_config['website'] = xpaths.pop("website")
            parsed_config['spider'] = "financial_detail"
            parsed_config['domain'] = "financial"
            parsed_config['crawl_method'] = "SCRAPY_GET"
            parsed_config['allowed_domains'] = [parsed_config['website'].replace("https://", "").replace("http://", "")]
            parsed_config['parsing_type'] = "xpath"
            parsed_config['country'] = "US"
            parsed_config['language'] = "ENGLISH"
            detail = dict()
            parsed_config["detail"] = detail
            detail["crawl_method"] = xpaths.pop("crawl_method")
            detail["parsing_type"] = "xpath"
            detail['start_urls'] = xpaths.pop("fund_url").replace("\r\n", "\n").split("\n")
            ext_codes = dict()
            detail["ext_codes"] = ext_codes
            for field in xpaths:
                ext_code = dict()
                if xpaths.get(field):
                    ext_codes[field] = ext_code
                    ext_code["paths"] = xpaths[field].replace("\r\n", "\n").split("\n")
                if cleanups.get(field):
                    ext_code["cleanup_functions"] = cleanups[field].replace("\r\n", "\n").split("\n")

                rt = return_types.get(field)
                s = selectors.get(field)
                if field == 'benchmarks':
                    rt = "list"
                elif field.startswith("temp_"):
                    rt = 'selector'
                    ext_code['child_return_strategy'] = s or 'multiple_objects'

                ext_code['return_type'] = rt or "str"
                ext_code['selector'] = s or 'root'
                if comments.get(field):
                    ext_code['comment'] = comments.get(field)

            domain = parsed_config['allowed_domains'][0]
            file_name = domain.replace("www.", '').replace(".", "_").replace("-", "_") + ".json"
            parsed_config_list[file_name] = parsed_config
        return parsed_config_list

    def save_configs(self, configs, config_dir):
        for filename, jsn in configs.items():
            fp = os.path.join(config_dir, filename)
            print(fp)
            with open(fp, 'w') as w:
                w.write(json.dumps(jsn, indent=4))

    def main(self, config_dir):
        csv_rows = self.download_csv_file(GOOGLE_LINK)
        config_map = self.get_config_map(csv_rows)
        p_configs = self.create_configs(config_map)
        self.save_configs(p_configs, config_dir)
