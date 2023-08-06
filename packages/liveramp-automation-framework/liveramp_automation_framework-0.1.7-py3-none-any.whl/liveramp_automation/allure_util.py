import allure


def allure_attach_screenshot(page, name):
    allure.attach(page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)


def allure_attach_text(text1, text):
    allure.attach(text1, text, allure.attachment_type.TEXT)


def allure_attach_json(text1, json):
    allure.attach(text1, json, allure.attachment_type.JSON)
