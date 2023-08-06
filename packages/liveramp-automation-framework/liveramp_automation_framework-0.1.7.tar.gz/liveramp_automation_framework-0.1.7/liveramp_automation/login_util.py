import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from liveramp_automation.logger import Logger
from liveramp_automation.time_util import windows_wait


class Login:

    @staticmethod
    def liveramp_okta_login_page(page, config, USERNAME, PASSWORD):
        # navigate to the Okta login page
        Logger.info("We are going to login to OKTA")
        url = config['login_url']
        Logger.info("The login url is {}".format(url))
        page.goto(url)
        windows_wait()
        url_new = page.url
        Logger.info("The current url is {}".format(url_new))
        if url_new.__contains__(url):
            Logger.info("We've already logan to OKTA succefully")
        else:
            page.fill('#idp-discovery-username', USERNAME)
            page.get_by_role("button", name="Next").click()
            page.get_by_role("textbox", name="Password").fill(PASSWORD)
            page.get_by_role("button", name="Sign In").click()
            Logger.info("We could login to OKTA successfully")
            # wait for the login process to complete
            windows_wait(20)

    @staticmethod
    def liveramp_okta_login_driver(driver, config, USERNAME, PASSWORD):
        # navigate to the Okta login page
        Logger.info("We are going to login to OKTA")
        url = config['login_url']
        Logger.info("The login url is {}".format(url))
        driver.get(url)
        windows_wait()
        if driver.current_url.__contains__(url):
            Logger.info("We've already logan to OKTA succefully")
        else:
            # username = driver.find_element_by_id('idp-discovery-username')
            username = driver.find_element(by=By.ID, value='idp-discovery-username')
            username.send_keys(USERNAME)
            username.send_keys(Keys.ENTER)
            windows_wait()
            # password = driver.find_element_by_id('okta-signin-password')
            password = driver.find_element(by=By.ID, value='okta-signin-password')
            password.send_keys(PASSWORD)
            # driver.find_element_by_id('okta-signin-submit').click()
            submit_button = driver.find_element(by=By.ID, value='okta-signin-submit')
            submit_button.click()
            Logger.info("We could login to OKTA successfully")
            # wait for the login process to complete
            windows_wait(20)

    @staticmethod
    def call_oauth2_get_token(APIUSERNAME, APIPASSWORD):
        params = {
            "grant_type": "password",
            "scope": "openid",
            "client_id": "liveramp-api"
        }
        Logger.info("The default params are the {}".format(params))
        headers = {"content-type": "application/x-www-form-urlencoded"}
        params.update(username=APIUSERNAME)
        params.update(password=APIPASSWORD)
        response = requests.post(
            "https://serviceaccounts.liveramp.com/authn/v1/oauth2/token", params=params, headers=headers)
        assert 200 == response.status_code
        access_token = response.json()['access_token']
        return "Bearer {}".format(access_token)
