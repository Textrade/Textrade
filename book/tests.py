import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from config import HOST, PORT
from models import BookToRent

driver = webdriver.Chrome("/Users/dsantos/WebDrivers/chromedriver")


def test_add_book_for_rent_automated():
    driver.get(HOST+":"+PORT+"/dashboard/rentals/")
    login_helper()
    assert "Your Rentals | Textrade" in driver.title
    driver.find_element_by_id("add-book").click()
    time.sleep(2)
    driver.switch_to_active_element()
    driver.find_element_by_id("book").send_keys("C How to Program")
    driver.find_element_by_id("isbn").send_keys("9780133976892")
    select = Select(driver.find_element_by_id("condition"))
    select.select_by_index(3)
    driver.find_element_by_id("condition_comment").send_keys("This is an automated test.")
    driver.find_element_by_id("marks").click()
    time.sleep(2)
    driver.find_element_by_id("send-request").send_keys(Keys.ENTER)

    driver.close()


def login_helper():
    driver.find_element_by_id("username").send_keys("admin")
    driver.find_element_by_id("password").send_keys("admin")
    driver.find_element_by_id("submit").send_keys(Keys.ENTER)


if __name__ == '__main__':
    test_add_book_for_rent_automated()
