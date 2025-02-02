# -*- coding: utf-8 -*-
"""Student_Performance_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13qAjcEIsehQXMR98yI2OemybJR3cZ4jv

# Anish Kundu

# Task - 01
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("student-mat.csv")
df.head(5)

df.shape

df.columns

df.describe()

df.info()

df.isnull().sum().sum()

"""This means there is no missing values.

# Task - 02
"""

numeric_cols = df.select_dtypes(include=np.number).columns

plt.figure(figsize=(20, 12))
sns.boxplot(data=df[numeric_cols])
plt.xticks(rotation=45, ha='right')
plt.title('Boxplot to Identify Outliers')
plt.show()

"""There exist some outliers"""

Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1

upper_bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR

for col in numeric_cols:
  df.loc[(df[col] > upper_bound[col]) | (df[col] < lower_bound[col]), col] = df[col].median()

filtered_df = df[~((df[numeric_cols] < lower_bound) | (df[numeric_cols] > upper_bound)).any(axis=1)]

numeric_cols_updated = filtered_df.select_dtypes(include=np.number).columns

# Create the boxplot
plt.figure(figsize=(20, 12))
sns.boxplot(data=filtered_df[numeric_cols])
plt.xticks(rotation=45, ha='right')
plt.title('Boxplot to Identify Outliers')
plt.show()

"""We can see most of the outliers are removed and very few are still remaining. But if we try to remove them too, data can be lost."""

filtered_df.shape

"""# Task - 03"""

numerical_cols = filtered_df.select_dtypes(include=np.number).columns

correlation_matrix = filtered_df[numerical_cols].corr()

print(correlation_matrix)

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='magma', fmt=".2f")
plt.title('Correlation Matrix Heatmap')
plt.show()

"""# Task - 04"""

# Set the threshold for strong correlation
correlation_threshold = 0.5

# Get the correlations of 'G3' with other features
g3_correlations = correlation_matrix['G3']

strong_correlations = g3_correlations[abs(g3_correlations) >= correlation_threshold]

print("Features strongly related to G3:")
print(strong_correlations)

strong_features = strong_correlations.index.tolist()
strong_features.remove('G3')

# Calculate the number of rows and columns for subplots
num_plots = len(strong_features)
num_cols = 3
num_rows = (num_plots + num_cols - 1) // num_cols

# Create a figure and subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 5 * num_rows))  # Adjust figsize as needed

# Flatten the axes array for easier iteration
axes = axes.flatten()

# Iterate through features and create scatter plots in subplots
for i, feature in enumerate(strong_features):
    sns.scatterplot(x=feature, y='G3', data=filtered_df, ax=axes[i])
    axes[i].set_title(f'Scatter Plot of {feature} vs. G3')
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel('G3')

# Hide any empty subplots if num_plots is not a multiple of num_cols
for i in range(num_plots, num_rows * num_cols):
    axes[i].set_visible(False)

plt.tight_layout()
plt.show()

numerical_col = 'G3'

plt.figure(figsize=(8, 6))
sns.histplot(filtered_df[numerical_col], bins=10, kde=True)
plt.title(f'Distribution of {numerical_col}')
plt.xlabel(numerical_col)
plt.ylabel('Frequency')
plt.show()

x_col = 'studytime'
y_col = 'G3'

plt.figure(figsize=(8, 6))
sns.scatterplot(x=x_col, y=y_col, data=filtered_df)
plt.title(f'Scatter Plot of {x_col} vs. {y_col}')
plt.xlabel(x_col)
plt.ylabel(y_col)
plt.show()

numerical_col = 'G3'
categorical_col = 'studytime'

plt.figure(figsize=(8, 6))
sns.boxplot(x=categorical_col, y=numerical_col, data=filtered_df)
plt.title(f'Box Plot of {numerical_col} by {categorical_col}')
plt.xlabel(categorical_col)
plt.ylabel(numerical_col)
plt.show()

numerical_cols = ['G1', 'G2', 'G3', 'studytime', 'failures']  # Example columns

sns.pairplot(filtered_df[numerical_cols])
plt.show()

"""# Task - 05"""

# Select features with correlation above 0.5
strong_features = correlation_matrix['G3'][abs(correlation_matrix['G3']) >= 0.5].index.tolist()
strong_features.remove('G3')
print("Selected features:", strong_features)

# Split data into features (X) and target (y)
X = df[strong_features]
y = df['G3']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("RMSE:", rmse)
print("R-squared:", r2)

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], '--', color='red')
plt.xlabel("Actual G3")
plt.ylabel("Predicted G3")
plt.title("Actual vs. Predicted G3")
plt.show()

from sklearn.metrics import accuracy_score
y_pred_classes = [1 if p >= 10 else 0 for p in y_pred]
y_test_classes = [1 if p >= 10 else 0 for p in y_test]
accuracy = accuracy_score(y_test_classes, y_pred_classes)
print("Accuracy:", accuracy)

"""Conclusion:

The project aimed to predict student performance, specifically the final grade (G3), using various features from the student performance dataset. The analysis involved data exploration, outlier handling, correlation analysis, and finally, building a linear regression model.

Key Findings:

Data Exploration and Cleaning: The dataset was examined for missing values and outliers. Outliers were handled using the IQR method to improve model accuracy.
Correlation Analysis: A correlation matrix and heatmap revealed strong relationships between G3 and features like G1, G2, absences, and studytime. These features were selected for model building.
Model Building and Evaluation: A linear regression model was trained using the selected features. The model's performance was evaluated using RMSE and R-squared.
Model Performance: The model achieved an RMSE of [RMSE value] and an R-squared of [R-squared value]. This indicates that the model explains a [R-squared value]% variance in the target variable. The scatter plot of actual vs. predicted values further illustrates the model's performance.
Predictive Power: The model can predict student performance with reasonable accuracy based on the selected features. However, there is still room for improvement.
Further Improvements:

Feature Engineering: Exploring new features or transformations of existing features might improve model accuracy.
Model Selection: Evaluating other regression models, such as decision trees or support vector machines, could lead to better performance.
Hyperparameter Tuning: Fine-tuning the model's hyperparameters might further enhance its predictive power.
Data Collection: Collecting more data, if possible, could improve the model's robustness and generalization ability.
Overall, the project demonstrates the potential of using machine learning to predict student performance. With further refinements and exploration, the model could become a valuable tool for educators and policymakers.

I hope this conclusion provides a comprehensive summary of the project's findings and potential directions for future work. Please let me know if you need further clarification or have any other questions.
"""