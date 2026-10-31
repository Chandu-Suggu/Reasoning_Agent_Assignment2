import json
import os
import re

def create_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.13.2"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    def add_md(text):
        nb["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": text.strip().splitlines(keepends=True)
        })

    def add_code(code):
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.strip().splitlines(keepends=True)
        })

    # Read clean definitions from reasoning_engine.py
    with open('reasoning_engine.py', 'r', encoding='utf-8') as f:
        engine_code = f.read()

    # 1. Title and Intro
    add_md("""# AI Assignment 2: Classical AI Reasoning System
## Natural Language Knowledge Base → Internal Representation → Classical Reasoning → True/False

**Course Assignment**: Autonomous Logical Entailment System  
**Pipeline**: Natural Language → Syntactic/Semantic Parser → Knowledge Representation (Facts + Horn Rules / CNF / Causal Graphs) → Classical Symbolic Reasoning Engine → Truth Prediction (`True` or `False`)

> **Strict Compliance**: The entire deductive inference and decision-making pipeline is executed strictly using classical AI reasoning algorithms (Forward Chaining with CWA, Backward Chaining with Unification, Resolution Refutation Theorem Proving, and Structural Causal $do$-calculus). Directly using generative AI to produce final True/False predictions is strictly prohibited and avoided.""")

    # 2. Imports and Environment Setup
    add_md("""## 1. Imports and Setup""")
    add_code("""import os
import sys
import re
import time
import json
from typing import List, Dict, Set, Tuple, Any, Optional
import pandas as pd
import sympy
from sympy.logic.inference import satisfiable
from sympy.logic.boolalg import And, Or, Not, Implies, Xor, Equivalent, to_cnf

print("SymPy version:", sympy.__version__)
print("Environment successfully initialized for classical symbolic reasoning.")""")

    # 3. Complete Implementation of Symbolic Reasoning Engine
    add_md("""## 2. Complete Implementation of Logical Representation & Classical Reasoning Engines
This cell contains the complete end-to-end implementation:
- **Logical Representations**: `Term`, `Literal`, `HornRule`, `Clause`
- **Robinson's First-Order Unification Algorithm** (with occurs check)
- **Generalized Modus Ponens (GMP) Forward Chaining** with Closed-World Assumption (Negation-as-Failure)
- **Goal-Directed Backward Chaining** with Depth-First Search and Cycle Detection (Memoization/Tabling)
- **Resolution Refutation Theorem Proving** with Unit Preference and Set-of-Support Heuristics
- **Structural Causal Graph Engine** with Pearl's $do$-calculus (Abduction-Action-Prediction)
- **Natural Language Knowledge Base & Semantic Parsers**
- **Unified `ReasoningAgent` Orchestrator**""")

    clean_code = re.sub(r'^"""[\s\S]*?"""', '', engine_code).strip()
    clean_code = re.sub(r"if __name__ == '__main__':[\s\S]*$", '', clean_code).strip()
    add_code(clean_code)

    # 4. Assignment Example Demonstration
    add_md("""## 3. Demonstration on Problem Statement Example
Problem Statement from PDF Section 2:
```
Context:
Bob is young.
Bob is kind.
If someone is young, then they are smart.
If someone is smart and kind, then they are successful.

Query:
Bob is successful.

Expected Answer: True
Derivation:
Young(Bob) -> Smart(Bob)
and
Smart(Bob) ^ Kind(Bob) -> Successful(Bob)
```""")
    add_code("""agent = ReasoningAgent()

kb_text = \"\"\"Bob is young.
Bob is kind.
If someone is young, then they are smart.
If someone is smart and kind, then they are successful.\"\"\"
query_text = "Bob is successful."

result = agent.solve(kb_text, query_text)
print("=== Problem Statement Example Execution ===")
print("Context:\\n", kb_text)
print("\\nQuery:", query_text)
print("\\nPredicted Label:", result["prediction"])
print("Reasoning Engine:", result["engine"])
print("Execution Latency:", f"{result['execution_time_ms']:.3f} ms")
print("\\nFormal Reasoning Trace:")
for step in result["reasoning_trace"]:
    print("  *", step)""")

    # 5. Backward Chaining Demonstration on Assignment Example
    add_md("""## 4. Verification via Goal-Directed Backward Chaining
To demonstrate multi-algorithm consistency, we also verify the query via top-down Backward Chaining with Robinson's Unification.""")
    add_code("""# Define the problem explicitly in First-Order Horn form
facts = {
    Literal("young", [Term("bob")]),
    Literal("kind", [Term("bob")])
}
rules = [
    HornRule(Literal("smart", [Term("x", is_var=True)]), [Literal("young", [Term("x", is_var=True)])]),
    HornRule(Literal("successful", [Term("x", is_var=True)]), [
        Literal("smart", [Term("x", is_var=True)]),
        Literal("kind", [Term("x", is_var=True)])
    ])
]
q_goal = Literal("successful", [Term("bob")])

bc_status, bc_trace = backward_chain(q_goal, facts, rules)
print("Backward Chaining Proven:", bc_status)
print("Backward Chaining Proof Tree Trace:")
for step in bc_trace:
    print("  *", step)""")

    # 6. Evaluation on Public Datasets
    add_md("""## 5. Comprehensive Empirical Evaluation Across Public Benchmarks
In compliance with Section 3 and Section 5 of the assignment specifications, we evaluate our system across:
1. **RuleTaker Dataset** (AllenAI synthetic multi-hop deduction)
2. **CounterBench Dataset** (Deterministic counterfactual and causal graph benchmarks)
3. **FOLIO Dataset** (Yale-LILY First-Order Logic reasoning benchmark)""")

    add_code("""records = []
results_summary = {}

# 1. RuleTaker
rt_file = 'data/ruletaker/test_sample.jsonl'
if os.path.exists(rt_file):
    print("Evaluating RuleTaker Benchmark...")
    with open(rt_file, 'r', encoding='utf-8') as f:
        rt_samples = [json.loads(line) for line in f][:1000]
    rt_correct = 0
    t0 = time.perf_counter()
    for i, s in enumerate(rt_samples):
        res = agent.solve(s['context'], s['question'])
        actual = (s['label'].strip().lower() == 'entailment')
        pred = res['prediction']
        if pred == actual: rt_correct += 1
        records.append({"id": f"ruletaker_{i:04d}", "dataset": "RuleTaker", "predicted_label": pred, "ground_truth": actual, "execution_time_ms": res['execution_time_ms']})
    rt_time = time.perf_counter() - t0
    results_summary['RuleTaker'] = {'count': len(rt_samples), 'correct': rt_correct, 'accuracy': (rt_correct/len(rt_samples))*100.0, 'total_time_s': rt_time, 'avg_time_ms': (rt_time/len(rt_samples))*1000.0}

# 2. CounterBench Alpha
cb_file = 'data/counterbench/data_balanced_alpha_V1.json'
if os.path.exists(cb_file):
    print("Evaluating CounterBench Alpha...")
    with open(cb_file, 'r', encoding='utf-8') as f:
        cb_samples = json.load(f)
    cb_correct = 0
    t0 = time.perf_counter()
    for i, s in enumerate(cb_samples):
        res = agent.solve(s['given_info'], s['question'])
        actual = (str(s['answer']).strip().lower() in ['yes', 'true'])
        pred = res['prediction']
        if pred == actual: cb_correct += 1
        records.append({"id": f"counterbench_alpha_{i:04d}", "dataset": "CounterBench-Alpha", "predicted_label": pred, "ground_truth": actual, "execution_time_ms": res['execution_time_ms']})
    cb_time = time.perf_counter() - t0
    results_summary['CounterBench-Alpha'] = {'count': len(cb_samples), 'correct': cb_correct, 'accuracy': (cb_correct/len(cb_samples))*100.0, 'total_time_s': cb_time, 'avg_time_ms': (cb_time/len(cb_samples))*1000.0}

# 3. CounterBench Backdoor
cb_bd_file = 'data/counterbench/data_balanced_backdoor_V2.json'
if os.path.exists(cb_bd_file):
    print("Evaluating CounterBench Backdoor...")
    with open(cb_bd_file, 'r', encoding='utf-8') as f:
        cb_bd_samples = json.load(f)
    cb_bd_correct = 0
    t0 = time.perf_counter()
    for i, s in enumerate(cb_bd_samples):
        res = agent.solve(s['given_info'], s['question'])
        actual = (str(s['answer']).strip().lower() in ['yes', 'true'])
        pred = res['prediction']
        if pred == actual: cb_bd_correct += 1
        records.append({"id": f"counterbench_backdoor_{i:04d}", "dataset": "CounterBench-Backdoor", "predicted_label": pred, "ground_truth": actual, "execution_time_ms": res['execution_time_ms']})
    cb_bd_time = time.perf_counter() - t0
    results_summary['CounterBench-Backdoor'] = {'count': len(cb_bd_samples), 'correct': cb_bd_correct, 'accuracy': (cb_bd_correct/len(cb_bd_samples))*100.0, 'total_time_s': cb_bd_time, 'avg_time_ms': (cb_bd_time/len(cb_bd_samples))*1000.0}

# 4. FOLIO
folio_file = 'data/folio/folio-validation.jsonl'
if os.path.exists(folio_file):
    print("Evaluating FOLIO...")
    with open(folio_file, 'r', encoding='utf-8') as f:
        folio_samples = [json.loads(line) for line in f]
    folio_correct = 0
    t0 = time.perf_counter()
    for i, s in enumerate(folio_samples):
        res = agent.solve(s.get('premises-FOL', s.get('premises')), s.get('conclusion-FOL', s.get('conclusion')))
        actual = (s['label'].strip().lower() == 'true')
        pred = res['prediction']
        if pred == actual: folio_correct += 1
        records.append({"id": f"folio_{i:04d}", "dataset": "FOLIO", "predicted_label": pred, "ground_truth": actual, "execution_time_ms": res['execution_time_ms']})
    folio_time = time.perf_counter() - t0
    results_summary['FOLIO'] = {'count': len(folio_samples), 'correct': folio_correct, 'accuracy': (folio_correct/len(folio_samples))*100.0, 'total_time_s': folio_time, 'avg_time_ms': (folio_time/len(folio_samples))*1000.0}

df = pd.DataFrame(records)
total_q = len(df)
total_correct = (df['predicted_label'] == df['ground_truth']).sum()
overall_acc = (total_correct / total_q) * 100.0
total_time = sum(v['total_time_s'] for v in results_summary.values())
avg_latency = (total_time / total_q) * 1000.0

print("\\n" + "=" * 75)
print("FINAL BENCHMARK EVALUATION SUMMARY")
print("=" * 75)
print(f"{'Dataset':<25} | {'Count':<7} | {'Correct':<8} | {'Accuracy (%)':<12} | {'Avg Latency (ms)':<16}")
print("-" * 75)
for dname, stats in results_summary.items():
    print(f"{dname:<25} | {stats['count']:<7} | {stats['correct']:<8} | {stats['accuracy']:<12.2f} | {stats['avg_time_ms']:<16.2f}")
print("-" * 75)
print(f"{'OVERALL AGGREGATE':<25} | {total_q:<7} | {total_correct:<8} | {overall_acc:<12.2f} | {avg_latency:<16.2f}")
print("=" * 75)""")

    # 7. Generation of submission.csv
    add_md("""## 6. Generation of `submission.csv`
Generates the submission file containing query ID and predicted labels (`True` or `False`).""")
    add_code("""sub_df = df[['id', 'predicted_label']].rename(columns={'predicted_label': 'prediction'})
os.makedirs('submission', exist_ok=True)
output_path = 'submission/submission.csv'
sub_df.to_csv(output_path, index=False)

print(f"Generated {output_path} successfully!")
print(f"Total rows: {len(sub_df)}")
print("\\nFirst 10 rows of submission.csv:")
print(sub_df.head(10))""")

    # 8. Reasoning Traces Examples
    add_md("""## 7. Examples of Diverse Reasoning Traces
Showcasing detailed reasoning traces across all reasoning modes:
1. Multi-hop deduction via Forward Chaining
2. Goal-directed search via Backward Chaining
3. Resolution Refutation Theorem Proving deriving empty clause $\\square$
4. Causal counterfactual evaluation via graph surgery""")

    add_code("""print("=== 1. FORWARD CHAINING TRACE ===")
kb_demo = "The bear eats the mouse. The mouse is green. If someone is green and they eat the bear then they visit the mouse."
res_fc = agent.solve(kb_demo, "The mouse visits the mouse.")
for t in res_fc['reasoning_trace']:
    print("  *", t)

print("\\n=== 2. CAUSAL GRAPH DO-INTERVENTION TRACE ===")
causal_demo = "We know that Ziklo causes Blaf, Blaf and Ziklo together cause Trune, Trune causes not Vork, and Vork causes Lumbo."
res_causal = agent.solve(causal_demo, "Would Lumbo occur if not Ziklo instead of Ziklo?")
for t in res_causal['reasoning_trace']:
    print("  *", t)

print("\\n=== 3. RESOLUTION REFUTATION TRACE ===")
c1 = Clause([("Smart_bob", False), ("Successful_bob", True)])
c2 = Clause([("Smart_bob", True)])
c3 = Clause([("Successful_bob", False)]) # Negated query
is_unsat, res_trace = resolution_theorem_prover([c1, c2, c3])
for t in res_trace:
    print("  *", t)""")

    # Save to file
    out_file = 'submission/reasoning_agent.ipynb'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2)
    print(f"Created notebook {out_file} with {len(nb['cells'])} cells.")

if __name__ == '__main__':
    create_notebook()
