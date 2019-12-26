# -*- coding: utf-8 -*-


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
import os

from __project_root__ import ROOT_DIR


def test_default(testdir):
    testdir.makepyfile(
        """
        def test_default(driver_listener):
            assert not driver_listener
    """
    )
    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(
        ["*::test_default PASSED*",]
    )
    assert result.ret == 0


def test_eventfiring_driver(testdir):
    testdir.makepyfile(
        """
        def test_default(driver):
            from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
            assert type(driver.browser) == EventFiringWebDriver
    """
    )
    listener_module = os.path.join(ROOT_DIR, "testing", "test_files", "event_listener.py")
    result = testdir.runpytest(f"--driver-listener={listener_module}", "-v")
    result.stdout.fnmatch_lines(
        ["*::test_default PASSED*",]
    )
    assert result.ret == 0


def test_override(testdir):
    testdir.makepyfile(
        """
        def test_override(driver_listener):
            assert driver_listener == 'src/example/listenermodule.py'
    """
    )
    result = testdir.runpytest("--driver-listener=src/example/listenermodule.py", "-v")
    result.stdout.fnmatch_lines(
        ["*::test_override PASSED*",]
    )
    assert result.ret == 0


def fix_this(testdir):
    testdir.makepyfile(
        """
        def test_file_not_found_override(driver):
            from pylenium.exceptions.exceptions import PyleniumEventFiringWrapperException
            with pytest.raises(PyleniumEventFiringWrapperException):
                pass
    """
    )
    result = testdir.runpytest(f"--driver-listener=/made/up/path", "-v")
    result.stdout.fnmatch_lines(
        ["*::test_file_not_found_override FAILED*",]
    )
    assert result.ret == 4
