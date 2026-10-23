"""This file contains the websearch chain. To be able to pass into the chain an executable function I use the RunnableLambda expression"""
from ..prompts.prompt_template import Prompt_Temps
from ..llm.llm_instance import LLM
from ..utilities.utilities import to_obj
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

prompt_templates = Prompt_Temps()
llm_client = LLM()



NUM_SEARCH_QUERIES = 2

web_query_chain = (RunnableLambda(lambda x:{

    'assistant_instructions': x['assistant_instructions'],
     'num_search_queries': NUM_SEARCH_QUERIES,
     'user_question':x['user_question']
})
| prompt_templates.WEB_SEARCH_PROMPT_TEMPLATE | llm_client.get_llm() | StrOutputParser() | to_obj 
)


##invoke the chain for testing
assistant_instrction_dict = {
    "assistant_type": "Tour guide assistant",
    "assistant_instructions": (
        "You are a world-travelled AI tour guide assistant. "
        "Your main purpose is to draft engaging, insightful, unbiased, "
        "and well-structured travel reports on given locations, "
        "including history, attractions, and cultural insights."
    ),
    "user_question": (
        "What can I see and do in the Spanish town of Astorga?"
    )
}

web_query_results = web_query_chain.invoke(assistant_instrction_dict) #execute the web query
print(web_query_results)

