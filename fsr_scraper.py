#https://link.springer.com/book/10.1007/978-981-15-9460-1#toc
#['conference name', 'publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link', ... author name/link]
#out to a csv file

import os
import requests

from bs4 import BeautifulSoup

import json

def find_author(tag):
    return not tag.has_attr('class') and tag.has_attr('span')

URL = "https://link.springer.com/book/10.1007/978-981-15-9460-1?page={}&oscar-books=true#toc"
pagenum = 1

api_link = "https://api.semanticscholar.org/graph/v1/paper/{}?fields=citationCount"

outfile = '0910test.csv'

with open(outfile, 'w') as f:
    f.write("'conference name','publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link','... remaining authors name and link'\n")


#two pages
    while pagenum <=2:

        #get page
        print(URL.format(pagenum))
        page = requests.get(URL.format(pagenum))
        soup = BeautifulSoup(page.content, "html.parser")

        #get confrence

        #get papers

        for paper in papers:

            #write conference name
            f.write('"'+conference+'",')
            #write year
            #write paper title
            f.write("'"+title+"',")#maybe change if commas cause issues
            #write paper link
            f.write("'"+link+"',")

            #use api with doi to find citation count
            #doi = end of paper link
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
          #  authors = paper.cite.find_all('a')
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
            pagenum += 1
