"""Load a model and answer three yes/no prompts. Checks the model runs and logprobs parse."""
import argparse
import json

from src.config import model_cfg
from src.llm import Model, first_token_probs

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
a = p.parse_args()
cfg = model_cfg(a.model)
m = Model(cfg)
from vllm import SamplingParams
msgs = [[{"role": "user", "content": q}] for q in [
    "Is Paris the capital of France? Answer with only one word: Yes or No.",
    "Is 7 an even number? Answer with only one word: Yes or No.",
    "क्या दिल्ली भारत की राजधानी है? केवल एक शब्द में उत्तर दें: Yes या No.",
]]
outs = m.llm.chat(msgs, SamplingParams(max_tokens=4, temperature=0, logprobs=20), use_tqdm=False,
                  chat_template_kwargs=m.chat_kwargs or None)
for o in outs:
    mass, tot = first_token_probs(o.outputs[0].logprobs[0])
    print("SMOKE", json.dumps({"text": o.outputs[0].text, "mass": mass, "total": round(tot, 4)}, ensure_ascii=False))
print("SMOKE_OK", a.model)
