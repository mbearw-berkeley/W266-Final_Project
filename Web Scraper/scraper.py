import requests, csv, pandas as pd, pprint, time
from bs4 import BeautifulSoup
import lxml,html5lib

data_dict = {'name':[], 
'date':[],
'platform': [],
'score':[],
'summary':[],
'url':[],
'userscore':[]}


def numberPages(response): 
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find_all('li', {"class":"page last_page"})
    pagesCleaned = pages[0].find('a', {"class":"page_num"})
    return (pagesCleaned.text)

def scraper(num_loops,content):
    tblnum = 0
    while tblnum < num_loops:
        #get Game name
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td',{"class":"clamp-summary-wrap"})
            print(td)
            data_dict['name'].append(td[1].find_all("a",{"class":"title"})[0].text)
                

        #get Game release date
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for date in td[1].find_all('span',{"class":""}):
                data_dict['date'].append(date.text)
            

        #get platform
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for platform in td[1].find_all('span',{"class":"data"}):
                data_dict['platform'].append(platform.text.strip())
                

        #get Game score
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for user in td[0].find_all('div',{"class":"metascore_w"}):
                data_dict['score'].append(user.text.strip())
                
        #get Game Description
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all("td")
            for summary in td[1].find_all("div",{"class":"summary"}):
                data_dict["summary"].append(summary.text.strip())
                


        #getting game url
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for a in td[1].find_all('a', {"class":"title"} ,href=True):
                data_dict['url'].append(a['href'])
             

        #get Game userscore
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for score in td[1].find_all('div', {"class":"metascore_w"}):
                data_dict['userscore'].append(score.text)
                
        tblnum += 1

def pages(lastPageNum): 
    currentPage = 0
    while currentPage < int(lastPageNum):
        url = url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page='+str(currentPage)
        userAgent = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=userAgent)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find_all('table')

        num_loops = len(content)
        print(num_loops)
        scraper(num_loops,content)
        #print(data_dict)
        currentPage += 1
        print(currentPage)
        time.sleep(6)

def main():
    url = 'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered'
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    n_pages = numberPages(response)
    print("number of pages: "+ str(n_pages))
    pages(int(n_pages))

    xData = (pd.DataFrame.from_dict(data_dict))
    xData.to_csv('mc_full.csv')

main()