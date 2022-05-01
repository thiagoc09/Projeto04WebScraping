from ast import keyword
from email import header
from unicodedata import name
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime



def extracao(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    url = f'https://br.indeed.com/jobs?q=Python&l=S%C3%A3o%20Paulo%2C%20SP&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transformar(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        try:
            title = item.find('a').text.strip()
        except: 
            title =''    
        try:
            empresa = item.find('span', class_ = 'companyName').text.strip()
        except: 
            empresa =''    
        loc = item.find('div', class_ = 'companyLocation').text.strip()
        try:
            salario = item.find('div', class_ = 'metadata salary-snippet-container').text.strip()
        except:
            salario = ''
        try:
            resumo = item.find('div', class_ = 'job-snippet').text.strip().replace('\n', '')
        except: 
            resumo =''      
        
        try:
            dataPost = item.find('span', 'date').text
        except:
            dataPost = ''    
        try:
            hoje = datetime.today().strftime('%Y-%m-%d')
        except:
            hoje = ''    
        
        try:
            url_vaga = 'https://www.br.indeed.com' + item.h2.a.get('href')
        except:
            url_vaga = ''    
           
        
        job = {
            'vaga': title,
            'empresa': empresa,
            'localizacao': loc,
            'salario': salario,
            'dataPostagem':dataPost,
            'dataRaspagem':hoje,
            'requisitos': resumo,
            'job_url':url_vaga
        }
        joblist.append(job)
    return

joblist = []

for i in range(0,30,10):
    print(f'Vaga: {i} ')
    c = extracao(i)
    transformar(c)

df = pd.DataFrame(joblist)

print(df.head())


excel = input("Nome da planilha: ")
df.to_csv(excel+'.csv')

