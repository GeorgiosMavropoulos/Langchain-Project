"""This file contains the prompte templates this agent will use"""
from langchain_core.prompts import PromptTemplate

class PromptTemplates:
    def __init__(self):
        pass

    prompt_template = PromptTemplate.from_template(
"""
You are an expert mathematician who solve innovative mathematical formulas. 
You will receive a sequence and you have to define whether it's strange or not.
{Question:}
Examples:

Q: is the following sequence strange: 1, 4, 6, 8, 20

A: 1 is an odd number; I need at least two odd numbers // Not Strange

Q: is the following sequence strange: 5, 6, 7, 8, 20

A: 5 and 7 are odd numbers; the sum of 5 and 7 is 12; 12 is divisible by 3 // Strange

Q: is the following sequence strange: 1, 5, 6, 7, 8, 20

A: 1, 5 and 7 are odd numbers; the sum of 1, 5 and 7 is 13; 13 is not divisible by 3 // Not Strange

Q: is the following sequence strange: 5, 6, 7, 8, 9, 20

A: 5, 7, 9 are odd numbers; the sum of 5, 7 and 9 is 21; 21 is divisible by 3 // Strange


 
""")