import os

from colorama import Fore, Style

from .frameworks.api import APIFramework
from .frameworks.selenium import SeleniumFramework


class FrameworkFactory:
    def __init__(self, project_name, project_path=None):
        self.stdout = print
        self.project_name = project_name
        self.project_path = project_path
        self.project_dir = os.path.join(self.project_path, self.project_name)
        self.frameworks = {
            "selenium": SeleniumFramework,
            "api": APIFramework,
        }

    def get_framework(self, framework):
        self.stdout(f"{Fore.BLUE}Creating {framework.upper()} project...{Style.RESET_ALL}")
        return self.frameworks[framework](self.project_dir)