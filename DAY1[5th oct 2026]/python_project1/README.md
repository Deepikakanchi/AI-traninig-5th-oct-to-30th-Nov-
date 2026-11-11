# Python Data Analysis Practice

This repository contains small, standalone Python learning exercises. The examples progress from basic Python and array operations to working with tabular, JSON, text, and SQLite data. Several scripts also demonstrate summaries and visualizations with Pandas, Matplotlib, and Seaborn.

The scripts are intended for learning and experimentation. They use the sample files included in this folder and generally print results to the terminal. Some scripts display charts in a separate window.

## Learning topics

- Python scripts, variables, lists, loops, conditionals, and file reading
- NumPy arrays and descriptive statistics
- Pandas DataFrames, row and column selection, filtering, new columns, sorting, grouping, and aggregation
- Reading CSV files with Pandas
- Loading nested JSON with Python and flattening it with `pandas.json_normalize()`
- Searching plain-text files and counting words or occurrences
- Reading a SQLite database query into a Pandas DataFrame
- Creating basic bar charts with Matplotlib and Seaborn

## Requirements

- Python 3
- NumPy
- Pandas
- Matplotlib
- Seaborn

Install the third-party packages using pip:

```bash
python -m pip install numpy pandas matplotlib seaborn
```

The examples use the Python standard-library modules `json` and `sqlite3` as well; these do not need to be installed separately.

To confirm Python is available, run:

```bash
python --version
```

If your system uses the `py` launcher instead, substitute `py` for `python` in the commands below.

## Getting started

1. Open a terminal in the project folder.
2. Install the packages listed above.
3. Run any exercise by passing its filename to Python. For example:

   ```bash
   python numpy_basics.py
   python structured_assignment.py
   python "pandas matplotlib exercises.py"
   ```

Run scripts from this folder because the data exercises refer to their sample files using relative paths. For filenames containing spaces, put the filename in quotes. Chart examples may open a GUI window; close the window to let the script finish.

## Exercises

### Python and numerical analysis

| File | What it demonstrates |
|---|---|
| `hello.py` | Basic `print()` statements. |
| `main.py` | A simple PyCharm starter script and a function call. |
| `python basics.py` | Builds a small product DataFrame; inspects, filters, and selects data; calculates totals; groups and sorts results; plots sales. |
| `numpy_basics.py` | Creates a NumPy array and calculates its mean, maximum, and minimum. |
| `pandas matplotlib exercises.py` | Creates an employee training DataFrame; filters and sorts records; calculates statistics and department summaries; draws Matplotlib and Seaborn charts. |

### Structured data: CSV and SQLite

| File | Input | What it demonstrates |
|---|---|---|
| `structred_demo.py` | `ev_sessions.csv` | Reads EV charging sessions and inspects the data, columns, shape, types, and selected fields. |
| `structured_assignment.py` | `library_loans.csv` | Selects loan fields, filters fines, adds a fine-status column, calculates average borrowed days, and totals fines by book category. |
| `database_demo.py` | `cinema.db` | Reads the SQLite `bookings` table into a Pandas DataFrame. |

### Semi-structured data: JSON

| File | Input | What it demonstrates |
|---|---|---|
| `semistructred.py` | `support_tickets.json` | Loads ticket records, accesses nested customer details, handles an optional priority field, and flattens JSON into a DataFrame. |
| `semi_structured_assignment.py` | `festival_events.json` | Loads event records, accesses nested location data, checks optional features, and normalizes JSON into a DataFrame. |

### Unstructured data: plain text

| File | Input | What it demonstrates |
|---|---|---|
| `unstructred_demo.py` | `incident_notes.txt` | Reads a text report, counts words, and searches for a term. |
| `unstructured_assignment.py` | `wildlife_report.txt` | Counts words and occurrences of a term, checks whether it appears, and prints matching lines. |

## Sample data files

- `ev_sessions.csv` — EV session identifiers, charging stations, cities, duration, energy, and amount.
- `library_loans.csv` — loan identifiers, member names, book categories, borrowed days, and fines.
- `festival_events.json` — event names, nested location information, visitor counts, and optional features.
- `support_tickets.json` — ticket identifiers, nested customer information, issues, tags, and optional priority.
- `incident_notes.txt` — plain-text incident notes used by the text-reading demo.
- `wildlife_report.txt` — plain-text wildlife report used by the text-search assignment.
- `cinema.db` — SQLite database expected to contain a `bookings` table with booking details.

## Notes

- Each exercise is a separate script; there is no single application entry point or required run order.
- Keep the sample data files in the same folder as the scripts that read them.
- `database_demo.py` expects the `bookings` table to exist in `cinema.db`. The example statements for creating and inserting records are present as commented-out code in that script.
- The project includes filenames such as `structred_demo.py` and `semistructred.py`; use the filenames exactly as shown when running them.
