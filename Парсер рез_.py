import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
Host = 'https://enbek.kz'
URL = 'https://enbek.kz/ru/search/res'
Takyryptar = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.4.837 Yowser/2.5 Safari/537.36',
           'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
def html_alu(url, params=None):
    z = requests.get(url, headers=Takyryptar, params=params)
    return z
def better_sanyn_alu(html):
    soup = BeautifulSoup(html, "html.parser")
    better_sany = soup.find_all('li', class_='page')
    if better_sany:
        return int(better_sany[-1].get_text())
    else:
        return 1
def mazmun_alu(html):
    soup=BeautifulSoup(html, "html.parser")
    elementter=soup.find_all('div', class_='item-list')
    vakansialar=[]
    for element in elementter:
        try:
            gorod=element.find('li', class_='location d-flex align-items-center').get_text(strip=True)
        except:
            gorod='не указано'
        try:
            zarplata=element.find('li', class_='price d-flex align-items-center').get_text(strip=True)
        except:
            zarplata='не указано'
        try:
            opyt=element.find('div', class_='stag mb-2').get_text(strip=True)
        except:
            opyt='отсутствует'
        try:
            obrazovanie=element.find('li', class_='education d-flex align-items-center').get_text(strip=True)
        except:
            obrazovanie='отсутствует'
        html2=html_alu(Host+element.find('div', class_='title').find('a').get('href'))
        if html2.status_code==200:
            soup2=BeautifulSoup(html2.text, 'html.parser')
            elementter2=soup2.find('div', class_='text').find_all('div', class_='d-lg-flex')
            for element2 in elementter2:
                element_d=element2.find('ul', class_='info column mb-3').find_all('li')
                try:
                    pv=element_d[2].find('span').get_text(strip=True).split()
                except:
                    pv='не указано'
                try:
                    usl=element_d[0].find('span').get_text(strip=True)
                except:
                    usl='не указано'
                try:
                    przd=element_d[1].find('span').get_text(strip=True)
                except:
                    przd='не указано'
        else:
            print('!Қате')
        vakansialar.append({
            'Должность': element.find('div', class_='title').get_text(strip=True),
            'Зарплата': zarplata,
            'Город/Район': gorod,
            'Опыт': opyt,
            'Образование': obrazovanie,
            'Пол': pv[0][0:-1],
            'Возраст': pv[1],
            'Условия': usl,
            'Переезд': przd,
            'Дата': element.find('div', class_='d-flex align-items-center mt-3').get_text(strip=True),
            'Ссылка на резюме': Host + element.find('div', class_='title').find('a').get('href')
        })
    return vakansialar
def Filega_zhazu(elementter, path):
    with open (path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Должность','Зарплата','Город/Район','Опыт','Образование','Пол','Возраст','Условия','Переезд','Дата','Ссылка на резюме'])
        for element in elementter:
            writer.writerow([element['Должность'],element['Зарплата'],element['Город/Район'],element['Опыт'],element['Образование'],element['Пол'],element['Возраст'],element['Условия'],element['Переезд'],element['Дата'],element['Ссылка на резюме']])
def parse():
    html = html_alu(URL)
    if html.status_code == 200:
        vakansialar=[]
        better_sany = better_sanyn_alu(html.text)
        for bet in range(1, better_sany+1):
            print(f'{bet}-беттің деректері сәтті жиналды')
            html = html_alu(URL, params={'page': bet})
            vakansialar.extend(mazmun_alu(html.text))
        Filega_zhazu(vakansialar, 'Резюме.csv')
        zhana_df=pd.read_csv('Резюме.csv', delimiter=';')
        koshiru=pd.ExcelWriter('Резюме_.xlsx')
        zhana_df.to_excel(koshiru, index = None, header=True)
        koshiru.save()
        os.system("start EXCEL.EXE Резюме_.xlsx")
    else:
        print('!Қате')
parse()
