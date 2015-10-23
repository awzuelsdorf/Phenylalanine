#! /usr/bin/python3

import selenium
import selenium.webdriver
from sys import exit, stderr, argv, stdout

def safeFindElementByID(driver, theID, failOnError=True):
    while True:
        try:
            return driver.find_element_by_id(theID)
        except:
            #stderr.write("Could not find {0} by id\n".format(theID))
            if failOnError:
                return None

def safeFindElementsByTagName(driver, tagName, failOnError=True):
    while True:
        try:
            return driver.find_elements_by_tag_name(tagName)
        except:
            #stderr.write("Could not find {0} by tag name\n".format(tagName))
            if failOnError:
                return None

def safeFindElementsByClassName(driver, className, failOnError=True):
    while True:
        try:
            return driver.find_elements_by_class_name(className)
        except BaseException as e:
            if failOnError:
                return None

def safeFindElementsByXPath(driver, theXPath, failOnError=True):
    while True:
        try:
            return driver.find_elements_by_xpath(theXPath)
        except BaseException as e:
            if failOnError:
                return None

def safeFindElementByName(driver, theName, failOnError=True):
    while True:
        try:
            return driver.find_element_by_name(theName)
        except:
            #stderr.write("Could not find {0} by name\n".format(theName))
            if failOnError:
                return None

def clickCloseButton(driver):
    notClicked = True

    while notClicked:
        closeButtons = safeFindElementsByXPath(driver, "//a[@class='enterCodeSuccessClose enterCodeToolTipClose']", False)

        #stdout.write("Found {0} button(s)\n".format(len(closeButtons)))
        for closeButton in closeButtons:
            try:
                closeButton.click()
                #stdout.write("Clicked close button\n")
                notClicked = False
                break
            except BaseException as e:
                #print(e)
                pass

def enterCokeCardCode(driver, code):
    #Enter coke codes.
    codeField = safeFindElementByName(driver, "enterCodeField", False)
    submitButton = safeFindElementsByClassName(driver, "enterCodeSubmit", False)

    #print(submitButton)
    codeField.clear()
    codeField.send_keys(code)
    submitButton[0].click()

    message = getCodeStatusMessage(driver)

    if "try again" in message.lower():
        stderr.write(code + " received an error message: " + message + "\n")
    else:
        stdout.write(code + " received a success message: " + message + "\n")

#Returns a 2-tuple. The first element is whether there
#was an error (True) or not (False). The second is the
#error or success message, whichever the case may be.
def getCodeStatusMessage(driver):
    while True:
        errorMessages = safeFindElementsByClassName(driver, "enterCodeErrorMessage", True)
        if errorMessages is not None:
            errorMessage = "\n".join([msg.text for msg in errorMessages if len(msg.text.strip()) != 0])
            if errorMessage != "":
                return errorMessage

        successMessages = safeFindElementsByClassName(driver, "enterCodeSuccessMessage", True)
        if successMessages is not None:
            successMessage = "\n".join([msg.text for msg in successMessages if len(msg.text.strip()) != 0])
            if successMessage != "":
                return successMessage

def enterCokeCapCode(driver, code):
    #Enter coke codes.
    codeField = safeFindElementByName(driver, "enterCodeField", False)
    submitButton = safeFindElementsByClassName(driver, "enterCodeSubmit", False)

    #print(submitButton)
    codeField.clear()
    codeField.send_keys(code)
    submitButton[0].click()

    foundBrand = False
   
    while not foundBrand: 
        brandButtons = safeFindElementsByTagName(driver, "a", False)
        errorMessages = safeFindElementsByClassName(driver, "enterCodeErrorMessage", False)
        if errorMessages is not None:
            errorMessage = "\n".join([msg.text for msg in errorMessages if len(msg.text.strip()) != 0])
            if errorMessage != "":
                stderr.write("{0} received error messages: \n\"{1}\"\n".format(code, errorMessage))
                foundBrand = True
                break
        for button in brandButtons:
            if button is not None and button.get_attribute("brand-id") is not None:
                try:
                    button.click()
                    #print("Clicking button "+button.get_attribute("brand-id") + " succeeded")
                    stdout.write(code + " entered successfully.\n")
                    clickCloseButton(driver)
                    foundBrand = True
                    break
                except:
                    pass
                    #print("Clicking button " + button.get_attribute("brand-id") + " failed")

def logout(driver):
    signOutButton = safeFindElementByID(driver, "h-profilePhoto-id", False)
    signOutButton.click()

    notClicked = True

    while notClicked:
        try:
            realSignOutButton = safeFindElementByID(driver, "h-signOutLink", False)
            if realSignOutButton is not None:
                realSignOutButton.click()
                notClicked = False
            else:
                stderr.write("Couldn't find the sign out button!\n")
        except:
            pass

def main():
    if len(argv) != 3:
        stderr.write("Usage: {0} <codes_caps_file> <codes_cardboard_file>\n".format(argv[0]))
        exit(-1)

    #Go to mycokerewards.com
    driver = selenium.webdriver.Firefox()
    driver.get("http://www.mycokerewards.com")

    #Sign in to mycokerewards.com
    signInButton = safeFindElementByID(driver, "h-signInJoinLink", False)
    signInButton.click()

    email = safeFindElementByID(driver, "capture_signIn_traditionalSignIn_emailAddress", False)
    password = safeFindElementByID(driver, "capture_signIn_traditionalSignIn_password", False)

    email.send_keys(input("Please enter your email address: "))
    password.send_keys(input("Please enter your password: ")) #Cannot use
    #getpass because I need to enter password by sending data to this
    #program from a file

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
                    #print("Yay it worked!")
                    succeeded = True
                    break
                except BaseException as ex:
                    pass
                    #print(type(ex))

    #Enter code from bottlecaps
    with open(argv[1], 'r') as codeCapsFile:
        for code in codeCapsFile:
            enterCokeCapCode(driver, code.strip())

    #Enter code from big cardboard boxes
    with open(argv[2], 'r') as codeCardFile:
        for code in codeCardFile:
            enterCokeCardCode(driver, code.strip())

    input("Press enter to logout.")

    logout(driver)

    input("Press enter to quit")
    print()
    driver.close()

if __name__ == "__main__":
    main()
