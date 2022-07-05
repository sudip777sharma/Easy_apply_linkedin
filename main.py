from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import json

class EasyApplyLinkedin:
    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']
        options = Options()
        options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=data['driver_path'])

    def login_linkedin(self):
        # go to linkedin login page
        self.driver.get("https://www.linkedin.com/login")
        self.driver.maximize_window()

        # fill email
        login_email = self.driver.find_element(By.ID, "username")
        login_email.clear()
        login_email.send_keys(self.email)

        # fill password 
        login_password = self.driver.find_element(By.ID, "password")
        login_password.clear()
        login_password.send_keys(self.password)

        # login button enter
        login_password.send_keys(Keys.ENTER)
    
    def wait_click(self, ele, by):
        wait = WebDriverWait(self.driver, 60)
        if by == 'xpath':
            wait.until(EC.element_to_be_clickable((By.XPATH, ele))).click()
        if by == 'link_text':
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, ele))).click()

    def solve(self):
        # security check click verify
        sleep(3)
        try:
            self.driver.switch_to.frame("captcha-internal")
            self.driver.switch_to.frame("arkoseframe")
            self.driver.switch_to.frame("fc-iframe-wrap")
            self.driver.switch_to.frame("CaptchaFrame")
            xpath = "//*[name()='button' and @id='home_children_button']"
            self.wait_click(xpath, "xpath")
        except Exception as e:
            print("got some error:", e)

        # click job
        job = 0
        while(not job):
            try:
                xpath = "//*[@id=\"global-nav\"]/div/nav/ul/li[3]/a/div/div/li-icon"
                job = self.driver.find_element(By.XPATH, xpath)
                self.wait_click(xpath, "xpath")
            except Exception as e:
                print("not found job yet")
        
        # scroll to "show all" button and click it
        show_all = 0
        while(not show_all):
            try:
                xpath = "//*[name()='a' and @href='https://www.linkedin.com/jobs/collections/recommended']"
                show_all = self.driver.find_element(By.XPATH, xpath)
                ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH, xpath)).perform()
                self.wait_click(xpath, "xpath") 
            except Exception as e:
                print("not found 'show all' yet")

        # minimize chat section
        chat_minimize = 0
        while(not chat_minimize):
            try:
                xpath = "//*[name()='li-icon' and @class='artdeco-button__icon' and @type='chevron-down']"
                chat_minimize = self.driver.find_element(By.XPATH, xpath)
                self.wait_click(xpath, "xpath")
            except Exception as e:
                print("not found chat minimize yet")

        # select company to apply
        no_next_page = False
        while(1):
            # create and store xpath_element of all companies in a list
            companies = 0
            while(not companies):
                try:
                    xpath = "//*[name()='ul' and @class='scaffold-layout__list-container']"
                    companies = self.driver.find_element(By.XPATH, xpath)
                    companies = companies.find_elements(By.XPATH, "./li")
                except Exception as e:
                    print("not found 'all companies section' yet")

            # move to each company
            sleep(3)
            for company in companies:
                try:
                    # finding easy apply tag element
                    sleep(1)
                    job_id = int(company.get_attribute("data-occludable-job-id"))
                    xpath = f"//*[name()='ul' and @class='scaffold-layout__list-container']//*[name()='li' and @data-occludable-job-id='{job_id}']/div/div[1]/ul/li[2]"
                    easy_apply_tag = self.driver.find_element(By.XPATH, xpath)

                    # print the name company name
                    try:
                        xpath = f"//*[name()='ul' and @class='scaffold-layout__list-container']//*[name()='li' and @data-occludable-job-id='{job_id}']/div/div[1]/div[1]/div[2]/div[1]/a"
                        company_name = self.driver.find_element(By.XPATH, xpath)
                        print("------------------------------------------------------")
                        print("company name:", company_name.text)
                        print("------------------------------------------------------")
                    except Exception as e:
                        print("error with finding the company name element")

                    # if found a company with easy apply tag
                    if easy_apply_tag.text == 'Easy Apply':
                        # then click to that company
                        sleep(1)
                        ActionChains(self.driver).move_to_element(company).click().perform()


                        # find easy_apply_button and click it
                        # easy_apply_button = 0
                        # while(not easy_apply_button):
                        sleep(3)
                        try:
                            xpath = f"//*[name()='button' and @data-job-id='{job_id}' and @class='jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view']"
                            easy_apply_button = self.driver.find_element(By.XPATH, xpath)
                            self.wait_click(xpath, "xpath")
                        except Exception as e:
                                print("not found easy apply button yet")

                        # find submit application button and click it
                        sleep(1)
                        submit = 0
                        try:
                            xpath = "//*[name()='button' and @aria-label='Submit application']"
                            submit = self.driver.find_element(By.XPATH, xpath)
                            ActionChains(self.driver).move_to_element(submit).click().perform()
                            sleep(2)
                            # click to done
                            xpath = "//*[name()='button' and @class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view mlA block']"
                            self.wait_click(xpath, "xpath")
                        except Exception as e:
                            print("no direct submit application")

                        sleep(1)
                        # cancel and discard submit application
                        xpath = "//*[name()='button' and @aria-label='Continue to next step']"
                        next = self.driver.find_element(By.XPATH, xpath)
                        if next and not submit:
                            xpath = "//*[name()='button' and @aria-label='Dismiss']"
                            self.wait_click(xpath, "xpath")
                            xpath = "//*[name()='button' and @data-control-name='discard_application_confirm_btn']"
                            self.wait_click(xpath, "xpath")

                        # sleep(1)

                except Exception as e:
                    print("This company doesn't have Easy Apply:")
            
            # create and store xpath_ele of current active page
            try:
                xpath = "//*[name()='li' and @class='artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view']"
                curr_page = self.driver.find_element(By.XPATH, xpath)

                # increament page no by 1 of the current page no
                page_no = int(curr_page.get_attribute("data-test-pagination-page-btn"))
                page_no = page_no + 1
                page_no = str(page_no)
            except Exception as e:
                print("only one page")

            try:
                # create and store xpath_ele of next page
                xpath = f"//*[name()='li' and @data-test-pagination-page-btn='{page_no}']"
                next_page = self.driver.find_element(By.XPATH, xpath)

                # move to next page and click it
                ActionChains(self.driver).move_to_element(next_page).perform()
                sleep(1)
                self.wait_click(xpath, "xpath")
            except Exception as e:
                print("No next page present:")
                no_next_page = True

            if no_next_page:
                break

if __name__ == "__main__":
    with open('config.json') as config_file:
        data = json.load(config_file)
    bot = EasyApplyLinkedin(data)
    bot.login_linkedin()
    bot.solve()















