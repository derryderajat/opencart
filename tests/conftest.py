import os
import warnings
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from selenium.webdriver.edge.service import Service as ServiceEdge
from selenium.webdriver.safari.service import Service as ServiceSafari
from selenium.webdriver.ie.service import Service as ServiceIe
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager

# Set WebDriver Manager log level
os.environ['WDM_LOG_LEVEL'] = '0'

@pytest.fixture(scope="session")
def base_url():
    """Fixture for the base URL of the application."""
    return "https://www.saucedemo.com"

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser choice: chrome, firefox, edge, safari, ie")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")

@pytest.fixture(scope="class")
def init_driver(request, base_url):
    warnings.simplefilter("ignore", ResourceWarning)
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = None
    options = None

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=ServiceChrome(ChromeDriverManager().install()), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(service=ServiceFirefox(GeckoDriverManager().install()), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(service=ServiceEdge(EdgeChromiumDriverManager().install()), options=options)

    elif browser == "safari":
        options = SafariOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Safari(service=ServiceSafari())

    elif browser == "ie":
        options = IeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Ie(service=ServiceIe(IEDriverManager().install()))

    else:
        raise ValueError("Browser not supported: {}".format(browser))

    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    # Store driver, wait, and base_url in the test class (request.cls)
    request.cls.driver = driver
    request.cls.wait = wait
    request.cls.base_url = base_url

    # Yield driver for teardown
    yield driver
    
    # Teardown: clean up after test
    driver.delete_all_cookies()
    driver.quit()
