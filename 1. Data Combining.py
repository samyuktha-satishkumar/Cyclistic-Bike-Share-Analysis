#Data Combining

import pandas as pd
import os

# Set folder directory and list all monthly files
data_dir='csv_files'
data_dir
os.listdir(data_dir)
all_df=[]
files=os.listdir(data_dir)

# Loop through and read each CSV file into a list
for filename in files:
    full_path=os.path.join(data_dir,filename)
    df=pd.read_csv(full_path)
    all_df.append(df)

# Merge all files into one master table
combined_df=pd.concat(all_df)

# Verify the grand total row count
len(combined_df)
combined_df.head()

