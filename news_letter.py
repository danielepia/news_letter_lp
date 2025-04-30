from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set your OpenAI API Key
import os

newsletter_prompt = PromptTemplate(
    input_variables=["initial_thoughts", "question1", "answer1", "question2", "answer2", "question3", "answer3"],
    template="""
You are helping to write a newsletter based on the following information:

Initial Thoughts:
{initial_thoughts}

Deepening Questions and Answers:
1. Question: {question1}
   Answer: {answer1}

2. Question: {question2}
   Answer: {answer2}

3. Question: {question3}
   Answer: {answer3}

Task:
Using the initial thoughts and the expanded answers, write a well-structured, engaging newsletter.

Important:
- Notice the news letter is about a catholic mom that wants to deepen her faith and share her thoughts with other moms that may be in a similar position.
- Make sure it is between 300–500 words long.

Requirements:
- Start with a short, engaging introduction that sets the tone.
- Expand on the initial idea using the answers to the questions.
- Ensure the newsletter flows logically and maintains a conversational, approachable tone.
- Reference a catholic Saint that relates to what writer is sharing
- Conclude with a thoughtful takeaway or call to action for the readers.


Write it in a way that feels personal and insightful, as if the writer is sharing their authentic thoughts with their audience.
"""
)


def generate_news_letter(raw_data,openai_api_key=None):
    formatted_data = {
    "initial_thoughts": raw_data["initial_thoughts"],
    "question1": raw_data["question 1"],
    "answer1": raw_data["answer 1"],
    "question2": raw_data["question 2"],
    "answer2": raw_data["answer 2"],
    "question3": raw_data["question 3"],
    "answer3": raw_data["answer 3"],
}



    # Load the LLM
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

    final_prompt = newsletter_prompt.format(**formatted_data)

    # Create the chain with the PromptTemplate, not a string
    chain = LLMChain(llm=llm, prompt=newsletter_prompt)

    # Run the chain with formatted inputs
    result = chain.run(formatted_data)
    return result

