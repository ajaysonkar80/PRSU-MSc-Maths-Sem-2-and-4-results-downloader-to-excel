import base64
import requests
import openpyxl
import re
from bs4 import BeautifulSoup

# Load the Excel workbook
workbook = openpyxl.load_workbook("A:\MY-PROJECTS\MScSemIIResult.xlsx")

# Select the sheet where you want to insert the data
ws = workbook.active  # Assuming you want to insert into the active sheet


def encrypt(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def url_maker(year='23',college_code='101',college_roll='001',sem='2',s_type='REGULAR',stream="Master of Science in Mathematics"):
    roll_number='4382'+year+college_code +'88' +college_roll+'@@7178'
    e_roll_number=encrypt(roll_number)
    e_sem=encrypt(sem)
    e_s_type=encrypt(s_type)
    e_stream=encrypt(stream)
    generated_url="http://www.prsuuniv.in/home/student/result19/"+e_sem+"/"+e_s_type+"/"+e_roll_number+"/"+e_stream
    return generated_url


def percentage_finder(text):
  pattern = r"\b(\d{3})/500\b"
  match = re.search(pattern, text)
  if match:
    percentage=int(match.group(1))/5
    percentage=round(percentage, 2)
  else:
    percentage="percentage not found"
  return percentage

student_results=[]
for i in range(1,40):
    college_roll = f"{i:03d}"
    i_th_url = url_maker("22","101",college_roll,'4', "REGULAR", "Master of Science in Mathematics")
    # Make a request
    page = requests.get(i_th_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # print the result
    text=soup.get_text()
    if "Registration Number Not Found" in text:
        continue
        print("RESULT NOT FOUND")
    #Using only useful information and deleting rest  
    start_text_index=text.find('Roll')
    end_text_index=text.find('Note')
    end_word='Note'

    # Adjust indices to include the starting and ending words
    start_text_index = max(0, start_text_index)  # Avoid negative index
    end_text_index += len(end_word)  # Include the ending word itself

    text=text[start_text_index:end_text_index]
    
    #Searching for name
    start_text_index=text.find('(SHRI/SMT./KU.)')
    end_text_index=text.find('F/H Name')

    if start_text_index == -1 or end_text_index == -1:
      name='No words found'  # Words not found
    
    name=text[start_text_index+18:end_text_index].split("\n")[0]

    #Result status
    isPass=text.find("PASS")
    isATKT=text.find("ATKT")

    #Pass_Status
    if isPass!=-1:
      pass_status="PASS"
    if isATKT!=-1:
      pass_status="ATKT"
    
    index_of_percentage=text.find("PERCENTAGE")
    percentage=text[index_of_percentage+10:index_of_percentage+14]
    #NOW SEARCH FOR PERCENTAGE
    overall_percentage=str(percentage)+"%" if percentage!='er\n ' else 'Sem II Result awaited'
    sem_percentage=percentage_finder(text)
    result=[name,pass_status,sem_percentage,overall_percentage]  
    print(result)
    student_results.append(result)

#print(student_results)
for row in student_results:
    ws.append(row)
workbook.save('A:\MY-PROJECTS\MScSemIVResult.xlsx')