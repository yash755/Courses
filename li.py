import requests
import re
import time
import pymysql.cursors
from bs4 import BeautifulSoup
import csv
import json


open_file = open('li.html','r')

html = BeautifulSoup(open_file, 'html.parser')

lis = html.find_all('li')

for li in lis:
    id = li.get('id')

    subject_name = li.text.strip()

    subject_str = subject_name.replace('-','')
    subject_str = subject_str.replace('&', '')
    subject_str = subject_str.replace('#', '')
    subject_str = subject_str.replace('+', '')
    subject_str = subject_str.replace(',', '')
    subject_str = subject_str.replace('/', '')
    subject_str = subject_str.lower()

    subject_str = subject_str.replace(' ','-')
    subject_str = subject_str.replace('.','-')

    subject_str = subject_str.replace('--', '-')
    subject_str = subject_str.replace('---', '-')



    if '-net' in subject_str:
        subject_str = subject_str.replace('-net','net')

    if '++' in subject_name:
        subject_url = 'https://www.testgorilla.com/test-library/job-role/' + str(subject_str) + '-tests-3'

    elif '#' in subject_name:
        subject_url = 'https://www.testgorilla.com/test-library/job-role/' + str(subject_str) + '-tests-2'
    else:
        subject_url = 'https://www.testgorilla.com/test-library/job-role/' + str(subject_str) + '-tests'


    id = id.split('-')

    id = id[len(id)-1]

    offset = 0



    while True:


        url = "https://www.testgorilla.com/wp-json/api/load_more"

        payload = "job_roles=" +  str(id) +"&offset=" + str(offset)
        print (payload)
        headers = {
            'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            'accept': "*/*",
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua-mobile': "?0",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'cache-control': "no-cache",
            'postman-token': "bb100494-bf71-2dca-0b36-bc3ccc9a568f"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        data = json.loads(response.text)

        if 'result' in data:
            data_html = data['result']
            if data_html == '':
                break

            else:

                data_html = BeautifulSoup(data_html, 'html.parser')

                cards = data_html.find_all('div',{'class':'mat-card'})

                for card in cards:

                    title = ''
                    desc = ''
                    time = ''
                    course_url = ''
                    course_card =''
                    hire = ''
                    skill_str = ''



                    try:
                        title = card.find('span',{'class':'mat-card-title'})
                        title = title.text.strip()

                    except:
                        print ("error")

                    try:
                        desc = card.find('div',{'class':'mat-card-text'})
                        desc = desc.text.strip()

                    except:
                        print ("error")

                    try:
                        time = card.find('div',{'class':'test-card__duration'})
                        time = time.text.strip()

                    except:
                        print ("error")

                    try:
                        buttons = card.find('div',{'class':'mat-card-buttons'})
                        a_tag = buttons.find('a')

                        course_url = a_tag.get('href')

                        print (course_url)

                        response1 = requests.request("GET", course_url, headers=headers)

                        course_html = BeautifulSoup(response1.content, 'html.parser')

                        try:
                            course_card = course_html.find('div',{'class':'tg-card'})
                            course_card = course_card.text.strip()
                            course_card = course_card.replace('Type','')
                            course_card = course_card.replace('\n', '')
                            print (course_card)

                        except:
                            print ("Error")


                        try:
                            hire = course_html.find('div',{'class':'tg-section tg-content'})
                            hire = hire.find('p')

                            hire = hire.text.strip()

                        except:
                            print ("pErro")


                        try:
                            skills = course_html.find('div',{'class':'tg-section test-skills'})
                            skills = skills.find_all('li')



                            for skill in skills:
                                skill_str = skill_str + skill.text.strip() + ','



                        except:
                            print ("pErro")

                    except:
                        print ("error")


                    arr = []
                    temp = []
                    temp.append(subject_url)
                    temp.append(subject_name)
                    temp.append(course_url)
                    temp.append(title)
                    temp.append(time)
                    temp.append(desc)

                    if skill_str == '':
                        temp.append('N/A')
                    else:
                        temp.append(skill_str)
                    temp.append(hire)
                    temp.append(course_card)

                    arr.append(temp)

                    with open('data2.csv', 'a+') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerows(arr)






                offset = offset + 20



print (len(lis))

