from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import json

# First we are setting up the databases that we will need to be using later
# This is basically copied and paisted from Homework #8

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCategoriesTable(data, cur, conn):
    category_list = []
    for business in data['businesses']:
        business_categories = business['categories']
        for category in business_categories:
            if category['title'] not in category_list:
                category_list.append(category['title'])

    cur.execute("DROP TABLE IF EXISTS Categories")
    cur.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(category_list)):
        cur.execute("INSERT INTO Categories (id,title) VALUES (?,?)",(i,category_list[i]))
    conn.commit()


# This section pulls data from the espn websight on attendance data
def get_nfl(year):
    url = 'http://www.espn.com/nfl/attendance/_/year/' + str(year)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    l = []
    for i in soup.find_all('tr'):
        l.append(i.text.strip().split('\n'))
    return l

def get_mlb(year):
    url = 'http://www.espn.com/mlb/attendance/_/year/' + str(year)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    l = []
    #appending headers
    l.append(['RK','TEAM','GMS','TOTAL','AVG','PCT'])
    for i in soup.find_all('tr'):
        team = []
        text = i.text
        try:
            #rank
            team.append(re.findall(r'\b([1-9](|[0-9]))\D', text)[0][0])
            #name
            team.append(re.findall(r'\d([\D]+)\d{3}', text)[0].strip())
            #games
            team.append(re.findall(r'(\b|\w)(([78][0-9]))', text)[0][1])
            #total
            team.append(re.findall(r'\d{2}((?:\d\,)?\d{3}\,\d{3})', text)[0])
            #average
            team.append(re.findall(r'(\d{2}\,\d{3})\d{1,3}\.', text)[0])
            #pct
            team.append(re.findall(r'\d{2}\,\d{3}(\d{1,3}\.\d)', text)[0])
        except:
            continue
        l.append(team)
    return l

def get_nba(year):
    url = 'http://www.espn.com/nba/attendance/_/year/' + str(year)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    l = []
    line_counter = 0
    head = ['RK','TEAM','GMS','TOTAL','AVG','PCT']
    l.append(head)
    team = []
    for i in soup.find_all('td'):
        if line_counter > 15 and line_counter < 424:
            if (line_counter-16)%12 == 0:
                team = []
                team.append(i.text)
            if (line_counter-16)%12 == 1:
                team.append(i.text)
            if (line_counter-16)%12 == 2:
                team.append(i.text)
            if (line_counter-16)%12 == 3:
                team.append(i.text)
            if (line_counter-16)%12 == 4:
                team.append(i.text)
            if (line_counter-16)%12 == 5:
                team.append(i.text)
                l.append(team)
        line_counter+=1
    return l

def get_nhl(year):
    url = 'http://www.espn.com/nhl/attendance/_/year/' + str(year)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    l = []
    l.append(['RK','TEAM','GMS','TOTAL','AVG','PCT'])
    for i in soup.find_all('tr'):
        team = []
        text = i.text
        try:
            #rank
            team.append(re.findall(r'\b([1-9][0-9]?)\D', text)[0])
            #name
            team.append(re.findall(r'\d([\D]+)\d{3}', text)[0].strip())
            #games
            team.append(re.findall(r'[3,4][0,1]', text)[0])
            #total
            team.append(re.findall(r'\d{2}((?:\d\,)?\d{3}\,\d{3})', text)[0])
            #average
            team.append(re.findall(r'(\d{2}\,\d{3})', text)[1])
            #pct
            team.append(re.findall(r'\d{2}\,\d{3}\d{2}\,\d{3}(.+)[3-4][0-1]', text)[0])
        except:
            continue
        l.append(team)
    return l

# for i in range(1,20):
#     year = 2000+i
#     if len(get_nhl(year)) == 31:
#         print('okay')
#     else:
#         print(year)

print(get_nhl(2019))
    
