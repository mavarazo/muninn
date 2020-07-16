from dataclasses import dataclass

import requests


@dataclass
class Job:
    name: str
    url: str
    healthy: bool
    status: bool


class JenkinsClient:

    API_PREFIX = '/api/json?pretty=true'

    def __init__(self, username, token):
        self.JENKINS_USERNAME = username
        self.JENKINS_TOKEN = token

    def fetch(self, job):
        api = job.url + self.API_PREFIX
        self.response, httperror = self.__urlopen(api)

    def get_health(self):
        if self.response is None:
            return None

        last_build_number = self.__get_build_number_or_zero(self.response['lastBuild'])
        last_successful_build_number = self.__get_build_number_or_zero(self.response['lastSuccessfulBuild'])
        last_failed_build_number = self.__get_build_number_or_zero(self.response['lastFailedBuild'])

        return last_successful_build_number > last_failed_build_number and last_build_number != last_failed_build_number


    def get_status(self):
        if self.response is None:
            return None

        last_build_number = self.__get_build_number_or_zero(self.response['lastBuild'])
        last_failed_build_number = self.__get_build_number_or_zero(self.response['lastFailedBuild'])

        return last_build_number != last_failed_build_number


    def __urlopen(self, url):
        try:
            response = requests.get(url, auth=(self.JENKINS_USERNAME, self.JENKINS_TOKEN))
            if response.status_code == 401:
                return None, 'Jenkins 401 Unauthorized'

            if response.status_code != 200:
                return None, 'Jenkins not available'
            
            return response.json(), None
        except (requests.ConnectionError, requests.HTTPError) as err:
            return None, 'Jenkins not available'


    def __get_build_number_or_zero(self, last_build):
        number = 0
        if last_build and 'number' in last_build:
            number = last_build['number']
        return number
