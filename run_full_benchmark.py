import os
import json
import time
import pandas as pd
from reasoning_engine import ReasoningAgent

def main():
    agent = ReasoningAgent()
    os.makedirs('submission', exist_ok=True)
    
    print("=" * 70)
    print("AI ASSIGNMENT 2 - CLASSICAL REASONING SYSTEM EVALUATION BENCHMARK")
    print("=" * 70)
    
    records = []
    results_summary = {}

    # 1. RuleTaker Evaluation
    rt_file = 'data/ruletaker/test_sample.jsonl'
    if os.path.exists(rt_file):
        print("\n--> Evaluating RuleTaker Benchmark...")
        with open(rt_file, 'r', encoding='utf-8') as f:
            rt_samples = [json.loads(line) for line in f][:1000]
            
        rt_correct = 0
        t0 = time.perf_counter()
        for i, s in enumerate(rt_samples):
            res = agent.solve(s['context'], s['question'])
            actual = (s['label'].strip().lower() == 'entailment')
            pred = res['prediction']
            if pred == actual:
                rt_correct += 1
            records.append({
                "id": f"ruletaker_{i:04d}",
                "dataset": "RuleTaker",
                "predicted_label": pred,
                "ground_truth": actual,
                "execution_time_ms": res['execution_time_ms']
            })
        rt_time = time.perf_counter() - t0
        rt_acc = (rt_correct / len(rt_samples)) * 100.0
        results_summary['RuleTaker'] = {
            'count': len(rt_samples),
            'correct': rt_correct,
            'accuracy': rt_acc,
            'total_time_s': rt_time,
            'avg_time_ms': (rt_time / len(rt_samples)) * 1000.0
        }
        print(f"    RuleTaker Accuracy: {rt_correct}/{len(rt_samples)} = {rt_acc:.2f}% | Total Time: {rt_time:.3f}s ({rt_time/len(rt_samples)*1000.0:.2f} ms/query)")

    # 2. CounterBench Alpha Evaluation
    cb_alpha_file = 'data/counterbench/data_balanced_alpha_V1.json'
    if os.path.exists(cb_alpha_file):
        print("\n--> Evaluating CounterBench (Alpha Split)...")
        with open(cb_alpha_file, 'r', encoding='utf-8') as f:
            cb_samples = json.load(f)
            
        cb_correct = 0
        t0 = time.perf_counter()
        for i, s in enumerate(cb_samples):
            res = agent.solve(s['given_info'], s['question'])
            actual = (str(s['answer']).strip().lower() in ['yes', 'true'])
            pred = res['prediction']
            if pred == actual:
                cb_correct += 1
            records.append({
                "id": f"counterbench_alpha_{i:04d}",
                "dataset": "CounterBench-Alpha",
                "predicted_label": pred,
                "ground_truth": actual,
                "execution_time_ms": res['execution_time_ms']
            })
        cb_time = time.perf_counter() - t0
        cb_acc = (cb_correct / len(cb_samples)) * 100.0
        results_summary['CounterBench-Alpha'] = {
            'count': len(cb_samples),
            'correct': cb_correct,
            'accuracy': cb_acc,
            'total_time_s': cb_time,
            'avg_time_ms': (cb_time / len(cb_samples)) * 1000.0
        }
        print(f"    CounterBench Alpha Accuracy: {cb_correct}/{len(cb_samples)} = {cb_acc:.2f}% | Total Time: {cb_time:.3f}s ({cb_time/len(cb_samples)*1000.0:.2f} ms/query)")

    # 3. CounterBench Backdoor Evaluation
    cb_bd_file = 'data/counterbench/data_balanced_backdoor_V2.json'
    if os.path.exists(cb_bd_file):
        print("\n--> Evaluating CounterBench (Backdoor Split)...")
        with open(cb_bd_file, 'r', encoding='utf-8') as f:
            cb_bd_samples = json.load(f)
            
        cb_bd_correct = 0
        t0 = time.perf_counter()
        for i, s in enumerate(cb_bd_samples):
            res = agent.solve(s['given_info'], s['question'])
            actual = (str(s['answer']).strip().lower() in ['yes', 'true'])
            pred = res['prediction']
            if pred == actual:
                cb_bd_correct += 1
            records.append({
                "id": f"counterbench_backdoor_{i:04d}",
                "dataset": "CounterBench-Backdoor",
                "predicted_label": pred,
                "ground_truth": actual,
                "execution_time_ms": res['execution_time_ms']
            })
        cb_bd_time = time.perf_counter() - t0
        cb_bd_acc = (cb_bd_correct / len(cb_bd_samples)) * 100.0
        results_summary['CounterBench-Backdoor'] = {
            'count': len(cb_bd_samples),
            'correct': cb_bd_correct,
            'accuracy': cb_bd_acc,
            'total_time_s': cb_bd_time,
            'avg_time_ms': (cb_bd_time / len(cb_bd_samples)) * 1000.0
        }
        print(f"    CounterBench Backdoor Accuracy: {cb_bd_correct}/{len(cb_bd_samples)} = {cb_bd_acc:.2f}% | Total Time: {cb_bd_time:.3f}s ({cb_bd_time/len(cb_bd_samples)*1000.0:.2f} ms/query)")

    # 4. FOLIO Evaluation
    folio_file = 'data/folio/folio-validation.jsonl'
    if os.path.exists(folio_file):
        print("\n--> Evaluating FOLIO (First-Order Logic Benchmark)...")
        with open(folio_file, 'r', encoding='utf-8') as f:
            folio_samples = [json.loads(line) for line in f]
            
        folio_correct = 0
        t0 = time.perf_counter()
        for i, s in enumerate(folio_samples):
            res = agent.solve(s.get('premises-FOL', s.get('premises')), s.get('conclusion-FOL', s.get('conclusion')))
            actual = (s['label'].strip().lower() == 'true')
            pred = res['prediction']
            if pred == actual:
                folio_correct += 1
            records.append({
                "id": f"folio_{i:04d}",
                "dataset": "FOLIO",
                "predicted_label": pred,
                "ground_truth": actual,
                "execution_time_ms": res['execution_time_ms']
            })
        folio_time = time.perf_counter() - t0
        folio_acc = (folio_correct / len(folio_samples)) * 100.0
        results_summary['FOLIO'] = {
            'count': len(folio_samples),
            'correct': folio_correct,
            'accuracy': folio_acc,
            'total_time_s': folio_time,
            'avg_time_ms': (folio_time / len(folio_samples)) * 1000.0
        }
        print(f"    FOLIO Validation Accuracy: {folio_correct}/{len(folio_samples)} = {folio_acc:.2f}% | Total Time: {folio_time:.3f}s ({folio_time/len(folio_samples)*1000.0:.2f} ms/query)")

    # Aggregate Metrics
    df = pd.DataFrame(records)
    total_q = len(df)
    total_correct = (df['predicted_label'] == df['ground_truth']).sum()
    overall_acc = (total_correct / total_q) * 100.0
    total_time = sum(v['total_time_s'] for v in results_summary.values())
    avg_latency = (total_time / total_q) * 1000.0
    
    print("\n" + "=" * 70)
    print("FINAL BENCHMARK EVALUATION SUMMARY")
    print("=" * 70)
    print(f"{'Dataset':<25} | {'Count':<7} | {'Correct':<8} | {'Accuracy (%)':<12} | {'Avg Latency (ms)':<16}")
    print("-" * 75)
    for dname, stats in results_summary.items():
        print(f"{dname:<25} | {stats['count']:<7} | {stats['correct']:<8} | {stats['accuracy']:<12.2f} | {stats['avg_time_ms']:<16.2f}")
    print("-" * 75)
    print(f"{'OVERALL AGGREGATE':<25} | {total_q:<7} | {total_correct:<8} | {overall_acc:<12.2f} | {avg_latency:<16.2f}")
    print("=" * 70)

    # Export submission.csv
    # The requirement: "contains id and predicted labels"
    sub_df = df[['id', 'predicted_label']].rename(columns={'predicted_label': 'prediction'})
    sub_df.to_csv('submission/submission.csv', index=False)
    print(f"\nSaved submission/submission.csv with {len(sub_df)} rows.")

    # Save summary json for report generation
    with open('submission/benchmark_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            "summary": results_summary,
            "overall": {
                "total_queries": int(total_q),
                "total_correct": int(total_correct),
                "overall_accuracy": float(overall_acc),
                "total_time_seconds": float(total_time),
                "avg_latency_ms": float(avg_latency)
            }
        }, f, indent=2)
    print("Saved submission/benchmark_results.json")

if __name__ == '__main__':
    main()
