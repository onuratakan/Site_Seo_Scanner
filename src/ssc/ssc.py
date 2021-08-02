import requests

from bs4 import BeautifulSoup

from collections import Counter
from string import punctuation

from fpdf import FPDF

import argparse
import sys



class site_seo_scanner:

    def set_domain(self, domain):
        self.domain = domain
        self.results = []
    def get_domain(self):
        try:
            return self.domain
        except:
            raise("Please set domain")

    def set_https(self,https):
        self.https = https
    def get_https(self):
        try:
            return self.https
        except:
            raise("Please set https")


    def set_url(self):
        if self.get_https:
            self.url = f"https://{self.get_domain()}/"
        else:
            self.url = f"http://{self.get_domain()}/"        
    def get_url(self):
        try:
            return self.url
        except:
            self.set_url()
            return self.url

    def set_sitemap(self, sitemap):
        self.sitemap = sitemap
        if self.sitemap:
            self.sitemapsoup = BeautifulSoup(requests.get(f"{self.get_url()}sitemap.xml").content, 'lxml')
            self.sitemapurls = self.sitemapsoup.find_all("loc")
    def get_sitemap(self):
        try:
            return self.sitemap
        except expression as identifier:
            raise("Please set sitemap")



    
    def start(self):
        if self.get_sitemap():
            if not len(self.sitemapurls) == 0:
                for sitemapurl in self.sitemapurls:
                    self.scan(sitemapurl.text)
        else:
            self.scan(self.get_url())


    def scan(self, url):
        source = BeautifulSoup(requests.get(url).text, 'html.parser')

        the_result = self.result(
            self.get_domain(),
            self.title(source),
            self.canonical(source),
            self.hs(source),
            self.words(source),
            self.images(source),
            self.links(source),
            self.robotstxt(source),
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

    def robotstxt(self, source):
        return BeautifulSoup(
            requests.get(f"{self.get_url()}robots.txt").content, 'html.parser'
            ).get_text()
    

    def print_results(self):
        for result in self.results:
            result.print_result()

    def export_pdf_results(self, folder):
        for result in self.results:
            result.export_pdf(folder)


    class result:
        def __init__(self, domain, title, canonical, hs, words, images, links, robotstxt):
            self.domain = domain
            self.title = title
            self.canonical = canonical
            self.hs = hs
            self.words = words
            self.images = images      
            self.links = links
            self.robotstxt = robotstxt

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
            print()
            print("Robots Txt: ")
            print(self.robotstxt)

        def export_pdf(selfi, folder):

            pdf = FPDF('P', 'mm', 'A4')
            
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
            for link in self.links:
                pdf.cell(100, 10, txt = f"- {link}", 
                    ln = 1, align = 'C')
            pdf.cell(200, 10, txt = "Robots Txt: ", 
                    ln = 1, align = 'C') 
            pdf.cell(100, 10, txt = str(self.robotstxt), 
                    ln = 1, align = 'C')

            pdf.output(f"{folder}/{self.get_domain()}-seo_analysis.pdf")


    def arguments(self, arguments = None):
        parser = argparse.ArgumentParser()

        parser.add_argument('-d', '--domain', type=str, required=True,
                            help='Domain')

        parser.add_argument('-s', '--ssl', action='store_true',
                            help='HTTPS')
        
        parser.add_argument('-sm', '--sitemap', action='store_true',
                            help='Use site map')

        parser.add_argument('-p', '--pdf', type=str,
                            help='Export as pdf')


        if not arguments is None:
            args = parser.parse_args(arguments.split(" "))
        else:
            args = parser.parse_args()
        if len(sys.argv) < 2:
            parser.print_help()


        self.set_domain(args.domain)
        self.set_https(args.ssl)
        self.set_sitemap(args.sitemap)

        self.start()

        self.print_results()
        if not args.pdf is None:
            self.export_pdf_results(args.pdf)


SSC = site_seo_scanner()

if __name__ == "__main__":
    SSC.arguments()
