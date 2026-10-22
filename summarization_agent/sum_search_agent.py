from langchain_openai import ChatOpenAI
import openai
import os
from dotenv import load_dotenv
load_dotenv()
from .web_search_mod.web_search import WebSearch
from .web_scrap.web_scraper import WebScrapper
from .utilities.utilities import to_obj
from .prompts.prompt_template import Prompt_Temps
web_search = WebSearch()
prompt_templates = Prompt_Temps()
web_scrap = WebScrapper()
class SummarizationSearchAgent:
    def __init__(self):
        self.GEMINI_MODEL = os.getenv('GEMINI_MODEL')
        self.GEMINI_API_URL = os.getenv('GEMINI_API_URL')
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        self.NUM_SEARCH_QUERIES = 2
        self.NUM_SEARCH_RESULTS_PER_QUERY = 2
        self.RESULT_TEXT_MAX_CHARACTERS = 5000

        #initialize the model
        self.llm = ChatOpenAI(
            model=self.GEMINI_MODEL,
            base_url=self.GEMINI_API_URL,  
            api_key=self.GEMINI_API_KEY,      
            temperature=0.6,
        )

    #function to get user's answer
    def get_user_input(self):
        while True:
         try:
            question = str(input('Insert your question: ').strip())
            if not question:
                print(f'Please enter your question')
            else:
                return question
         except Exception as e:
            raise ValueError('Invalid input:{e}')
    
    

    #method to call the llm
    def call_the_agent(self):
         try:
             question = self.get_user_input() #call the method to get user's input
             #format the question with assistant's selection prompt so the model can choose which assistant's prompt to pick
             router_template_prompt = prompt_templates.ASSISTANT_SELECTION_PROMPT_TEMPLATE.invoke({"user_question": question})

             #send the prompt to the router model so it can pick the right assistant
             router_result = self.llm.invoke(router_template_prompt)
             print(router_result)

             #convert the assistant's json result into py dictionary
             formated_assistant_result = to_obj(router_result.content)
             assistant_instructions = formated_assistant_result.get("assistant_instructions", "You are a helpful research assistant.")
             
             #scrape the web with assistant's instructions
             search_prompt = prompt_templates.WEB_SEARCH_PROMPT_TEMPLATE.invoke({
                 "assistant_instructions": assistant_instructions,
                 "num_search_queries": self.NUM_SEARCH_QUERIES,
                 "user_question": question
             })

             #llm produce the query's list
             search_response = self.llm.invoke(search_prompt)
             #convert the response into python list
             queries_list = to_obj(search_response.content)

             if isinstance(queries_list, dict):
                 #if llm return a dict instead of a list I convert it to list
                 queries_list = queries_list.get("queries", [queries_list])

             final_reports = []
             #loop through queries list to extract each query
             for query in queries_list:
              query_text = query.get("search_query", question)

              #search the web for URLs for each query
              search_the_web_for_urls = web_search.web_search(query_text, self.NUM_SEARCH_RESULTS_PER_QUERY)
              print(search_the_web_for_urls)
              #iterate each url for the query the search_web method returned 
              for index, item in enumerate(search_the_web_for_urls, 1):
                 
                 #scrap the web with each query
                 scraped_text = web_scrap.web_scraping(item)
                 

                 #restrict characters based on the deadlock
                 scraped_text = scraped_text[:self.RESULT_TEXT_MAX_CHARACTERS]
                 
                 #fill summary's prompt
                 summary_prompt = prompt_templates.SUMMARY_PROMPT_TEMPLATE.invoke({
                     "search_result_text": scraped_text,
                     "search_query": query_text
                 })

                 #create the summary
                 summary_text = self.llm.invoke(summary_prompt)

                 #fill report's prompt
                 report_prompt = prompt_templates.RESEARCH_REPORT_PROMPT_TEMPLATE.invoke({"research_summary":summary_text.content,"user_question":question})
                 
                 #append report's response to the llm
                 report_response = self.llm.invoke(report_prompt)
                 #fill final reports list
                 final_reports.append(report_response.content)
                 #print report
                 for report in final_reports:
                     print(report)

         #handle rate limit errors
         except openai.RateLimitError:
            return f'You hit your token rate limit error.'
         #handle unsupported parameters
         except openai.BadRequestError as e:
             return f'Unsupported parameters'
         #handle authentication errors
         except openai.AuthenticationError:
             return f'Expired or wrong API KEYS'
         #handle network errors
         except openai.APIConnectionError:
             return f'Network errors'


sum_agent = SummarizationSearchAgent()

if __name__=='__main__':
 sum_agent.call_the_agent()
 
         

