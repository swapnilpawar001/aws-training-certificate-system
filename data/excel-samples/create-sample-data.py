import pandas as pd

# Create realistic student data
students = [
    {"sixerclass_id": "SIX001", "student_name": "Rahul Sharma", "batch_number": "AWS-2024-001"},
    {"sixerclass_id": "SIX002", "student_name": "Priya Patel", "batch_number": "AWS-2024-001"},
    {"sixerclass_id": "SIX003", "student_name": "Amit Kumar", "batch_number": "AWS-2024-001"},
    {"sixerclass_id": "SIX004", "student_name": "Neha Gupta", "batch_number": "AWS-2024-002"},
    {"sixerclass_id": "SIX005", "student_name": "Vikram Singh", "batch_number": "AWS-2024-002"},
    {"sixerclass_id": "SIX006", "student_name": "Anita Desai", "batch_number": "AWS-2024-002"},
]

df = pd.DataFrame(students)

# Add batch dates (3-month batches)
batch_dates = {
    "AWS-2024-001": {"start": "2024-01-15", "end": "2024-04-15"},
    "AWS-2024-002": {"start": "2024-02-01", "end": "2024-05-01"},
}

df["batch_start_date"] = df["batch_number"].map(
    lambda x: batch_dates.get(x, {}).get("start", "2024-01-01")
)
df["batch_end_date"] = df["batch_number"].map(
    lambda x: batch_dates.get(x, {}).get("end", "2024-04-01")
)

# Reorder columns
df = df[["sixerclass_id", "student_name", "batch_number", 
         "batch_start_date", "batch_end_date"]]

# Save to Excel
output_file = "data/excel-samples/student-data.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"✅ Sample Excel data created: {output_file}")
print(f"📊 Total students: {len(df)}")
print("\n📋 Preview:")
print(df.to_string())

# Also save as CSV for backup
df.to_csv("data/excel-samples/student-data.csv", index=False)
print(f"✅ Also saved as CSV: student-data.csv")
