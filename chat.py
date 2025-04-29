from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import ast

# Set your OpenAI API Key
import os

openai_api_key = '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'


# Define the template for the chatbot
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are an expert content writing coach and editor. Your task is to help refine and deepen a newsletter draft.

I will provide you with:
- A description of my idea
- A draft of the newsletter

Your job:
- Analyze the idea and draft
- Ask me exactly 3 thoughtful, specific questions that will help me expand, clarify, or strengthen my topic

Important:
- Return ONLY the 3 questions inside a valid Python list data structure.
- Each question should be a string inside the list.

Example output:
[
    "First question?",
    "Second question?",
    "Third question?"
]

Here is my input:
{user_input}

Please provide the list of questions now.
"""
)

# Load the LLM
llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

# Create the chain
chatbot = LLMChain(llm=llm, prompt=prompt)


def get_questions(user_message):
    response = chatbot.run(user_input=user_message)
    return ast.literal_eval(response)

