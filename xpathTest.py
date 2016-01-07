#! /usr/bin/env python3

from mycoke2 import *

import selenium.webdriver

def main():
    driver = selenium.webdriver.Firefox()

    driver.get("file:///home/jimmy/COKE/mypage.html")

    clickCloseButton(driver)

    input("Press enter to quit.")
    driver.close()

if __name__ == "__main__":
    main()
