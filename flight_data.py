from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time
import itertools
import os
import sys
import csv

def extract_flight_data(origin, destination):

    doj = "2020-01-06"
    carriers = 'AA,DL,UA'
    choice = np.random.randint(1,4)

    if choice ==1:
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')
        driver = webdriver.Chrome("chromedriver.exe")
    elif choice==2:
        driver = webdriver.Edge()
    else:
        ff_opt = webdriver.FirefoxOptions()
        ff_opt.add_argument('--log-level=3')
        driver = webdriver.Firefox()
    driver.implicitly_wait(50)
    url = 'https://www.kayak.com/flights/'+ origin +'-' + destination + '/'+ doj +'?fs=flexdepart=20200106;landing=0001,0107@0000;providers='+carriers+';airports='+origin+','+destination+';stops=0;baditin=baditin&sort=depart_a'
    driver.get(url)
    time.sleep(np.random.randint(5,10))
    close_popup = driver.find_elements_by_xpath("//button[contains(@aria-label, 'Close') and contains(@id, '-dialog-close') and contains(@class,'Button-No-Standard-Style') and contains(@class,'close')]")
    driver.implicitly_wait(20)
    for button in close_popup:
        if button.is_displayed():
            button.click()

    while True:
        try:
            loadMoreButton = driver.find_element_by_class_name("moreButton")
            time.sleep(np.random.randint(10,25))
            if loadMoreButton. loadMoreButton.is_displayed():
                loadMoreButton.click()
            else:
                break
        except Exception as e:
            # print(e)
            break
    time.sleep(np.random.randint(10,30))
    soup=BeautifulSoup(driver.page_source, 'lxml')

    deptimes = soup.find_all('span', attrs={'class': 'depart-time base-time'})
    arrtimes = soup.find_all('span', attrs={'class': 'arrival-time base-time'})
    meridies = soup.find_all('span', attrs={'class': 'time-meridiem meridiem'})
    aircrafts = soup.find_all('div', attrs={'class': 'planeDetails details-subheading'})
    airports = soup.find_all('div', attrs={'class': 'js-airport'})
    if len(airports) == 0:
        airports = soup.find_all('span', attrs={'class': 'js-airport'})
    carriers = []
    for airline in soup.find_all('span', attrs={'class': 'airlines'}):
        carriers += airline.find('span', attrs={'class': 'airline-label'})
    if len(carriers)<1:
        for airline in soup.find_all('div', attrs={'class': 'Flights-Results-LegInfo'}):
            carriers += airline.find('div', attrs={'class': 'bottom'})

    flight_from=[]
    flight_to=[]
    deptime = []
    for div in deptimes:
        deptime.append(div.getText()[:-1])    
            
    arrtime = []
    for div in arrtimes:
        arrtime.append(div.getText()[:-1])

    aircraft = []
    for craft in aircrafts:
        aircraft.append(craft.getText().strip('\n').strip(' '))
    
    airline = []
    for carrier in carriers:
        airline.append(carrier.strip('\n').strip(' '))

    meridiem_dep = []
    meridiem_arr = []
    for i in range(0,len(meridies),2):
        meridiem_dep.append(meridies[i].getText())  
        meridiem_arr.append(meridies[i+1].getText())
    for i in range(0,len(airports),2):
        flight_from.append(airports[i].getText().strip('\n'))
        flight_to.append(airports[i+1].getText().strip('\n'))
            
    # deptime = np.asarray(deptime)
    # arrtime = np.asarray(arrtime)
    # meridiem_dep = np.asarray(meridiem_dep)
    # meridiem_arr = np.asarray(meridiem_arr)

    # stri = 'From:'+origin+' | To:'+destination+ ' | flight_from: '+str(len(flight_from))+ ' | flight_to: '+str(len(flight_to))+ ' | deptime: '+str(len(deptime))+ ' | meridiem_dep: '+str(len(meridiem_dep))+ ' | arrtime: '+str(len(arrtime))+ ' | meridiem_arr: '+str(len(meridiem_arr))+ ' | aircraft: '+str(len(aircraft)) + str(len(soup))
    if len(flight_from)<1:
        flight_from = list([origin])
        flight_to = list([destination])
        deptime = list(['xx']) 
        meridiem_dep = list(['xx']) 
        arrtime = list(['xx'])
        meridiem_arr = list(['xx'])
        airline = list(['xx'])
        aircraft = list(['xx'])
        print(origin, destination)
    driver.close()
    return flight_from, flight_to, deptime, meridiem_dep, arrtime, meridiem_arr, airline, aircraft

def main():
    ff, ft, dt, md, at, ma, ac = [],[],[],[],[],[],[]
    initial_origin = "LAX"
    final_destination = "JFK"
    layover = ['SFO','SEA','PHX','DEN','ORD','ATL','IAD','BOS']

    # flights between LAX-JFK, no stops
    ff, ft, dt, md, at, ma, al, ac = extract_flight_data(initial_origin, final_destination)
    # flights from LAX to connecting airports
    for destination in layover:
        flight_from, flight_to, deptime, meridiem_dep, arrtime, meridiem_arr, airline, aircraft = extract_flight_data(initial_origin, destination)
        ff += (flight_from)
        ft += (flight_to)
        dt += (deptime)
        md += (meridiem_dep)
        at += (arrtime)
        ma += (meridiem_arr)
        al += airline
        ac += (aircraft)
    # flights form connecting airports to JFK
    for origin in layover:
        flight_from, flight_to, deptime, meridiem_dep, arrtime, meridiem_arr, airline, aircraft = extract_flight_data(origin, final_destination)
        ff += (flight_from)
        ft += (flight_to)
        dt += (deptime)
        md += (meridiem_dep)
        at += (arrtime)
        ma += (meridiem_arr)
        al += airline
        ac += (aircraft)
    # flights between connecting airports
    for origin,destination in list(itertools.permutations(layover, 2)):
        flight_from, flight_to, deptime, meridiem_dep, arrtime, meridiem_arr, airline, aircraft = extract_flight_data(origin, destination)
        ff += (flight_from)
        ft += (flight_to)
        dt += (deptime)
        md += (meridiem_dep)
        at += (arrtime)
        ma += (meridiem_arr)
        al += airline
        ac += (aircraft)
    
    print(len(at))
    rows = zip(ff,ft,dt,md,at,ma,al,ac)

    with open(os.path.join("flight_data"+str(np.random.randint(1,200000))+".csv"), mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["From","To","Departure","Meridian","Arrival","Meridian","Airlines","Aircraft"])
        for row in rows:
            csv_writer.writerow(row)

if __name__ == "__main__":
    main()
