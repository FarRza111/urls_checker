import abc
import csv
import os
import requests
from fake_useragent import UserAgent


class WebsiteCheckerABC(abc.ABC):
    @abc.abstractmethod
    def get_status_description(self, status_code) -> str:
        pass

    @abc.abstractmethod
    def check_website(self):
        pass


class WebsiteChecker(WebsiteCheckerABC):
    def __init__(self, website, user_agent):
        self.website = website
        self.user_agent = user_agent

    def get_status_description(self, status_code) -> str:
        try:
            return requests.status_codes._codes[status_code][0]
        except KeyError:
            return f"Status code {status_code} is not known!"

    def check_website(self):
        try:
            code: int = requests.get(self.website, headers={'User-Agent': self.user_agent}).status_code
            print(self.website, self.get_status_description(code))
        except Exception:
            print(f'Cannot get information from website: "{self.website}"')


class Web:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.websites = self.get_websites()
        self.user_agent = self.get_user_agent()

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
        return [WebsiteChecker(website, self.user_agent) for website in self.websites]

    def main(self):
        website_checkers = self.create_website_checkers()
        for checker in website_checkers:
            checker.check_website()


if __name__ == "__main__":
    web_instance = Web(os.path.join(os.getcwd(), 'websites.csv'))
    web_instance.main()
