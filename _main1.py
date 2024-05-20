import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

# CREDENTTALS:
EMAIL = "slubhatti@gmail.com"
PASSWORD = "tradingbot786"
# ID FOR DEMO ACCOUNT SELECTION
ID = 41804616

# FLAG TO INDICATE THE FIRST TRADE
first_trade = True

# SET PROFIT MARGIN
desired_profit = float(input("Enter the profit you desire: $"))

# SETTING UP CHROME WEBDRIVER
driver = uc.Chrome()
driver.implicitly_wait(15)
driver.get("https://qxbroker.com/en")
driver.maximize_window()

# FUNCTION: TO PRESS THE UP-BUTTON
def press_up():
    """ Press the Up Button """
    btn_Up = driver.find_element(By.XPATH, '//div[@class="section-deal__success  percent"]')
    btn_Up.click()

# FUNCTION: TO PRESS THE DOWN-BUTTON
def press_down():
    """ Press the Down Button """
    btn_Down = driver.find_element(By.XPATH, "//button[@class='button button--danger button--spaced put-btn section-deal__button ']")
    btn_Down.click()

# FUNCTION: SET INITIAL TRADING AMOUNT 
def initial_trade_value(initial_amount):
    """ Set the initial value for the first trade """

    investment_section = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[5]/div[2]/div/div/input')
    investment_section.click()
    investment_section.send_keys(Keys.CONTROL + 'a')    
    investment_section.send_keys(Keys.BACK_SPACE)    
    investment_section.send_keys(initial_amount)

# FUNCTION: CHANGING AMOUNT FUNCTION FOR NEXT TRADES
def click_investment_section(new_amount):
    """ Set the value for the next trades after the first trade """

    investment_section = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[5]/div[2]/div/div/input')    
    investment_section.click()    
    investment_section.send_keys(Keys.CONTROL + 'a')    
    investment_section.send_keys(Keys.BACK_SPACE)    
    investment_section.send_keys(new_amount)


# FUNCTION: TO GET CURRENT TIME
def current_time():
    """ Returns Every Second of a Minute"""
    timer = driver.find_element(By.XPATH, '//div[@class="server-time online"]')
    sp = timer.text.split()
    real_time = sp[0]
    # Extract the seconds part (last 2 characters in the time string)
    seconds_part = real_time[-2:]
    time.sleep(1)
    return seconds_part

# STARTING OF THE CODE
element = driver.find_element(By.XPATH, "//*[@id='top']/div/div[1]/a[2]")
element.click()

# PROVIDE EMAIL AND PASSWORD FOR SIGNIN BUTTON
time.sleep(1)
email_entry = driver.find_element(By.XPATH, "//*[@id='tab-1']/form/div[1]/input").send_keys(EMAIL)
password_entry = driver.find_element(By.XPATH, "//*[@id='tab-1']/form/div[2]/input").send_keys(PASSWORD)
signin_button = driver.find_element(By.XPATH, "//*[@id='tab-1']/form/button/div").click()


# input()
# DEMO ACCOUNT SELECTION
# CLICKING ON THE USER MENU
time.sleep(10)
# CLICKING ON THE USER MENU
u_menu = driver.find_element(By.XPATH, "//div[@class='usermenu__info-wrapper']")
u_menu.click()

# GETTING USER ID 
span_user_id = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div[2]/ul[1]/li[1]/div[2]/div/span")
user_id_string = span_user_id.text

user_id_list = user_id_string.split()
real_user_id = int(user_id_list[1])

# CHECK IF USER ID MATCHES
try:
    if real_user_id == ID:
        # CLICKING ON DEMO ACCOUNT MENU
        dm_ac_menu = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div[2]/ul[1]/li[3]/a")
        dm_ac_menu.click()
        
        # CLOSING ANY POP-UP IF PRESENT
        close_button = driver.find_element(By.XPATH, "//*[@id='root']/div/div[3]/div/div/div/div[2]/button").click()

        time.sleep(10)
        # Initialize current profit
        current_profit = 0

        # Initialize the initial trading amount according to the user desire
        initial_trading_amount = int(input("Set your initial trading amount: $"))
        # Track the current trading amount
        current_trading_amount = initial_trading_amount
        initial_trade_value(initial_trading_amount)

        # RETRIVING INITIAL DEMO ACCOUNT MONEY
        demo_account_money = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div/div[3]/div[2]")
        dollars = demo_account_money.text
        previous_demo_account_money = float(dollars[1:].replace(',', ''))

        buttons = [press_up, press_down]
        current_btn = random.choice(buttons)

        # LOOP FOR TRADING
        while True:
            string_seconds = current_time()
            d = int(string_seconds)

            # Condition to place a trade at the start of each minute (when seconds are 0)
            if d == 0:
                # time.sleep(2)
                # Choose a random button to press in the first trade
                if first_trade:
                    current_btn = random.choice(buttons)
                    current_btn()
                    first_trade = False
                    time.sleep(2)
                else:
                    # time.sleep(1)
                    print(previous_demo_account_money)
                    # Calculate profit after the trade
                    demo_account_money = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div/div[3]/div[2]")
                    dollars = demo_account_money.text
                    current_demo_account_money = float(dollars[1:].replace(',', ''))
                    print(current_demo_account_money)
                    profit = current_demo_account_money - previous_demo_account_money
                    # Introducing r_profit variable for storing the changes made in every trade
                    r_profit = profit

                    # Update current profit for the next iteration
                    current_profit += int(profit)

                    print(f"Get profit after trade: ${profit}")
                    print(f"Current Profit: ${current_profit}")

                    # Update previous demo account money for the next iteration
                    previous_demo_account_money = current_demo_account_money

                    time.sleep(5)

                    # Check if the desired profit is reached
                    if current_profit >= desired_profit:
                        print(f"Target Achieved! Desire profit of ${desired_profit}reached.  Quit the program.")
                        driver.quit()
                        break

                    # Reset the amount to the initial value after a profit
                    if r_profit >= 0:
                        time.sleep(0.5)
                        current_trading_amount = initial_trading_amount
                        # Click the button and update the investment amount
                        click_investment_section(current_trading_amount)
                        current_btn()

                    else:
                        time.sleep(1)
                        # Double the amount in the next iteration if there is a loss
                        current_trading_amount = str(int(current_trading_amount) * 2)
                        # Switch the button in the next iteration
                        current_btn = press_down if current_btn == press_up else press_up

                        # Click the button and update the investment amount
                        click_investment_section(current_trading_amount)
                        current_btn()

                    r_profit = 0       # Here we are making r_profit zero or empty

except:
    print("Something find error.....")
