from urllib.parse import urlparse, urlunsplit
from liveramp_automation.time_util import MACROS


class SeleniumUtils:

    def navigate_url(driver, scheme=None, host_name=None, path=None, query=None):
        parsed_uri = urlparse(driver.url)
        driver.get(urlunsplit((parsed_uri.scheme if scheme is None else scheme,
                               parsed_uri.hostname if host_name is None else host_name,
                               parsed_uri.path if path is None else path,
                               parsed_uri.query if query is None else query,
                               '')))

    def savescreenshot(driver, name):
        name = "reports/{}_{}.png".format(MACROS["now"], name)
        driver.save_screenshot(path=name)
