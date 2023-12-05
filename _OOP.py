import abc
import csv
import os
import requests
from fake_useragent import UserAgent
from http import HTTPStatus
import abc


class StatusDescriptionStrategy(abc.ABC):
    @abc.abstractmethod
    def get_status_description(self, status_code) -> str:
        pass


class DefaultStatusDescriptionStrategy(StatusDescriptionStrategy):
    def get_status_description(self, status_code) -> str:
        for value in HTTPStatus:
            if value == status_code:
                description: str = f'({value} {value.name}) {value.description}'
                return description

        return 'Status code is not known !!!!'


class WebsiteChecker:
    def __init__(self, website, user_agent, status_description_strategy):
        self.website = website
        self.user_agent = user_agent
        self.status_description_strategy = status_description_strategy

    def check_website(self):
        try:
            code: int = requests.get(self.website, headers={'User-Agent': self.user_agent}).status_code
            print(self.website, self.status_description_strategy.get_status_description(code))
        except Exception:
            print(f'Cannot get information from website: "{self.website}"')


class Web:
    def __init__(self, csv_path, status_description_strategy=None):
        self.csv_path = csv_path
        self.websites = self.get_websites()
        self.user_agent = self.get_user_agent()
        self.status_description_strategy = status_description_strategy or DefaultStatusDescriptionStrategy()

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

    def get_user_agent(self) -> str:
        """Returns a user agent that can be used with requests"""
        ua = UserAgent()
        return ua.chrome

    def create_website_checkers(self):
        return [WebsiteChecker(website, self.user_agent, self.status_description_strategy) for website in self.websites]

    def main(self):
        website_checkers = self.create_website_checkers()
        for checker in website_checkers:
            checker.check_website()


if __name__ == "__main__":
    web_instance = Web(os.path.join(os.getcwd(), 'websites.csv'))
    web_instance.main()
