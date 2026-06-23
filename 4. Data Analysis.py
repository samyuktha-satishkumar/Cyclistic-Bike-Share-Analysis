# Check the maximum ride duration in the cleaned data
clean_df['ride_length'].max()

# Identify the most common day of the week for bike trips
clean_df['day_of_week'].mode()[0]

# Calculate the overall average ride length for each user type
clean_df.groupby('member_casual')['ride_length'].mean()

# Set a strict chronological order for the days of the week
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
clean_df['day_of_week'] = pd.Categorical(clean_df['day_of_week'], categories=order, ordered=True)

# Group by user type and day of the week to calculate average durations and trip counts
final_summary = clean_df.groupby(['member_casual', 'day_of_week'], observed=False)['ride_length'].agg(['mean', 'count']).reset_index().sort_values(by='count', ascending=False)
final_summary.to_csv('final_summary.csv', index=False)

# Group by user type and bike type to find structural preferences
bike_summary = clean_df.groupby(['member_casual', 'rideable_type']).size().reset_index(name='total_trips')
bike_summary.to_csv('bike_summary.csv', index=False)

# Extract time dimensions for detailed monthly and hourly trends
clean_df['month'] = clean_df['started_at'].dt.month_name()
clean_df['hour_of_day'] = clean_df['started_at'].dt.hour

# Combine user habits across months, days, and hours into a single time summary file
time_summary = clean_df.groupby(['member_casual', 'month', 'day_of_week', 'hour_of_day'], observed=False)['ride_length'].agg(['count', 'mean']).reset_index()
time_summary.columns = ['member_casual', 'month', 'day_of_week', 'hour_of_day', 'total_trips', 'average_duration'] 
time_summary.to_csv('time-summary.csv', index=False)

# Group by user type and starting station, averaging coordinates and calculating totals
station_summary = clean_df.groupby(['member_casual', 'start_station_name'], observed=False).agg(
    start_lat=('start_lat', 'mean'),
    start_lng=('start_lng', 'mean'),
    total_trips=('ride_length', 'count'),
    average_duration=('ride_length', 'mean')
).reset_index()

# Drop any rows where the station name is missing or blank
station_summary = station_summary.dropna(subset=['start_station_name'])

# Export the final map summary dataset for Tableau visualization
station_summary.to_csv('station_summary.csv', index=False)
