# Google Data Analytics Capstone: Cyclistic Case Study

# Introduction
In this case study, I am performing the real-world tasks of a junior data analyst for a fictional bike-share company in Chicago, Cyclistic. To answer our core business questions, I am walking through the complete data analysis lifecycle: Ask, Prepare, Process, Analyze, Share, and Act.

# Quick Links
Analysis Tool: Python via Google Colab Notebook
Data Source: [divvy_tripdata](https://divvy-tripdata.s3.amazonaws.com/index.html)

🎯 Ask Phase
Cyclistic’s finance team has concluded that annual members are much more profitable than casual riders. My manager and the director of marketing, Lily Moreno, believes that maximizing our annual memberships is the absolute key to the company's future growth.

The Core Problem
We need to design a targeted marketing strategy to convert our existing casual riders into annual members. To do that, we first need to answer a foundational question: How do annual members and casual riders use Cyclistic bikes differently?

🗂️ Prepare Phase
Our analysis covers the most recent 12 consecutive months of historical trip records available (May 2025 to April 2026).

Data Properties & Integrity:
The Scale: The data is spread across 12 separate monthly .csv files, combining for a total of 5,697,455 raw rows.

The Columns: Each file contains a flat table layout tracking unique ride IDs, bicycle categories (classic, electric, or docked), timestamps, station markers, and a column indicating whether the user is a "member" or a "casual" rider.

Privacy: The data is strictly anonymized. It contains zero Personally Identifiable Information (PII)—no names, addresses, or credit cards are attached to the entries.

Anomaly Note: The data file for January 2026 was wrapped in a zip package labeled 202601, but the internal text file was accidentally labeled 202501-divvy-tripdata.csv. I scanned the internal timestamps to verify that the transactions safely belong to 2026 despite the typo.

🛠️ Process Phase
Because Excel cannot open files with more than 1 million rows, I chose Python via Google Colab to clean and process our millions of records smoothly.

Data Cleaning Checklist:
Converted the started_at and ended_at time columns from plain text strings into real datetime64 objects so Python can calculate chronological differences.

Created a new column called ride_length to compute the total duration of each bike trip in minutes.

Created a new column called day_of_week where 1 represents Monday and 7 represents Sunday.

Dropped location coordinates to speed up cloud processing speeds.

Outlier Removal: I searched for records where ride_length was less than or equal to zero minutes. This happens occasionally when staff test the bike locks or service equipment.

The Result: Exactly 29 anomaly rows were caught and deleted, leaving us with a pristine dataset of 5,697,426 rows ready for grouping.

📊 Analyze & Share Phases
I aggregated our cleaned data to compare how our two user groups behave across different days of the week. The data tells a very clear story of two completely different customer profiles.

Key Finding 1: The Trip Duration Gap
Casual Riders average 22.45 minutes per trip.

Annual Members average 12.44 minutes per trip.

Takeaway: Casual riders consistently keep bikes out for almost twice as long as our subscribers.

Key Finding 2: Weekly Inversion of Ride Volume
Members (The Commuters): Their trip volume stays consistently massive from Monday through Friday, hitting a peak on Thursday with 602,097 rides. Their activity drops significantly on weekends. They use our fleet as a functional daily utility to get to work or school.

Casuals (The Leisure Users): Their trip volumes are low during the week but spike drastically on weekends, peaking on Saturday with 416,578 rides. They treat the service as a fun weekend activity for relaxation, tourism, and exercise.

🚀 Act Phase: Strategic Recommendations
Based on our findings, we should not market memberships to casual riders as a "commute to work" option—they clearly do not use the bikes that way. Instead, we should pitch a membership that fits their weekend lifestyle.

Launch a "Weekend Warrior" Subscription: Introduce a seasonal or annual membership tier that is valid exclusively from Friday afternoons through Sunday nights. This captures the massive weekend leisure audience who cannot justify the price of a full weekly subscription.

Implement App Alerts for Long Rides: Create an automated mobile notification that pops up whenever a casual rider passes 20 minutes on a single trip. Show them a clean, digital math calculator showing exactly how much cash they would save by upgrading to a membership plan.

Run Hotspot Marketing Near Parks and Beaches: Deploy physical advertisements and digital signs specifically at our top 10 highest-traffic weekend leisure docking stations. Promote member-only benefits, such as the ability to reserve a bike in advance or zero unlock fees on Saturdays.
