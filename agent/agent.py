from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class Agent:
    def __init__(self):
     self.model = os.getenv('model')
     self.ollama_url = os.getenv('ollama_url')

     #initialize the model
     self.llm = ChatOpenAI(
        model=self.model,
        base_url=self.ollama_url,  
        api_key="ollama",      
        temperature=0.6,
    )
     
    def call_agent(self):
        #validate that the model is activate
        response = self.llm.invoke("Hello, who are you?")
        print(response.content)


agent = Agent()
if __name__ == '__main__':
   agent.call_agent()