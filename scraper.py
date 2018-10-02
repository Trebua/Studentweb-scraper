from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import ast
import sys
import numpy as np
from collections import Counter

url = "https://idp.feide.no/simplesaml/module.php/feide/login.php?asLen=169&AuthState=_41e67986da33cb1be903b3796b1c61ba1118d6230c%3Ahttps%3A%2F%2Fidp.feide.no%2Fsimplesaml%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Ffsweb.no%252Fstudentweb%26cookieTime%3D1538497429"
my_username = "" #WRITE YOUR FEIDE-USERNAME HERE
my_password = "" #WRITE YOUR FEIDE-PASSWORD HERE
my_school = "NTNU" #WRITE YOUR SCHOOL NAME HERE
my_school_fullname = "norges teknisk-naturvitenskap" #WRITE THE FULL NAME OF YOUR SCHOOL HERE

driver = webdriver.Chrome()
driver.get(url)
ac = webdriver.ActionChains(driver)

#DEL 1 - Velg skole
schoolpath = "//input[@id='org_selector-selectized']"
driver.find_element_by_xpath(schoolpath).send_keys(my_school)
driver.find_element_by_xpath(schoolpath).send_keys(Keys.ENTER)


#DEL 2 - Logg inn på studentweb
loginpaths =  { 
    'username' : "//input[@id='username']",
    'password' : "//input[@id='password']",
}
driver.find_element_by_xpath(loginpaths['username']).send_keys(my_username)
password_field = driver.find_element_by_xpath(loginpaths['password'])
password_field.send_keys(my_password, Keys.ENTER)

#DEL 3 - Velge skole igjen!?  
element = driver.find_element_by_id("institusjonsvalg")
ac.move_to_element(element).click().perform()
ac.send_keys(my_school_fullname, Keys.ENTER)
ac.move_to_element(element).move_by_offset(70,0).click().perform()

#DEL 4 - Trykk logg inn med feide eeeeen gang til
driver.find_element_by_link_text('Log on using Feide').click()

#DEL 5 - Åpner karaktersiden
driver.get("https://fsweb.no/studentweb/resultater.jsf")

#DEL 6 - Hent karakterer
table = driver.find_element_by_id('resultatlisteForm:HeleResultater:resultaterPanel')
table_body = table.find_elements_by_tag_name("tbody")[0]

graded = table_body.find_elements_by_class_name("resultatTop")
passed = table_body.find_elements_by_class_name("none")
rows = graded + passed

def clean_emne(emne):
    list_ = emne.split("\n")
    return list_[0], list_[1]

def create_dict(rows):
    results = {}
    for row in rows:
        cols = row.find_elements_by_tag_name("td")
        emne_code, emne_name = clean_emne(cols[1].text)
        grade = cols[5].text
        results[emne_code] = [emne_name,grade]
    return results

def write_results_to_file(results, filename):
    with open(filename, 'w') as f:
        f.write(str(results))

def read_results_from_file(filename):
    with open(filename, 'r') as f:
        return ast.literal_eval(f.read())

def compare_results(prev, new):
    prev_keys = prev.keys()
    new_keys = new.keys()
    if len(new_keys) != len(prev_keys): #Hvis ny karakter har kommet
        diff = np.setdiff1d(list(new_keys),list(prev_keys))
        for key in diff:
            print(f"Fått karakter i {key} {new[key][0]}:{new[key][1]}")
    for key in prev: #Hvis en karakter er endret
        if prev[key][1] != new[key][1]:
            print(f"Endret karakter i {key} {prev[key][0]}: {new[key][1]}")
    print("Sammenligning ferdig")

new = create_dict(rows)
#read fra file først her egentlig
write_results_to_file(new, "previous_results.txt")
prev = read_results_from_file("test.txt")
compare_results(prev,new)




