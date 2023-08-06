
import os
from dotenv import load_dotenv
from gpt4_openai import GPT4OpenAI
load_dotenv()

import csv

input_file = "phones.csv"

prompt1 = 'Find me the price of '
prompt2 = ' mobile phone. Maybe check amazon.de, mediamarkt.de, gearbest, banggood, etc. Output JSON of this format: {\"price\": \"$1,000\", \"source\": \"https://amazon.com/product\"}. If there are multiple variants with different prices, use the lowest price.'

with open(input_file, "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = [row for row in reader]

for row in rows:
    try:
        phone_name = row[0]
        _chip = row[1]
        # Check if it has row 2
        if 2 < len(row) and row[2] != "":  # If it has row 2
            print(phone_name, "has above 2 rows")
            continue # Skip

        llm = GPT4OpenAI(token=os.environ["OPENAI_ACCESS_TOKEN"], model='gpt-4-browsing',
                 plugin_ids=[
                    #  'plugin-aa8a399d-a369-432e-81b7-ee6e889c1b8f', # Currency conversion
                     'plugin-d1d6eb04-3375-40aa-940a-c2fc57ce0f51', # Wolfram Alpha
                    ]
                 )
        response = llm(prompt1 + phone_name + prompt2)
        print(phone_name, response)
        row.append(response)
    except Exception as e:
        print(e)
        if str(e).startswith('Field missing'):
            continue
        else:
            break


with open(input_file, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
with open('phones2.csv', "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';', lineterminator='\r\n')
    writer.writerows(rows)
