import pandas as pd

# ---------- Create sample data and save as a CSV ----------
events = [
    {"subscriber_id": "S001", "usage_type": "data",  "amount": 500},
    {"subscriber_id": "S001", "usage_type": "data",  "amount": 1200},
    {"subscriber_id": "S001", "usage_type": "voice", "amount": 30},
    {"subscriber_id": "S001", "usage_type": "sms",   "amount": 5},
    {"subscriber_id": "S002", "usage_type": "data",  "amount": 300},
    {"subscriber_id": "S002", "usage_type": "voice", "amount": 120},
    {"subscriber_id": "S002", "usage_type": "sms",   "amount": 40},
    {"subscriber_id": "S002", "usage_type": "sms",   "amount": 25},
    {"subscriber_id": "S003", "usage_type": "data",  "amount": 8000},
    {"subscriber_id": "S003", "usage_type": "voice", "amount": 10},
    {"subscriber_id": "S001", "usage_type": "voice", "amount": 45},
    {"subscriber_id": "S003", "usage_type": "sms",   "amount": 2},
    {"subscriber_id": "S002", "usage_type": "data",  "amount": 700},
    {"subscriber_id": "S003", "usage_type": "data",  "amount": 2500},
]
pd.DataFrame(events).to_csv("usage_events.csv", index=False)

# ---------- Process the file in chunks ----------
partial_results = []

for chunk in pd.read_csv("usage_events.csv", chunksize=5):
    partial = chunk.groupby(['subscriber_id', 'usage_type'])['amount'].sum()
    partial_results.append(partial)

# ---------- Combine the partial summaries ----------
combined = pd.concat(partial_results)
final_totals = combined.groupby(level=['subscriber_id', 'usage_type']).sum()

usage_table = final_totals.unstack(fill_value=0)
usage_table = usage_table.rename(columns={
    'data': 'data_mb',
    'voice': 'voice_min',
    'sms': 'sms_count'
})

# ---------- Compare to plan limits ----------
usage_table['data_over'] = usage_table['data_mb'] > 5000
usage_table['voice_over'] = usage_table['voice_min'] > 100
usage_table['sms_over'] = usage_table['sms_count'] > 50

print(usage_table)

# ---------- Heaviest data users ----------
print("\nTop data users:")
print(usage_table.sort_values('data_mb', ascending=False).head(2)[['data_mb']])