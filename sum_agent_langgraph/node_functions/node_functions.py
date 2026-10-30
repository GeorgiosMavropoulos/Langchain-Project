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
#initialize an object of prompt templates
prompt_temps = Prompt_Temps()
llm_client = LLM()

import json
#helper method to parse info into json format
def _parse_assistant_info(content:str)->str:
     return json.loads(content)


#helper method to parse web queries into json format
def _parse_web_queries(queries:str)->str:
    return json.loads(queries)


#helper method to parse summary into json format
def _parse_summary(summary:str)->str:
    return json.loads(summary)

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


    def generate_summary(state:dict)->dict:
      """Generate summary based on the given text"""

      #generated queries
      generated_text= state['search_result_text'] 
      user_question = state['search_query']

      prompt= prompt_temps.SUMMARY_PROMPT_TEMPLATE.format(text = generated_text['search_result_text'],
                                                          user_question= user_question
                                                          )

      #get LLMs response
      respone = llm_client.get_llm().invoke(prompt)

      #parse LLM's response
      summary = _parse_summary(respone.content)

      return {"summary":summary}