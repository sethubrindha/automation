import random
from time import sleep
from selenium.webdriver.common.by import By

# constant
ELEMENT_TYPE = ['button', 'text']
QUERY_SETTINGS = "Settings:  Show subtitles in the video. Don't use iStock"
# EMAIL = 'sethumd609'
# PASS = 'SETHUpathi@123'


def msg(
        _option_,
        _message_
        ):
    if _option_ == 1:
        print('\x1b[0;32;40m> %s\x1b[0m' % _message_)
    elif _option_ == 2:
        print('\x1b[0;32;40m>\x1b[0m %s' % _message_)
    elif _option_ == 3:
        print('\n\x1b[0;32;40m[\x1b[0m%s\x1b[0;32;40m]\x1b[0m' % _message_)
    else:
        print('\n\x1b[0;31;40m[ERROR]\x1b[0m')

def timer(sec=None):
    if sec:
        sleep(sec)
    else:
        sleep(random.randint(1,4))



def element_action(driver, element_dict): 
    timer(5)
    elementXpath = element_dict['elementXpath'] if 'elementXpath' in element_dict else None
    element_type = element_dict['element_type'] if 'element_type' in element_dict else None
    keys = element_dict['keys'] if 'keys' in element_dict else None
    sec = element_dict['timer'] if 'timer' in element_dict else None
    Xpath = f"//*[contains(text(), '{elementXpath}')]"

    element = driver.find_element(By.XPATH, elementXpath)
    if element_type == ELEMENT_TYPE[0]:
        element.click()
    else:
        element.click()
        element.send_keys(keys)
    timer(sec)
