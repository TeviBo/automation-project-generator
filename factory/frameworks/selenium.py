import os

from colorama import Fore, Style


class SeleniumFramework:
    def __init__(self, project_dir):
        self.stdout = print
        self.project_dir = project_dir
        self.directories = {
            "environments": {},
            "features": {
                "steps": {},
                "pages": {}
            },
            "logs": {},
            "reports": {},
            "screenshots": {},
            "tests": {},
            "utils": {
                "handlers": {}

            }
        }
        self.create_project()

    def create_directories(self):
        for directory_name, subdirs in self.directories.items():
            self.stdout(
                f'{Fore.BLUE}Creating {directory_name} directory...{Style.RESET_ALL}')
            full_path = os.path.join(self.project_dir, directory_name)
            os.makedirs(full_path, exist_ok=True)
            self.stdout(
                f'{Fore.GREEN}{directory_name} created...{Style.RESET_ALL}')
            if subdirs:
                self.create_subdirectories(subdirs, full_path)

    def create_subdirectories(self, subdirectories, parent_path=''):
        for subdirectory_name, subdirs in subdirectories.items():
            self.stdout(
                f'{Fore.BLUE}Creating {subdirectory_name} directory...{Style.RESET_ALL}')
            subdirectory_path = os.path.join(parent_path, subdirectory_name)
            os.makedirs(subdirectory_path, exist_ok=True)
            self.stdout(
                f'{Fore.GREEN}{subdirectory_name} created...{Style.RESET_ALL}')

    def create_files(self):
        files = {
            os.path.join(self.project_dir, "environments", "local.json"): "{}",
            os.path.join(self.project_dir, "environments", "dev.json"): "{}",
            os.path.join(self.project_dir, "environments", "stg.json"): "{}",
            os.path.join(self.project_dir, "features", "__init__.py"): "",
            os.path.join(self.project_dir, "features", "steps", "__init__.py"): "",
            os.path.join(self.project_dir, "features", "pages", "__init__.py"): "",
            os.path.join(self.project_dir, "features", "pages", "base.py"): {
                "content": [
                    "from selenium.webdriver.support import expected_conditions as ec",
                    "from selenium.webdriver.support.ui import WebDriverWait",
                    "",
                    "",
                    "class BasePage:",
                    "\tdef __init__(self, driver):",
                    "\t\tself.driver = driver",
                    "",
                    "\tdef open_page(self, page_url):",
                    "\t\tself.driver.get(page_url)",
                    "",
                    "\tdef clear_input(self, locator):",
                    "\t\tself.get_element_by_locator(locator).clear()",
                    "",
                    "\tdef get_element_by_locator(self, locator, timeout=10):",
                    "\t\twait = WebDriverWait(self.driver, timeout)",
                    "\t\treturn wait.until(ec.presence_of_element_located(locator))",
                    "",
                    "\tdef clear_input(self, locator):",
                    "\t\telement = self.get_element_by_locator(locator)",
                    "\t\telement.clear()",
                    "",
                    "\tdef take_screenshot(self, scenario_name, step_name):",
                    "\t\tif not os.path.exists('screenshots'):",
                    "\t\t\tos.makedirs('screenshots')",
                    "\t\ttimestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')",
                    "\t\tscreenshot_path = 'screenshots/{scenario_name}_{step_name}_{timestamp}.png'",
                    "\t\tself.driver.save_screenshot(screenshot_path)",
                    "\t\treturn screenshot_path",
                ]
            },
            os.path.join(self.project_dir, "features", "environment.py"): {
                "content": [
                    "import json",
                    "import os",
                    "import allure",
                    "from utils.browser import BrowserConfig",
                    "",
                    "ENV_DIR = os.path.join(os.path.dirname(__file__), '..', 'environments')",
                    "",
                    "",
                    "def before_all(context):",
                    "\tcontext.actual_environment = context.config.userdata.get('environment')",
                    "\twith open(os.path.join(ENV_DIR, f'{context.actual_environment}.json'), 'rb') as f:",
                    "\t\tcontext.values = json.load(f)",
                    "",
                    "def before_scenario(context, scenario):",
                    "\tbrowser_config = BrowserConfig(context.config.userdata.get('browser'))",
                    "\tcontext.driver = browser_config.get_driver()",
                    "",
                    "def after_step(context, step):",
                    "\treports_dir = os.path.join(os.path.dirname(__file__), '../..', 'reports')",
                    "\tstep_name = ''",
                    "\tif not os.path.exists(reports_dir):",
                    "\t\tos.makedirs(reports_dir)",
                    "\tif context.scenario.status != 'passed':",
                    "\t\tfor step in scenario.steps:",
                    "\t\t\tif step.status != 'passed':",
                    "\t\t\t\tstep_name = step.name",
                    "\t\t\t\tscreenshot_path = context.actual_page.take_screenshot(context.scenario.name,step_name)",
                    "\t\t\t\twith open(screenshot_path, 'rb') as f:",
                    "\t\t\t\t\tcontent = f.read()",
                    "\t\t\t\t\tallure.attach(content, attachment_type=allure.attachment_type.PNG)",
                ]
            },
            os.path.join(self.project_dir, 'features', 'Sample.feature'): {
                "content": [
                    "Feature: Sample feature",
                    "'''",
                    "\tAs a user",
                    "\tI want to test my project",
                    "\tSo that I can be sure that it works",
                    "'''",
                    "",
                    "\tScenario: Sample scenario",
                    "\t\tGiven I am on the sample page",
                    "\t\tWhen I do something",
                    "\t\tThen I should see something",
                    "\t\tAnd I should see something else",
                    "\t\tBut I should not see something",
                    "",
                    "\tScenario Outline: Sample outline scenari",
                    "\t\tGiven I am on the <animal> page",
                    "\t\tWhen I filter by <breed>",
                    "\t\tThen I should see the animal\'s breed",
                    "\tExamples:",
                    "\t\t| animal | breed |",
                    "\t\t| dog | poodle |",
                    "\t\t| cat | persian |",
                    "\t\t| bird | parrot |",
                ]
            },
            os.path.join(self.project_dir, "features", "pages", "__init__.py"): "",
            os.path.join(self.project_dir, "utils", "handlers", "response_handler.py"): {
                "content": [
                    "import json",
                    "import logging",
                    "import allure",
                    "from allure_commons.types import AttachmentType",
                    "",
                    "",
                    "class ResponseHandler:",
                    "\tdef __init__(self, response):",
                    "\t\tself.status_code = response.status_code",
                    "\t\tself.body = response.text",
                    "\t\tself.method = response.request.method",
                    "\t\tself.endpoint = response.url",
                    "\t\tself.request = response.request.body",
                    "\t\tself.headers = response.request.headers",
                    "\t\tself.text = response.text",
                    "",
                    "\tdef logger(self):",
                    "\t\tif self.status_code == 200:",
                    "\t\t\tself.body = json.loads(self.text)",
                    "\t\telif self.status_code != 200 and self.status_code < 500:",
                    "\t\t\tself.body = json.loads(self.text)",
                    "\t\t\tlogging.info(",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'////////////////////////////\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'|     [Request Data]       |\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\tf'[Endpoint]: {self.endpoint}\\n'",
                    "\t\t\t\tf'[Method]: {self.method}\\n'",
                    "\t\t\t\tf'[Headers]: {self.headers}\\n'",
                    "\t\t\t\tf'[Request Payload]: {self.request}\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'////////////////////////////\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'|     [Response Data]       |\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\tf'[Status Code]: {self.status_code}\\n'",
                    "\t\t\t\tf'[Response Body]: \\n{self.text}\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'///////////////////////////\\n'",
                    "\t\t\t\t'****************************\\n')",
                    "\t\t\tallure.attach(str(",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'////////////////////////////\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'|     [Request Data]       |\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\tf'[Endpoint]: {self.endpoint}\\n'",
                    "\t\t\t\tf'[Method]: {self.method}\\n'",
                    "\t\t\t\tf'[Headers]: {self.headers}\\n'",
                    "\t\t\t\tf'[Request Payload]: {self.request}\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'////////////////////////////\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'|     [Response Data]       |\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\tf'[Status Code]: {self.status_code}\\n'",
                    "\t\t\t\tf'[Response Body]: \\n{self.text}\\n'",
                    "\t\t\t\t'****************************\\n'",
                    "\t\t\t\t'///////////////////////////\\n'))",
                    "\t\telse:",
                    "\t\t\tlogging.info(f'self.response.text')",
                    "\t\t\tallure.attach(str(f'self.response.text'), name='Response', attachment_type=AttachmentType.TEXT)",
                ]
            },
            os.path.join(self.project_dir, 'utils', 'browser.py'): {
                "content": [
                    "from selenium import webdriver",
                    "from selenium.common.exceptions import SessionNotCreatedException",
                    "from selenium.webdriver import DesiredCapabilities",
                    "from selenium.webdriver.chrome.options import Options",
                    "",
                    "",
                    "class BrowserConfig:",
                    "\tdef __init__(self, browser_name):",
                    "\t\tself.browser_name = browser_name",
                    "",
                    "\tdef get_driver(self):",
                    "\t\toptions = Options()",
                    "\t\toptions.add_argument('--disable-notifications')",
                    "\t\toptions.add_argument('--user-data-dir=/tmp/user-data-dir')",
                    "\t\toptions.add_argument('--disable-extensions')",
                    "\t\toptions.add_argument('--disable-gpu')",
                    "\t\toptions.add_argument('--no-sandbox')",
                    "\t\toptions.add_argument('--disable-dev-shm-usage')",
                    "\t\toptions.add_argument('--disable-popup-blocking')",
                    "\t\toptions.add_argument('--start-maximized')",
                    "\t\toptions.add_argument('--headless')",
                    "\t\tdriver = None",
                    "\t\ttry:",
                    "\t\t\tdriver = getattr(webdriver, self.browser_name.capitalize())(options=options,)",
                    "\t\texcept (Exception, SessionNotCreatedException) as ex:",
                    "\t\t\traise Exception(ex.msg)",
                    "\t\tfinally:",
                    "\t\t\treturn driver",
                ]
            },
            os.path.join(self.project_dir, "requirements.txt"): {
                "content": [
                    "selenium",
                    "allure-behave",
                    "allure-python-commons",
                    "behave",
                    "Unipath",
                ]
            },
            os.path.join(self.project_dir, "requirements.dev.txt"): {
                "content": [
                    "flake8",
                ]
            },
            os.path.join(self.project_dir, ".flake8"): {
                "content": [
                    "[flake8]",
                    "max-line-length = 88",
                    "exclude=",
                    "\tmigrations,",
                    "\t__pycache__,",
                    "\tmanage.py,",
                    "\tsettings.py,",
                    "\t.git",
                    "ignore = E203, W503",
                    "select = C,E,F,W,B,B950",
                    "import-order-style = google",
                    "inline-quotes = single",
                    "multiline-quotes = double",
                    "docstring-convention = numpy",
                ]
            },
            os.path.join(self.project_dir, "README.md"): {
                "content": [
                    f"# {self.project_dir.capitalize()}",
                    "",
                    "Fill with project description",
                ]
            },
        }

        for file_path, file_content in files.items():
            if isinstance(file_content, str):
                self.stdout(
                    f"{Fore.BLUE}Creating {file_path} file...{Style.RESET_ALL}")
                dir_path = os.path.dirname(file_path)
                os.makedirs(dir_path, exist_ok=True)
                self.stdout(
                    f"{Fore.GREEN}{file_path} created...{Style.RESET_ALL}")

                with open(file_path, 'w') as f:
                    pass
            elif isinstance(file_content, dict):
                self.stdout(
                    f"{Fore.BLUE}Creating {file_path}...{Style.RESET_ALL}")
                dir_path = os.path.dirname(file_path)
                os.makedirs(dir_path, exist_ok=True)
                self.stdout(
                    f"{Fore.GREEN}{file_path} created...{Style.RESET_ALL}")

                with open(file_path, 'w') as f:
                    self.stdout(
                        f"{Fore.BLUE}Writting {file_path} file content...{Style.RESET_ALL}")
                    for line in file_content['content']:
                        f.write(line + '\n')
                    self.stdout(
                        f"{Fore.BLUE}{file_path} content wroted...{Style.RESET_ALL}")

    def create_project(self):
        self.stdout(f"{Fore.BLUE}Creating directories...{Style.RESET_ALL}")
        self.create_directories()
        self.stdout(
            f"{Fore.GREEN}All directories were created...{Style.RESET_ALL}"
        )

        self.stdout(f"{Fore.BLUE}Creating files...{Style.RESET_ALL}")
        self.create_files()
        self.stdout(f"{Fore.GREEN}All files were created...{Style.RESET_ALL}")
