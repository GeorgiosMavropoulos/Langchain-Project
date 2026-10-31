"""
Here I create the following type dict classes:
AssistantInfo:
This class contains the assistant type (e.g. researcher,websearch etc)
SearchQuery:
The query the agent generated and user's question

SearchResult:
The resulted urls
The query the agent executed to retrieve the URLs
user's question
is_fallback declare if the field comes from an alternative procedure


SearchSummary:
Text summarization
The URLs where the agent retrieved the text
User's question
is_fallback declare if the field comes from an alternative procedure

Research Report:
The generated Report

Research State:
This compines all the other classes and:
final_report: the final generated report
used_fallback_search: True or False if the agent fall back to re-search on the web
relevance_evaluation: was the retrieved URLs relevant?
should_regenerate_querie: should the agent retrieve text from the URLs?
iteration_count: how many times the agent iterate through this graph to generate the results
"""
from typing import List, Dict, Any, TypedDict, Optional


class AssistantInfo(TypedDict):  #1
    assistant_type: str
    assistant_instructions: str
    user_question: str

class SearchQuery(TypedDict):  #1
    search_query: str
    user_question: str

class SearchResult(TypedDict):  #1
    result_url: str
    search_query: str
    user_question: str
    is_fallback: Optional[bool]

class SearchSummary(TypedDict):  #1
    summary: str
    result_url: str
    user_question: str
    is_fallback: Optional[bool]

class ResearchReport(TypedDict):  #1
    report: str

class ResearchState(TypedDict):  #2
    user_question: str
    assistant_info: Optional[AssistantInfo]
    search_queries: Optional[List[SearchQuery]]
    search_results: Optional[List[SearchResult]]
    search_summaries: Optional[List[SearchSummary]]
    search_result_text: Optional[str]
    final_report: Optional[str]
    used_fallback_search: Optional[bool]
    relevance_evaluation: Optional[Dict[str, Any]]
    should_regenerate_queries: Optional[bool]
    iteration_count: Optional[int]