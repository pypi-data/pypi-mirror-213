import keyring
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


def get_login_details(service_name):
    """
    Get login details from keyring.

    :param service_name: (str) Name of service to retrieve login details for.
    :return: (tuple) Username and password.
    """
    username = keyring.get_password(service_name, 'username')
    password = keyring.get_password(service_name, 'password')
    return username, password


def find_and_click_element(driver, search_type, identifier):
    """
    Find and click element.

    :param driver: (selenium.webdriver) Selenium webdriver.
    :param search_type: (selenium.webdriver.common.by.By) Search type.
    :param identifier: (str) Identifier for element.
    :return: (None)
    """
    element = driver.find_element(search_type, identifier)
    element.click()
    driver.implicitly_wait(5)


def wait_and_click_element(driver, search_type, identifier, wait_time=10):
    """
    Wait for element to be clickable and then click.

    :param driver: (selenium.webdriver) Selenium webdriver.
    :param search_type: (selenium.webdriver.common.by.By) Search type.
    :param identifier: (str) Identifier for element.
    :param wait_time: (int) Time to wait for element to be clickable.
    :return: (None)
    """
    element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((search_type, identifier)))
    element.click()
    driver.implicitly_wait(5)


def get_page_source():
    """
    Get page sources for subaccount morningstar reports.

    :return: (None)
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    service = Service('../webdrivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.jackson.com/login/login.xhtml')

    # Login
    web_username, web_password = get_login_details('JacksonQuery')

    driver.find_element(By.NAME, 'loginForm:userName').send_keys(web_username)
    driver.find_element(By.NAME, 'loginForm:password').send_keys(web_password)

    def two_factor_authentication(web_driver):
        find_and_click_element(web_driver, By.ID, 'mfaForm:text')

        # Wait for the page to navigate and the passcodeForm:code element to be present
        WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.ID, 'passcodeForm:code')))

        # Get the passcode from the user
        passcode = input("Enter the passcode sent to your phone: ")

        # Enter the passcode
        web_driver.find_element(By.ID, 'passcodeForm:code').send_keys(passcode)

        # Wait for the continueButton to be clickable
        WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.ID, 'passcodeForm:continueButton')))

        # Click Verify button
        find_and_click_element(web_driver, By.ID, 'passcodeForm:continueButton')

        # Wait for the next page to load
        web_driver.implicitly_wait(60)

    find_and_click_element(driver, By.ID, 'loginForm:loginLink')

    # Wait for 2FA to complete
    two_factor_authentication(driver)

    try:
        find_and_click_element(driver, By.CSS_SELECTOR, '#onetrust-reject-all-handler')
    except NoSuchElementException:
        print("REJECT COOKIES element not found")

    try:
        find_and_click_element(driver, By.CSS_SELECTOR, '#NoThanksButton')
    except NoSuchElementException:
        print("NO THANKS element not found")

    # Wait for element to load and then click
    wait_and_click_element(driver, By.LINK_TEXT, 'Portfolio Construction Tool')
    wait_and_click_element(driver, By.ID, 'button132358')
    try:
        wait_and_click_element(driver, By.LINK_TEXT, 'Edit')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#perfFundNameColumn > a')))
    except Exception as e:
        print("An error occurred: ", e)

    # Wait for the elements to be present
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btm-nav')))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btm-allocation-label')))

    js_script = '''\
    document.getElementsByClassName('btm-nav')[0].setAttribute("hidden","");
    document.getElementsByClassName('btm-allocation-label')[0].setAttribute("hidden","");
    '''
    driver.execute_script(js_script)

    # Get the number of rows in the table
    driver.implicitly_wait(20)
    table_rows = driver.find_elements(
        By.CSS_SELECTOR, "#ungroupedSubCategoryPerfTable > tr")
    num_rows = len(table_rows)
    print('Number of table rows: {}'.format(num_rows))

    # Iterate over each row
    for i in tqdm(range(1, num_rows + 1)):
        main_window_handle = driver.current_window_handle  # Save the main window handle
        try:
            report_link = driver.find_element(By.CSS_SELECTOR, "#ungroupedSubCategoryPerfTable > tr:nth-child({}) > "
                                                               "td:nth-child(1) > a".format(i))
            report_link_name = report_link.text.replace('/', '_').replace('®', '').replace('.', '').replace(
                ' ', '_').replace('-', '_')
            report_link.click()
            driver.implicitly_wait(5)

            # Switch to new window
            for handle in driver.window_handles:
                if handle != main_window_handle:
                    driver.switch_to.window(handle)
                    break

            page_source = driver.page_source
            with open(f'../data/page_contents/{report_link_name}.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            driver.close()

            # Switch back to the main window
            driver.switch_to.window(main_window_handle)
        except NoSuchElementException:
            # Print the name of the subaccount if the link is not found
            try:
                report_link_name = driver.find_element(
                    By.CSS_SELECTOR, "#ungroupedSubCategoryPerfTable > "
                                     "tr:nth-child({}) > td:nth-child(1)".format(i)).text
                print(f"Link not found for subaccount: {report_link_name}")
            except NoSuchElementException:
                print(f"Row {i} link not found.")
            continue


if __name__ == "__main__":
    get_page_source()
