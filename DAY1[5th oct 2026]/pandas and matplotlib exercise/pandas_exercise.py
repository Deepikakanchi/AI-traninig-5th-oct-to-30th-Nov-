import pandas as pd

data = {
"Employee": ["Aisha", "Rahul", "Neha", "Omar", "Priya", "Karan", "Fatima","deep"],
"Department": ["HR", "IT", "Finance", "IT", "HR", "Finance", "IT", "HR"],
"Training_Hours": [12, 18, 10, 22, 15, 8, 20, 14],
"Assessment_Score": [78, 88, 72, 91, 84, 69, 95, 80],
"Completed": ["Yes", "Yes", "No", "Yes", "Yes", "No", "Yes", "Yes"]
}

df = pd.DataFrame(data)
print(df)


# 1. Display the complete DataFrame.
print(df)
# 2. Display only the first 4 rows.
print(df.head(4))

# 3. Display only these columns:
# Employee
# Assessment_Score
print(df[["Employee","Assessment_Score"]])

# 4. Show only employees from the IT department.
print(df[df["Department"]=="IT"])

# 5. Show employees whose Assessment_Score is greater than 80.
print(df[df["Assessment_Score"]>80])

# 6. Show employees who completed the training:
# Completed = Yes
print(df[df["Completed"]=="Yes"])

# 7. Show employees who:
# belong to IT
# and scored above 85
print(df[(df["Department"] == "IT") & (df["Assessment_Score"] > 85)])

# 8. Create a new column called:
# Passed
# Condition:
# Assessment_Score >= 75
# Store:
# Pass
# Fail
df["Passed"] = (df["Assessment_Score"] >= 75).map({True: "Pass", False: "Fail"})
# 9. Find the average assessment score.
print(df["Assessment_Score"].mean())
# 10. Find:
# highest assessment score
print(df["Assessment_Score"].max())
# lowest assessment score
print(df["Assessment_Score"].min())
# 11. Find the average training hours.
print(df["Training_Hours"].mean())

# 12. Sort employees by Assessment_Score from highest to lowest.
print(df.sort_values("Assessment_Score", ascending=False))

# 13. Group by Department and find the average assessment score.
print(df.groupby("Department")["Assessment_Score"].mean())

# 14. Group by Department and find the total training hours.
print(df.groupby("Department")["Training_Hours"].sum())

# 15. Count how many employees belong to each department.
print(df["Department"].value_counts())
# 16. Count how many employees completed training.
print((df["Completed"]=="Yes").value_counts())
# 17. Using NumPy, take the assessment scores:
import numpy as np
scores = df["Assessment_Score"].to_numpy()
# Find:
# mean
print(np.mean(scores))
# maximum
print(np.max(scores))
# minimum
print(np.min(scores))

# standard deviation
print(np.std(scores))

# 18. Create a bar chart showing average score by department.
import matplotlib.pyplot as plt

average_scores = df.groupby("Department")["Assessment_Score"].mean()
average_scores.plot(kind="bar", title="Average Assessment Score by Department",
                    xlabel="Department", ylabel="Average Assessment Score")
plt.tight_layout()
plt.show()

# 19. Create a bar chart showing total training hours by department.
total_training_hours = df.groupby("Department")["Training_Hours"].sum()
total_training_hours.plot(kind="bar", title="Total Training Hours by Department",
                          xlabel="Department", ylabel="Total Training Hours")
plt.tight_layout()
plt.show()

# 20. Create a Seaborn chart comparing:
# Department vs Assessment_Score
import seaborn as sns

sns.boxplot(data=df, x="Department", y="Assessment_Score")
plt.title("Assessment Scores by Department")
plt.tight_layout()
plt.show()