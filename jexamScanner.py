from bs4 import BeautifulSoup
import json
import os
import dryscrape
from time import sleep

'the website we gonne observe'
url = "https://jexam.inf.tu-dresden.de/"
'current working dir'
location = os.getcwd()


def get_website_dryscrape():
    try:
        dryscrape.start_xvfb()
        session = dryscrape.Session()
        sleep(3)
        session.visit(url)
        sleep(3)
        response = session.body()
        soup = BeautifulSoup(response, "html.parser").find("div", {"id":"news-wrapper"}).find("ul")
        liste = []
        for i in soup.findAll("li"):
            exam = str(i).replace("<li>", "").replace("</li>", "").split("(")[0]
            if len(exam) > 10:
                if not "\\" in exam:
                    liste.append(exam)
        return liste
    except:
        return []
   
'''get all old exams out of json file'''
def file_handler():
    list = []
    with open('{}/database/klausuren.json'.format(location)) as file:
        for i in file:
            list.append(i)
    return list

'''
    compare both files
    find out which files are new
'''
def compare_files(old_exams, new_exams):
    updates = []
    for i in new_exams:
        if i not in old_exams and len(i)> 3:
            updates.append(i)
    return updates



'''write all new exams to file'''
def write_all_exams_to_json(list):
    if len(list) > 0:
        with open('{}/database/klausuren.json'.format(location), 'w', encoding='utf-8') as file:
            json.dump(list, file, ensure_ascii=False, indent=4)



'''organizes all, first get the old and new data, compare it and send all new exams to the webhook'''
def generate_data():
    old = file_handler()
    write_all_exams_to_json(get_website_dryscrape())
    temp = file_handler()
    return compare_files(old, temp)
