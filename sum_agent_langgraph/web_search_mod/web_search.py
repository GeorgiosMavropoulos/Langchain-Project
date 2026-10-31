"""This file contains the web search utility method"""
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from typing import List

class WebSearch:
    def __init__(self):
        self.search = DuckDuckGoSearchAPIWrapper()

    #create the web search method
    def web_search(self,query:List[str], max_results:int)->List[str]:
        all_links = []
        #loop through each query and return a list
        for q in query:
            results = self.search.results(q, max_results)

            for result in results:
                all_links.append(result["link"])

        return all_links


