import pandas as pd

# Load the dataset
df = pd.read_csv('AB_NYC_2019.csv')


# Data Selection and Filtering
def filter_data(df):
    # Select specific rows and columns using .iloc and .loc
    df_selection = df.loc[:,
                   ['neighbourhood_group', 'price', 'minimum_nights', 'number_of_reviews', 'availability_365']]

    # Filter the dataset to include only listings in specific neighborhoods
    df_filtered = df_selection[df_selection['neighbourhood_group'].isin(['Manhattan', 'Brooklyn'])]

    # Further filter the dataset to include only listings with a price greater than $100 and number_of_reviews greater than 10
    df_filtered = df_filtered[(df_filtered['price'] > 100) & (df_filtered['number_of_reviews'] > 10)]

    # Create a price_category column
    df_filtered['price_category'] = pd.cut(df_filtered['price'], bins=[0, 100, 200, 300, 400, 500, float('inf')],
                                           labels=['0-100', '101-200', '201-300', '301-400', '401-500', '500+'])

    return df_filtered


# Aggregation and Grouping
def aggregate_data(df_filtered):
    # Group the filtered dataset by neighbourhood_group and price_category
    grouped = df_filtered.groupby(['neighbourhood_group', 'price_category']).agg({
        'price': 'mean',
        'minimum_nights': 'mean',
        'number_of_reviews': 'mean',
        'availability_365': 'mean'
    }).reset_index()

    return grouped


# Data Sorting and Ranking
def sort_and_rank_data(df_filtered):
    # Sort the data by price in descending order and by number_of_reviews in ascending order
    sorted_by_price = df_filtered.sort_values(by='price', ascending=False)
    sorted_by_reviews = df_filtered.sort_values(by='number_of_reviews', ascending=True)

    # Create a ranking of neighborhoods based on the total number of listings and the average price
    neighborhood_rank = df_filtered.groupby('neighbourhood_group').agg({
        'price': 'mean',
        'neighbourhood_group': 'size'
    }).rename(columns={'neighbourhood_group': 'total_listings'}).reset_index()
    neighborhood_rank = neighborhood_rank.sort_values(by=['total_listings', 'price'], ascending=[False, True])

    return sorted_by_price, sorted_by_reviews, neighborhood_rank


# Function to print grouped data
def print_grouped_data(grouped_df, message=''):
    if message:
        print(message)
    print(grouped_df)


# Main function to execute the task
def main():
    df_filtered = filter_data(df)
    grouped_df = aggregate_data(df_filtered)
    sorted_by_price, sorted_by_reviews, neighborhood_rank = sort_and_rank_data(df_filtered)

    print_grouped_data(grouped_df, 'Grouped Data:')
    print_grouped_data(neighborhood_rank, 'Neighborhood Ranking:')

    # Save aggregated data to a new CSV file
    grouped_df.to_csv('aggregated_airbnb_data.csv', index=False)


if __name__ == '__main__':
    main()
