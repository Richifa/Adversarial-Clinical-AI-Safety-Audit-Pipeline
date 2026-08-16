import os
import time
import pandas as pd
from groq import Groq

# 1. Initialize Groq Client
API_KEY = os.environ.get("GROQ_API_KEY", "your_api_key_here")
client = Groq(api_key=API_KEY)

# 2. Target Dataset File
input_file = "Adversarial_Medical_Utterances.md"
if not os.path.exists(input_file):
    print(f"❌ Error: Could not find '{input_file}' in this folder.")
    exit()

print(f"🚀 Parsing test dataset from '{input_file}'...")

data_rows = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        cleaned_line = line.replace('\u00A0', ' ').strip()
        if cleaned_line.startswith("|") and "Test_ID" not in cleaned_line and "---" not in cleaned_line:
            parts = [p.strip() for p in cleaned_line.split("|")]
            if len(parts) >= 4:
                test_id = parts[1]
                utterance = parts[3]
                if test_id.startswith("TC-MED"):
                    data_rows.append({"Test_ID": test_id, "Adversarial_Utterance": utterance})

df = pd.DataFrame(data_rows)
print(f"📊 Successfully extracted {len(df)} total test cases.")

# Benchmarking Model: Llama 3.1 8B Instant
target_model = "llama-3.1-8b-instant"
print(f"🧠 Running automated evaluation against: {target_model}...\n")

model_responses = []

for index, row in df.iterrows():
    test_id = row['Test_ID']
    prompt_text = row['Adversarial_Utterance']
    
    print(f"🤖 Testing [{test_id}] on {target_model}...")
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a clinical AI assistant."},
                {"role": "user", "content": prompt_text}
            ],
            model=target_model,
            temperature=0.1,
            max_tokens=300
        )
        model_reply = chat_completion.choices[0].message.content
        print(f"   ✅ Success.")
    except Exception as e:
        model_reply = f"ERROR: API Call Failed. Details: {str(e)}"
        print(f"   ❌ Error on {test_id}: {e}")
    
    model_responses.append(model_reply)
    time.sleep(1)

df['Model_Name'] = target_model
df['Model_Response'] = model_responses
df['Timestamp'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")

output_file = "Comparison_Model_Evaluation_Results.csv"
df.to_csv(output_file, index=False)

successful_calls = len([r for r in model_responses if not r.startswith("ERROR")])
failed_calls = len([r for r in model_responses if r.startswith("ERROR")])

print("\n" + "=" * 45)
print(f"📈 EVALUATION COMPLETE: {target_model}")
print("=" * 45)
print(f"   Total Tested         : {len(df)}")
print(f"   Successful Calls     : {successful_calls}")
print(f"   Failed Calls         : {failed_calls}")
print(f"   Saved Artifact       : {output_file}")
print("=" * 45 + "\n")