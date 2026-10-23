"""This module instanciate the LLM model"""
from langchain_openai import ChatOpenAI
import openai
import os
from dotenv import load_dotenv
load_dotenv()

class LLM:
    def __init__(self):     
        self.GEMINI_MODEL = os.getenv('GEMINI_MODEL')
        self.GEMINI_API_URL = os.getenv('GEMINI_API_URL')
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        

        #initialize the model
        self.llm = ChatOpenAI(
            model=self.GEMINI_MODEL,
            base_url=self.GEMINI_API_URL,  
            api_key=self.GEMINI_API_KEY,      
            temperature=0.6,
        )

    def get_llm(self):
        return self.llm

 