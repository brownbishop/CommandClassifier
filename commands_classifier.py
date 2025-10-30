from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
import numpy as np

cleaned_lines: list[list[str]] = []
with open('commands.csv', 'r') as file:
    for line in file:
        parts  = line.strip().rsplit(maxsplit=1)
        if len(parts) == 2:
            cleaned_lines.append(parts)

train = pd.DataFrame(cleaned_lines, columns=['commands', 'danger'])

print(train)

# target distribution
target_dist = np.unique(train['danger'], return_counts=True)

print(target_dist)

# delete unwanted target
train=train[train['danger']!='"/sys/bus/usb/devices/usb1/power/control']

# now it's balanced
dist = np.unique(train['danger'],return_counts=True)
print(dist)

train['num_words'] = train['commands'].apply(lambda x: len(str(x).split()))
dist = np.unique(train['num_words'], return_counts=True)
print(dist)

hist = plt.hist(train['num_words'])

# Create the bar chart
plt.figure(figsize=(12, 8))
plt.title('Top 20 Most Frequent Commands')
plt.xlabel('Command')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the chart to a file
plt.savefig('command_distribution.png')
