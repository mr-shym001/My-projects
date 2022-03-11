import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
Host='https://enbek.kz'
URL='https://enbek.kz/ru/search/vac?passwd%5B1%5D=1&passwd%5B2%5D=2&passwd%5B4%5D=4&passwd%5B5%5D=5&passwd%5B7%5D=7&agr=1&feed_name%5Brabota.nur.kz%5D=rabota.nur.kz&feed_name%5Bmarket.kz%5D=market.kz&feed_name%5Bzarplata.kz%5D=zarplata.kz&feed_name%5Bjumys.sitcen.kz%5D=jumys.sitcen.kz&feed_name%5Brabota.kz%5D=rabota.kz'
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
            address=element.find('li', class_='location d-flex align-items-center me-lg-3').get_text(strip=True)
        except:
            address='отсутствует'
        try:
            zarplata=element.find('div', class_='price').get_text(strip=True)
        except:
            zarplata='отсутствует'
        try:
            stavka=element.find('li', class_='time d-flex align-items-center me-lg-3').get_text(strip=True)
        except:
            stavka='отсутствует'
        try:
            opyt=element.find('li', class_='experience d-flex align-items-center').get_text(strip=True)
        except:
            opyt='отсутствует'
        try:
            obrazovanie=element.find('li', class_='education d-flex align-items-center').get_text(strip=True)
        except:
            obrazovanie='отсутствует'
        vakansialar.append({
            'Должность': element.find('div', class_='title').get_text(strip=True),
            'Зарплата': zarplata,
            'Компания': element.find('ul', class_='list-unstyled d-lg-flex').get_text(strip=True),
            'Адрес': address,
            'Ставка': stavka,
            'Опыт': opyt,
            'Дата': element.find('div', class_='right-content ms-auto').get_text(strip=True),
            'Образование': obrazovanie,
            'Ссылка на вакансию': Host + element.find('div', class_='title').find('a').get('href')
        
        })
    return vakansialar
def Filega_zhazu(elementter, path):
    with open (path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Должность','Зарплата','Компания','Адрес','Ставка','Опыт', 'Дата', 'Образование', 'Ссылка на вакансию'])
        for element in elementter:
            writer.writerow([element['Должность'], element['Зарплата'], element['Компания'], element['Адрес'], element['Ставка'], element['Опыт'], element['Дата'], element['Образование'], element['Ссылка на вакансию']])
def parse():
    html = html_alu(URL)
    if html.status_code == 200:
        vakansialar=[]
        better_sany = better_sanyn_alu(html.text)
        print(better_sany)
        for bet in range(1, better_sany + 1):
            print(f'{bet}-беттің деректері сәтті жиналды')
            html = html_alu(URL, params={'page': bet})
            vakansialar.extend(mazmun_alu(html.text))
        Filega_zhazu(vakansialar, 'Вакансия.csv')
        zhana_df=pd.read_csv('Вакансия.csv', delimiter=';')
        koshiru=pd.ExcelWriter('Вакансия.xlsx')
        zhana_df.to_excel(koshiru, index = None, header=True)
        koshiru.save()
        os.system("start EXCEL.EXE Вакансия.xlsx")
    else:
        print('!Қате')
parse()
