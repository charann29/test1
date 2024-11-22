import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from scipy import stats

def load_and_clean_data(filepath):
    """Load and clean the wind turbine dataset."""
    df = pd.read_csv(filepath)
    
    # Convert coordinates to numeric, assuming they're in string format
    df[['Latitude', 'Longitude']] = df['Coordinates'].str.split(',', expand=True).astype(float)
    
    # Convert capacity to numeric, handling any unit conversions if needed
    df['Installed_Capacity'] = pd.to_numeric(df['Installed_Capacity'], errors='coerce')
    
    return df

def generate_statistical_summary(df):
    """Generate statistical summary of the dataset."""
    stats_summary = {
        'total_projects': len(df),
        'total_states': df['State'].nunique(),
        'total_capacity': df['Installed_Capacity'].sum(),
        'avg_capacity': df['Installed_Capacity'].mean(),
        'capacity_stats': df['Installed_Capacity'].describe(),
        'state_counts': df['State'].value_counts(),
        'facility_counts': df['Facility'].value_counts()
    }
    return stats_summary

def create_visualizations(df):
    """Create various visualizations for the analysis."""
    # Set style
    plt.style.use('seaborn')
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 20))
    
    # 1. State Distribution
    plt.subplot(4, 1, 1)
    sns.countplot(data=df, y='State', order=df['State'].value_counts().index)
    plt.title('Distribution of Wind Installations by State')
    plt.xlabel('Number of Installations')
    
    # 2. Capacity Distribution
    plt.subplot(4, 1, 2)
    sns.histplot(data=df, x='Installed_Capacity', bins=20)
    plt.title('Distribution of Installed Capacity')
    plt.xlabel('Installed Capacity (MW)')
    
    # 3. Facility Type Distribution
    plt.subplot(4, 1, 3)
    sns.countplot(data=df, y='Facility', order=df['Facility'].value_counts().index)
    plt.title('Distribution of Wind Installations by Facility Type')
    plt.xlabel('Number of Installations')
    
    # 4. Capacity vs Number of Units
    plt.subplot(4, 1, 4)
    sns.scatterplot(data=df, x='Number_of_Units', y='Installed_Capacity')
    plt.title('Installed Capacity vs Number of Units')
    plt.xlabel('Number of Units')
    plt.ylabel('Installed Capacity (MW)')
    
    plt.tight_layout()
    return fig

def create_map(df):
    """Create an interactive map of wind installations."""
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], 
                   zoom_start=4)
    
    # Add markers for each installation
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            popup=f"Project: {row['Project_Name']}<br>"
                  f"Facility: {row['Facility']}<br>"
                  f"Capacity: {row['Installed_Capacity']} MW",
            color='blue',
            fill=True
        ).add_to(m)
    
    return m

def perform_analysis(df):
    """Perform detailed analysis of the data."""
    analysis_results = {
        # Regional Analysis
        'capacity_by_state': df.groupby('State')['Installed_Capacity'].agg(['sum', 'mean', 'count']),
        
        # Facility Analysis
        'capacity_by_facility': df.groupby('Facility')['Installed_Capacity'].agg(['sum', 'mean', 'count']),
        
        # Correlation Analysis
        'capacity_units_correlation': stats.pearsonr(
            df['Number_of_Units'],
            df['Installed_Capacity']
        )[0]
    }
    
    return analysis_results

def generate_report(stats_summary, analysis_results):
    """Generate a summary report of the findings."""
    report = f"""
    Wind for Schools Project Analysis Report
    
    Overview:
    - Total Projects: {stats_summary['total_projects']}
    - States Covered: {stats_summary['total_states']}
    - Total Installed Capacity: {stats_summary['total_capacity']:.2f} MW
    
    Key Findings:
    1. Geographic Distribution:
    - Top 3 states by number of installations:
    {stats_summary['state_counts'].head(3).to_string()}
    
    2. Facility Distribution:
    - Most common facility types:
    {stats_summary['facility_counts'].head(3).to_string()}
    
    3. Capacity Analysis:
    - Average capacity per installation: {stats_summary['avg_capacity']:.2f} MW
    - Correlation between capacity and units: {analysis_results['capacity_units_correlation']:.2f}
    
    4. State-Level Analysis:
    - Top 3 states by total capacity:
    {analysis_results['capacity_by_state']['sum'].sort_values(ascending=False).head(3).to_string()}
    """
    
    return report

def main(filepath):
    """Main function to run the entire analysis."""
    # Load and clean data
    df = load_and_clean_data(filepath)
    
    # Generate statistical summary
    stats_summary = generate_statistical_summary(df)
    
    # Create visualizations
    fig = create_visualizations(df)
    
    # Create map
    map_viz = create_map(df)
    
    # Perform detailed analysis
    analysis_results = perform_analysis(df)
    
    # Generate report
    report = generate_report(stats_summary, analysis_results)
    
    return df, stats_summary, fig, map_viz, analysis_results, report

if __name__ == "__main__":
    # Replace with your actual filepath
    filepath = "wind_schools_data1.csv"
    df, stats, fig, map_viz, analysis, report = main(filepath)
    
    # Save outputs
    fig.savefig('wind_analysis_plots.png')
    map_viz.save('wind_installations_map.html')
    with open('analysis_report.txt', 'w') as f:
        f.write(report)