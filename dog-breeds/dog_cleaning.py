import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('breed_data.csv')
df = df.drop_duplicates()
df['Breed Group'] = df['Breed Group'].str.replace(" »", "", regex=False)
df['Height'] = df['Height'].str.replace(" inches", "", regex=False)
df['Height'] = df['Height'].str.replace(" (male)", "", regex=False)
df['Height'] = df['Height'].str.replace(" (TOY)", "", regex=False)
df['Weight'] = df['Weight'].str.replace(" (TOY)", "", regex=False)
df['Weight'] = df['Weight'].str.replace(" (male)", "", regex=False)
df['Weight'] = df['Weight'].str.replace(" pounds", "", regex=False)



df['Life Expectancy'] = df['Life Expectancy'].str.replace(" years", "", regex=False)


print(df)
df.to_csv("dog_data.csv", index=False)


def extract_avg(range_str):
    if isinstance(range_str, str):
        try:
            # Remove any non-numeric characters (e.g., extra spaces)
            range_str = range_str.replace(' ', '')
            # Split the range and calculate the average
            low, high = range_str.split('-')
            return (float(low) + float(high)) / 2
        except ValueError:
            return None  # If the format doesn't match, return None
    return None

# Apply function to both columns
df['Height'] = df['Height'].apply(extract_avg)
df['Life Expectancy'] = df['Life Expectancy'].apply(extract_avg)
df['Weight'] = df['Weight'].apply(extract_avg)


# Ensure that both columns are converted to numeric (float) type
df['Height'] = pd.to_numeric(df['Height'], errors='coerce')
df['Life Expectancy'] = pd.to_numeric(df['Life Expectancy'], errors='coerce')
df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')



# Check for any remaining non-numeric entries
print(df[['Height', 'Life Expectancy']].dtypes)

# Total sample size
print(f"Total sample size: {len(df)}\n")

# Counts of categorical variables
print("Counts of categorical variables:")
for col in df.select_dtypes(include=['object', 'category']).columns:
    print(f"\n{col}:\n{df[col].value_counts()}")

# Summary statistics for numeric variables
print("\nSummary statistics for numeric variables:")
print(df.describe())



plt.figure(figsize=(10, 6))
sns.regplot(x='Weight', y='Life Expectancy', data=df, scatter_kws={'alpha':0.5}, line_kws={'color': 'red'})

plt.title("Relationship between Dog Weight and Life Expectancy")
plt.xlabel("Weight (pounds)")
plt.ylabel("Life Expectancy (years)")
plt.show()


plt.figure(figsize=(10, 6))
sns.regplot(x='Height', y='Life Expectancy', data=df, scatter_kws={'alpha':0.5}, line_kws={'color': 'red'})

plt.title("Relationship between Dog Height and Life Expectancy")
plt.xlabel("Height (inches)")
plt.ylabel("Life Expectancy (years)")
plt.show()



plt.figure(figsize=(12, 6))
sns.boxplot(x='Breed Group', y='Life Expectancy', data=df)

plt.title("Life Expectancy Comparison by Breed Group")
plt.xlabel("Breed Group")
plt.ylabel("Life Expectancy (years)")
plt.xticks(rotation=20)  # Rotate x-axis labels if they are too long
plt.show()
