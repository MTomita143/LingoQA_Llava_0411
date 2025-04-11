# LingoQA Evaluation Setup Instructions

Follow the steps below to set up your environment and obtain the LingoQA score.

## 1. Visit the Repository

Visit the LingoQA repository on GitHub:  
```bash
git clone https://github.com/wayveai/LingoQA.git
```

## 2. Place Your Predictions File

Place your `predictions.csv` file named `path_to_predictions` under `LingoQA`.


## 3. Update the Evaluation Script

Replace the existing evaluation script:

- **Original File:** `LingoQA/Benchmark/evaluate.py`
- **Replacement File:** `evaluate_fixed.py`

Place `evaluate_fixed.py` into the `LingoQA/benchmark/` directory.

## 4. Obtain the LingoQA Score

Run the evaluation script from the repository's root directory:

```bash
python3 ./benchmark/evaluate_fixed.py --predictions_path ./path_to_predictions/predictions.csv
