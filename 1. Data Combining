
```python
import pandas as pd
import os
data_dir='csv_files'
data_dir
os.listdir(data_dir)
all_df=[]
files=os.listdir(data_dir)
for filename in files:
    full_path=os.path.join(data_dir,filename)
    df=pd.read_csv(full_path)
    all_df.append(df)
combined_df=pd.concat(all_df)
len(combined_df)
combined_df.head()
```
