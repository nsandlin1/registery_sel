from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from datetime import datetime

from time import sleep

def check(options):
    # instantiate browser
    browser = webdriver.Chrome(options=options)

    try:
        browser.get("https://boss.latech.edu/ia-bin/tsrvweb.cgi?&WID=W&tserve_tip_write=%7C%7CWID&tserve_trans_config=astulog.cfg&tserve_host_code=HostZero&tserve_tiphost_code=TipZero")
    except:
        print("could not access web".ljust(30, ' ') + str(datetime.now()))
        return 1

    # login
    try:
        browser.find_element(By.NAME, "SID").send_keys("")
    except:
        print("boss down".ljust(30, ' ') + str(datetime.now()))
        return 1
    browser.find_element(By.NAME, "PIN").send_keys("")
    browser.find_element(By.NAME, "submitbutton").click()

    # go to Course Selections
    element = browser.find_element(By.ID, "menuHeading4")
    actions = ActionChains(browser)
    actions.move_to_element(element).perform()
    browser.find_element(By.XPATH, '//*[@id="menu4"]/a[1]').click()

    # Click computer science and submit
    Select(browser.find_element(By.NAME, 'Subject')).select_by_visible_text("Computer Science")
    browser.find_element(By.NAME, "submitbutton").click()

    # Click Cloud computing and submit
    Select(browser.find_element(By.NAME, 'CourseID')).select_by_visible_text("CSC -452 DISTRIBUTED & CLOUD COMPUTING")
    browser.find_element(By.NAME, "submitbutton").click()

    # get class status
    status = browser.find_element(By.XPATH, '/html/body/div[3]/form/table[2]/tbody/tr[5]/td[3]').text

    # if class is not closed, enroll
    if status == "Closed ":
        print("class closed".ljust(30, ' ') + str(datetime.now()))
        return 1
    else:
        # go to Drop and Add classes
        element = browser.find_element(By.ID, "menuHeading3")
        actions = ActionChains(browser)
        actions.move_to_element(element).perform()
        browser.find_element(By.XPATH, '//*[@id="menu3"]/a[1]').click()
        
        # drop other cloud computing class
        Select(browser.find_element(By.XPATH, '/html/body/div[3]/form/table[1]/tbody/tr[4]/td[4]/select')).select_by_visible_text("Drop")

        # add other class
        browser.find_element(By.XPATH, "/html/body/div[3]/form/table[3]/tbody/tr[2]/td[1]/input[2]").send_keys("12447")

        # do the damage
        browser.find_element(By.NAME, "submitbutton").click()

        print("!!!class joined!!!".ljust(30, ' ') + str(datetime.now()))
        exit(0)

if __name__ == '__main__':
    options = Options()
    # don't show gui
    options.add_argument("--headless")

    minutes = 45
    while check(options) == 1:
        sleep(60 * minutes)