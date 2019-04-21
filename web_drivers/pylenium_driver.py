from __future__ import annotations

import logging
import threading

from selenium.webdriver.common.by import By

from configuration.config import PyleniumConfig
from core.locators import PyLocator
from exceptions.exceptions import PyPageException
from pages.page_object import PyPage
from utility.meta import Singleton
from web_drivers.driver_strategy import ChromeBrowserStrategy, FirefoxBrowserStrategy

log = logging.getLogger("pylenium")
config = PyleniumConfig()

threaded = threading.local()


class PyleniumDriver:
    def __init__(self):
        self._driver = None
        self._driver = threaded.driver if hasattr(threaded, 'driver') else self._get_browser_strategy().instantiate()
        threaded.driver = self._driver

    @property
    def driver(self):
        return self._driver

    def goto(self, entry_point):
        url = (
            PyleniumConfig().base_url + entry_point
            if isinstance(entry_point, str)
            else entry_point.url
        )
        if not url:
            raise PyPageException(
                "The url was empty, did your page object specify the self.url parameter?"
            )
        else:
            self.driver.get(url)
            if isinstance(entry_point, PyPage):
                return entry_point
        return self

    def maximize(self) -> PyleniumDriver:
        self.driver.maximize_window()
        return self

    def quit(self):
        log.info("Quit called, terminating the browser")
        self.driver.quit()
        del threaded.driver

    def url(self) -> str:
        return self.driver.current_url

    def execute_javascript(self, script: str, *args):
        log.info('Executing javascript command')
        return self.driver.execute_script(script, args)

    @staticmethod
    def find(locator: PyLocator):
        from core.pylenium import PyElementWrapper
        return PyElementWrapper(locator)

    def X(self, identifier: str):
        return self.find(PyLocator(By.XPATH, identifier))

    def ID(self, identifier: str):
        return self.find(PyLocator(By.ID, identifier))

    def CSS(self, identifier: str):
        return self.find(PyLocator(By.CSS_SELECTOR, identifier))

    def PLT(self, identifier: str):
        return self.find(PyLocator(By.PARTIAL_LINK_TEXT, identifier))

    def LT(self, identifier: str):
        return self.find(PyLocator(By.LINK_TEXT, identifier))

    def NAME(self, identifier: str):
        return self.find(PyLocator(By.NAME, identifier))

    def TAG_NAME(self, identifier: str):
        return self.find(PyLocator(By.TAG_NAME, identifier))

    def CLASS(self, identifier: str):
        return self.find(PyLocator(By.CLASS_NAME, identifier))

    @staticmethod
    def _get_browser_strategy():
        if config.browser.value == "chrome":
            log.info("Creating a chrome browser instance")
            return ChromeBrowserStrategy()
        elif config.browser.value == "firefox":
            return FirefoxBrowserStrategy()