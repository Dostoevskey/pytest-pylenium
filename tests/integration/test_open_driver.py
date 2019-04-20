from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By

from conditions.condition import Text
from core.locators import Tag
from core.pylenium import start, find, terminate


@pytest.mark.IT
class TestOpen(object):

    # Page Objects and business logic sold separately!
    @pytest.mark.skip
    def test_my_login(self):
        start('https://www.google.co.uk')
        find(By.NAME, 'q').set_value("Cheese!")
        find(By.CSS_SELECTOR, '#submit').click()
        find(By.CSS_SELECTOR, '#password').should_have(Text("Hello, Simon!"))
        terminate()

    @pytest.mark.travis
    def test_travis(self):
        google = 'https://www.google.co.uk/'
        actual = start(google).url()
        tag_is = find(Tag('h1')).tag_name()
        assert actual == google
