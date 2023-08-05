# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selenium_testing_library']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.0.0,<4.0.0', 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'selenium-testing-library',
    'version': '2021.6.19b1',
    'description': 'A Python Selenium library inspired by the Testing Library',
    'long_description': '# Selenium Testing Library\n\nSlenium Testing Library (STL) is a Python library for Selenium inspired by [Testing-Library](https://testing-library.com/).\n\n## Finding elements\n\n`get_by` returns the element matched and throws an exception if zero or more than one elements matched.\n`query_by` returns the element matched or `None` if no element matched. It throws and exception if more than 1 elements matched.\n`find_by` behaves like `get_by`, but uses a `WebDriverWait` to wait until the element is present in the DOM.\n\n`get_all_by` returns a list of elements matched. It raises an exception if no elements matched.\n`query_all_by` returns a list of elements matched. It returns an empty list when no elements matched.\n`find_all_by` behaves like `get_all_by`, but uses a `WebDriverWait` to wait until the elements jare present in the DOM.\n\nExamples:\n\n```python\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium_testing_library import Screen\n\nscreen = Screen(webdriver.Chrome())\nscreen.query_by((By.ID, "my_id")) # you can use regular tuples as if you were using Selenium\'s find_element()\nscreen.find_by((By.XPATH, "//div"), timeout=5, poll_frequency=0.5) # locators for searching through text also work\nscreen.get_by((By.CSS, ".my_class")) # Will throw an exception if the element is not found\n```\nFor a more detail description check out the [Testing-Library](https://testing-library.com/docs/queries/about)\'s documentation.\n\n## Helper functions\n\n`get_by_role(role_name)` Queries for elements by given role. Does not currently support default roles.\n`get_by_label_text(text)` Queries for label elements that match the the text string and returns the corresponding input element.\n`get_by_placeholder_text(text)` Queries elements with the matching placeholder attribute.\n`get_by_text(text)` Queries elements where the content matches the provided text.\n`get_by_display_value(value)` Queries inputs, textareas, or selects with matching display value.\n`get_by_alt_text(text)` Queries elements with the matching alt attribute.\n`get_by_title(text)` Queries elements with the matching title attribute.\n`get_by_test_id(value)` Queries elements matching the `data-testid` value.\n`get_by_css(css)` Queries elements matching the specified css selector.\n`get_by_xpath(xpath)` Queries elements matching the specified xpath selector.\n\nExamples:\n\n```python\nfrom selenium import webdriver\nfrom selenium_testing_library import Screen\n\nscreen = Screen(webdriver.Chrome())\nscreen.query_by_role("role_name")\nscreen.get_by_label_text("label text")\nscreen.find_all_by_text("my text", timeout=5, poll_frequency=0.5)\nscreen.get_all_by_alt_text("alt text")\n```\n\n## Locators\n\nLocators are utility classes that simplify writing (By.XXX, selector) tuples. They can be used even when using native selenium functions `driver.find_element(locators.Id("my_id"))`.\n\nAvailable locators:\n\n`Css`, `XPath`, `Id`, `Name`, `TagName`, `LinkText`, `PartialLinkText`, `ClassName`, `Role`, `Text`, `PlaceholderText`, `LabelText`, `AltText`, `Title`, `TestId`, `DisplayValu`\n\nExamples:\n\n```python\nfrom selenium import webdriver\nfrom selenium_testing_library import Screen, locators\n\nscreen.query_by(locators.Id("my_id"))\nscreen.find_by(locators.XPath("//div"), timeout=5, poll_frequency=0.5)\nscreen.get_by(locators.Css(".my_class"))\nscreen.get_all_by(locators.Text("my text"))\nscreen.get_by(locators.LinkText("my link text"))\nscreen.query_all_by(locators.ClassName("my-class-name"))\n```\n\n## Wait functions\n\n`wait_for(condition_function)` Waits until condition function returns a truthy value.\n`wait_for_stale(element)` Waits until the element is removed from the DOM.\n\n\nExamples:\n\n```python\nfrom selenium import webdriver\nfrom selenium_testing_library import Screen, locators\n\nscreen = Screen(webdriver.Chrome())\n\n# Wait for the element to be clickable:\nelement = screen.get_by_text("Submit")\nscreen.wait_for(lambda _: element.is_enabled(), timeout=5, poll_frequency=0.5)\n# Wait for the element to be removed from the page:\nscreen.wait_for_stale(element)\n```\n\n## Querying within elements\n\n`Within(element)` Used to limit the query to the children of the provided element\n\nExample:\n\n```python\nfrom selenium import webdriver\nfrom selenium_testing_library import Screen, Within\n\nscreen = Screen(webdriver.Chrome())\nparent_element = screen.get_by_css(".container")\nWithin(parent_element).get_by_title("My title inside the container")\n```\n\n# Contributing\n\nSetting up a local development environment\n\n```shell\ngit clone https://github.com/Smotko/selenium-testing-library.git && cd selenium-testing-library\npoetry install && poetry shell\n# Make sure `chromedriver` is in your PATH, download from https://chromedriver.chromium.org/downloads\n# run tests:\npytest --selenium-headless\n# run tests and display coverage info:\npytest --selenium-headless --cov=selenium_testing_library --cov-report html\n```\n',
    'author': 'Anže Pečar',
    'author_email': 'anze@pecar.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Smotko/selenium-testing-library',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
