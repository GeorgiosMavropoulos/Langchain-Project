"""This file contains the selection's instructions chain. It imports the assistant selection's template and the instance of the llm in order to create 
a chain where the output of the assistant's selection template becomes the input of the llm

"""
#import llm instance
from ..llm.llm_instance import LLM
#import assistant's prompt template
from ..prompts.prompt_template import Prompt_Temps
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from ..utilities.utilities import to_obj #import this method to parse the json output into python format

prompt_templates = Prompt_Temps()
call_llm = LLM()


#instanciate an object which feeds its output to llm's input
#RunnablePassthrough takes the output and passes it unchanged to the input of the model, while to_obj converts the json into a python dictionary.
#StrOutputParser extracts text from the LLM's content property
assistant_instructions_chain = ({'user_question': RunnablePassthrough()}
                                |prompt_templates.ASSISTANT_SELECTION_PROMPT_TEMPLATE|
                                 call_llm.get_llm()|StrOutputParser() | to_obj)

#test if chain works
question = 'What can I see and do in the Spanish town of Astorga?'

assistant_instructor = assistant_instructions_chain.invoke(question)
print(assistant_instructor)


