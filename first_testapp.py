from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select

url_website = "http://localhost:5173"
PASSWORD = "Trytry1!"
id_cook = "c8554618-ed57-4f2f-bd70-98fabf08f0ed"
id_wait = "cbaad999-5cbd-48f8-9ce2-aa7c8a44b3fd"


def click_button(id, driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id)))
    button = driver.find_element(By.ID, id)
    button.click()


def tick_all_checkboxes(driver):
    
    try:
        checkboxes_present = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="checkbox"]'))
        )

        if checkboxes_present:
            all_checkboxes_ticked = False
            
            while not all_checkboxes_ticked:
                checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
                all_checkboxes_ticked = True
                
                for checkbox in checkboxes:
                    if not checkbox.is_selected():
                        checkbox.click()
                        all_checkboxes_ticked = False
                    time.sleep(1)
            
            print("All checkboxes are now ticked.")
        else:
            print("No checkboxes found.")
        
    except Exception as e:
        print(f"No checkboxes found or encountered an issue: {e}")


def tick_checkbox(id, driver):
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, str(id)))
    )
    
    if not checkbox.is_selected():
        checkbox.click()
    
    assert checkbox.is_selected()


def login_user(driver):
    driver.get(url_website)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element(By.ID, 'email').send_keys('283127@student.pwr.edu.pl')
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        driver.find_element(By.ID, 'password').send_keys(PASSWORD)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_button')))
        driver.find_element(By.ID, 'login_button').click()
        
        time.sleep(5)
    except Exception as e:
        print(f"User test encountered an issue: {e}")


def login_admin(driver, email, password):
    driver.get(url_website + "/loginadmin")
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element(By.ID, 'email').send_keys(email)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        driver.find_element(By.ID, 'password').send_keys(password)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_button')))
        driver.find_element(By.ID, 'login_button').click()
        
        time.sleep(5)
    except Exception as e:
        print(f"Admin test encountered an issue: {e}")


def add_dish_and_submit(driver):
    
    try:
        for i in range(1,3):
            click_button(str(i), driver)
            notes_input_id = 'notes'
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, notes_input_id)))
            driver.find_element(By.ID, notes_input_id).send_keys(f'This is a note for the dish.')
            if i % 2 == 0:
                click_button("increase", driver)
            time.sleep(2)

            click_button("add_to_order", driver)
            time.sleep(2)
            click_button("back", driver)
            time.sleep(2)
        click_button("order", driver)
        time.sleep(2)
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "num_table"))
        )
        select = Select(select_element)

        select.select_by_visible_text('1')
        click_button("submit_order", driver)
    except Exception as e:
        print(f"Add dish test encountered an issue: {e}")


def manage_complete_order(driver, num_order):
    login_admin(driver, "buosog@yahoo.it", PASSWORD)
    click_button("Manage", driver)
    click_button(num_order, driver)
    click_button("+_cook", driver)
    tick_checkbox(id_cook, driver)
    click_button("cook_save", driver)
    click_button("+_cook", driver) #close button
    click_button("+_waiter", driver)
    tick_checkbox(id_wait, driver)
    click_button("wait_save", driver)
    login_admin(driver, "daviibuoso@gmail.com", PASSWORD)
    tick_all_checkboxes(driver)
    login_admin(driver, "buosogabriele@gmail.com", PASSWORD)
    tick_all_checkboxes(driver)


def user_pay_order(driver):
    click_button("confirm_to_pay", driver)
    click_button("accept", driver)
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'points')))
    driver.find_element(By.ID, 'points').send_keys('10')
    time.sleep(1)
    click_button("submit_points", driver)
    time.sleep(1)


def admin_confirm_payment(num_order):
    driver_staff = webdriver.Chrome()
    login_admin(driver_staff, "buosog@yahoo.it", PASSWORD)
    click_button("Payments", driver_staff)
    time.sleep(1)
    click_button(f"div_order_{str(num_order)}", driver_staff)
    time.sleep(1)
    click_button(str(num_order), driver_staff)
    time.sleep(1)
    driver_staff.refresh()
    time.sleep(1)


def main():
    num_order = 262
    try:
        driver = webdriver.Chrome()
        login_user(driver)
        add_dish_and_submit(driver)
        driver_staff = webdriver.Chrome()
        manage_complete_order(driver_staff, num_order)
        driver_staff.quit()
        user_pay_order(driver)
        admin_confirm_payment(num_order)
    finally:
        driver.quit()
        driver_staff.quit()


main()


# https://github.com/GabrieBu/test_webapp