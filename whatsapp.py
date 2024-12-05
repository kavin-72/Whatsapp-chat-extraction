from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Path to the ChromeDriver executable
PATH = r"C:\Program Files (x86)\chromedriver.exe"
service = Service(PATH)

# Set Chrome options
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-handle-verifier")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Set a timeout
driver.set_page_load_timeout(30)

# Open WhatsApp Web
try:
    driver.get("https://web.whatsapp.com")
    print("Please scan the QR code to log in.")
   
    # Wait for user to scan QR code
    input("Press Enter after logging in...")

    # Monitor for new messages
    print("Monitoring chats...")
    chat_data = []  # To store chat data
    processed_messages = set()  # To track processed messages

    while True:
        time.sleep(3)  # Polling interval
        chats = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')

        for chat in chats:
            try:
                message_text = chat.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]').text
                timestamp = chat.find_element(By.XPATH, './/div[contains(@class, "copyable-text")]').get_attribute("data-pre-plain-text")
                unique_id = f"{timestamp} - {message_text}"  # Create a unique identifier for the message

                if unique_id not in processed_messages:
                    processed_messages.add(unique_id)  # Mark this message as processed
                    chat_data.append({"Timestamp": timestamp, "Message": message_text})
                    print(f"New message: {timestamp} - {message_text}")
            except Exception as e:
                continue  # Skip if elements are not found

        # Save to Excel
        if chat_data:  # Save only if there are new messages
            df = pd.DataFrame(chat_data)
            df.to_excel("whatsapp_chats.xlsx", index=False)
            print("Data saved to whatsapp_chats.xlsx")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
