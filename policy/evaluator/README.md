# Starting evaluator

Read [the evaluation contract](../../docs/perpetua/evaluation.md).

This directory contains an evidence-integrity inventory and its regression tests, not a LabVIEW benchmark.
The owner remains the change gate. Run tests with:

```sh
python3 -m unittest discover -s policy/evaluator -p 'test_*.py' -v
python3 policy/evaluator/evaluate.py --check
python3 policy/evaluator/evaluate.py --baseline . --candidate .
```

The last two commands explicitly report missing benchmark evidence and unmeasured tool quality.
The initial evaluator cannot accept changes or mark improvement. A future evaluator needs independent verification
before use, and accepted criteria before interpreting a measurement as goal completion.
