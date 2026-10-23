"""This file contains a function which scraps the web page's text using the provided URL, generate's a summary of the scraped text and incorporates the source URL into the summary"""

from ..llm.llm_instance import LLM
from ..web_scrap.web_scraper import WebScrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from ..prompts.prompt_template import Prompt_Temps
from ..utilities.utilities import to_obj
prompt_templates = Prompt_Temps()
llm_client = LLM()
web_scrapper = WebScrapper()
RESULT_TEXT_MAX_CHARACTERS = 10000


# The following function retrieves the text from the given URL by using the web_scraping function
# Then it runs paraller the summarization process to summarize all given texts
# Finaly it passes the output (result url and text summary with user's questions to the lambda runner)
search_result_text_and_summary_chain = (
    RunnableLambda(lambda x, **kwargs:
        {
            'search_result_text': 
                web_scrapper.web_scraping(url=x['result_url'])[
                    :RESULT_TEXT_MAX_CHARACTERS],
            'result_url': x['result_url'], 
            'search_query': x['search_query'],
            'user_question': x['user_question']
        }
    )
    | RunnableParallel (
        {
            'text_summary': prompt_templates.SUMMARY_PROMPT_TEMPLATE 
               | llm_client.get_llm() | StrOutputParser(),
            'result_url': lambda x: x['result_url'],
            'user_question': lambda x: x['user_question']            
        }
    )
      | RunnableLambda(lambda x: 
        {
            'summary': 
               f"Source Url: {x['result_url']}\nSummary: {x['text_summary']}",              
            'user_question': x['user_question']
        }
    ) 
)


#test the function
# test chain invocation
#create a mocked url
result_url_str = '{"result_url":"https://citiesandattractions.com/spain/astorga-spain-uncovering-the-jewels-of-a-hidden-spanish-gem/",' \
'"search_query":"Astorga Spain attractions",' \
'"user_question": "What can I see and do in the Spanish town of Astorga?"}'
#convert the string to a dictionary
result_url_dict = to_obj(result_url_str)
#execute the function and delegate the response into a new variable

result_text = search_result_text_and_summary_chain.invoke(result_url_dict)
print(result_text)
