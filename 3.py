import pandas as pd

# Load the dataset
df = pd.read_csv('AB_NYC_2019.csv')


# Advanced Data Manipulation
def analyze_pricing_trends(df):
    # Analyze pricing trends across neighborhoods and room types
    pricing_summary = pd.pivot_table(df, values='price', index='neighbourhood_group', columns='room_type',
                                     aggfunc='mean')
    return pricing_summary


def transform_data_for_metric_analysis(df):
    # Transform the dataset from wide to long format
    df_long = pd.melt(df, id_vars=['id', 'neighbourhood_group', 'room_type'], value_vars=['price', 'minimum_nights'],
                      var_name='metric', value_name='value')
    return df_long


def classify_listings_by_availability(df):
    # Create availability_status column
    def availability_status(row):
        if row['availability_365'] < 50:
            return 'Rarely Available'
        elif row['availability_365'] <= 200:
            return 'Occasionally Available'
        else:
            return 'Highly Available'

    df['availability_status'] = df.apply(availability_status, axis=1)
    return df


def analyze_trends_by_availability_status(df):
    # Analyze trends and patterns using the new availability_status column
    availability_analysis = df.groupby('availability_status').agg({
        'price': ['mean', 'median'],
        'number_of_reviews': ['mean', 'median'],
        'neighbourhood_group': 'count'
    }).reset_index()
    return availability_analysis


# Descriptive Statistics
def perform_descriptive_statistics(df):
    # Perform descriptive statistics on numeric columns
    desc_stats = df[['price', 'minimum_nights', 'number_of_reviews']].describe()
    return desc_stats


# Time Series Analysis
def time_series_analysis(df):
    # Convert last_review to datetime and set as index
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    df = df.set_index('last_review')

    # Resample to observe monthly trends
    monthly_trends = df.resample('M').agg({
        'number_of_reviews': 'sum',
        'price': 'mean'
    }).dropna()

    # Group by month to analyze seasonal patterns
    df['month'] = df.index.month
    seasonal_patterns = df.groupby('month').agg({
        'number_of_reviews': 'mean',
        'price': 'mean'
    }).reset_index()

    return monthly_trends, seasonal_patterns


# Function to print analysis results
def print_analysis_results(data, message=''):
    if message:
        print(message)
    print(data)


# Main function to execute the task
def main():
    # Analyze pricing trends
    pricing_summary = analyze_pricing_trends(df)
    print_analysis_results(pricing_summary, 'Pricing Trends Summary:')

    # Transform data for metric analysis
    df_long = transform_data_for_metric_analysis(df)
    print_analysis_results(df_long.head(), 'Transformed Data for Metric Analysis:')

    # Classify listings by availability
    df_classified = classify_listings_by_availability(df)
    availability_analysis = analyze_trends_by_availability_status(df_classified)
    print_analysis_results(availability_analysis, 'Trends by Availability Status:')

    # Perform descriptive statistics
    desc_stats = perform_descriptive_statistics(df)
    print_analysis_results(desc_stats, 'Descriptive Statistics:')

    # Perform time series analysis
    monthly_trends, seasonal_patterns = time_series_analysis(df_classified)
    print_analysis_results(monthly_trends, 'Monthly Trends:')
    print_analysis_results(seasonal_patterns, 'Seasonal Patterns:')

    # Save the results of time series analysis as a CSV file
    monthly_trends.to_csv('time_series_airbnb_data.csv', index=True)


if __name__ == '__main__':
    main()
