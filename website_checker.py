import csv
import requests
from http import HTTPStatus
from fake_useragent import UserAgent


def get_websites(csv_path: str) -> list[str]:

    websites: list[str] = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if 'https://' not in row[1]:
                websites.append(f'https://{row[1]}')
            else:
                websites.append(row[1])

    return websites


def get_user_agent() -> str:
    """Returns a user agent that can be used with requests"""

    ua = UserAgent()
    return ua.chrome

def get_status_description(status_code: int) -> str:

    for value in HTTPStatus:
        if value == status_code:
            description: str = f'({value} {value.name}) {value.description}'
            return description

    return 'Status code is not known !!!!'


def check_website(website: str, user_agent: str):

    try:
        code: int = requests.get(website, headers={'User-Agent': user_agent}).status_code
        print(website, get_status_description(code))
    except Exception:
        print(f'cant get information from website: "{website}"')


def main():
    sites: list[str] = get_websites('websites.csv')
    user_agent: str = get_user_agent()
    for i, site in enumerate(sites):
        check_website(site, user_agent)


if __name__ == '__main__':
    main()
