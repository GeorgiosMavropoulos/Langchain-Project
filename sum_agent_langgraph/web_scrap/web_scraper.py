"""This file contains the webscrapper class which utilizes a method to parse html content from a website to exclude gibberish"""
import requests
from bs4 import BeautifulSoup

class WebScrapper:
    def __init__(self):
        pass

    def web_scraping(self,url:str)->str:
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0"
            }
            response = requests.get(url, headers=headers, timeout=15) #fetch the results, camouflage the headers and set a timeout limit
            #if response is ok parse the html and format the text
            if response.status_code == 200:
                soup = BeautifulSoup(response.text,'html.parser')
                page_text = soup.get_text(' ',strip=True)
                return page_text
            
            else:
            
                raise Exception(f"Scraping failed due to error: {response.status_code}")

                #catch exceptions
        except ValueError as e:
            return f'Invalid url characters:{e}'
        except Exception as e:
            print(e)
            return f"Could not retrieve the webpage: {e}"

