# Google Data Analytics Capstone: Cyclistic Case Study

## Introduction
In this case study, I preformed the real-world tasks of a junior data analyst for a fictional bike-share company in Chicago- **Cyclistic**. To answer the core business questions, I followed the steps of the data analysis process: **Ask, Prepare, Process, Analyze, Share, and Act**.

## Quick Links
1. **Data Source:** [divvy_tripdata](https://divvy-tripdata.s3.amazonaws.com/index.html)
2. **Analysis Tool:** Python via [Jupyter Notebook](http://localhost:8889/notebooks/Cyclistic_Analysis.ipynb?)
3. **Interactive Visualizations:** [Explore my Tableau dashboard](https://public.tableau.com/views/Cyclistic_Data_Analysis_Capstone_Project/Sheet1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)


---
## Background and Business context


### About Cyclistic
In 2016, Cyclistic launched a highly successful bike-share offering in Chicago. Over the years, the program expanded into a robust infrastructure featuring a fleet of 5,824 geotracked bicycles locked across a network of 692 stations. The system offered users the flexibility to unlock a bike from any station and return it to any other location across the city grid. 

Historically, Cyclistic’s marketing strategy focused on building broad consumer awareness by offering flexible pricing structures:
* **Casual Riders:** Customers who purchased single-ride or full-day passes.
* **Cyclistic Members:** Customers who committed to full annual memberships.

### The Strategic Shift
While pricing flexibility successfully drove high user acquisition, Cyclistic’s financial analysts concluded that **annual members were significantly more profitable** than casual riders. 

Recognizing this financial dynamic, **Lily Moreno (Cyclistic’s Director of Marketing)** determined that maximizing annual memberships was the definitive key to the company's future growth. Instead of executing an expensive marketing campaign targeting entirely new customers, the marketing analytics team identified a major opportunity to convert existing casual riders into annual members. Because casual riders were already familiar with the Cyclistic brand and actively utilized the infrastructure for their mobility needs, they represented a warm, highly convertible audience.

### The Scenario
As a Junior Data Analyst working on the marketing analyst team, I was tasked with executing an end-to-end data lifecycle analysis to support this strategic pivot. Because Cyclistic executives required highly compelling data insights and professional data visualizations to approve any final marketing recommendations, the project demanded rigorous data cleaning, processing, and visualization standards.

------------------------

## Key Phases of the study

### Ask Phase
#### 1. Business Objective
The core objective of this project was to analyze Cyclistic’s historical trip data to uncover the distinct behavioral trends and usage patterns between **casual riders** and **annual members**. By isolating these trends, the marketing team could design a targeted digital media strategy to convert existing casual riders into high-value annual members, ultimately securing formal approval from the Cyclistic Executive Committee.

#### 2. Primary Business Questions
Three questions to guide the marketing program:
* **How did annual members and casual riders use Cyclistic bikes differently?**
* **Why would casual riders be motivated to purchase a Cyclistic annual membership?**
* **How could digital media be leveraged to influence their marketing tactics?**

#### 3. Core Stakeholders
* **Lily Moreno (Director of Marketing):** Responsible for developing campaigns to promote the bike-share program through print, digital, and social channels.
* **Cyclistic Marketing Analytics Team:** A team of data analysts responsible for collecting, analyzing, and reporting data to guide marketing strategy.
* **Cyclistic Executive Committee:** The detail-oriented executive team responsible for approving the final recommended marketing program.

---
### Prepare Phase
This phase focuses on the data sourcing, structure, and integrity checks required before any code is written. The analysis covers the most recent 12 consecutive months of historical trip records available (May 2025 to April 2026). 

#### 1. Data Structure and Organization:
  
The data is spread across 12 separate monthly .csv files, combining for a total of **5,697,455** raw rows.

##### The Columns:

 Each file contains a flat table layout with the following fields: 
 
 1. unique ride IDs
 2.  bicycle categories (classic, electric, or docked)
 3.  timestamps
 4.  station markers
 5.   whether the user is a "member" or a "casual" rider.

#### 2. ROCCC Assessment (Data Quality Check)
* **Reliable:** Yes. The dataset contains precise, unmanipulated system logs tracking automated dock locks and GPS triggers.
* **Original:** Yes. This is primary first-party operational data collected straight from Cyclistic’s physical network.
* **Comprehensive:** Yes. It accounts for over 5.5 million individual rides with no seasonal gaps.
* **Current:** Yes. The analysis covers a complete, consecutive 12-month trailing cycle.
* **Cited:** Yes. Cleanly documented under an official public data sharing license.
  
#### 3. Privacy:
The data is strictly anonymized. It contains zero Personally Identifiable Information (PII)—no names, addresses, or credit cards are attached to the entries.

#### 4. Anomaly Note:
The data file for January 2026 was wrapped in a zip package labeled 202601, but the internal text file was accidentally labeled 202501-divvy-tripdata.csv. I scanned the internal timestamps to verify that the transactions safely belong to 2026 despite the typo.

---

### Process Phase
In the Process phase. the consolidated dataset is cleaned, transformed, and prepared for analysis.

#### 1. Combining the Data
* The historical trip logs were split across 12 separate monthly CSV files. Manually opening and merging over 5.6 million rows of data across individual files is slow, tedious, and impossible to do in standard spreadsheet tools like Excel.

* I used Python's os library to scan the data folder and automatically list all 12 files. Then, I built a quick loop to read each file one by one and used pd.concat() to stack them vertically into a single consolidated master table containing all **5,697,455** rows.
  
**Python code :** [Data Combining](./1.%20Data%20Combining.py)

#### 2: Transforming Time Fields & Feature Engineering
* The raw timestamp columns (started_at and ended_at) initially loaded as text strings (object data types), which prevented mathematical calculations. Additionally, the dataset lacked clear columns to measure how long each trip lasted or to see which days of the week were busiest.


<img src="https://github.com/user-attachments/assets/4fad16ae-b35f-40db-8c17-2f36b3cd75f9" width="35%" />


* I converted both timestamp columns into proper datetime64[ns] format using pd.to_datetime(). I then calculated a new column called ride_length by finding the difference between the end and start times in minutes, and extracted a day_of_week column using .dt.day_name() to track trip schedules.

<img src="https://github.com/user-attachments/assets/fccf4fd2-6fe1-4b53-a52f-27ea87141487" width="45%" />




**Python code :** [Time transformation](./2.%20Time%20Transformation.py)


#### 3: Data Exploration & Cleaning
* Checking missing data revealed **1,215,745 blank entries** for starting station names and IDs, alongside **1,279,863 blank entries** for ending stations.
<img src="https://github.com/user-attachments/assets/77b3ec41-4c42-48ab-b2fa-530dd209199a" width="35%" />


* Running a statistical summary check (`.describe()`) on the new ride_length column exposed critical data quality issues: a minimum ride duration of **-54.79 minutes**. These negative values represent system errors where a bike's return time was clocked before its departure time. 

<img src="https://github.com/user-attachments/assets/176e1cbe-5c57-4299-983d-7ded20b3c742" width="35%" />

* To prevent system errors from skewing the metrics, I created a filtered DataFrame called `clean_df` that only keeps trips lasting **1 minute or longer** (`ride_length >= 1`). This removed **155,945 false starts and system bugs**, dropping the dataset from 5,697,455 raw entries to **5,541,510 clean rows** ready for analysis.

**Python code :** [Data exploration and cleaning](./3.%20Data%20Exploration%20and%20Cleaning.py)


#### The Result:
* Merged 12 monthly data files into a single master dataset of **5,697,455** initial rows.
* Discovered over **1.2 million missing station names** and an incorrect minimum trip duration of **-54.79 minutes**.
* Set a clear rule to keep only real trips lasting **1 minute or longer**.
* Successfully removed **155,945 recording errors, system tests, and accidental false starts**.
* Finalized the cleaning step with exactly **5,541,510 correct rows** ready for analysis.

---

### Analyze and Share
* With the dataset finalized, I used Python to summarize the data by bike preferences, trip durations, seasonal trends, and locations. This analysis showed a clear difference in how the two groups use the service: **annual members** rely on it for short, routine workweek commutes, while **casual riders** take longer trips for leisure, with usage peaking heavily on weekends and during warmer months.

* To make these insights interactive, I saved the summarized data into separate CSV files (`final_summary.csv`, `bike_summary.csv`, `time-summary.csv`, and `station_summary.csv`) and imported them into Tableau. Splitting the data this way kept the files small, allowing me to build a fast interactive dashboard that maps thousands of trip coordinates and displays weekly patterns smoothly without any slowdown.

**Python code :** [Data Analysis](./4.%20Data%20Analysis.py)

#### Data Visualization & Insights
The core question is: How do annual members and casual riders use Cyclistic bikes differently? To find the answer, let's explore how their trip habits compare across bike options, timeframes, and geographic settings.

#### 1. Bike Preferences
Annual members and casual riders are compared first by the categories of bikes they prefer using. Across the entire network, electric bikes are the clear favorite, making up 65.06% of total trips (41.69% member + 23.37% casual). Classic bikes represent the remaining 34.94% (22.98% member + 11.96% casual). Both groups share the exact same preference, proving that electric bikes drive the clear majority of total rides.

<img src="https://github.com/user-attachments/assets/your-bike-type-chart-id" width="55%" />

#### 2. Time-Based Usage Trends
##### Monthly Activity Trends :
Both casual riders and annual members follow similar seasonal patterns when looking at monthly trip numbers. Rides peak heavily during the summer months from June to August and drop to their lowest counts in December and January. The gap in total ride volume between the two groups shrinks significantly during the peak summer season.
<img src="https://github.com/user-attachments/assets/your-bike-type-chart-id" width="55%" />

##### Weekly Habits :
Comparing the days of the week reveals opposite riding habits between the two groups. Casual riders take significantly more trips over the weekend, showing a sharp rise on Saturdays and Sundays. Meanwhile, annual members maintain high trip volumes from Monday through Friday—peaking on Thursdays—and show a steep drop in activity over the weekend.
  
<img src="https://github.com/user-attachments/assets/your-bike-type-chart-id" width="55%" />

##### Hourly Peak Patterns :
Hourly trip data highlights two clear peak traffic times for annual members. Member activity jumps sharply during morning commute hours around 8:00 AM and spikes again in the evening at 5:00 PM. On the other hand, casual trips grow steadily throughout the day until 5:00 PM before dropping consistently after dark.

These patterns show that annual members mostly use Cyclistic bikes for weekday commuting to work or school, while casual riders use the fleet throughout the day for leisure and open-ended travel.

<img src="https://github.com/user-attachments/assets/your-bike-type-chart-id" width="55%" />


#### 3. Ride Trip Durations
##### By Day of the Week :
Casual riders consistently cycle for nearly double the length of annual members across the entire week. The average ride time for annual members remains short and steady at around 12 minutes every day. In contrast, casual riders show changing habits, with their trip lengths jumping significantly over the weekend to peak at 24 minutes on Saturdays and Sundays.

##### By Month :
Both groups take longer trips during warmer months, but annual members maintain a steady baseline while casual riders are much more affected by the seasons. Casual riders significantly extend their travel times during the spring and summer, peaking around June at over 25 minutes per trip.

##### By Hour of the Day :
Annual members keep their trips short and consistent, averaging 11 to 13 minutes regardless of the time of day. Casual riders follow a completely different pattern: their trip times vary heavily, spiking up to nearly 30 minutes late at night (12:00 AM to 3:00 AM) and rising steadily during afternoon leisure hours.

<img src="https://github.com/user-attachments/assets/your-bike-type-chart-id" width="55%" />

#### 4. Station Locations
Mapping the start and end locations highlights clear differences in where people travel. Casual riders frequently use stations near parks, museums, beaches, and tourist spots. For example, popular tourist destinations like Navy Pier (32,221 trips) and DuSable Lake Shore Drive are dominated by casual users.

Meanwhile, annual members mostly travel around offices, universities, and major transit stations. Their busiest stations are commuter hubs like Kingsbury St & Kinzie St (23,034 trips) and Canal St & Madison St (22,291 trips).

<img src="https://github.com/user-attachments/assets/your-bike-type-chart-id" width="55%" />
<img src="https://github.com/user-attachments/assets/your-bike-type-chart-id" width="55%" />

### Act Phase
Understanding the clear differences between casual riders and annual members allows to create targeted marketing plans. These strategies aim to encourage casual riders to switch to long-term annual memberships.

* Targeted Seasonal Campaigns: Run focused marketing campaigns during the spring and summer months at waterfront tourist locations, public beaches, and popular parks. These are the exact areas where casual rider activity is highest.

* Tailored Membership Tiers: Offer new seasonal subscriptions or weekend-only membership plans. Since casual riders are mostly active on weekends and during warm weather, these options can attract a leisure audience that does not need a full annual pass.

* Duration-Based Incentives: Create promotions or discounts tailored around longer trip times. Because casual riders take significantly longer trips on average, showing them how much they would save per minute can clearly prove the financial value of an annual membership.
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
