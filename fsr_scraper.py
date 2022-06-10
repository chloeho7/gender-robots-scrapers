#https://link.springer.com/book/10.1007/978-981-15-9460-1#toc
#['conference name', 'publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link', ... author name/link]
#out to a csv file

import os
import requests

from bs4 import BeautifulSoup

import json

URL = "https://link.springer.com/book/10.1007/978-981-15-9460-1?page={}&oscar-books=true#toc"
pagenum = 1

api_link = "https://api.semanticscholar.org/graph/v1/paper/{}?fields=citationCount"

api_author_link="https://api.semanticscholar.org/graph/v1/paper/{}/authors?fields=url"

outfile = 'fsr_2019.csv'

with open(outfile, 'w') as f:

    f.write("'conference name','publication year','paper name','link to paper','ciation count','first author name','first author link','last author name','last author link','... remaining authors name and link'\n")

    while pagenum <=2:

        #get page
        page = requests.get(URL.format(pagenum))
        soup = BeautifulSoup(page.content, "html.parser")

        #get confrence
        conf = soup.find('div',class_="c-book-evaluation-divider").contents[3].a.text
        #get year
        yr = soup.find_all('div',class_="c-book-evaluation-divider")[2].p.text[-48:-44]
        #get papers
        papers = soup.find_all('li',class_="c-card c-list-group__item c-card--flush u-pa-16")

        for paper in papers:

            #write conference name
            f.write('"'+conf+'",')
            #write year
            f.write('"'+yr+'",')
            #write paper title
            title = paper.h3.a
            if pagenum == 1:
                doi = title["href"][9:]
            else:
                doi = title["href"][-28:]
            link = ("https://link.springer.com/chapter/"+doi)
            f.write('"'+title.text+'",')#changed to "" bc commas cause issues
            #write paper link
            f.write("'"+link+"',")
            #use api with doi to find citation count
            #uncommment below line to temporarily leave citation count blank 
            #f.write(",")
            api_return = requests.get(api_link.format(doi))
            api_content = json.loads(api_return.content)

            cite_count = api_content["citationCount"]
            f.write("'"+str(cite_count)+"',")

            #get authors
            authors = paper.find('li',class_="c-author-list__item").text.split(",")

            #use paper link for authors if find et. al
            if any("et al." in author for author in authors):
                paper_page = requests.get(link)
                soup = BeautifulSoup(paper_page.content, "html.parser")
                new_authors_info = soup.find_all('li',class_="c-article-author-list__item")
                for i,author_info in enumerate(new_authors_info):
                    if i < len(authors)-1:
                        authors[i] = "'"+author_info.a.text+"'"
                    else:
                        authors.append("'"+author_info.a.text+"'")

            #use author api to get all author links 
            api_authors_return = requests.get(api_author_link.format(doi))
            api_authors_content = json.loads(api_authors_return.content)["data"]
            #put all author links in lists
            authors_links = []
            for author_info in api_authors_content:
                authors_links.append("'"+author_info["url"]+"'")

            #write first author
            f.write(authors[0])
            f.write(","+authors_links[0])
            #write last author
            if len(authors)>1:
                f.write(","+authors[-1])
                f.write(","+authors_links[-1])
            #write remaining authors
            i = 1
            while i<len(authors)-1:
                f.write(","+authors[i])
                f.write(","+authors_links[i])
                i+=1
            f.write('\n')
        pagenum += 1
