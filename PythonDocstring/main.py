from langchain.llms import CTransformers
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Any, Dict, List, Union
import sys

model_id = 'TheBloke/Mistral-7B-codealpaca-lora-GGUF'
config = {'temperature':0.00,'context_length':8000,}

llm = CTransformers(model=model_id,
                    model_type='mistral',
                    config=config,
                    )

prompt = PromptTemplate.from_template("you are an assistant answer the following: {query}")

chain = LLMChain(llm=llm, prompt=prompt)

def genai_engine(query):
    response = chain.run(query)
    return response

def write_conversation_to_file(conversation, filename):
    try:
        with open(filename, 'a') as file:
            for role, content in conversation:
                file.write(f"{role}: {content}\n")
        return True
    except Exception as e:
        print("Error occurred while writing conversation to file:", e)
        return False
