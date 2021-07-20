import requests

from bs4 import BeautifulSoup

from collections import Counter
from string import punctuation


class result:
    def __init__(self,title, canonical, h1, h2, h3, h4, h5, h6, words, images, links):
        self.title = title
        self.canonical = canonical
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5
        self.h6 = h6
        self.words = words
        self.images = images      
        self.links = links

    def print_result(self):
        print(f"*** {self.title} ***")
        print()
        print(f"Canonical: {self.canonical}")
        print()
        print("H Numbers:")
        print(f"- H1 {self.h1}")
        print(f"- H2 {self.h2}")
        print(f"- H3 {self.h3}")
        print(f"- H4 {self.h4}")
        print(f"- H5 {self.h5}")
        print(f"- H6 {self.h6}")
        print()
        print("Words: ")
        for word in self.words:
            print(f"- {word[0]} * {word[1]}")
        print()
        print("Images: ")
        for image in self.images:
            try:
                print(f"- {image[0]} * {image[1]}")
            except:
                print(f"- {image[0]}")
        print()
        print("Links: ")
        for link in self.links:
            print(f"- {link}")

class site_seo_scanner:
    def __init__(self, domain, https = False, sitemap = False):
        if https:
            self.url = f"https://{domain}/"
        else:
            self.url = f"http://{domain}/"
        

        # Robots.txt
        self.robotsource = BeautifulSoup(requests.get(f"{self.url}robots.txt").content, 'html.parser').get_text()

        if sitemap:
            self.sitemapsoup = BeautifulSoup(requests.get(f"{self.url}sitemap.xml").content, 'lxml')
            self.sitemapurls = self.sitemapsoup.find_all("loc")

        self.results = []


        self.sitemap = sitemap

        self.start()


    
    def start(self):
        if self.sitemap:
            if not len(self.sitemapurls) == 0:
                for sitemapurl in self.sitemapurls:
                    self.scan(sitemapurl.text)
        else:
            self.scan(self.url)


    def scan(self, url):
        source = BeautifulSoup(requests.get(url).text, 'html.parser')

        the_result = result(
            self.title(source),
            self.canonical(source),
            self.h1(source),
            self.h2(source),
            self.h3(source),
            self.h4(source),
            self.h5(source),
            self.h6(source),
            self.words(source),
            self.images(source),
            self.links(source),
        )
        self.results.append(the_result)
    
    def title(self, source):
        for titles in source.find_all('title'):
            return titles.get_text()        

    def links(self, source):
        return [ x.get('href') for x in source.findAll('a') ]
    
    def canonical(self, source):
        try:
            return source.find('link', {'rel': 'canonical'})['href']   
        except:
            return "Non-canonical"
    
    def words(self, source):
        wordsfinder = (''.join(s.findAll(text=True))for s in source.findAll('p'))
        return Counter(
                (x.rstrip(punctuation).lower() for y in wordsfinder for x in y.split())
                ).most_common()

    
    def images(self, source):
        imagesfinder = source.find_all('img')
        imagelist = []
        for images in imagesfinder:
                try:
                    foundedalts = images['alt']
                except:
                    foundedalts = "Alt missing"            
                try:
                    foundedimages = images['src']
                except:
                    foundedimages = images['src'], "Don't have image"
                    
                images = (foundedalts, foundedimages)
                imagelist.append(images)
        return imagelist   
         
    
    def h1(self, source):
        return len(source.find_all('h1'))
    
    def h2(self, source):
        return len(source.find_all('h2'))    
    
    def h3(self, source):
        return len(source.find_all('h3'))      
    
    def h4(self, source):
        return len(source.find_all('h4'))     
    
    def h5(self, source):
        return len(source.find_all('h5'))  
 
    def h6(self, source):
        return len(source.find_all('h6'))

    def print_results(self):
        for result in self.results:
            result.print_result()
    



the_site_seo_scanner = site_seo_scanner("decentra-network.github.io/Decentra-Network", True)
the_site_seo_scanner.print_results()
