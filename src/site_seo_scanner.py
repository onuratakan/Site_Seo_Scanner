import requests

from bs4 import BeautifulSoup

from collections import Counter
from string import punctuation

from fpdf import FPDF

class result:
    def __init__(self,title, canonical, hs, words, images, links):
        self.title = title
        self.canonical = canonical
        self.hs = hs
        self.words = words
        self.images = images      
        self.links = links

    def print_result(self):
        print(f"*** {self.title} ***")
        print()
        print(f"Canonical: {self.canonical}")
        print()
        print("H Numbers:")
        for h in self.hs:
            print(f"{h[0]} * {h[1]}")
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

    def export_pdf(self):

        pdf = FPDF()
        
        pdf.add_page()
        
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 10, txt = f"*** {self.title} ***", 
                ln = 1, align = 'C')     
        pdf.cell(200, 10, txt = f"Canonical: {self.canonical}", 
                ln = 1, align = 'C')
        pdf.cell(200, 10, txt = f"H Numbers:", 
                ln = 1, align = 'C')
        for h in self.hs:
            pdf.cell(100, 10, txt = f"{h[0]} * {h[1]}", 
                ln = 1, align = 'C')
        pdf.cell(200, 10, txt = "Words: ", 
                ln = 1, align = 'C')
        for word in self.words:
            pdf.cell(100, 10, txt = f"- {word[0]} * {word[1]}", 
                ln = 1, align = 'C')            

        pdf.cell(200, 10, txt = "Images: ", 
                ln = 1, align = 'C')        
        for image in self.images:
            try:
                pdf.cell(100, 10, txt = f"- {image[0]} * {image[1]}", 
                    ln = 1, align = 'C')                  
            except:
                pdf.cell(100, 10, txt = f"- {image[0]}", 
                    ln = 1, align = 'C')                   
        pdf.cell(200, 10, txt = "Links: ", 
                ln = 1, align = 'C') 
        print("Links: ")
        for link in self.links:
            pdf.cell(100, 10, txt = f"- {link}", 
                ln = 1, align = 'C')


    
        pdf.output(f"export/pdf/{self.title}seo_analysis.pdf")

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
            self.hs(source),
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
         
    
    def hs(self, source):
        the_list = []
        for i in range(1, 7, 1):
            the_list.append(
                (f"H{i}", len(source.find_all(f"h{i}")))
                )
        return the_list
    

    def print_results(self):
        for result in self.results:
            result.print_result()

    def export_pdf_results(self):
        for result in self.results:
            result.export_pdf()
