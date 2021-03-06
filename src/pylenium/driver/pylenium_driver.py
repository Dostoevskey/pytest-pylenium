#  MIT License
#
#  Copyright (c) 2019 Simon Kerr
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
#  NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from pylenium.utilities.plugin_utility import get_instance_of_listener_from_path
from pylenium.elements.pylenium_wait import PyleniumWait
from pylenium.elements.pylenium_element import PyleniumElement


class PyleniumDriver:
    def __init__(self, config, browser):
        self.config = config
        self.browser = browser
        self.browser._web_element_cls = PyleniumElement
        self.wait = PyleniumWait(
            self.config.explicit_wait, self.config.polling_interval
        )

    @property
    def browser(self):
        return self._browser

    @browser.setter
    def browser(self, value):
        path = self.config.driver_listener
        self._browser = (
            value
            if not path
            else EventFiringWebDriver(value, get_instance_of_listener_from_path(path))
        )

    # Navigational capabilities
    def get(self, url):
        self.browser.get(url)
        return self

    def quit(self):
        self.browser.close()

    @property
    def title(self):
        return self.browser.title

    def xpath(self, expression: str) -> PyleniumElement:
        return self.browser.find_element_by_xpath(expression)
