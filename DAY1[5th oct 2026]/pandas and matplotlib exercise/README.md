# Pandas Employee Training Exercise

A beginner-friendly Python exercise using a small employee training dataset to practice data inspection, filtering, calculations, grouping, sorting, and plotting.

## Dataset

The script creates a pandas DataFrame with eight employees and these columns:

- `Employee` — employee name
- `Department` — HR, IT, or Finance
- `Training_Hours` — hours of training completed
- `Assessment_Score` — assessment score
- `Completed` — whether the employee completed training
- `Passed` — calculated from the assessment score (`Pass` for scores of 75 or higher; otherwise `Fail`)

## What the exercise covers

1. Displaying all rows, the first four rows, or selected columns
2. Filtering employees by department, assessment score, and completion status
3. Combining filter conditions
4. Adding a calculated `Passed` column
5. Calculating averages, minimums, and maximums
6. Sorting and grouping data by department
7. Counting department membership and training completion
8. Calculating statistics with NumPy
9. Plotting department score averages and training-hour totals with Matplotlib
10. Comparing department assessment scores with a Seaborn box plot

## Requirements

Python 3 and the following packages:

- pandas
- numpy
- matplotlib
- seaborn

Install the packages from a terminal:

```powershell
python -m pip install pandas numpy matplotlib seaborn
```

## Run the exercise

Open a terminal in this folder and run:

```powershell
python pandas_exercise.py
```

The script prints the DataFrame and calculation results, then opens three charts. Keep `README.md` and `pandas_exercise.py` in the same folder.
