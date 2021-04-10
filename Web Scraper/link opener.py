import csv, pandas as pd, time, requests,re
from bs4 import BeautifulSoup

metacriticURL = 'https://www.metacritic.com'
data = pd.read_csv('mc_1995_2021.csv')
data['fullurl'] = metacriticURL + data['url']

def getItems(link):
    url = link
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Getting Genre from HTML
    genreListItems = soup.find_all('li', {"class":"summary_detail product_genre"})
    genre = genreListItems[0].find_all('span', {"class":"data"})
    #Getting Developer from HTML
    devlistItems = soup.find_all('li', {"class":"summary_detail developer"})
    developer = devlistItems[0].find_all('span', {"class":"data"})
    genres = [i.text for i in genre] #list comprehension to consolidate games with multiple genres
    #Getting Number of user ratings
    numberratings = soup.find_all('span', {"class":"count"})
    userRatings = numberratings[1].find_all('a')
    if  len(userRatings) > 0:
        userReviewsLink = userRatings[0].get("href")
        user_reviews = getMoreReviews(metacriticURL+ userReviewsLink,False)
    else:
        user_reviews = []
    #Getting url for critic reviews
    CriticRatings = numberratings[0].find_all('a') 
    if len(CriticRatings) > 0:
        criticReviewsLink = CriticRatings[0].get("href")
        critic_reviews = getMoreReviews(metacriticURL + criticReviewsLink)
    else:
        critic_reviews=[]
    
    return developer[0].text.strip(), genres, user_reviews, critic_reviews

def getMoreReviews(link,critic=True):
    url = link
    userAgent = {"User-agent": "Mozilla/5.0"}
    response = requests.get(url,headers = userAgent)
    soup = BeautifulSoup(response.text,"html.parser")
    if critic:
        reviewList = soup.find_all("ol",{"class":"reviews critic_reviews"})
        reviews = [t.text.replace("\n","").strip() for t in reviewList[0].find_all("div",{"class":"review_body"})]
    else:
        reviewList = soup.find_all("ol",{"class":"reviews user_reviews"})
        reviews = [t.text.replace("\n","").strip() for t in reviewList[0].find_all("span",{"class":"blurb blurb_expanded"})]
    return reviews

data['developer'] = ""
data['genre'] = ""
data["user_reviews"] = ""
data["critic_reviews"] = ""
index = 10000
while index < data.shape[0]: 
    print(index) #for troubleshooting
    try:
        data['developer'].loc[index] = (getItems(data['fullurl'][index])[0]) #looks at the row represented by (loc[index]) and sets that equal to the first output of the "getGenreDev" function
        data['genre'].loc[index] = (getItems(data['fullurl'][index])[1])
        data['user_reviews'].loc[index] = (getItems(data['fullurl'][index])[2])
        data['critic_reviews'].loc[index] = (getItems(data['fullurl'][index])[3])
    except:
        data['developer'].loc[index] = "No Data"
        data['genre'].loc[index] = "No Data"
        data['user_reviews'].loc[index] = "No Data"
        data['critic_reviews'].loc[index] = "No Data"
    index += 1
    time.sleep(3.25)    
data.to_csv('next_7000.csv')