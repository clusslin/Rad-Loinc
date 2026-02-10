
import pandas as pd
from vllm import LLM, SamplingParams
import json
import sys
from typing import List, Dict

def classify_studies(input_file: str, output_file: str, model_name: str = "Qwen/Qwen2.5-3B-Instruct"):
    print(f"Loading data from {input_file}...")
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Prepare unique descriptions to classify
    descriptions = df['Study Description'].dropna().unique().tolist()
    print(f"Found {len(descriptions)} unique descriptions to classify.")

    # Prepare prompts
    prompts = []
    system_prompt = (
        "You are a helpful assistant that acts as a radiology terminology expert. "
        "Extract the following information from the radiology study description: "
        "1. Body Part (e.g., Chest, Brain, Abdomen) "
        "2. Modality (e.g., XR, CT, MRI, US) "
        "3. Laterality (Left, Right, Bilateral, or None) "
        "4. Contrast (Yes, No, or Unknown) "
        "Output ONLY a valid JSON object with keys: 'body_part', 'modality', 'laterality', 'contrast'."
    )
    
    for desc in descriptions:
        # Chat format for instruction tuned models
        prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\nDescription: {desc}\nOutput JSON:<|im_end|>\n<|im_start|>assistant\n"
        prompts.append(prompt)

    # Initialize VLLM
    print(f"Initializing VLLM with model: {model_name}...")
    # trustworthy_remote_code might be needed for some models like Qwen
    try:
        # On Mac with 16GB, we need to be careful with memory
        llm = LLM(model=model_name, trust_remote_code=True, dtype="float16", gpu_memory_utilization=0.6)
    except Exception as e:
        print(f"Failed to initialize VLLM: {e}")
        print("Note: On Mac with 16GB RAM, ensure you are using a small model (approx 3B parameters).")
        return

    sampling_params = SamplingParams(temperature=0.0, max_tokens=100)

    # Generate
    print("Generating classifications...")
    outputs = llm.generate(prompts, sampling_params)

    # Parse results
    results = {}
    for desc, output in zip(descriptions, outputs):
        generated_text = output.outputs[0].text.strip()
        # Clean up potential markdown formatting
        if generated_text.startswith("```json"):
            generated_text = generated_text.replace("```json", "").replace("```", "")
        
        try:
            # Try to parse JSON
            start_idx = generated_text.find('{')
            end_idx = generated_text.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = generated_text[start_idx:end_idx]
                data = json.loads(json_str)
                results[desc] = data
            else:
                results[desc] = {'error': generated_text}
        except Exception as e:
            results[desc] = {'error': f"Parse Error: {generated_text}"}

    # Map back to DataFrame
    print("Mapping results back to dataframe...")
    
    def get_attr(desc, attr):
        if desc in results and isinstance(results[desc], dict):
            return results[desc].get(attr, '')
        return ''

    df['LLM_Body_Part'] = df['Study Description'].apply(lambda x: get_attr(x, 'body_part'))
    df['LLM_Modality'] = df['Study Description'].apply(lambda x: get_attr(x, 'modality'))
    df['LLM_Laterality'] = df['Study Description'].apply(lambda x: get_attr(x, 'laterality'))
    df['LLM_Contrast'] = df['Study Description'].apply(lambda x: get_attr(x, 'contrast'))

    print(f"Writing results to {output_file}...")
    df.to_excel(output_file, index=False)
    print("Done!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="examples/rad_prepared.xlsx")
    parser.add_argument("--output", default="rad_llm_classified.xlsx")
    parser.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    args = parser.parse_args()
    
    classify_studies(args.input, args.output, args.model)
