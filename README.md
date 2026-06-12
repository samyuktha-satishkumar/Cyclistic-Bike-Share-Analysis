# Google Data Analytics Capstone: Cyclistic Case Study

## Introduction
In this case study, I preformed the real-world tasks of a junior data analyst for a fictional bike-share company in Chicago- **Cyclistic**. To answer the core business questions, I followed the steps of the data analysis process: **Ask, Prepare, Process, Analyze, Share, and Act**.

## Quick Links
1. **Analysis Tool:** Python via Google Colab Notebook
2. **Data Source:** [divvy_tripdata](https://divvy-tripdata.s3.amazonaws.com/index.html)

---
## Background

### About the company
In 2016, Cyclistic launched a successful bike-share offering. Since then, the program has grown to a fleet of 5,824 bicycles that are geotracked and locked into a network of 692 stations across Chicago. The bikes can be unlocked from one station and returned to any other station in the system anytime. Until now, Cyclistic’s marketing strategy relied on building general awareness and appealing to broad consumer segments. One approach that helped make these things possible was the flexibility of its pricing plans: single-ride passes, full-day passes, and annual memberships. Customers who purchase single-ride or full-day passes are referred to as casual riders. Customers who purchase annual memberships are Cyclistic members. 

Cyclistic’s finance analysts have concluded that annual members are much more profitable than casual riders. Although the pricing flexibility helps Cyclistic attract more customers, Moreno believes that maximizing the number of annual members will be key to future growth. Rather than creating a marketing campaign that targets all-new customers, Moreno believes there is a solid opportunity to convert casual riders into members. She notes that casual riders are already aware of the Cyclistic program and have chosen Cyclistic for their mobility needs.

Moreno has set a clear goal: Design marketing strategies aimed at converting casual riders into annual members. In order to do that, however, the team needs to better understand how annual members and casual riders differ, why casual riders would buy a membership, and how digital media could affect their marketing tactics. Moreno and her team are interested in analyzing the Cyclistic historical bike trip data to identify trends.

### Scenario

I am a junior data analyst working on the marketing analyst team at Cyclistic, a bike-share company in Chicago. The director of marketing believes the company’s future success depends on maximizing the number of annual memberships. Therefore, the team wants to understand how casual riders and annual members use Cyclistic bikes differently. From these insights, the team will design a new marketing strategy to convert casual riders into annual members. But first, Cyclistic executives must approve my recommendations, so they must be backed up with compelling data insights and professional data visualizations.

------------------------

## Key Phases of the study

### Ask Phase
Cyclistic’s finance team has concluded that annual members are much more profitable than casual riders. My manager and the director of marketing, Lily Moreno, believes that **maximizing our annual memberships** is the absolute key to the company's future growth.
Three questions will guide the future marketing program: 
1. How do annual members and casual riders use Cyclistic bikes differently?
2.  Why would casual riders buy Cyclistic annual memberships?
3.  How can Cyclistic use digital media to influence casual riders to become members?
  
   Moreno has assigned me the first question to answer: **How do annual members and casual
riders use Cyclistic bikes differently?**

#### The Business Task
The core objective of this project was to analyze Cyclistic’s historical trip data to uncover the distinct behavioral trends and usage patterns between **casual riders** and **annual members**.

By understanding exactly how these two groups utilize the bike-share network differently, I will design a targeted marketing strategy to convert existing casual riders into annual subscribers. This shift is critical for driving long-term customer lifetime value and fueling company growth. Because the final presentation is for the detail-oriented Cyclistic Executive Team, the final findings and visualizations must be rigorous, highly polished, and visually compelling.

---
### Prepare Phase
The analysis covers the most recent 12 consecutive months of historical trip records available (May 2025 to April 2026).

#### Data Properties & Integrity:
  
The data is spread across 12 separate monthly .csv files, combining for a total of **5,697,455** raw rows.

#### The Columns:

 Each file contains a flat table layout with the following fields: 
 
 1. unique ride IDs
 2.  bicycle categories (classic, electric, or docked)
 3.  timestamps
 4.  station markers
 5.   whether the user is a "member" or a "casual" rider.

#### Privacy:
The data is strictly anonymized. It contains zero Personally Identifiable Information (PII)—no names, addresses, or credit cards are attached to the entries.

#### Anomaly Note:
The data file for January 2026 was wrapped in a zip package labeled 202601, but the internal text file was accidentally labeled 202501-divvy-tripdata.csv. I scanned the internal timestamps to verify that the transactions safely belong to 2026 despite the typo.

---

### Process Phase
Because Excel cannot open files with more than 1 million rows, I chose **Python via Google Colab** to clean and process millions of records smoothly.

#### 1. Selective Column Loading & Memory Optimization
To prevent running out of cloud RAM, I loaded the 12 individual files using glob and usecols to only extract the 7 columns essential to our business task. During ingestion, I immediately downcasted text variables into memory-saving categorical data types.

```python
import pandas as pd
import glob
import os
# get the csv files from google drive
path = '/content/drive/MyDrive/Cyclistic_Data'
all_files = glob.glob(os.path.join(path, "*.csv"))
# Columns we actually need
columns_to_keep = [
    'ride_id', 'rideable_type', 'started_at', 'ended_at',
    'start_station_name', 'end_station_name', 'member_casual'
]
optimized_list = []
print("Starting cloud-optimized file processing...")
for filename in all_files:
    print(f"Processing: {os.path.basename(filename)}")
    df = pd.read_csv(filename, usecols=columns_to_keep)

    # Convert text columns to 'category' types to save massive memory space
    df['member_casual'] = df['member_casual'].astype('category')
    df['rideable_type'] = df['rideable_type'].astype('category')

    optimized_list.append(df)

# 3. Combine everything into one giant table stacked vertically
print("\nMerging all files into a master dataset...")
all_trips = pd.concat(optimized_list, ignore_index=True)

print("\n--- ONLINE MERGE SUCCESSFUL ---")
print(f"Total Rows Combined: {all_trips.shape[0]:,}")
print(f"Total Columns Kept: {all_trips.shape[1]}")
```
#### 2. Trip Durations
Converted the started_at and ended_at time columns from plain text strings into real datetime64 objects so Python can calculate chronological differences. Created a new column called ride_length to compute the total duration of each bike trip in minutes.

```python
# Convert 'started_at' and 'ended_at' columns to datetime objects
all_trips['started_at'] = pd.to_datetime(all_trips['started_at'])
all_trips['ended_at'] = pd.to_datetime(all_trips['ended_at'])
# 1. Calculate ride length in minutes
all_trips['ride_length'] = (all_trips['ended_at'] - all_trips['started_at']).dt.total_seconds() / 60
# 2. Extract the day of the week (1=Monday, 2=Tuesday, ..., 7=Sunday)
all_trips['day_of_week'] = all_trips['started_at'].dt.isocalendar().day
all_trips[['started_at', 'ended_at', 'ride_length', 'day_of_week']].head()
```

#### 3. Outlier Removal
I searched for records where ride_length was less than or equal to zero minutes. I filtered out the errors and stored only clean records in a new table for analysis.

```python
# Find out how many rows have a ride length of 0 or negative minutes
bad_rows = all_trips[all_trips['ride_length'] <= 0].shape[0]
print(f"Number of rows with invalid/negative trip durations: {bad_rows:,}")
# Keep only the rows where ride_length is greater than 0
all_trips_clean = all_trips[all_trips['ride_length'] > 0].copy()
print(f"New cleaned row count: {all_trips_clean.shape[0]:,}")
```

#### The Result:
Exactly 29 anomaly rows were caught and deleted, leaving us with a pristine dataset of **5,697,426** rows ready for grouping.

---

### Analyze 
I aggregated the cleaned data to compare how the two user groups behave across different days of the week. The data tells a very clear story of two completely different customer profiles.

 **Data Aggregation:**  Summarized the clean table to isolate how annual members and casual riders behave over time.
**Baseline Overview:** Compared overall mean and maximum ride lengths grouped by user type.

```python
import numpy as np
print("DESCRIPTIVE ANALYSIS")
# 1. Oveall Comparison: Calculate mean and max ride lengths grouped by user type
overall_stats = all_trips_clean.groupby('member_casual')['ride_length'].agg(['mean', 'max']).reset_index()
print("\nOverall Ride Length Statistics (in Minutes):")
print(overall_stats)
# 2. Analyze by Day of the Week: Calculate average duration and total number of rides
weekly_analysis = all_trips_clean.groupby(['member_casual', 'day_of_week']).agg(
    average_ride_length=('ride_length', 'mean'),
    number_of_rides=('ride_id', 'count')
).reset_index()
# Sort the results chronologically by day of the week (1=Monday to 7=Sunday)
weekly_analysis = weekly_analysis.sort_values(by=['member_casual', 'day_of_week'])
print("\nRide Statistics by Day of the Week (1=Monday, 7=Sunday):")
print(weekly_analysis)
Chronological Grouping: Grouped data by user type and day of the week (1=Monday to 7=Sunday) to calculate daily ride volume and average duration.
```

#### Key Finding 1: The Trip Duration Gap
Casual Riders average 22.45 minutes per trip.
Annual Members average 12.44 minutes per trip.
Takeaway: Casual riders consistently keep bikes out for almost twice as long as our subscribers.

#### Key Finding 2: Weekly Inversion of Ride Volume
* Members (The Commuters): Their trip volume stays consistently massive from Monday through Friday, hitting a peak on Thursday with 602,097 rides. Their activity drops significantly on weekends. They use our fleet as a functional daily utility to get to work or school.

* Casuals (The Leisure Users): Their trip volumes are low during the week but spike drastically on weekends, peaking on Saturday with 416,578 rides. They treat the service as a fun weekend activity for relaxation, tourism, and exercise.

🚀 Act Phase: Strategic Recommendations
Based on our findings, we should not market memberships to casual riders as a "commute to work" option—they clearly do not use the bikes that way. Instead, we should pitch a membership that fits their weekend lifestyle.

Launch a "Weekend Warrior" Subscription: Introduce a seasonal or annual membership tier that is valid exclusively from Friday afternoons through Sunday nights. This captures the massive weekend leisure audience who cannot justify the price of a full weekly subscription.

Implement App Alerts for Long Rides: Create an automated mobile notification that pops up whenever a casual rider passes 20 minutes on a single trip. Show them a clean, digital math calculator showing exactly how much cash they would save by upgrading to a membership plan.

Run Hotspot Marketing Near Parks and Beaches: Deploy physical advertisements and digital signs specifically at our top 10 highest-traffic weekend leisure docking stations. Promote member-only benefits, such as the ability to reserve a bike in advance or zero unlock fees on Saturdays.
