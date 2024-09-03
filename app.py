#!/usr/bin/env python
# coding: utf-8

# In[12]:


from flask import Flask, request
import requests
from dotenv import load_dotenv
import os
import logging


# In[13]:


load_dotenv()

app = Flask(__name__)


# In[14]:


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DUNE_API_KEY = os.getenv('DUNE_API_KEY')
DUNE_QUERY_ID = os.getenv('DUNE_QUERY_ID')

print(TELEGRAM_BOT_TOKEN)
print(DUNE_API_KEY)
print(DUNE_QUERY_ID)


# In[15]:


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info("Incoming request: %s", data)  # Log incoming requests
    chat_id = data['message']['chat']['id']
    user_input = data['message']['text']

    # Prepare the JSON payload
    payload = {"parameters": {"input": user_input}}
    
    # Print the JSON payload for debugging
    print("JSON Payload:", payload)

    # Run Dune Analytics query with user input
    query_url = f'https://api.dune.com/api/v1/query/{DUNE_QUERY_ID}/execute'
    headers = {'x-dune-api-key': DUNE_API_KEY}
    response = requests.post(query_url, headers=headers, json={"parameters": {"input": user_input}})


    # Send result back to Telegram
    if response.status_code == 200:
        result = response.json()
        logging.info("Dune Analytics response: %s", result)  # Log Dune Analytics response
        send_message(chat_id, result['data'])
    else:
        logging.error("Failed to retrieve data from Dune Analytics: %s", response.text)
        send_message(chat_id, "Failed to retrieve data from Dune Analytics.")

    return 'ok'


# In[16]:


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)
    logging.info("Telegram API response: %s", response.json())  # Log Telegram API response

# In[17]:


if __name__ == '__main__':
    app.run(port=5000)

