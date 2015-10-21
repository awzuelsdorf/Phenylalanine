#! /usr/bin/python3

import selenium
import selenium.webdriver
import time
from sys import exit, stderr

def safeFindElementByID(driver, theID, failOnError=True):
    while True:
        try:
            return driver.find_element_by_id(theID)
        except:
            stderr.write("Could not find {0} by id\n".format(theID))
            if failOnError:
                return None

def safeFindElementsByTagName(driver, tagName, failOnError=True):
    while True:
        try:
            return driver.find_elements_by_tag_name(tagName)
        except:
            stderr.write("Could not find {0} by tag name\n".format(tagName))
            if failOnError:
                return None

def safeFindElementsByClassName(driver, className, failOnError=True):
    while True:
        try:
            return driver.find_elements_by_class_name(className)
        except:
            stderr.write("Could not find {0} by class name\n".format(className))
            if failOnError:
                return None

def safeFindElementByName(driver, theName, failOnError=True):
    while True:
        try:
            return driver.find_element_by_name(theName)
        except:
            stderr.write("Could not find {0} by name\n".format(theName))
            if failOnError:
                return None

def main():
    #Go to mycokerewards.com
    driver = selenium.webdriver.Firefox()
    driver.get("http://www.mycokerewards.com")

    #Sign in to mycokerewards.com
    signInButton = safeFindElementByID(driver, "h-signInJoinLink", False)

    signInButton.click()

    email = safeFindElementByID(driver, "capture_signIn_traditionalSignIn_emailAddress", False)
    password = safeFindElementByID(driver, "capture_signIn_traditionalSignIn_password", False)

    email.send_keys("azuelsdorf16@gmail.com")
    password.send_keys("y0L0v1ll3")
    signInButton = safeFindElementByID(driver, "capture_signIn_traditionalSignIn_signInButton", False)
    signInButton.click()

    #Get past the "Connect with Facebook and Twitter" garbage
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

    #Enter coke codes.
    codeField = safeFindElementByName(driver, "enterCodeField", False)
    submitButton = safeFindElementsByClassName(driver, "enterCodeSubmit", False)

    print(submitButton)

    codeField.send_keys("7jnv5xprpx5fwx")
    submitButton[0].click()

    input("Press enter to quit")
    driver.close()

if __name__ == "__main__":
    main()
