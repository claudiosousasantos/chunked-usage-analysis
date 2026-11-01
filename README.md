# Chunked Usage Analysis

A Python script that processes a usage data file in small pieces (chunks) instead of loading it all at once, a technique for working with files too large to fit in memory.

## How it works
- Creates a sample CSV of subscriber usage events (data, voice, and SMS)
- Reads the file in chunks of 5 rows with `pd.read_csv(..., chunksize=5)`
- Summarizes each chunk with `groupby`, keeping only the small partial totals
- Combines the partial totals and adds them up per subscriber and usage type
- Reshapes the result into one row per subscriber with `.unstack()`
- Flags subscribers who exceed plan limits: over 5,000 MB of data, over 100 voice minutes, or over 50 SMS
- Lists the heaviest data users

## Example results (sample data)
| Subscriber | Data (MB) | Voice (min) | SMS | Over limit |
|------------|-----------|-------------|-----|------------|
| S001       | 1,700     | 75          | 5   | none       |
| S002       | 1,000     | 120         | 65  | voice, SMS |
| S003       | 10,500    | 10          | 2   | data       |

## How to run
```bash
python usage_chunking.py
```
This creates `usage_events.csv` in the same folder when run.

## What I learned
- Using `chunksize` in `pd.read_csv()` to read a large file piece by piece
- Why chunking works for totals: a sum of partial sums equals the overall sum
- Using `groupby(level=[...])` to regroup after combining results that have a multi-level index
- Using `.unstack(fill_value=0)` to turn a category level into columns
- Using `.rename(columns={...})` to give columns clearer names with units
- Creating True/False flag columns by comparing usage to plan limits

## Limitations
- The sample file has only 14 rows, so the chunk size of 5 is just to demonstrate the idea. Real use would have chunks of tens or hundreds of thousands of rows.
- This approach works for sums and counts. Averages and medians can't be combined this way without extra steps.

## Dependencies
Requires pandas:
```bash
pip install pandas
```
