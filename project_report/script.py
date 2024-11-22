import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create DataFrame
data = {
    'Turbine_ID': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008'],
    'Project_Name': [f'Project_{i}' for i in range(1, 9)],
    'Facility': ['Community Center', 'Technical College', 'K-12 School', 'Community Center', 
                 'Community Center', 'Technical College', 'K-12 School', 'K-12 School'],
    'State': ['OK', 'NY', 'KS', 'IA', 'OK', 'IA', 'TX', 'KS'],
    'Installed_Capacity': [1.733693, 1.374243, 1.174680, 1.426943, 1.522472, 0.294048, 0.987171, 0.681184],
    'Number_of_Units': [1, 4, 4, 2, 4, 4, 2, 3]
}

df = pd.DataFrame(data)

def analyze_wind_data(df):
    # Set figure size
    plt.figure(figsize=(15, 10))
    
    # 1. State Distribution
    plt.subplot(2, 2, 1)
    state_counts = df['State'].value_counts()
    sns.barplot(x=state_counts.values, y=state_counts.index)
    plt.title('Wind Installations by State')
    plt.xlabel('Count')
    
    # 2. Facility Distribution
    plt.subplot(2, 2, 2)
    facility_counts = df['Facility'].value_counts()
    sns.barplot(x=facility_counts.values, y=facility_counts.index)
    plt.title('Wind Installations by Facility Type')
    plt.xlabel('Count')
    
    # 3. Capacity Distribution
    plt.subplot(2, 2, 3)
    plt.hist(df['Installed_Capacity'], bins=6)
    plt.title('Distribution of Installed Capacity')
    plt.xlabel('Installed Capacity (MW)')
    plt.ylabel('Count')
    
    # 4. Capacity vs Units
    plt.subplot(2, 2, 4)
    plt.scatter(df['Number_of_Units'], df['Installed_Capacity'])
    plt.title('Installed Capacity vs Number of Units')
    plt.xlabel('Number of Units')
    plt.ylabel('Installed Capacity (MW)')
    
    plt.tight_layout()
    plt.savefig('wind_analysis.png')
    
    # Generate summary statistics
    summary = {
        'Total Projects': len(df),
        'States Count': df['State'].nunique(),
        'Total Capacity': df['Installed_Capacity'].sum(),
        'Average Capacity': df['Installed_Capacity'].mean(),
        'State Distribution': df.groupby('State')['Installed_Capacity'].agg(['count', 'sum', 'mean']),
        'Facility Distribution': df.groupby('Facility')['Installed_Capacity'].agg(['count', 'sum', 'mean'])
    }
    
    return summary

# Run analysis
summary = analyze_wind_data(df)

# Print results
print("\nWind Energy Analysis Summary:")
print(f"\nTotal Projects: {summary['Total Projects']}")
print(f"Number of States: {summary['States Count']}")
print(f"Total Installed Capacity: {summary['Total Capacity']:.2f} MW")
print(f"Average Capacity per Installation: {summary['Average Capacity']:.2f} MW")

print("\nState-wise Analysis:")
print(summary['State Distribution'])

print("\nFacility-wise Analysis:")
print(summary['Facility Distribution'])