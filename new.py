import pandas as pd
import Functions

dat_long = pd.read_csv('MerckCombined.csv')

# Separate scores from ranges and convert scores to numeric
dat_long[['Score', 'range']] = dat_long['Score'].str.split(' ', expand=True)
dat_long['Score'] = dat_long['Score'].astype(float)
dat_long['range'] = dat_long['range'].fillna(' ')
dat_long['label'] = dat_long['Score'].astype(str) + ' ' + dat_long['range']


# Filter data based on ScaleID
s = 1

Attitude_and_Motivation = ['MOTAI', 'MOTSN', 'MOTNC', 'LEff']

for each in Attitude_and_Motivation:
    Functions.create_chart(dat_long, each+ f'{s}', 'report_images/')
