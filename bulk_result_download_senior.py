from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import base64

url_msc_sr="http://www.prsuuniv.in/home/student/result19/Mg==/UkVHVUxBUg==/NDM4MjIzMTAxODgwMDJAQDcxNzg=/TWFzdGVyIG9mIFNjaWVuY2UgaW4gTWF0aGVtYXRpY3M="

"""
MEANING OF Mg== IS 2
MEANING OF UkVHVUxBUg== IS REGULAR and QVRLVA== IS ATKT
MEANING OF NDM4MjIzMTAxODgwMDJAQDcxNzg= IS 43822310188002@@7178
43822310188002@@7178 can be written as 4382 + 23 (chose Year 23 or 22) + 101 (college code) + 88 (maybe msc maths code) + 002 (college roll number)
MEANING OF TWFzdGVyIG9mIFNjaWVuY2UgaW4gTWF0aGVtYXRpY3M= IS Master of Science in Mathematics

"""
#e_ means encrypted 
def encrypt(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def url_maker(year='23',college_code='101',college_roll='001',sem='2',s_type='REGULAR',stream="Master of Science in Mathematics"):
  #chose 23 or 22
    #year='23' if True else '22'
    #chose college
    #college_code = '101' if True else str(input("enter your college code:"))
    #college_roll='004' if True else str(input("enter your college roll:"))
    roll_number='4382'+year+college_code +'88' +college_roll+'@@7178'
    #print(roll_number)
    e_roll_number=encrypt(roll_number)
    #sem='2'
    #print(encrypt(sem))
    e_sem=encrypt(sem)
    #Student Type
    #s_type='REGULAR' if False else "ATKT"
    e_s_type=encrypt(s_type)

    #Stream
    #stream="Master of Science in Mathematics"
    #s="UG9zdC1HcmFkdWF0ZSBEaXBsb21hIGluIENvbXB1dGVyIEFwcGxpY2F0aW9u"
    e_stream=encrypt(stream)
    generated_url="http://www.prsuuniv.in/home/student/result19/"+e_sem+"/"+e_s_type+"/"+e_roll_number+"/"+e_stream

    return generated_url

def encrypt(value):
  encoded_string = base64.b64encode(value.encode('utf-8')).decode('utf-8')
  #print(encoded_string)
  return encoded_string


def open_and_execute_with_roll_numbers(num_tabs):
  driver = webdriver.Chrome()

  # Loop through tabs and generate URLs
  for i in range(1,num_tabs):
    # Open a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the newly opened tab

    college_roll = f"{i:03d}"

    # Generate URL using url_maker
    url_to_convert = url_maker("22","101",college_roll,'4', "REGULAR", "Master of Science in Mathematics")
    #year='23',college_code='101',college_roll='001',sem='2',s_type='REGULAR',stream="Master of Science in Mathematics"

    # Access PDFmyURL website and enter the URL
    driver.get("https://pdfmyurl.com/")
    url_field = driver.find_element(By.XPATH, '//*[@id="url"]')
    url_field.send_keys(url_to_convert)
    url_field.send_keys(Keys.ENTER)  # Submit the form (triggers conversion)

  # Close tabs after waiting 6 seconds
  for window_handle in driver.window_handles[1:]:  # Skip the first (main) tab
    driver.switch_to.window(window_handle)
    time.sleep(6)
    driver.close()
  driver.quit()  # Close the browser

# Example usage (optional)
open_and_execute_with_roll_numbers(40)  # Open 5 tabs with different URLs
