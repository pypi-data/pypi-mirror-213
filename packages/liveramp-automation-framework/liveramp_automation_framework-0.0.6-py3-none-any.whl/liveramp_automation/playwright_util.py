from urllib.parse import urlparse, urlunsplit
from liveramp_automation.time_util import MACROS


class PlaywrightUtils:

    def __init__(self, page):
        self.page = page

    def navigate_url(self, scheme=None, host_name=None, path=None, query=None):
        parsed_uri = urlparse(self.page.url)
        self.page.goto(urlunsplit((parsed_uri.scheme if scheme is None else scheme,
                                   parsed_uri.hostname if host_name is None else host_name,
                                   parsed_uri.path if path is None else path,
                                   parsed_uri.query if query is None else query,
                                   '')))

    def savescreenshot(self, name):
        name = "reports/{}_{}.png".format(MACROS["now"], name)
        self.page.screenshot(path=name)
