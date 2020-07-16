from dataclasses import dataclass
from typing import List

import requests
from requests.auth import HTTPBasicAuth


@dataclass
class Application:
    key: str
    bugs: int = 0
    new_bugs: int = 0
    vulnerabilities: int = 0
    new_vulnerabilities: int = 0
    sqale_index: int = 0
    new_technical_debt: int = 0
    code_smells: int = 0
    new_code_smells: int = 0
    coverage: int = 0
    new_coverage: int = 0
    new_lines_to_cover: int = 0
    duplicated_lines_density: int = 0
    new_duplicated_lines_density: int = 0
    new_lines: int = 0

    def add_bugs(self, value):
        self.bugs = value

    def add_new_bugs(self, value):
        self.new_bugs = value

    def add_vulnerabilities(self, value):
        self.vulnerabilities = value

    def add_new_vulnerabilities(self, value):
        self.new_vulnerabilities = value

    def add_sqale_index(self, value):
        self.sqale_index = value

    def add_new_technical_debt(self, value):
        self.new_technical_debt = value

    def add_code_smells(self, value):
        self.code_smells = value

    def add_new_code_smells(self, value):
        self.new_code_smells = value

    def add_coverage(self, value):
        self.coverage = value

    def add_new_coverage(self, value):
        self.new_coverage = value

    def add_new_lines_to_cover(self, value):
        self.new_lines_to_cover = value

    def add_duplicated_lines_density(self, value):
        self.duplicated_lines_density = value

    def add_new_duplicated_lines_density(self, value):
        self.new_duplicated_lines_density = value

    def add_new_lines(self, value):
        self.new_lines = value

@dataclass
class Portfolio:
    name: str
    url: str
    applications: List[Application]

class SonarQubeClient:

    METRICS_MAPPING = {
        'bugs': Application.add_bugs,
        'new_bugs': Application.add_new_bugs,
        'vulnerabilities': Application.add_vulnerabilities,
        'new_vulnerabilities': Application.add_new_vulnerabilities,
        'sqale_index': Application.add_sqale_index,
        'new_technical_debt': Application.add_new_technical_debt,
        'code_smells': Application.add_code_smells,
        'new_code_smells': Application.add_new_code_smells,
        'coverage': Application.add_coverage,
        'new_coverage': Application.add_new_coverage,
        'new_lines_to_cover': Application.add_new_lines_to_cover,
        'duplicated_lines_density': Application.add_duplicated_lines_density,
        'new_duplicated_lines_density': Application.add_new_duplicated_lines_density,
        'new_lines': Application.add_new_lines
    }

    def __init__(self, token, url):
        self.SONARQUBE_TOKEN = token
        self.SONARQUBE_URL_COMPONENT = url

    def fetch(self, portfolio):
        for application in portfolio.applications:
            querystring = {
            "component": application.key,
            "qualifiers": "APP",
            "metricKeys": 'bugs,new_bugs,vulnerabilities,new_vulnerabilities,sqale_index,new_technical_debt,code_smells,new_code_smells,coverage,new_coverage,new_lines_to_cover,duplicated_lines_density,new_duplicated_lines_density,new_lines',
            "ps": 500
            }

            response = requests.request('GET',
                self.SONARQUBE_URL_COMPONENT,
                auth=HTTPBasicAuth(self.SONARQUBE_TOKEN, ''),
                params=querystring)

            if response.status_code != 200:
                break
            
            for measure in response.json()['baseComponent']['measures']:
                try:
                    key = measure['metric']
                    value =  measure['value'] if 'value' in measure else measure['periods'][0]['value']
                    self.METRICS_MAPPING[key](application, value)
                except KeyError as e:
                    print(f"Error {e}: {measure}")
