import pandas as pd


# Function to load the dataset and print initial information
def load_and_inspect_data(file_path):
    df = pd.read_csv(file_path)
    print("Initial Data Inspection:")
    print(df.head())
    print(df.info())
    return df


# Function to handle missing values
def handle_missing_values(df):
    df['name'].fillna('Unknown', inplace=True)
    df['host_name'].fillna('Unknown', inplace=True)
    df['last_review'].fillna(pd.NaT, inplace=True)
    return df


# Function to categorize listings by price range
def categorize_by_price(df):
    conditions = [
        (df['price'] < 100),
        (df['price'] >= 100) & (df['price'] < 300),
        (df['price'] >= 300)
    ]
    choices = ['Low', 'Medium', 'High']
    df['price_category'] = pd.cut(df['price'], bins=[-1, 99, 299, float('inf')], labels=choices)
    return df


# Function to categorize listings by length of stay
def categorize_by_length_of_stay(df):
    conditions = [
        (df['minimum_nights'] <= 3),
        (df['minimum_nights'] > 3) & (df['minimum_nights'] <= 14),
        (df['minimum_nights'] > 14)
    ]
    choices = ['short-term', 'medium-term', 'long-term']
    df['length_of_stay_category'] = pd.cut(df['minimum_nights'], bins=[-1, 3, 14, float('inf')], labels=choices)
    return df


# Function to remove rows with price equal to 0
def remove_zero_price_rows(df):
    df = df[df['price'] > 0]
    return df


# Function to print DataFrame information with an optional message
def print_dataframe_info(df, message=""):
    print(message)
    print(df.info())
    print(df.isnull().sum())


# Main execution function
def main():
    file_path = 'AB_NYC_2019.csv'  # Update the file path if necessary

    # Load and inspect data
    df = load_and_inspect_data(file_path)

    # Print initial state of the DataFrame
    print_dataframe_info(df, "Before Cleaning:")

    # Handle missing values
    df = handle_missing_values(df)

    # Categorize listings by price and length of stay
    df = categorize_by_price(df)
    df = categorize_by_length_of_stay(df)

    # Remove rows with price equal to 0
    df = remove_zero_price_rows(df)

    # Print final state of the DataFrame
    print_dataframe_info(df, "After Cleaning:")

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv('cleaned_airbnb_data.csv', index=False)


# Run the main function
if __name__ == "__main__":
    main()
