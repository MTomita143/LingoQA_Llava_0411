"""
val.parquetの
question_id, segment_id, images[2], questionからoutputを取得して、csvにする
"""

import pandas as pd
import PIL
from vllm import LLM, SamplingParams
import os
import csv

def makePrompt(question):
    prompt = f"USER: <image>\n{question}\nASSISTANT:"
    return prompt

def runVllm(llm, prompt, img_path, sampling_params):
    image = PIL.Image.open(img_path)
    output = llm.generate({
        "prompt": prompt,
        "multi_modal_data": {"image": image},
        "parameter": sampling_params
    })

    return output[0].outputs[0].text
    
def main():
    #validation file
    val_df = pd.read_parquet('val.parquet')
    print(len(val_df))
    
    #LLM setups
    seed = 50411
    llm = LLM(model="llava-hf/llava-1.5-7b-hf", tensor_parallel_size=2, seed=seed)
    sampling_params = SamplingParams(temperature=0.8, top_p=0.9)
    
    #to write
    csv_path = "/workspace/LingoQA/path_to_predictions/predictions.csv"
    header = ['question_id', 'segment_id', 'question', 'answer']
    
    for i in range(len(val_df)): #i行目について
        q_id = val_df['question_id'].iloc[i]
        s_id = val_df['segment_id'].iloc[i]
        img_path = val_df['images'].iloc[i][2]
        question = val_df['question'].iloc[i]
        prompt = makePrompt(question)
        answer = runVllm(llm, prompt, img_path, sampling_params)
        answer_clean = answer.replace('\n', ' ').replace('\r', ' ')
        
        row = {
            'question_id': q_id,
            'segment_id': s_id,
            'question': question,
            'answer': answer_clean
        }

        file_is_empty = not os.path.exists(csv_path) or os.stat(csv_path).st_size == 0

        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            if file_is_empty:
                writer.writeheader()
            writer.writerow(row)
        
if __name__ == "__main__":
    main()