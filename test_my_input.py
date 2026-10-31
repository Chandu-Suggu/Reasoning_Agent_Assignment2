"""
Interactive Testing Tool for Classical AI Reasoning System
Run this script to test any custom Knowledge Base and Query.

Usage:
    python test_my_input.py
"""

import sys
from reasoning_engine import ReasoningAgent

def interactive_session():
    agent = ReasoningAgent()
    print("=" * 70)
    print("CLASSICAL AI REASONING SYSTEM - INTERACTIVE INPUT TESTER")
    print("=" * 70)
    print("This system performs deductive reasoning using classical AI techniques:")
    print(" - First-Order Forward Chaining with Closed-World NAF")
    print(" - Backward Chaining with Robinson's Unification")
    print(" - Resolution Refutation Theorem Proving")
    print(" - Pearl's Structural Causal Graph Reasoner")
    print("=" * 70)

    # Preset examples for quick testing
    presets = {
        "1": {
            "name": "Assignment PDF Example (Bob is young & kind...)",
            "context": "Bob is young.\nBob is kind.\nIf someone is young, then they are smart.\nIf someone is smart and kind, then they are successful.",
            "query": "Bob is successful."
        },
        "2": {
            "name": "Multi-Hop Deduction with Animals (RuleTaker style)",
            "context": "The bear eats the mouse. The bear is cold. The mouse is green. If someone is green and they eat the bear then they visit the mouse.",
            "query": "The mouse visits the mouse."
        },
        "3": {
            "name": "Closed-World Negation-As-Failure (NAF)",
            "context": "Bob is furry. Charlie is furry. Harry is not green. If someone is not kind then they are quiet.",
            "query": "Charlie is quiet."
        },
        "4": {
            "name": "Causal Counterfactual Reasoning (CounterBench style)",
            "context": "We know that Ziklo causes Blaf, Blaf and Ziklo together cause Trune, Trune causes not Vork, and Vork causes Lumbo.",
            "query": "Would Lumbo occur if not Ziklo instead of Ziklo?"
        }
    }

    print("\nOptions:")
    print("  [1-4] Run a preset example")
    print("  [c]   Enter your own custom Knowledge Base & Query")
    print("  [q]   Quit")
    
    choice = input("\nEnter choice (1/2/3/4/c/q): ").strip().lower()
    
    if choice == 'q':
        print("Exiting.")
        return
        
    if choice in presets:
        ctx = presets[choice]["context"]
        qry = presets[choice]["query"]
        print(f"\n--> Running Preset: {presets[choice]['name']}")
    else:
        print("\nEnter your Knowledge Base (facts and rules).")
        print("End with an empty line or line with 'END':")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END' or (not line.strip() and lines):
                break
            if line.strip():
                lines.append(line)
        ctx = "\n".join(lines)
        
        print("\nEnter your Query statement:")
        qry = input().strip()

    print("\n" + "-" * 70)
    print("EVALUATING REASONING ENGINE...")
    print("-" * 70)
    print(f"Context:\n{ctx}\n")
    print(f"Query: {qry}\n")
    
    result = agent.solve(ctx, qry)
    
    print("=" * 70)
    print(f"PREDICTED VERDICT : {result['prediction']} ({'TRUE / ENTAILED' if result['prediction'] else 'FALSE / NOT ENTAILED'})")
    print(f"REASONING ENGINE  : {result['engine']}")
    print(f"INFERENCE TIME    : {result['execution_time_ms']:.3f} ms")
    print("=" * 70)
    print("\nSTEP-BY-STEP REASONING TRACE:")
    for i, step in enumerate(result['reasoning_trace'], 1):
        print(f"  {i}. {step}")
    print("=" * 70)

if __name__ == '__main__':
    interactive_session()
