import transformers
import torch

model = 8

## Here you paste your cloned repos location
if model == 8:
    model_id = "/data/share_weight/Meta-Llama-3-8B-Instruct"
elif model == 70:
    model_id = "/data/share_weight/Meta-Llama-3.1-70B-Instruct"
else:
    print("Please choose a existing model to use")

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="cuda",
)

messages = [
    {"role": "user", "content": "Who are you?"},
]

outputs = pipeline(
    messages,
    max_new_tokens=256,
)
print(outputs[0]["generated_text"][-1])