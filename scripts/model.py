# Copyright (c) Guangsheng Bao.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import transformers
import torch
import time

# predefined models
model_fullnames = {  'gpt2': 'gpt2',
                     'gpt2-xl': 'gpt2-xl',
                     'opt-2.7b': 'facebook/opt-2.7b',
                     'gpt-neo-2.7B': 'EleutherAI/gpt-neo-2.7B',
                     'gpt-j-6B': 'EleutherAI/gpt-j-6B',
                     'gpt-neox-20b': 'EleutherAI/gpt-neox-20b',
                     'mgpt': 'sberbank-ai/mGPT',
                     'pubmedgpt': 'stanford-crfm/pubmedgpt',
                     'mt5-xl': 'google/mt5-xl'}

def get_model_fullname(model_name):
    return model_fullnames[model_name] if model_name in model_fullnames else model_name

def load_model(model_name, device, cache_dir):
    model_name = get_model_fullname(model_name)
    print(f'Loading model {model_name}...')
    model_kwargs = {}
    if 'gpt-j' in model_name or 'neox' in model_name:
        model_kwargs.update(dict(torch_dtype=torch.float16))
    if 'gpt-j' in model_name:
        model_kwargs.update(dict(revision='float16'))
    model = transformers.AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs, cache_dir=cache_dir)

    print('Moving model to GPU...', end='', flush=True)
    start = time.time()
    model.to(device)
    print(f'DONE ({time.time() - start:.2f}s)')
    return model


def load_tokenizer(model_name, for_dataset, cache_dir):
    model_name = get_model_fullname(model_name)
    optional_tok_kwargs = {}
    if "facebook/opt-" in model_name:
        print("Using non-fast tokenizer for OPT")
        optional_tok_kwargs['fast'] = False
    if for_dataset in ['pubmed']:
        optional_tok_kwargs['padding_side'] = 'left'
    base_tokenizer = transformers.AutoTokenizer.from_pretrained(model_name, **optional_tok_kwargs, cache_dir=cache_dir)
    base_tokenizer.pad_token_id = base_tokenizer.eos_token_id
    return base_tokenizer

def load_gpt2_tokenizer(cache_dir):
    tokenizer = transformers.GPT2Tokenizer.from_pretrained('gpt2', cache_dir=cache_dir)
    tokenizer.pad_token_id = tokenizer.eos_token_id
    return tokenizer

