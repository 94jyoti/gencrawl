import json
import pandas as pd
import sys
def convert_to_json(file_path):
    """
    :param file_path: csv file in std nfn format
    :return: convert the standard csv file format to nfn specific json format
    """
    file_name = file_path.replace('csv', 'json')
    final_data = dict()
    df = pd.read_csv(file_path)
    df.fillna('NULL', inplace=True)

    # add keys with blank rows
    for col in df.columns:
        final_data[col] = []
    domains = df.Domain.unique()

    for i in range(len(domains)):
        domain = domains[i]
        domain_data = df[df['Domain'] == domain]
        # get the list of unique fund names
        fund_names = domain_data['Fund Name/Ticker'].unique()
        for j in range(len(fund_names)):
            fund_name = fund_names[j]
            fund_data = df[domain_data['Fund Name/Ticker'] == fund_name]
            class_names = fund_data['Class Name'].unique()
            for k in range(len(class_names)):
                class_name = class_names[k]
                if str(class_name) != 'NULL':
                    class_data = df[(domain_data['Class Name'] == class_name) & (domain_data['Fund Name/Ticker'] == fund_name)]
                else:
                    class_data = fund_data.copy()
                for key in class_data.keys():
                    if key in ['Domain', 'Page URL', 'Fund Name/Ticker']:
                        value = ''.join(class_data[key].unique())
                        final_data[key].append(value)
                    else:
                        key_data = list(class_data[key])
                        # print(key_data)
                        if '.'.join(map(str, set(key_data))) != 'NULL':
                            final_data[key].append(key_data)
                        else:
                            final_data[key].append(None)

    with open(file_name, "w") as outfile:
        json.dump(final_data, outfile)
if __name__ == '__main__':
    filepath = sys.argv[1]
    convert_to_json(filepath)