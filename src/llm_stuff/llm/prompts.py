system_message = """
You are the best model to map raw texts to desired Json format. you will be provided invoice's texts that you need to map into a JSON format. 
You are tasked with converting the given text into a JSON object with the specified structure. 
Please follow these guidelines:

1. - If the provided text is empty or does not contain any relevant information, return the JSON structure with all values as empty strings.
   - If the provided text contains multiple instances of the same information (e.g., multiple names), use the first occurrence.
   - If the provided text contains conflicting information (e.g., different ages), use the first occurrence.

2. Extract relevant information from the provided text and map it to the corresponding keys in the JSON structure.

3. If a particular key's value is not found in the given text, leave the value as an empty string.

4. Do not include any additional information or formatting beyond the requested JSON object.

Here are some examples, I'm gonna provide you the raw_texts and json structure.
raw_texts:  "💥Повторний вибух у Павлограді."
json_structure: {json_structure}
"""

json_structure = """{{
  "text": "💥Повторний вибух у Павлограді.",
  "date": "2024-09-06T07:18:07+00:00",
  "channel": "monitorwarr",
  "link": "https://t.me/monitorwarr/23895"
}}"""