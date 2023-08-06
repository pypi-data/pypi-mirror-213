import requests
from liveramp_automation.allure_util import allure_attach_text
from liveramp_automation.logger import Logger


def request_post(url, headers, data=None, json=None):
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is POST")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is POST", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
        allure_attach_text(data, "The request data infomation is as the following." )
    if json:
        Logger.info("The json in request body is {}".format(json))
        allure_attach_text("The json in request body is:", json)
    try:
        response = requests.post(url=url, data=data, json=json, headers=headers)
        Logger.info("The response infomation is {}".format(response.text))
        allure_attach_text(response.text,"The response infomation is as the following.")
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_get(url, headers, data=None, json=None):
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is GET")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is GET", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.get(url=url, data=data, json=json, headers=headers)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_options(url, headers):
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is OPTIONS")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is OPTIONS", "Method")
    try:
        response = requests.options(url=url, headers=headers)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_delete(url, headers, data=None, json=None):
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is DELETE")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is DELETE", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.delete(url=url, data=data, json=json, headers=headers)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_head(url, headers, data=None, json=None):
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is HEAD")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is HEAD", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.head(url=url, data=data, json=json, headers=headers)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_put(url, headers, data=None, json=None):
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is PUT")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is PUT", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.put(url=url, data=data, json=json, headers=headers)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response


def request_patch(url, headers, data=None, json=None):
    Logger.info("The url infomation is {}".format(url))
    Logger.info("The request method is PATCH")
    allure_attach_text("The url infomation is {}".format(url), "URL")
    allure_attach_text("The request method is PATCH", "Method")
    if data:
        Logger.info("The request data infomation is {}".format(data))
    if json:
        Logger.info("The json in request body is {}".format(json))
    try:
        response = requests.patch(url=url, data=data, json=json, headers=headers)
        Logger.info("The response infomation is {}".format(response.text))
    except requests.exceptions.HTTPError as error:
        Logger.info("HTTP error occurred {}".format(error))
    except requests.exceptions.Timeout as error:
        Logger.info("Request timed out {}".format(error))
    except requests.exceptions.RequestException as error:
        Logger.info("An error occurred {}".format(error))
    return response
