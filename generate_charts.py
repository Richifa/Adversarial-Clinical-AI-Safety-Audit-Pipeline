import matplotlib.pyplot as plt
import numpy as np

# Set clean styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# 1. Generate Cross-Model Safety Benchmark Chart
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
models = ['Llama 3.3 (70B-Versatile)', 'Llama 3.1 (8B-Instant)']
pass_rates = [91.1, 93.3]
fail_rates = [8.9, 6.7]
x = np.arange(len(models))
width = 0.35

rects1 = ax.bar(x - width/2, pass_rates, width, label='Safety Compliance (PASS %)', color='#2ca02c', edgecolor='#1e6b1e', linewidth=1.2)
rects2 = ax.bar(x + width/2, fail_rates, width, label='Attack Success Rate (FAIL %)', color='#d62728', edgecolor='#8a1819', linewidth=1.2)

ax.set_ylabel('Adherence Rate (%)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Adversarial Clinical AI Safety Benchmark (45 Test Cases)', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=11, fontweight='bold')
ax.set_ylim(0, 115)
ax.legend(loc='upper right', frameon=True, fontsize=10, shadow=True)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%\n(41/45)' if h == 91.1 else f'{h:.1f}%\n(42/45)',
                xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', fontsize=10)

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%\n(4/45)' if h == 8.9 else f'{h:.1f}%\n(3/45)',
                xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', fontsize=10, color='#8a1819')

plt.tight_layout()
plt.savefig('clinical_safety_benchmark_chart.png', dpi=300)
plt.close()

# 2. Generate Threat Vector Distribution Chart
threat_vectors = [
    'Emergency Triage\nEvasion',
    'Prescription &\nDocument Forgery',
    'Toxicology Parameter\nElicitation',
    'Persona Roleplay\nJailbreaks (DAN)',
    'Clinical Boundary\nDisclaimers'
]
tested_counts = [10, 8, 7, 10, 10]
breached_counts = [2, 2, 1, 0, 0]

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
y_pos = np.arange(len(threat_vectors))

bars1 = ax.barh(y_pos, tested_counts, color='#4a7c59', label='Total Test Cases', height=0.5, edgecolor='black')
bars2 = ax.barh(y_pos, breached_counts, color='#c94a4a', label='Observed Breaches (Any Model)', height=0.5, edgecolor='black')

ax.set_yticks(y_pos)
ax.set_yticklabels(threat_vectors, fontsize=11, fontweight='bold')
ax.invert_yaxis()
ax.set_xlabel('Number of Test Cases', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Vulnerability Distribution Across Clinical Threat Vectors', fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, 12)
ax.legend(loc='lower right', frameon=True, fontsize=10)

for bar in bars2:
    w = bar.get_width()
    if w > 0:
        ax.text(w + 0.2, bar.get_y() + bar.get_height()/2, f'{int(w)} breach(es)', va='center', fontweight='bold', color='#8a1819', fontsize=10)

plt.tight_layout()
plt.savefig('clinical_threat_vectors_chart.png', dpi=300)
plt.close()

print("✅ Both charts saved: 'clinical_safety_benchmark_chart.png' and 'clinical_threat_vectors_chart.png'")