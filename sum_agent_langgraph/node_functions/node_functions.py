"""This file contains the class with all the required nodes.
   The following nodes select the proper assistant,
   they generate web queries
   they perform web searches
   they summarize search results
   they evaluate search relevance
   and they compose the final report
"""
from ..prompts.prompt_template import Prompt_Temps
from ..llm.llm_instance import LLM
from ..web_scrap.web_scraper import WebScrapper
#initialize an object of prompt templates
prompt_temps = Prompt_Temps()
llm_client = LLM()
web_scrap = WebScrapper()

import json
#helper method to parse info into json format
def _parse_assistant_info(content:str)->str:
     return json.loads(content)


#helper method to parse web queries into json format
def _parse_web_queries(queries:str)->str:
    return json.loads(queries)



class Nodes:
    def __init__(self):
        pass


    def select_assistant(state: dict) -> dict:
        """Select the appropriate research assistant."""
        user_question = state["user_question"]

        # Use the LLM to select an assistant
        prompt = prompt_temps.ASSISTANT_SELECTION_PROMPT_TEMPLATE.format(
            user_question=user_question
        )
        response = llm_client.get_llm().invoke(prompt)

        #convert LLM's return content into json format
        assistant_info = _parse_assistant_info(
            response.content)  #1

        return {"assistant_info": assistant_info}  #2


    
    def generate_search_queries(state: dict) -> dict:
        """Generate search queries based on the question."""
        assistant_info = state["assistant_info"]
        user_question = state["user_question"]

        prompt = prompt_temps.WEB_SEARCH_PROMPT_TEMPLATE.format( #3
            assistant_instructions=assistant_info["assistant_instructions"],
            user_question=user_question,
            num_search_queries=3
        )
        response = llm_client.get_llm().invoke(prompt)

        search_queries = _parse_web_queries(
            response.content)  #4

        return {"search_queries": search_queries}  


    def scrap_web(state:dict)->dict:
        """Scrap the web to retrieve text"""
        queries = state['search_queries']

        scraped_text = web_scrap.web_scraping(queries)

        return {
        "search_result_text": scraped_text
    }

    

    def generate_summary(state:dict)->dict:
      """Generate summary based on the given text"""

      
      generated_text= state['search_result_text'] 
      user_question = state['user_question']

      prompt= prompt_temps.SUMMARY_PROMPT_TEMPLATE.format(text = generated_text,
                                                          user_question= user_question
                                                          )

      #get LLMs response
      response = llm_client.get_llm().invoke(prompt)


      return {"research_summary":response.content}


    def research_report(state:dict) -> dict:
        """Generate  report based on the given summary"""

        #summary
        summary = state['research_summary']
        user_question = state['user_question']

        #pass the prompt
        prompt = prompt_temps.RESEARCH_REPORT_PROMPT_TEMPLATE.format(research_summary =summary,user_question=user_question)

        #get LLM's response
        response = llm_client.get_llm().invoke(prompt)

        #return the report
        return {'report':response.content}