from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from prompt_templates.prompt_template import PromptTemplates
prompt_templates = PromptTemplates()
class Agent:
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

     #create prompt template's fromat
     self.prompt = prompt_templates.prompt_template.format(Question ='1,1,1')
     
    def call_agent(self):
        #validate that the model is activate
        response = self.llm.invoke(self.prompt)
        print(response.content)


agent = Agent()
if __name__ == '__main__':
   agent.call_agent()