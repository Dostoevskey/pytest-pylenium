from __future__ import annotations

import logging
import os
import time
import typing

from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement

import drivers.web_driver_runner as runner
from commands.click_command import ClickCommand
from commands.get_tag_command import GetTagCommand
from commands.get_text_command import GetTextCommand
from commands.should_have_command import ShouldHaveCommand
from conditions.condition import PyCondition
from configuration.config import PyleniumConfig
from core.locators import PyLocator
from drivers.driver import PyleniumDriver

log = logging.getLogger("pylenium")
log.setLevel(logging.INFO)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ascii:
with open(os.path.join(ROOT_DIR, "resources", "ascii.txt")) as art:
    for line in art:
        print(line)

# global configuration object
config = PyleniumConfig()


def start(entry_point):
    return get_pylenium_driver().start(entry_point)


def terminate() -> None:
    get_pylenium_driver().quit()


def get_pylenium_driver() -> PyleniumDriver:
    return runner.web_driver_container.get_pylenium_driver()


def find(locator: PyLocator) -> PyElement:
    return get_pylenium_driver().find(locator)


def ID(selector: str) -> PyElement:
    return get_pylenium_driver().find(PyLocator(By.ID, selector))


def X(selector: str) -> PyElement:
    return find(PyLocator(By.XPATH, selector))


# refreshes the underlying web element to prevent staleness etc
def anti_staleness(f):
    def wrapper(*args):
        log.info("refresh reference to the underlying webelement to prevent staleness")
        args[0].wrapped_element = get_pylenium_driver().driver.web_driver.find_element(
            args[0].locator.by, args[0].locator.selector
        )
        return f(*args)

    return wrapper


def ready_state(f):
    def wrapper(*args):
        start_ready_state = time.time()
        log.info("Waiting for page ready state")
        while time.time() < start_ready_state + config.explicit_wait_timeout:
            if get_pylenium_driver().execute_javascript("return document.readyState") == "complete":
                break
        else:
            log.error("page was not ready in time...")
        log.info("Waiting for jquery")
        start_jquery = time.time()
        while time.time() < start_jquery + config.explicit_wait_timeout:
            if not get_pylenium_driver().execute_javascript("return !!window.jQuery && window.jQuery.active == 0"):
                break
        else:
            log.error("Jquery was not finished in time")
        return f(*args)

    return wrapper


# apply a decorator to every 'callable' method in a class
def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr) and attr != '__init__'):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


class PyElement(WebElement):
    __soft_asserts = {
        "should",
        "should_be",
        "should_have",
        "should_not",
        "should_not_have",
        "should_not_be",
        "wait_until",
        "wait_while"
    }

    def __init__(self, locator, parent, id_):
        super().__init__(parent, id_)
        self.locator = locator
        self.wrapped_element: webelement = None

    @ready_state
    @anti_staleness
    def tag_name(self) -> str:
        return GetTagCommand(self).execute()

    @ready_state
    @anti_staleness
    def text(self) -> str:
        return GetTextCommand(self).execute()

    @ready_state
    @anti_staleness
    def should_have(self, conditions: typing.Union[PyCondition, typing.List[PyCondition]]) -> PyElement:
        return ShouldHaveCommand(self, conditions).execute()

    @ready_state
    @anti_staleness
    def click(self):
        return ClickCommand(self).execute()
