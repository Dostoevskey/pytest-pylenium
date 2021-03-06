<kbd>
  <img src="https://github.com/symonk/pylenium/blob/master/.github/.images/pylenium_logo.png">
</kbd>
  <p></p>

[![Build Status](https://api.travis-ci.org/symonk/pytest-pylenium.svg?branch=master)](https://travis-ci.org/symonk/pytest-pylenium)
[![License Apache](https://img.shields.io/badge/license-Apache%202-brightgreen.svg)](https://github.com/symonk/pylenium/blob/master/LICENSE)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=symonk_pylenium&metric=bugs)](https://sonarcloud.io/dashboard?id=symonk_pylenium)
[![codecov](https://codecov.io/gh/symonk/pytest-pylenium/branch/master/graph/badge.svg)](https://codecov.io/gh/symonk/pytest-pylenium)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=symonk_pylenium&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=symonk_pylenium)
[![Find_Me LinkedIn](https://img.shields.io/badge/Find_Me-LinkedIn-brightgreen.svg)](https://www.linkedin.com/in/simonk09/)
[![Find_Me Slack](https://img.shields.io/badge/Find_Me-Slack-brightgreen.svg)](https://testersio.slack.com)

## What is pytest-pylenium? :flags: 
Pylenium is a frontend automated test framework for driving end to end tests of user interface(s).  Written in Python
and running with pytest it allows a quick time to market on your automated tests while erradicating flakyness through
smart waiting and various other mechanisms to make selenium more test-friendly.

Pylenium Goals:
 - Quickly write **stable** end 2 end web application frontend tests
 - Support xdist for parallel execution of tests
 - Support distributed selenium grid setups to increase parallelisation even more
 - Expose an intuitive interface so building bigger projects is easy, but also writing simple scripts is easy too!

#### Important Notes:
 - pytest-pylenium will **never** attempt to support python versions less than 3.7
 - pytest-pylenium will **never** attempt to support alternative test runners to pytest e.g (nose/unittest etc)
 
 ---
 
### Simple Example :hearts:
Human readable, concise and most importantly **stable!**

```python
    @pytest.mark.pylenium(case='testcase-101', issue_id='issue-949', description='Logging in is so easy!')
    def test_my_login():
      open('http://www.google.co.uk')
      find(name('user.name')).set_value('simon')
      find(name('password')).set_value('securepassword')
      find('#submit')).click()  # default selector
      find(id('username')).should_have(text('Hello, Simon!'))    
      
      # alternatively
       by_xpath("//*[@class='find']").child("span").should_be(hidden()) 

    # But I want page objects! - so easy: @see: below
    def test_with_pages(self):
        start(MyLoginPage) # no need to pass a driver through to page objects
```

---

### Page Objects :hearts:
Easy, hassle free, abstracted -> Exactly how page objects should be!

```python
    # pages are not necessary, but recommended! (@see: our page objectless example code!)
    # pyleniums own web element is very smart and handles waiting to increase stability
    @loadable(page='/login.php')
    class ExampleLoginPage:
        _text_field_on_login_page = ID("some_id_attribute_value")
    
        def retrieve_the_text(self) -> str:
            return self._text_field_on_login_page.text()
    
        def set_the_text(self, value: str) -> ExampleLoginPage:
            self._text_field_on_login_page.set_text(value)
            self._text_field_on_login_page.should_have(Text(value))
            return self             
```

---

### Pytest Fixtures :star:
Pylenium exposes a ton of helpful fixtures for your tests, these are outlined below including their scopes and autouse
declarations.


```python
import pylenium

def test_something_cool(driver):
    driver.open("https://www.google.com")
```
    
---

### Support for EventFiringWebDriver :star:
Pylenium supports an event firing webdriver for advanced logging and listener capabilities.  In order for pylenium to 
wrap the driver successfully you should implement the following two goals

    - Subclass seleniums AbstractEventListener and implement your desired behaviour
    - Provide a --driver-listener=path/to/your/py/file/containing/the/subclass
    - n.b your subclass MUST be called PyleniumEventListener due to limitations of the run_py module (very important)
    
An example of how to subclass and pass a py module to pylenium is outlined below:

```python
# module.py file living in /path/to/
class PyleniumEventListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        print("Navigating to!")
 
```        

```bash
pytest --driver-listener=path/to/module.py
```

---

### Pylenium Desired Capabilities :star:
Configuring browser capabilities is easy with pylenium, just pass us a --browser-capabilities-file=[FILE_PATH] at runtime
and we will do the rest, the file should be a .yaml format and adhere to the yaml spec, see below:

```yaml
Capabilities:
    'os': 'Windows'
    'os_version': 'Sierra'
    'browser': 'Chrome'
    'browser_version': '79.0'
    'browserstack.local': 'false'
    'browserstack.selenium_version': '3.14.0'
    'browserstack.chrome.driver': '2.43'

```
    
---

### Configuration :clipboard:
Pylenium aims to be configurable, but sensible when required to be implicit.  We consider our config a singleton tho,
when we instantiate the driver, it really shouldn't be modified! All options can be seen in the pylenium-pytest plugin
module.


```python
@dataclass
class PyleniumConfig:
    browser: SupportedBrowser = SupportedBrowser()
    headless: bool = False
    remote: bool = False
    server: str = LOCALHOST_URL
    server_port: int = 4444
    browser_size: str = '1366x768'
    browser_version: str = 'latest'
    browser_maximized: bool = True
    aquire_binary: bool = True
    browser_path: str = None
    page_load_strategy: PageLoadingStrategy = PageLoadingStrategy()
    browser_capabilities: BrowserCapabilities = None
    load_base_url: bool = False
    base_url: ValidUrl = LOCALHOST_URL
    explicit_wait: int = 15000
    polling_interval: int = 200
    screenshot_on_fail: bool = False
    page_source_on_fail: bool = False
    stack_trace_on_fail: bool = False
    click_with_js: bool = False
    sendkeys_with_js: bool = False
    default_selector: str = 'CSS'
```
---

### Page Actions :trophy:
Repeatable steps and chains of page object commands, all wrapped under one roof!

    - clean abstractions
    - repeatable and very test friendly
    
---

###  :star: Companies who back the project:

[![Intellij IDEA](https://cloud.google.com/tools/images/icon_IntelliJIDEA.png )](http://www.jetbrains.com/idea)
[![BrowserStack](https://www.browserstack.com/images/mail/browserstack-logo-footer.png)](https://www.browserstack.com)

---
