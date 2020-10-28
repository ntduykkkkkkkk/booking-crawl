from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import BrowserManagementKeywords
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from SeleniumLibrary.keywords import WaitingKeywords
import json
import requests
from robot.libraries.BuiltIn import BuiltIn
import os, platform

__version__ = '1.0.0'


class BrowserKeywords(LibraryComponent):

    WINDOWS_FIREFOX_DRIVER_PATH = r'\Drivers\geckodriver.exe'
    WINDOWS_CHROME_DRIVER_PATH = r'\Drivers\chromedriver.exe'
    WINDOWS_EDGE_DRIVER_PATH = r'\Drivers\MicrosoftWebDriver.exe'
    LINUX_FIREFOX_DRIVER_PATH = r'\Drivers\geckodriver'
    LINUX_CHROME_DRIVER_PATH = r'\Drivers\chromedriver'
    FIREFOX_DOWNLOAD_LOCATION = r'\Results\Exported\Firefox_exported'
    CHROME_DOWNLOAD_LOCATION = r'\Results\Exported\Chrome_exported'
    EDGE_DOWNLOAD_LOCATION = r'\Results\Exported\Edge_exported'
    EDGE_REG_DOWNLOAD_PATH = r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Storage\microsoft.microsoftedge_8wekyb3d8bbwe\MicrosoftEdge\Main"
    EDGE_REG_DOWNLOAD_POPUP_PATH = r"Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Storage\microsoft.microsoftedge_8wekyb3d8bbwe\MicrosoftEdge\Download"
    EDGE_REG_DOWNLOAD_KEY = r"Default Download Directory"
    EDGE_REG_DOWNLOAD_POPUP_KEY = "EnableSavePrompt"
    EDGE_TURN_OFF_DOWNLOAD_POPUP = "0"

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.waiting_management = WaitingKeywords(ctx)
        self.browser_management = BrowserManagementKeywords(ctx)

    @keyword
    def get_current_os(self):
        return platform.system()

    @keyword
    def format_os_path(self, path):
        # /: Linux
        # \: Windows
        return path.replace('\\', '/') if os.sep == '/' else path.replace('/', '\\')

    @keyword
    def get_current_path_of_project(self):
        current_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.dirname(os.path.dirname(os.path.join("..", current_path)))

    @keyword
    def enable_download_in_headless_chrome(self, driver, download_dir):
        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)

    @keyword
    def open_my_browser(self, setup):
        curr_path = self.get_current_path_of_project()
        if setup.get('setup').get('browser').lower() == 'firefox':
            options = FirefoxOptions()
            if setup.get('setup').get('headless').lower() == 'true':
                options.headless = True
            else:
                options.headless = False
            options.set_preference('pdfjs.previousHandler.alwaysAskBeforeHandling', False)
            options.set_preference('browser.download.folderList', 2)
            options.set_preference('browser.download.dir', curr_path + self.format_os_path(self.FIREFOX_DOWNLOAD_LOCATION))
            options.set_preference('browser.download.panel.shown', False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv," + "text/csv," +
                                   "application/x-msexcel,application/excel," +
                                   "application/vnd.openxmlformats-officedocument.wordprocessingml.document," +
                                   "application/x-excel,application/vnd.ms-excel" +
                                   "application / xml")
            if self.get_current_os().lower() == 'windows':
                driver = webdriver.Firefox(capabilities=None, options=options, executable_path=curr_path + self.format_os_path(self.WINDOWS_FIREFOX_DRIVER_PATH))
            else:
                driver = webdriver.Firefox(capabilities=None, options=options, executable_path=curr_path + self.format_os_path(self.LINUX_FIREFOX_DRIVER_PATH))
            driver.maximize_window()
        else:
            options = ChromeOptions()
            if setup.get('setup').get('headless').lower() == 'true':
                options.add_argument("headless")
            else:
                options.add_argument("--start-maximized")
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.default_directory": curr_path + self.format_os_path(self.CHROME_DOWNLOAD_LOCATION),
                     "directory_upgrade": True}
            options.add_experimental_option("prefs", prefs)
            if self.get_current_os().lower() == 'windows':
                driver = webdriver.Chrome(chrome_options=options,
                                          executable_path=curr_path + self.format_os_path(self.WINDOWS_CHROME_DRIVER_PATH))
            else:
                driver = webdriver.Chrome(chrome_options=options, executable_path=curr_path + self.format_os_path(self.LINUX_CHROME_DRIVER_PATH))
            if setup.get('setup').get('headless') == 'True':
                self.enable_download_in_headless_chrome(driver,
                                                        curr_path + self.format_os_path(self.CHROME_DOWNLOAD_LOCATION))
        driver.get(setup.get(BuiltIn().get_variable_value("${RESOURCE}")).get('url'))
        self.debug('Opened browser with session id %s.' % driver.session_id)
        return self.ctx.register_driver(driver, None)

    @keyword
    def setup_browser_driver(self, browser, path=''):
        """
        Create instance of selenium webdriver base on driver type
        :browser: browser type: chrome | firefox | ie
        :path: the path of executable driver
        """
        browser = browser.strip().lower()
        if browser == 'firefox':
            if path == '':
                path = self.get_project_path() + self.FIREFOX_DRIVER_PATH
            driver = Firefox(executable_path=self.format_executable_path(path))
        else:
            if path == '':
                path = self.get_project_path() + self.CHROME_DRIVER_PATH
            driver = Chrome(self.format_executable_path(path))
        driver.delete_all_cookies()
        return self.browser_management.ctx.register_driver(driver, None)

    def format_executable_path(self, path):
        if ".exe" in path:
            return path
        else:
            return path if os.sep == '/' else path + ".exe"

    def get_project_path(self):
        """
        Get the root directory of the project
        """
        return os.path.dirname(__file__).replace('\Libs\PCNLibrary\keywords','')

    def get_location(self):
        return self.browser_management.get_location()

    @keyword
    def wait_until_location_is(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
          lambda: self.get_location() == expected,
          "Location was not match '%s' in <TIMEOUT>. Actual value was '%s'" % (expected, self.get_location()),
          timeout,
          error
        )

    @keyword
    def wait_until_location_is_not(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: self.get_location() != expected,
            "Location did not change to value different to '%s' in <TIMEOUT>" % (expected, self.get_location()),
            timeout,
            error
        )

    @keyword
    def wait_until_location_contains(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected in self.get_location(),
            "Location '%s' did not contain '%s' in <TIMEOUT>" % (self.get_location(), expected),
            timeout,
            error
        )

    @keyword
    def location_should_not_be(self, expected):
        actual = self.get_location()
        if expected == actual:
            message = "Location should not be '%s' but it was NOT" % expected
            raise AssertionError(message)

    @keyword
    def element_css_property_value_should_be(self, locator, property_name, expected, message=''):
        element = self.find_element(locator)
        actual = element.value_of_css_property(property_name)
        if expected != actual:
            if not message:
                message = "The css value '%s' of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (property_name, locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def element_color_css_property_value_should_be(self, locator, property_name, expected, message=''):
        if self._is_rgb_color(expected):
            expected = self._convert_rgb_to_hex(expected)
        element = self.find_element(locator)
        actual = element.value_of_css_property(property_name)
        if self._is_rgb_color(actual):
            actual = self._convert_rgb_to_hex(actual)
        if expected != actual:
            if not message:
                message = "The color related css value '%s' of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (property_name, locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def wait_until_element_css_property_value_is(self, locator, property_name, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected == self.find_element(locator).value_of_css_property(property_name),
            "The css value '%s' of element '%s' did not match '%s' in <TIMEOUT>. Actual value is '%s'"
            % (property_name, locator, expected, self.find_element(locator).value_of_css_property(property_name)),
            timeout,
            error
        )

    @keyword
    def wait_until_element_css_property_value_is_not(self, locator, property_name, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected == self.find_element(locator).value_of_css_property(property_name),
            "The css value '%s' of element '%s' did not different to '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )