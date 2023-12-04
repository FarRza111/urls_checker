# .....

import csv
import os
import requests
from http import HTTPStatus
from fake_useragent import UserAgent

class Web:

    def __init__(self, csv_path):
        self.csv_path = csv_path


    def get_websites(self):

        websites: list[str] = []
        with open(self.csv_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if 'https://' not in row[1]:
                    websites.append(f'https://{row[1]}')
                else:
                    websites.append(row[1])

        return websites



cs = Web(os.path.join(os.getcwd(), 'websites.csv'))
print(cs.get_websites())

# print(get_websites(os.path.join(os.getcwd(), 'websites.csv')))
