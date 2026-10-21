"""This file contains the prompte templates this agent will use"""
from langchain_core.prompts import PromptTemplate

class PromptTemplates:
    def __init__(self):
        pass

    prompt_template = PromptTemplate.from_template(
"""You are an experienced copywriter. You write only on capital letters. 
Write a {num_words} words summary of the following text, 
using a {tone} tone: {text}""")