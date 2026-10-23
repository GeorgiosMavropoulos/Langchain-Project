from ..web_search_mod.web_search import WebSearch
from langchain_core.runnables import RunnableLambda
web_search = WebSearch()
NUM_SEARCH_RESULTS_PER_QUERY = 3

search_result_urls_chain = (
    RunnableLambda(lambda x: 
        [
            {
                'result_url': url, 
                'search_query': x['search_query'],
                'user_question': x['user_question']
            }
            for url in web_search.web_search(query=x['search_query'], max_results=NUM_SEARCH_RESULTS_PER_QUERY)
                
                
        ]
    )
)