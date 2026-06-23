# (Data loading and combining handled in previous step)

# Preview the first few rows of the data
combined_df.head()

# Review column names, non-null counts, and initial data types
combined_df.info()

# Count missing values across all columns
combined_df.isnull().sum()

# View initial summary statistics to check for data anomalies like negative trip lengths
combined_df['ride_length'].describe()

# Filter out trips shorter than 1 minute to remove test data or false starts
clean_df = combined_df[combined_df['ride_length'] >= 1].copy()

# View summary statistics of the cleaned dataset to verify the filter
clean_df['ride_length'].describe()

# Extract the day name from the start date for weekly analysis
clean_df['day_of_week'] = clean_df['started_at'].dt.day_name()

# Preview the first few rows to verify the updated dataset structure
clean_df[['started_at', 'ride_length', 'day_of_week']].head()

# Verify the updated minimum ride length and display final trip counts by user type
print(f"Minimum Ride Length: {clean_df['ride_length'].min()} minute")
print("\n Grand Total Rides by User Type ")
print(clean_df["member_casual"].value_counts())
