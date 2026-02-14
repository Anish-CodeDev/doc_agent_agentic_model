import pandas as pd
import random

# --- CONFIGURATION ---
filenames_doc = ["'contract.docx'", "'report_2026.pdf'", "'legal_v4.docx'", "'manual.docx'"]
filenames_pres = ["'pitch_deck.pptx'", "'quarterly_review.slides'", "'final_presentation.pptx'"]
topics = ["'Q3 Revenue'", "'AI Ethics'", "'Competitor Analysis'", "'Safety Protocols'", "'Budget'"]
formatting_reqs = ["'bold all headers'", "'set font to Arial'", "'increase margin size'", "'make text red'"]

def gen_complex_delete():
    fname = random.choice(filenames_pres)
    topic = random.choice(topics)
    input_t = f"Find the slide about {topic.strip(chr(39))} in {fname.strip(chr(39))} and delete it."
    # Multi-step: Find then Remove
    reasoning = (
        f"1. Use find_slide_tool(filename={fname}, topic={topic}) to locate the slide index.\n"
        f"2. Use remove_slide_tool(filename={fname}, index=`found_index`)."
    )
    return input_t, reasoning

def gen_complex_modify_pres():
    fname = random.choice(filenames_pres)
    topic = random.choice(topics)
    input_t = f"Locate the {topic.strip(chr(39))} slide in {fname.strip(chr(39))} and update its content."
    # Multi-step: Find then Modify
    reasoning = (
        f"1. Use find_slide_tool(filename={fname}, topic={topic}) to identify the target slide.\n"
        f"2. Use modify_content_of_presentation(filename={fname}, topic={topic})."
    )
    return input_t, reasoning

def gen_complex_doc_update():
    fname = random.choice(filenames_doc)
    topic = random.choice(topics)
    req = random.choice(formatting_reqs)
    input_t = f"Rewrite the {topic.strip(chr(39))} section in {fname.strip(chr(39))} and then {req.strip(chr(39))}."
    # Multi-step: Text Change then Formatting
    reasoning = (
        f"1. Use modify_text_of_doc(filename={fname}, topic={topic}).\n"
        f"2. Use modify_formatting_of_doc(filename={fname}, request={req})."
    )
    return input_t, reasoning

def gen_complex_insert():
    fname = random.choice(filenames_pres)
    topic = random.choice(topics)
    input_t = f"I need a new slide for {topic.strip(chr(39))} at the start of {fname.strip(chr(39))}, then update its content."
    # Multi-step: Insert then Modify
    reasoning = (
        f"1. Use insert_slide_tool(topic={topic}, filename={fname}, index=1).\n"
        f"2. Use modify_content_of_presentation(filename={fname}, topic={topic})."
    )
    return input_t, reasoning

# --- DATASET GENERATION ---
data = []
generators = [gen_complex_delete, gen_complex_modify_pres, gen_complex_doc_update, gen_complex_insert]

for _ in range(5000):
    gen_func = random.choice(generators)
    inp, out = gen_func()
    data.append({"Input_Task": inp, "Reasoning_Prompts": out})

df = pd.DataFrame(data)

# Display Verification
pd.set_option('display.max_colwidth', None)
print(f"Generated {len(df)} Multi-Step Samples.")
print(df.sample(5)) # Showing random samples to see variety
df.to_csv("agent_strict_tools_5k.csv", index=False)