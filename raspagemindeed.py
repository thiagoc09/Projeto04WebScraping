from ast import keyword
from email import header
from unicodedata import name
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extracao(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    url = f'https://br.indeed.com/jobs?q=python&l=S%C3%A3o%20Paulo%2C%20SP&start=10={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transformar(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('a').text.strip()
        empresa = item.find('span', class_ = 'companyName').text.strip()
        loc = item.find('div', class_ = 'companyLocation').text.strip()
        try:
            salario = item.find('div', class_ = 'metadata salary-snippet-container').text.strip()
        except:
            salario = ''
        resumo = item.find('div', class_ = 'job-snippet').text.strip().replace('\n', '')

        job = {
            'vaga': title,
            'empresa': empresa,
            'localização': loc,
            'salário': salario,
            'requisitos': resumo,
        }
        joblist.append(job)
    return

joblist = []

for i in range(0,40,10):
    print(f'Página:  {i}')
    c = extracao(0)
    transformar(c)

df = pd.DataFrame(joblist)

print(df.head())

df.to_csv('Vagas.csv')



