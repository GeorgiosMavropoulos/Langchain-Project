"""This file contains the prompte templates this agent will use"""
from langchain_core.prompts import PromptTemplate

class PromptTemplates:
    def __init__(self):
        pass

    prompt_template = PromptTemplate.from_template(
"""
You are a text summarization engine with a strict word-count constraint.

TASK:
{Instruction}

INPUT TEXT:
{Question}

MANDATORY RULES:

Your output MUST contain exactly {num_words} words.

Treat the word count as a hard constraint, not an estimate.

Write the summary, then count every word separated by whitespace.

If the count is not exactly {num_words}, rewrite the summary until it is correct.

Do not include a title, preamble, explanation, quotation marks, or word count.

Output ONLY the final summary.

FINAL VALIDATION:
Before responding, verify that the summary contains exactly {num_words} whitespace-separated words. Never return a summary that fails this requiremen
    
""")