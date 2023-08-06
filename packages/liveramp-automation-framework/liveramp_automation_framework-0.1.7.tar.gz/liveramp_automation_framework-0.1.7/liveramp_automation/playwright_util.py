from urllib.parse import urlparse, urlunsplit
from liveramp_automation.time_util import MACROS


class PlaywrightUtils:

    def navigate_url(page, scheme=None, host_name=None, path=None, query=None):
        parsed_uri = urlparse(page.url)
        page.goto(urlunsplit((parsed_uri.scheme if scheme is None else scheme,
                                  parsed_uri.hostname if host_name is None else host_name,
                                  parsed_uri.path if path is None else path,
                                  parsed_uri.query if query is None else query,
                                  '')))

    def savescreenshot(page, name):
        name = "reports/{}_{}.png".format(MACROS["now"], name)
        page.screenshot(path=name)