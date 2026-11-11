# Day 1 – Python & Data Analysis Basics (5th Oct 2026)

Exercises from **Day 1** of the AI training program (5th Oct – 30th Nov 2026). This folder covers the fundamentals of Python for data work: NumPy arrays, pandas DataFrames, charts with Matplotlib and Seaborn, reading CSV / JSON / text files, and storing data in a SQLite database.

Each subfolder is a small, standalone project with its own `README.md` that explains it in detail.

## Folder structure

```
DAY1[5th oct 2026]/
├── Database_demo/                    # SQLite + pandas: cinema bookings
├── pandas and matplotlib exercise/   # Employee training data analysis and charts
├── python basics/                    # Product sales DataFrame and NumPy basics
├── python_project1/                  # Structured, semi-structured and unstructured data practice
└── main.txt                          # Notes on Python basics and exercises
```

## Projects

### 1. `Database_demo` – Cinema Booking Database

Saves cinema booking records in a SQLite database (`cinema.db`) and reads them back.

- Connects to SQLite with Python's built-in `sqlite3` module
- Creates a `bookings` table (`booking_id`, `movie`, `seats`, `amount`)
- Inserts sample bookings, commits them, and reads them with `fetchall()`
- Loads the same query into a pandas DataFrame with `pd.read_sql_query()`

Run: `python database_demo.py`

> Note: the sample rows are inserted every time the script runs, so repeated runs create duplicates. Delete `cinema.db` to start fresh.

### 2. `pandas and matplotlib exercise` – Employee Training Analysis

Analyses a small dataset of eight employees across HR, IT, and Finance.

- Displays, selects, and filters rows (by department, score, completion status)
- Adds a calculated `Passed` column (score ≥ 75 → Pass)
- Computes averages, minimums, maximums, and NumPy statistics
- Sorts and groups data by department
- Plots department averages and training-hour totals (Matplotlib) and a score box plot (Seaborn)

Run: `python pandas_exercise.py`

### 3. `python basics` – Python Data Basics

Beginner examples with tabular data and arrays.

- `data_basics.py` – builds a product sales DataFrame, selects and sorts data, calculates totals, groups sales by product, and shows a bar chart
- `numpy_basics.py` – creates a NumPy array of prices and prints its mean, max, and min

Run: `py .\data_basics.py` or `py .\numpy_basics.py`

### 4. `python_project1` – Python Data Analysis Practice

A collection of scripts that work with different kinds of data.

| Data type | Scripts | Sample data |
|---|---|---|
| Basics | `hello.py`, `main.py`, `python basics.py`, `numpy_basics.py`, `pandas matplotlib exercises.py` | — |
| Structured (CSV / SQLite) | `structred_demo.py`, `structured_assignment.py`, `database_demo.py` | `ev_sessions.csv`, `library_loans.csv`, `cinema.db` |
| Semi-structured (JSON) | `semistructred.py`, `semi_structured_assignment.py` | `support_tickets.json`, `festival_events.json` |
| Unstructured (text) | `unstructred_demo.py`, `unstructured_assignment.py` | `incident_notes.txt`, `wildlife_report.txt` |

Highlights: reading CSVs with pandas, flattening nested JSON with `pandas.json_normalize()`, counting and searching words in text files, and querying SQLite into a DataFrame.

Run any script from inside the folder, e.g. `python structured_assignment.py`. Put filenames with spaces in quotes.

### 5. `main.txt`

Notes covering the Python basics and exercises from this session.

## Requirements

- Python 3
- pandas, NumPy, Matplotlib, Seaborn

`sqlite3` and `json` come with Python and need no installation.

```bash
python -m pip install pandas numpy matplotlib seaborn
```

On Windows, you can use `py` instead of `python` if that's how Python is set up on your machine.

## How to run

1. Clone the repository and open a terminal.
2. Install the requirements above.
3. `cd` into the project folder you want to try (scripts use relative paths to their sample data).
4. Run the script with `python <script_name>.py`.

Scripts that draw charts open a window; close it to let the script finish.

## Topics learned on Day 1

- Python variables, lists, loops, conditionals, and file reading
- NumPy arrays and descriptive statistics
- pandas: selecting, filtering, adding columns, sorting, grouping, aggregation
- Data visualisation with Matplotlib and Seaborn
- Working with structured (CSV, SQLite), semi-structured (JSON), and unstructured (text) data
- Basic SQL: `CREATE TABLE`, `INSERT`, `SELECT`, `commit()`
