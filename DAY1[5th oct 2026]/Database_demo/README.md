# Cinema Booking Database Demo

This beginner Python project demonstrates how to save cinema booking records in a SQLite database and read them back. It prints the results twice: first as regular Python data using `sqlite3`, and then as a pandas DataFrame.

## What the program does

When you run `database_demo.py`, it:

1. Imports Python's built-in `sqlite3` module and connects to `cinema.db`.
2. Creates a database cursor, which sends SQL statements to SQLite.
3. Creates a `bookings` table if it does not already exist.
4. Inserts two sample bookings: *Solar Drift* and *Midnight Code*.
5. Commits the inserts so they are saved in the database.
6. Runs a `SELECT` query and prints the rows with `fetchall()`.
7. Runs the query through pandas and prints the results as a DataFrame.

The database file is stored in the current working directory (normally the project folder when you run the command below).

## What you can learn

- **Connecting to a database:** `sqlite3.connect()` opens or creates a SQLite database file.
- **Creating a table:** `CREATE TABLE IF NOT EXISTS` defines the table once and avoids an error if it already exists.
- **Choosing column types:** `INTEGER`, `TEXT`, and `REAL` represent integer, text, and numeric values.
- **Using a primary key:** `booking_id INTEGER PRIMARY KEY` gives each booking a unique database ID.
- **Executing SQL:** A cursor runs SQL statements such as `CREATE TABLE`, `INSERT`, and `SELECT`.
- **Saving changes:** `commit()` persists changes made by insert statements.
- **Reading query results:** `fetchall()` returns query results as a Python list of rows.
- **Using pandas with SQL:** `pd.read_sql_query()` loads SQL results into a DataFrame for tabular display.

## Booking fields

| Field | Description |
|---|---|
| `booking_id` | Automatically assigned unique booking ID |
| `movie` | Movie title |
| `seats` | Number of seats booked |
| `amount` | Booking amount |

## Requirements

- Python 3
- pandas

`sqlite3` is included with Python. Install pandas if it is not already available:

```powershell
python -m pip install pandas
```

## Run

From the project directory, run:

```powershell
python database_demo.py
```

The output includes the rows as a Python list, followed by a pandas table. Exact booking IDs and the number of rows depend on the contents of `cinema.db`.

## Important note

The two sample bookings are inserted every time the script runs. Running it repeatedly therefore creates duplicate sample rows. To start over, remove `cinema.db` before running the script again.
