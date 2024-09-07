from langchain_core.prompts import ChatPromptTemplate
from prompts import json_structure, system_message
from langchain_openai import ChatOpenAI
from schemas import InvoiceJson
from dotenv import load_dotenv
from typing import Dict, List
import os

load_dotenv()

def _get_llm(model_name: str) -> ChatOpenAI:
    llm = ChatOpenAI(model=model_name, temperature=0)
    return llm

input_json = [
    {
        "text": "💥Повторний вибух у Павлограді.",
        "date": "2024-09-06T07:18:07+00:00",
        "channel": "monitorwarr",
        "link": "https://t.me/monitorwarr/23895"
    },
    {
        "text": "💥Повторні вибухи у Павлограді.",
        "date": "2024-09-06T07:01:12+00:00",
        "channel": "monitorwarr",
        "link": "https://t.me/monitorwarr/23894"
    }
]

def create_json_output():
    ... 


def collect_info(input_json: List[dict]) -> List[dict]:
    llm = _get_llm("gpt-4o-mini")    
    for entry in input_json:
        text = entry["text"]

        try:

            structured_llm = llm.with_structured_output(InvoiceJson)
            system_prompt = system_message.format(json_structure=json_structure)
            prompt = ChatPromptTemplate.from_messages(
                [("system", system_prompt), ("human", "{input}")]
            )
            few_shot_structured_llm = prompt | structured_llm
            
            input_prompt = f"raw_text: {text}"
            data = few_shot_structured_llm.invoke({"input": input_prompt})
            entry['emergency_info'] = data

        except Exception as e:
            print(e)
        
    return input_json
    

jsonr = collect_info(input_json=input_json)
print(jsonr)
