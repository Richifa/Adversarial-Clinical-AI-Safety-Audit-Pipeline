import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)

categories = ['Baseline Pipeline\n(Llama 3.3 70B)', 'Defended Middleware\n(+ Pre/Post Interceptors)']
pass_rates = [91.1, 100.0]
fail_rates = [8.9, 0.0]

x = np.arange(len(categories))
width = 0.32

rects1 = ax.bar(x - width/2, pass_rates, width, label='Safety Compliance (PASS %)', color='#2ca02c', edgecolor='#1e6b1e', linewidth=1.2)
rects2 = ax.bar(x + width/2, fail_rates, width, label='Attack Success Rate (FAIL %)', color='#d62728', edgecolor='#8a1819', linewidth=1.2)

ax.set_ylabel('Adherence Rate (%)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Remediation Impact: Baseline Audit vs. Defensive Guardrail Middleware', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
ax.set_ylim(0, 125)
ax.legend(loc='upper left', frameon=True, fontsize=10, shadow=True)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%\n({int(round(h*45/100))}/45)',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', fontsize=10)

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%\n({int(round(h*45/100))}/45)',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', fontsize=10, color='#8a1819')

plt.tight_layout()
plt.savefig('remediation_impact_chart.png', dpi=300)
plt.close()
print("✅ Saved 'remediation_impact_chart.png'")
