#https://ieeexplore.ieee.org/xpl/conhome/9187508/proceeding?isnumber=9196508&pageNumber=6
#ICRA 2020 = 9187508 , isnumber = 9196508


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
        time.sleep(5)                                            # wait for the web page to load
        render = driver.page_source                              # get the page source HTML
        driver.quit()                                            # quit ChromeDriver
        return render                                            # return the page source HTML



#yr_issue:#isnumber,
conferences = {"2019_1":8511008,#26
               "2019_2":8581687,#276
               "2019_3":8668830,#116
               "2019_4":8764082,#197
               "2020_1":8897054,#40
               "2020_2":8932682,#449
               "2020_3":9059055,#164
               "2020_4":9133350,#260
               "2021_1":9223766,#39
               "2021_2":9285111,#511
               "2021_3":9399748,#248
               "2021_4":9475905}#338
                                #2664  total
URL = "https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber={}&punumber=7083369&sortType=vol-only-seq&rowsPerPage=100&pageNumber={}"
outfile = 'IEEE Robotics and Automation Letters 2019-2021 test.csv'

with open(outfile, 'w') as f:
    f.write("'conference name','publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link','... remaining authors name and link\n'")

    for name, val in conferences.items():

        pagenum = 1
        firstpage = rendering(URL.format(val,pagenum))
        firstsoup = BeautifulSoup(firstpage, "html.parser")



        firstout_soup= firstsoup.find("xpl-root")
        conference = firstout_soup.find("h1")
        print(name)
        while pagenum<=6:
            #get page
            page = rendering(URL.format(val,pagenum))
            print(URL.format(val,pagenum))
            soup = BeautifulSoup(page, "html.parser")

            out_soup= soup.find("xpl-root")
            results = out_soup.find_all('div', class_="List-results-items")

            for result in results:
                #write conference name
                f.write("'"+conference.text+"',")
                #write conference year
                cited = result.find('div',class_="description text-base-md-lh")
                year = cited.find('span')
                f.write("'"+year.text[-4:]+"',")
                #write paper title
                name = result.find('a')
                f.write('"'+name.text+'",')
                #write link to paper
                f.write("'"+"https://ieeexplore.ieee.org"+name["href"]+"',")
                #write amnt of citations
                cites = cited.find('a')
                if cites:
                    s = cites.text
                    f.write("'"+s[s.find('(')+1:s.find(')')]+"',")
                else:
                    f.write("'0',")
                #make lists w authors and links
                authors_list = []
                authors_links = []
                authors = result.find('p',class_="author text-base-md-lh")
                if authors:
                    authorsinfo = authors.find_all('a')
                    for author in authorsinfo:
                        authorname = ("'"+author.text+"'")
                        authors_list.append(authorname)
                        if author.has_attr('href'):
                            authorlink = ("'"+"https://ieeexplore.ieee.org"+author["href"]+"'")
                            authors_links.append(authorlink)
                    #write first author
                    f.write(authors_list[0])
                    if authors_links:
                        f.write(","+authors_links[0])
                    else:
                        f.write(",")
                    #write last author
                    if len(authors_list)>1:
                        f.write(","+authors_list[-1])
                        if authors_links:
                            f.write(","+authors_links[-1])
                        else:
                            f.write(",")
                    #write remaining authors
                    i = 1
                    while i<len(authors_list)-1:
                        f.write(","+authors_list[i])
                        if authors_links:
                            f.write(","+authors_links[i])
                        else:
                            f.write(",")
                        i+=1
                f.write('\n')
            pagenum += 1

