#https://ieeexplore.ieee.org/xpl/conhome/9187508/proceeding?isnumber=9196508&pageNumber=6
#ICRA 2020 = 9187508 , isnumber = 9196508


##['conference name', 'year','paper name','link to paper',[('authornamte,'authorlink')],citation count]
#['conference name', 'publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link', ... author name/link]
#out to a csv file


import os
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

options = Options()
options.page_load_strategy = 'normal'

def rendering(url):
        # change '/usr/local/bin/chromedriver' to the path from you got when you ran 'which chromedriver'
        driver = webdriver.Chrome(options=options)
        driver.get(url)                                          # load the web page from the URL
        time.sleep(3)                                            # wait for the web page to load
        render = driver.page_source                              # get the page source HTML
        driver.quit()                                            # quit ChromeDriver
        return render                                            # return the page source HTML



URL = "https://ieeexplore.ieee.org/xpl/conhome/9541544/proceeding"

firstpage = rendering(URL)
firstsoup = BeautifulSoup(firstpage, "html.parser")

#change to more specific?
conference = firstsoup.find("strong")
print(conference.text)
outfile = conference.text+'.csv'
print(outfile)

#out = soup.find(id = "LayoutWrapper")
#results = out_soup.find_all('div _ngcontent-ruk-c254="" xpl-displayer="" class="col"')
#print(results.prettify())
with open(outfile, 'w') as f:
    f.write("'conference name','publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link','... remaining authors name and link\n'")

    page = rendering(URL)
    print(URL)
    soup = BeautifulSoup(page, "html.parser")
    #print(soup.prettify())

    out_soup= soup.find("xpl-root")
    #print(out_soup.prettify())


    results = out_soup.find_all('div', class_="List-results-items")

    for result in results:
        #write conference name
        f.write("'"+conference.text[5:]+"',")
         #write conference year
        f.write("'"+conference.text[:4]+"',")
        #write paper title
        name = result.find('a')
        f.write('"'+name.text+'",')
        #get link to paper
        f.write("'"+"https://ieeexplore.ieee.org"+name["href"]+"',")
        #get amnt of citations
        cited = result.find('div',class_="description text-base-md-lh")
        cites = cited.find('a')
        if cites:
            s = cites.text
            f.write("'"+s[s.find('(')+1:s.find(')')]+"',")
        else:
            f.write("'0',")

        authors_list = []
        authors_links = []
        authors = result.find('p',class_="author text-base-md-lh")
        if authors:
            authorsinfo = authors.find_all('a')
            for author in authorsinfo:
                authorname = ("'"+author.text+"'")
    #            print(authorname)
                authors_list.append(authorname)
                authorlink = ("'"+"https://ieeexplore.ieee.org"+author["href"]+"'")
                authors_links.append(authorlink)
    #get first author name
    #get first author link
    #get last name and link
    #get the rest
            #write first author
            f.write(authors_list[0])
            f.write(","+authors_links[0])
    #        print(authors_list)
     #       print(authors_links
            #write last author
            if len(authors_list)>1:
                f.write(","+authors_list[-1])
                f.write(","+authors_links[-1])
            #write remaining authors
            i = 1
            while i<len(authors_list)-1:
                f.write(","+authors_list[i])
                f.write(","+authors_links[i])
                i+=1
        f.write('\n')
#col= out.find("div", class_="ng2-app")
#inside = out.find("xpl-root")


#for ins in inside:
 #   print("test")
  #  print(ins, end="\n"*2)




