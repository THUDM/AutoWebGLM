def call_pretrain_model(query: str, model, tokenizer, cuda, sample_times: int=1):        
    def chatglm3_base_template(query, history=None, system=None):
        prompt = f'Q: {query}\n\nA: '
        return prompt
    
    def model_chat(prompt: str):
        output, updated_history = model.chat(tokenizer, prompt, history=None)
        return output
    
    def generation(prompt: str, sample_times: int=1):
        input_ids = tokenizer.encode(
            text=prompt,
            return_tensors='pt',
            max_length=8192,
            truncation=False
        ).to(f'cuda:{cuda}')

        if len(input_ids[0]) > 7500:
            return ''
        
        output_ids = model.generate(
            input_ids=input_ids,
            max_new_tokens=1024,
            do_sample=True,
            top_p=0.7,
            temperature=0.95,
            num_return_sequences=sample_times
        )
        
        output_text_list = []
        for i in range(sample_times):
            output_text = tokenizer.decode(output_ids[i], skip_special_tokens=True)
            output_text = output_text.split('A: ')[-1]
            output_text_list.append(output_text)
        
        output = output_text_list[0]
        return output
    
    prompt = chatglm3_base_template(query)
    output = generation(prompt)
    # output = model_chat(prompt)
    print('[Model]', output)
    return output
