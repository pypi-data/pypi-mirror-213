import allure


def allure_attach_screenshot(page, screenshot_name):
    allure.attach(page.screenshot(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)


def allure_attach_text(text1, text):
    allure.attach(text1, text, allure.attachment_type.TEXT)
