import config
import argparse

import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
from parse_string import LlamaParser
from agents import AgentAction, HuggingfaceChatbot
from utils import *
import random
import numpy as np
import torch


    
def set_seeds(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)


def main(args):
    set_seeds(args)
    log(str(args),args.log_path)
    dataset = load_dataset("AnonymousNodeGAE/MCIP")['validation']

    if args.api_name:
        chatbot = ''
    else:    
        chatbot = HuggingfaceChatbot(args.model)
        
    agents = AgentAction(chatbot, 
                         parser_fn = LlamaParser().parse_attack_type_trained,
                         template = args.prompt_template,
                         **vars(args))
    result_save_path = args.log_path.replace('.txt', '_results.txt')

    results = []
    if args.sample:
        dataset = random.sample(dataset, min(len(dataset), args.sample))
    y_true_bool = []
    y_pred_bool = []
    CHOICE2INDEX = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9,
        "K": 10,
    }
    LABEL2INDEX = {'true': 0, 'function_overlapping':1, 'excessive_privileges':2, 'function_dependency_injection':3, 'function_injection':4, 'causal_dependency_injection':5, 'ignore_prupose_prompt_injection':6, 'wrong_parameter_prompt_injection':7, 'data_injection':8, 'identity_injection':9,'replay_function':10}

    for i, item in enumerate(tqdm(dataset)):
        label = item['label']
        y_true_bool.append(LABEL2INDEX[label])
        decision = {}
        log(str(f"======== case: {i}\n"), args.log_path)
        for _ in range(args.generation_round):
            try:
                
                decision, message = agents.complete(**item)
                result = (CHOICE2INDEX[decision["decision"]] == LABEL2INDEX[label])
                results.append(result)
                acc = (sum(results) / len(results))
                print(acc)
                log(str(f"sample_id: {i} --- label:{label} --- result:{result} --- answer: {decision['decision']}\n"), args.log_path)
                decision['prompt'] = message
                log(str(decision)+"\n", args.log_path)
                if decision: 
                    y_pred_bool.append(CHOICE2INDEX[decision["decision"]])
                    break

            except Exception as e:
                print(e)
                continue
        if not decision: 
            y_pred_bool.append(-1)
            # results.append(-1)

    acc = (sum(results) / len(results))
    print(acc)
    y_true = pd.Series(y_true_bool)
    y_pred = pd.Series(y_pred_bool)
    y = pd.concat([y_true, y_pred], axis=1)
    torch.save(y, args.y_path)
    log(str(f"--- num_sample: {len(dataset)} --- accuracy:{acc}\n"), args.log_path)
    log(str(f"--- num_sample: {len(dataset)} --- accuracy:{acc}\n"), result_save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="AnonymousNodeGAE/MCIP_Guardian")
    parser.add_argument("--log_path", type=str, default="logs/try.txt")
    parser.add_argument("--prompt_template", type=str, default="prompts/MCP_attack_type.txt")
    parser.add_argument("--y_path", type=str, default="ys/try.pt")
    parser.add_argument("--max_new_tokens", type=int, default=1024)

    parser.add_argument("--generation_round", type=int, default=10)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--api_name", type=str, default='')
    ### newly appeneded
    # parser.add_argument("--domains", type=str, default='AI_ACT')
    # parser.add_argument("--api_model", type=str, default=config.api_model)
    parser.add_argument("--api_token", type=str, default='')
    parser.add_argument("--max_retry", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--sample", type=int, default=0)
    args = parser.parse_args()
    main(args)
