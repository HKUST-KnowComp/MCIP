from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pprint
from config import CACHE_DIR


class HuggingfaceChatbot:
    def __init__(self, model, max_mem_per_gpu='40GiB'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_hugging_face_model(model, max_mem_per_gpu)
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        


    def load_hugging_face_model(self, model, max_mem_per_gpu='40GiB'):

        MAX_MEM_PER_GPU = max_mem_per_gpu
        n_gpus = torch.cuda.device_count()
        memory_map = {}
        
        for i in range(n_gpus):
            memory_map[i] = MAX_MEM_PER_GPU
        
        model = AutoModelForCausalLM.from_pretrained(
            model,
            device_map="auto", 
            max_memory=memory_map, 
            cache_dir=CACHE_DIR,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        )
        return model

    def respond(self, message, max_new_tokens=128):
        message = message.replace("Assistant:", "").strip()
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
        message = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # 将输入放到第一个GPU上
        tokenized = self.tokenizer(message, return_tensors="pt")
        input_ids = tokenized.input_ids.to(self.model.device)
        attention_mask = tokenized.attention_mask.to(self.model.device)
        
        generation_config = self.model.generation_config
        # generation_config.max_length = 8192
        generation_config.max_new_tokens = max_new_tokens
        
        with torch.cuda.amp.autocast(): 
            output = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                generation_config=generation_config
            )
            
        response = self.tokenizer.batch_decode(output[:, input_ids.shape[1]:], skip_special_tokens=True)[0]
        response = response.strip()
        return response

if __name__ == '__main__':
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3-8B-Instruct",
    ).to("cuda:0")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
    print(1)