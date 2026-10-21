from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from prompt_templates.prompt_template import PromptTemplates
prompt_templates = PromptTemplates()
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

     #create prompt template's fromat
     self.prompt = prompt_templates.prompt_template.format(Instruction='write a summary for the following text',num_words = 30,
                                                           
    Question ='ome PCs from the 1980s were iconic pioneers of personal computing. Computers like the Apple II, IBM PC, and Commodore 64 revolutionized how we lived and worked. They introduced us to word processing, gaming, and the possibilities of home computing. The graphical user interface, as seen in the Apple Macintosh, changed the way we interacted with machines. These PCs, though less powerful by today’s standards, ignited a digital revolution, shaping the technology landscape we know today. They hold a special place in history, symbolizing the dawn of a new era in computing that laid the foundation for the modern digital age.' 
    )
     
    def call_agent(self):
        #validate that the model is activate
        response = self.llm.invoke(self.prompt)
        print(response.content)


agent = Agent()
if __name__ == '__main__':
   agent.call_agent()