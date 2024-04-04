import time
from collections import OrderedDict

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
URL = "http://sdetchallenge.fetch.com/"
BARS = list(range(9))
RESULT_FIELD = (By.ID, "reset")
WEIGH_BUTTON = (By.ID, "weigh")
RESET_BUTTON = (By.CSS_SELECTOR, "button.button#reset")
BOWL_CELLS = (By.CSS_SELECTOR, "input.bowl")


# Utility functions
def open_website():
    # Replace executable path with path of chromedriver.exe in your local system
    driver = webdriver.Chrome(
        executable_path='D:\Buffalo Courses\computer linguistics\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    driver.get(URL)
    return driver


def fill_bowls(driver, left_bars, right_bars):
    print("left bar ", left_bars)
    print("right bar ", right_bars)
    for i, left_bar in enumerate(left_bars):
        left_id = "left_" + str(i)
        cell = driver.find_elements(By.ID, left_id)[0]
        cell.send_keys(str(left_bars[i]))
        input_value = cell.get_attribute("value")

        # Print the input value
        print("Input value filled by cell:", int(input_value))
    for i, right_bar in enumerate(right_bars):
        right_id = "right_" + str(i)
        cell = driver.find_elements(By.ID, right_id)[0]
        cell.send_keys(str(right_bars[i]))
        input_value = cell.get_attribute("value")

        # Print the input value
        print("Input value filled by cell:", int(input_value))


def get_weighing_result(driver):
    time.sleep(2)
    try:
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(RESULT_FIELD))
        return str(button.text)
    except TimeoutException:
        return "TimeoutError: Result field not found"


def click_button(driver, button):
    # driver.find_element(*button).click()

    # Find all matching buttons
    buttons = driver.find_elements(*button)

    # Click each button
    for button in buttons:
        button.click()


def click_fake_bar(driver, bar_number):
    fake_id = "coin_" + str(bar_number)
    driver.find_element(By.ID, fake_id).click()
    time.sleep(3)


def get_alert_message(driver):
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        message = alert.text
        alert.accept()
        return message
    except TimeoutException:
        return "TimeoutError: Alert not found"


def get_weighing_list(driver):
    weighing_list = driver.find_element(By.ID, "history").text
    return weighing_list.split("\n")


# Algorithm
def find_fake_bar():
    driver = open_website()
    weighings = []

    # First weighing
    left_group = BARS[:3]
    right_group = BARS[3:6]
    fill_bowls(driver, left_group, right_group)
    click_button(driver, WEIGH_BUTTON)
    result = get_weighing_result(driver)
    weight = OrderedDict()
    weight["left"] = left_group
    weight["result"] = result
    weight["right"] = right_group

    weighings.append(weight)
    print(weighings)
    if "=" in result:
        remaining_group = BARS[6:]
        print(remaining_group)
    elif "<" in result:
        remaining_group = left_group
        print(remaining_group)
    else:
        remaining_group = right_group
        print(remaining_group)

    click_button(driver, RESET_BUTTON)

    # Second weighing
    left_group = remaining_group[0:1]
    right_group = remaining_group[1:2]
    fill_bowls(driver, left_group, right_group)
    click_button(driver, WEIGH_BUTTON)
    result = get_weighing_result(driver)
    weight = OrderedDict()
    weight["left"] = left_group
    weight["result"] = result
    weight["right"] = right_group

    weighings.append(weight)

    print (weighings)

    if "=" in result:
        fake_bar = remaining_group[2]
    elif "<" in result:
        fake_bar = left_group[0] if len(left_group) == 1 else left_group[1]
    else:
        fake_bar = right_group[0]
    print("fake ", fake_bar)

    click_fake_bar(driver, fake_bar)
    alert_message = get_alert_message(driver)
    print("Alert Message" + alert_message)
    print("Number of Weighings", len(weighings))
    print("Weighing List:")
    for weighing in weighings:
        print(weighing)

    driver.quit()


if __name__ == "__main__":
    find_fake_bar()
