"""This file contains the web search utility method"""
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from typing import List

class WebSearch:
    def __init__(self):
        pass
    #create the web search method
    def web_search(query:str, max_results:int)->list[str]:
        return [r["link"]  #return links
                #iterate through the results
            for r in DuckDuckGoSearchAPIWrapper().results(query,max_results)]


    #test the method 
    result = web_search(query="Who won the FIFA WORLD CUP OF 2026",max_results=1)
    print(result)
