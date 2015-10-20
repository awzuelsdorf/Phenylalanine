#! /usr/bin/python3

import selenium
import selenium.webdriver
import time

driver = selenium.webdriver.Firefox()

driver.get("http://www.mycokerewards.com")

print(driver.title)

signInButton = driver.find_element_by_id("h-signInJoinLink")

signInButton.click()

email = driver.find_element_by_id("capture_signIn_traditionalSignIn_emailAddress")
password = driver.find_element_by_id("capture_signIn_traditionalSignIn_password")

email.send_keys("azuelsdorf16@gmail.com")
password.send_keys("y0L0v1ll3")
signInButton = driver.find_element_by_id("capture_signIn_traditionalSignIn_signInButton")
signInButton.click()

for i in range(3):
    succeeded = False
    while not succeeded:
        skipButtons = driver.find_elements_by_class_name("connect-with-provider-skip-for-now")
        for button in skipButtons:
            try:
                button.click()
                print("Yay it worked!")
                succeeded = True
                break
            except BaseException as ex:
                print(type(ex))

input("Press enter to quit")
driver.close()
