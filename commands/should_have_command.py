from __future__ import annotations
import typing
from typing import Union

from commands.command import Command
from conditions.condition import PyCondition

if typing.TYPE_CHECKING:
    from core.pylenium import PyElement, PyleniumDriver


class ShouldHaveCommand(Command):
    def __init__(self, driver: PyleniumDriver, element: PyElement,
                 conditions: typing.Union[typing.List[PyCondition], PyCondition]):
        super().__init__(driver, element)
        self.conditions = conditions

    def execute(self) -> Union[str, PyElement, bool, int]:
        self.wait_for_element()
        self.wait_for_page_to_be_ready()
        if type(self.conditions) is not list:
            self.conditions.evaluate(self.element)
        else:
            for condition in self.conditions:
                condition.evaluate(self.element)
        return self.element
