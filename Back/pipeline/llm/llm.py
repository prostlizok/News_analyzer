from langchain_core.prompts import ChatPromptTemplate
from prompts import json_structure, system_message
from langchain_openai import ChatOpenAI
from schemas import InvoiceJson
from dotenv import load_dotenv
from typing import Dict, List
import os

load_dotenv()



OPENAI_MODEL_NAME = "gpt-4o-mini"

llm = ChatOpenAI(model=OPENAI_MODEL_NAME, temperature=0)

load_dotenv()

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
    extracted_info = []
    
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
            print(data)

        except Exception as e:
            print(e)
        #extracted_info.append(structured_output.dict())
    
    #return extracted_info

collect_info(input_json=input_json)
