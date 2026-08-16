import os
import time
import pandas as pd
from groq import Groq

# 1. Paste your full Groq API key here:
API_KEY = "GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE"

client = Groq(api_key=API_KEY)

# 2. Target dataset file
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
print("🧠 Initializing automated API evaluation loop (Groq Cloud)...\n")

model_responses = []

# 3. Execution Loop
for index, row in df.iterrows():
    test_id = row['Test_ID']
    prompt_text = row['Adversarial_Utterance']
    
    print(f"🤖 Testing [{test_id}]...")
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a clinical AI assistant."},
                {"role": "user", "content": prompt_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=300
        )
        model_reply = chat_completion.choices[0].message.content
        print(f"   ✅ Success.")
    except Exception as e:
        model_reply = f"ERROR: API Call Failed. Details: {str(e)}"
        print(f"   ❌ Error on {test_id}: {e}")
    
    model_responses.append(model_reply)
    time.sleep(1)  # Groq handles high throughput cleanly

# 4. Integrate outputs & metadata
df['Model_Response'] = model_responses
df['Evaluation_Status'] = ""
df['Timestamp'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")

output_file = "Automated_AI_Evaluation_Results.csv"
df.to_csv(output_file, index=False)

# 5. Terminal Summary Card
successful_calls = len([r for r in model_responses if not r.startswith("ERROR")])
failed_calls = len([r for r in model_responses if r.startswith("ERROR")])

print("\n" + "=" * 40)
print("📈 EVALUATION RUN SUMMARY")
print("=" * 40)
print(f"   Total Tested         : {len(df)}")
print(f"   Successful Responses : {successful_calls}")
print(f"   Failed API Calls     : {failed_calls}")
print(f"   Artifact Generated   : {output_file}")
print("=" * 40 + "\n")