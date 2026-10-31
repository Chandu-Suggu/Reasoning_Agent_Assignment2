================================================================================
AI ASSIGNMENT 2: GENERAL-PURPOSE CLASSICAL AI REASONING SYSTEM
================================================================================

COURSE ASSIGNMENT: Autonomous Logical Entailment Reasoning System
PIPELINE: Natural Language Knowledge Base -> Internal Representation -> Classical Reasoning -> True/False
STUDENT SUBMISSION DIRECTORY: submission/

--------------------------------------------------------------------------------
1. SUBMISSION PACKAGE STRUCTURE
--------------------------------------------------------------------------------
submission/
|-- reasoning_agent.ipynb       # Jupyter notebook with complete implementation,
|                               #   printed benchmark accuracy, inference latency,
|                               #   assignment example walkthrough, and CSV generation
|-- report.pdf                  # Comprehensive 5-page technical report describing:
|                               #   1. Chosen internal representations
|                               #   2. Reasoning algorithms used
|                               #   3. Empirical experiments on public benchmarks
|                               #   4. Concrete reasoning traces across paradigms
|-- submission.csv              # Test prediction file containing 'id' and 'prediction'
|                               #   for 2,404 benchmark queries (True / False)
|-- performance_metrics.png     # High-resolution benchmark comparison plot (Accuracy & Latency)
|-- report.typ                  # Typst source document used to compile report.pdf
`-- README.txt                  # System documentation and execution instructions (this file)

--------------------------------------------------------------------------------
2. SYSTEM ARCHITECTURE & COMPLIANCE
--------------------------------------------------------------------------------
In strict compliance with Assignment Rules 1 through 6:
- "The objective is to build a general-purpose reasoning system, not a system
  specifically designed for the released dataset."
- "The private test dataset must not be used during development."
- "Students must not manually create predictions for the private test set."
- "Directly using a generative AI system to produce the final answer to a query
  is not permitted."
- "The final inference must be performed using classical AI reasoning techniques."

Our system achieves this by implementing a pure symbolic AI architecture:
- Natural Language -> Parser -> Internal Representation -> Classical Engine -> Prediction

NO generative AI, LLM prompting, or blackbox heuristics are utilized in the
decision-making or inference loop.

--------------------------------------------------------------------------------
3. INTERNAL LOGICAL REPRESENTATIONS
--------------------------------------------------------------------------------
1. First-Order Terms and Literals:
   - Term: Ground constants c (e.g. 'bob', 'mouse') or logical variables ?x with
     occurs-check support.
   - Literal: Atomic predicate relations P(t_1, ..., t_n) or negated ~P(t_1, ..., t_n).

2. Horn Definite Clauses:
   - Rules of the form: B_1 & B_2 & ... & B_k -> H.
   - Evaluated under the Closed-World Assumption (CWA) and Stratified Negation As
     Failure (NAF).

3. Conjunctive Normal Form (CNF) Clauses:
   - General clauses L_1 \/ L_2 \/ ... \/ L_k for First-Order and Propositional
     Resolution Refutation Theorem Proving.

4. Structural Causal Equations (SCMs):
   - Formalized as M = <U, V, F> following Pearl's causality framework.
   - Directed acyclic graph relationships supporting single causes, joint causes
     (conjunction), disjunctive causes, and inhibitory mechanisms (~child).

--------------------------------------------------------------------------------
4. IMPLEMENTED CLASSICAL REASONING ENGINES
--------------------------------------------------------------------------------
1. Robinson's First-Order Unification Algorithm:
   - Implements Most General Unifier (MGU) computation across terms and compound
     literals with full occurs-check to prevent cyclic self-reference.

2. Generalized Modus Ponens (GMP) Forward Chaining:
   - Evaluates rule antecedents against working memory.
   - Integrates Closed-World Assumption (NAF) for non-monotonic negation.
   - Derives all consequence atoms iteratively until fixed-point closure.

3. Goal-Directed Backward Chaining:
   - Top-down goal reduction using SLD-resolution.
   - Features depth-first search with memoization / tabling (cycle detection) to
     guarantee termination on cyclic knowledge bases.

4. Resolution Refutation Theorem Proving:
   - Proves KB |= alpha by refuting KB /\ ~alpha |- \square (empty clause).
   - Powered by A* Heuristic Search and the Unit Preference heuristic, resolving
     unit clauses and shortest resolvents first.

5. Pearl's 3-Step Counterfactual Algorithm:
   - Step 1 (Abduction): Compute base factual states given background observations.
   - Step 2 (Action): Execute graph surgery do(X = v), severing incoming edges.
   - Step 3 (Prediction): Forward propagation across structural equations.

--------------------------------------------------------------------------------
5. EMPIRICAL BENCHMARK RESULTS
--------------------------------------------------------------------------------
Evaluated across 2,404 public test queries from RuleTaker, CounterBench, and FOLIO:

+-----------------------------+---------------+---------+--------------+------------------+
| Benchmark Dataset           | Total Queries | Correct | Accuracy (%) | Avg Latency (ms) |
+-----------------------------+---------------+---------+--------------+------------------+
| RuleTaker (Test Split)      | 1,000         | 1,000   | 100.00%      | 0.30 ms / query  |
| CounterBench (Alpha Split)  | 1,000         | 925     |  92.50%      | 0.15 ms / query  |
| CounterBench (Backdoor)     |   200         | 130     |  65.00%      | 0.14 ms / query  |
| FOLIO (Validation Split)    |   204         | 148     |  72.55%      | 2.04 ms / query  |
+-----------------------------+---------------+---------+--------------+------------------+
| OVERALL AGGREGATE           | 2,404         | 2,203   |  91.64%      | 0.37 ms / query  |
+-----------------------------+---------------+---------+--------------+------------------+

Total benchmark execution time: 0.888 seconds for 2,404 queries.
Average reasoning latency: 0.37 milliseconds per query.

--------------------------------------------------------------------------------
6. PREREQUISITES & REPRODUCIBILITY
--------------------------------------------------------------------------------
Requirements:
- Python 3.10+ (tested on Python 3.13)
- Standard scientific Python libraries:
    pip install pandas numpy sympy matplotlib

To run the complete system and reproduce all results:
1. Open and execute the Jupyter notebook:
    jupyter notebook submission/reasoning_agent.ipynb
   Or in VS Code / Jupyter Lab, execute all cells sequentially ("Run All").

2. Alternatively, run the stand-alone benchmark script from the root directory:
    python run_full_benchmark.py

3. Both methods will:
   - Print all individual and aggregate benchmark accuracies.
   - Print inference latencies.
   - Print demonstration traces for the PDF problem statement example.
   - Generate / update 'submission/submission.csv'.

4. To recompile report.pdf from Typst source (optional):
    python -c "import typst; typst.compile('submission/report.typ', output='submission/report.pdf')"

================================================================================
END OF README.txt
================================================================================
