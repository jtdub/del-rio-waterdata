#!/usr/bin/env python3

import requests
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Download the Data
url = "https://ibwcsftpstg.blob.core.windows.net/wad/TelemetryTXT/08453000.txt"
response = requests.get(url)
data_lines = response.text.splitlines()

# Step 2: Parse the Data
# Assuming the first few lines are headers and the data starts from a specific line
start_line = 4  # Example start line; adjust based on actual data structure
data = []
for line in data_lines[start_line:]:
    # Splitting based on spaces; adjust if the data is tab-separated or otherwise
    split_line = line.split()
    data.append(split_line)

# Assuming we know the columns based on the file structure
columns = ['Date', 'Time', 'Stage', 'Discharge', 'Precipitation']
df = pd.DataFrame(data, columns=columns)

# Step 3: Convert to a DataFrame & Clean/Prepare Data
# Convert Date and Time into a single datetime column
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
# Convert numerical values from strings to floats or ints
df['Stage'] = pd.to_numeric(df['Stage'], errors='coerce')
df['Discharge'] = pd.to_numeric(df['Discharge'], errors='coerce')
df['Precipitation'] = pd.to_numeric(df['Precipitation'], errors='coerce')

# Step 4: Plot the Data
plt.figure(figsize=(10, 6))
plt.plot(df['DateTime'], df['Stage'], label='Stage (m)')
plt.plot(df['DateTime'], df['Discharge'], label='Discharge (cms)')
plt.plot(df['DateTime'], df['Precipitation'], label='Precipitation (mm)')
plt.legend()
plt.title('San Felipe Springs Water Data Visualization')
plt.xlabel('DateTime')
plt.ylabel('Value')
plt.show()

