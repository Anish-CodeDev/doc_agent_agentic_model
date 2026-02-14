from flask import Flask,request
from unsloth import FastLanguageModel
from transformers import TextStreamer

app = Flask(__name__)
model,tokenizer = FastLanguageModel.from_pretrained(
    model_name="sft_model",
    max_seq_length=512,
    load_in_4bit=True,
    max_lora_rank=16
)
reasoning_start,reasoning_end = "<think>","</think>"
@app.route('/',methods=['POST'])
def respond():
   data = request.get_json()
   req = data.get('request')
   content = [{'content': f'You are given with a task to solve,Think about this task and provide the steps to solve this task.Place your answer between                          {reasoning_start} and {reasoning_end}.','role':'system'},
               {'content': req,
               'role': 'user'}]
   text = tokenizer.apply_chat_template(content,tokenize=False,add_generation_prompt=True)
   res = model.generate(
    **tokenizer(text,return_tensors='pt').to('cuda'),
    temperature=0.8,
    max_new_tokens=2048,
    streamer=TextStreamer(tokenizer,skip_prompt=False)
    )
   res = tokenizer.decode(res[0]).split('<|im_start|>')[3]
   return res
   
  
if __name__ == "__main__":
	app.run(debug=True)
