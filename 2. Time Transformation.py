# Convert trip start and end times from text to datetime format
combined_df['started_at'] = pd.to_datetime(combined_df['started_at'])
combined_df['ended_at'] = pd.to_datetime(combined_df['ended_at'])

# Verify the data type changes and check the dataframe structure
combined_df.info()

# Calculate the duration of each ride in minutes
combined_df['ride_length'] = (combined_df['ended_at'] - combined_df['started_at']).dt.total_seconds() / 60

# Preview the first few rows to verify the calculated ride lengths
combined_df[['started_at', 'ended_at', 'ride_length']].head()
