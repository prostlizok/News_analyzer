from langchain_core.prompts import ChatPromptTemplate
from prompts import json_structure, system_message ,system_message_upd,json_structure_upt
from langchain_openai import ChatOpenAI
from schemas import InvoiceJson , InvoiceJsonUpd 
from dotenv import load_dotenv
from typing import Dict, List
import json
import os
from openai import OpenAI

load_dotenv()

def _get_llm(model_name: str) -> ChatOpenAI:
    llm = ChatOpenAI(model=model_name, temperature=0)
    return llm

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
            result = [dict(region) for region in data.info]
            entry['emergency_info'] = result
        except Exception as e:
            print(e)
    
        
    return input_json
    
def get_updated_data(text: str ) -> dict:
    try :
        llm = _get_llm("gpt-4o-mini")   
        structured_llm = llm.with_structured_output(InvoiceJsonUpd) 
        system_prompt = system_message_upd.format(json_structure=json_structure_upt)
        prompt = ChatPromptTemplate.from_messages(
                    [("system", system_prompt), ("human", "{input}")]
        )
        dsns_data = prompt | structured_llm
        input_prompt = f"raw_text: {text}"
        data = dsns_data.invoke({"input": input_prompt})
        result = [dict(region) for region in data.info]
        return result[0]
    except Exception as e:
            print(e)
