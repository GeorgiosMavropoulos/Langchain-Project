"""This is the main entry point which calls the instructions assistant, the web search chain and summarization chain to create the workflow
Lastly but not least, the research prompt template will be used so as the model generates a coherent report like a real researcher
"""
from .summarization_chain import search_result_text_and_summary_chain
from .assistant_instructions_chain import assistant_instructions_chain
from .web_search_chain import web_query_chain
from .web_search import search_result_urls_chain
from ..llm.llm_instance import LLM
from ..prompts.prompt_template import Prompt_Temps
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

prompt_templates = Prompt_Temps()

llm_client = LLM()

# this functions searchs the web and fetches URLs, then searches those URLs to and scraps the text and finaly it creates a coherent summary.
#The map() function enables parallelism for each url to be searched and scrapped seperately
search_and_summarization_chain = (
    search_result_urls_chain 
    | search_result_text_and_summary_chain.map() # parallelize for each url
    | RunnableLambda(lambda x: 
        {
            """
             the Joined Summaries sub-chain is integrated directly within the larger Search and Summarization chain rather than as a separate entity
            """
            'summary': '\n'.join([i['summary'] for i in x]), 
            'user_question': x[0]['user_question'] if len(x) > 0 else ''
        })
)


#final research chain
research_chain = (
    assistant_instructions_chain| web_query_chain| search_and_summarization_chain.map() #summarize each url's content paraller
    | RunnableLambda(lambda x, **kwargs: {
        'research_summary': '\n\n'.join([i.get('summary', '') for i in x if isinstance(i, dict)]),
        'user_question': x[0].get('user_question', '') if len(x) > 0 and isinstance(x[0], dict) else ''
    })
        #use the reasearch prompt template to prompt the model to create a coherent PhD style report
    | prompt_templates.RESEARCH_REPORT_PROMPT_TEMPLATE | llm_client.get_llm() | StrOutputParser()

)

question = 'What can I see and do in the Spanish town of Astorga?'
web_research_report = research_chain.invoke(question)
print(web_research_report)

