import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy plot
datasets = ['RuleTaker', 'CounterBench\n(Alpha)', 'CounterBench\n(Backdoor)', 'FOLIO', 'Overall\nAggregate']
accuracies = [100.00, 92.50, 65.00, 72.55, 91.64]
colors = ['#2b5c8f', '#3690c0', '#67a9cf', '#02818a', '#e6550d']

bars = ax1.bar(datasets, accuracies, color=colors, width=0.55, edgecolor='black', linewidth=1.2)
ax1.set_ylim(0, 115)
ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax1.set_title('Reasoning Accuracy Across Benchmarks', fontsize=14, fontweight='bold', pad=12)

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha='center', va='bottom', fontsize=11, fontweight='bold')

# Latency plot
latencies = [0.30, 0.15, 0.14, 2.04, 0.37]
bars2 = ax2.bar(datasets, latencies, color='#41b6c4', width=0.55, edgecolor='black', linewidth=1.2)
ax2.set_ylabel('Average Inference Time (ms/query)', fontsize=12, fontweight='bold')
ax2.set_title('Inference Efficiency (Execution Latency)', fontsize=14, fontweight='bold', pad=12)

for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05, f"{yval:.2f} ms", ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('submission/performance_metrics.png', dpi=300)
print("Saved submission/performance_metrics.png")
