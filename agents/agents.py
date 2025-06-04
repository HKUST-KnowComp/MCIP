import copy
import sys
import os
#sys.path.append("../")
from agents.bm25 import BM25
from utils import Trie, list_intersection
import json
import requests
import openai
from openai import OpenAI
import time
import random
from config import MAX_REFERENCE_NUM

class OpenAI_model:
    def __init__(self, api_key: str, api_name: str):
        self.api_key = api_key
        self.api_name = api_name
        if(api_name == 'deepseek'):
            print('using ARK API to respond via deepseek r1...')
            self.client = OpenAI(
                api_key = self.api_key,
                base_url = "https://ark.cn-beijing.volces.com/api/v3",
            )
        else:
            self.client = OpenAI(
                api_key=self.api_key, 
                base_url="https://api.oneabc.org/v1"
            )

    def compeletion(self, model: str, messages: list, max_retries: int, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                if(self.api_name == 'deepseek'):
                    model = "deepseek-r1-250120"
                response = self.client.chat.completions.create(
                    model = model,
                    messages=messages,
                    **kwargs
                )

                msg = 'rationale: '+response.choices[0].message.reasoning_content+'response: '+response.choices[0].message.content
                assert isinstance(msg, str), "The retruned response is not a string."
                return msg  # Return the response if successful

            except Exception as e:
                # Catch all other exceptions
                print(f"Unexpected error: {e}. Retrying in 5 seconds...")
                retries += 1
                time.sleep(1)
        
        return ''  # Return an empty string if max_retries is exceeded

class AgentAction:
    def __init__(self, chatbot, template, parser_fn, 
                 max_new_tokens=1024,
                 api_name =None,
                 api_model = 'gpt-4o-mini',
                 api_token = None,
                 max_retry = 5,
                 temperature = 0.2,
                 **kwargs
                 ):
        '''
        api_name: str, the name of the api (use OpenAI API), if api is empty, use chatbot to respond
        '''
        self.api_token = api_token
        self.api_name = api_name
        self.api_model = api_model
        self.max_retry = max_retry
        self.temperature = temperature
        
        self.domain = kwargs.get('domain', None)

        if(not api_name):
            print('using HF chatbot to respond...')
            self.chatbot = chatbot
        else:
            print('using OpenAI API to respond...')
            self.chatbot = OpenAI_model(api_key=self.api_token, api_name = self.api_name)
        self.template = self.load_template(template)
        self.parse_fn = parser_fn
        self.max_new_tokens = max_new_tokens

    def load_template(self, path):
        with open(path, "r", encoding="utf-8") as f:
            template = f.read()
        return template

    def complete(self, **kwargs):
        message = self.template.format(**kwargs)
        # print(message)
        # exit(0)
        # print(message)
        if(not self.api_name):
            ### HF models
            ##msg will be stripped inside the respond function
            response = self.chatbot.respond(message, self.max_new_tokens)
            # print(response)
        else:
            ### use api
            # message = message.replace("Assistant:", "").strip()
            # message_list = [
            #     {"role": "system", "content": "You are a helpful assistant."},
            #     {"role": "user", "content": message}
            # ]
            message_list = [
                {"role": "user", "content": message}
            ]
            
            response = self.chatbot.compeletion(self.api_model, message_list, self.max_retry, temperature = self.temperature, max_tokens = self.max_new_tokens)
            
        ## TODO : complete the parsing
        parserd_response = self.parse_fn(response)
        return parserd_response, message

