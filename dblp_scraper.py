#['conference name', 'publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link', ... author name/link]
#out to a csv file

import os
import requests

from bs4 import BeautifulSoup

import json

def find_author(tag):
    return not tag.has_attr('class') and tag.has_attr('span')

                         #[name,year]
conferences = {'rss2021':["rss",2021],#93
               'rss2020':["rss",2020],#104
               'rss2019':["rss",2019],#85
               'isrr19':["isrr",2019],#62
               'iser20':["iser",2020],#56
               'corl21':["corl",2021],#167
               'corl20':["corl",2020],#166
               'corl19':["corl",2019]}#111
                                      #844 total (836 w just papers)


URL = "https://dblp.uni-trier.de/db/conf/{name}/{name}{year}.html"
#ex)"https://dblp.org/db/conf/rss/rss2021.html"

api_link = "https://api.semanticscholar.org/graph/v1/paper/{}?fields=citationCount"

outfile = '0908test.csv'

with open(outfile, 'w') as f:
    f.write("'conference name','publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link','... remaining authors name and link'\n")

    for val in conferences.values():

        #get page
        print(URL.format(name = val[0], year = val[1]))
        page = requests.get(URL.format(name = val[0], year = val[1]))
        soup = BeautifulSoup(page.content, "html.parser")

        #get confrence
        conf = soup.find('li',class_="entry editor")
        conference = conf.cite.find('span',class_="title").text
        print(conference)

        #get papers
        papers = soup.find_all('li',class_="entry inproceedings")

        for paper in papers:

            #write conference name
            f.write('"'+conference+'",')
            #write year
            f.write("'"+str(val[1])+"',")
            #write paper title
            title = paper.cite.find('span',class_="title").text
            f.write("'"+title+"',")#maybe change if commas cause issues
            #write paper link
            link = paper.nav.li.a["href"]
            f.write("'"+link+"',")

            #use api with doi to find citation count
            doi = link[16:]
            #temporarily leaving amnt of citations blank
    #        f.write(",")
            #commented out until more requests allowed
            api_return = requests.get(api_link.format(doi))
            api_content = json.loads(api_return.content)
            if("citationCount" in api_content):
                cite_count = json.loads(api_return.content)["citationCount"]
                f.write("'"+str(cite_count)+"',")
            else:
                f.write(",")
                print(link)
                print(api_return.content)


            #put all author info in lists
            authors_list = []
            authors_links = []
            authors = paper.cite.find_all('a')
            for author in authors:
                authors_list.append("'"+author.text+"'")
                authors_links.append("'"+author["href"]+"'")
            #write first author
            f.write(authors_list[0])
            f.write(","+authors_links[0])
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
