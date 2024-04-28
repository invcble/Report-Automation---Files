import pandas as pd
import Functions

################################################################################################

def get_feedback(combined_csv_path, feedback_csv_path, s):
    df = pd.read_csv(combined_csv_path)
    tempdf = df[df['ScaleID'] == 'MOTAI'+f'{s}']
    fname = tempdf['FName'].values[0].capitalize()
    lname = tempdf['LName'].values[0].capitalize()
    # print(fname, lname)

    df = pd.read_csv(feedback_csv_path)
    df1 =  df[(df['LName'] == lname) & (df['FName'] == fname)]['Q1'].dropna().values
    df2 =  df[(df['LName'] == lname) & (df['FName'] == fname)]['Q2'].dropna().values
    df3 =  df[(df['LName'] == lname) & (df['FName'] == fname)]['Q3'].dropna().values
    return [df1, df2, df3]

################################################################################################

def gen_name_image(path, s):
    dat_long = pd.read_csv(path)

    dat_long[['Score', 'range']] = dat_long['Score'].str.split(' ', expand=True)
    dat_long['Score'] = dat_long['Score'].str.replace('NaN', '0')
    dat_long['Score'] = dat_long['Score'].str.replace('NA', '0')
    dat_long['Score'] = dat_long['Score'].astype(float)
    dat_long['range'] = dat_long['range'].fillna(' ')
    dat_long['label'] = dat_long['Score'].astype(str) + ' ' + dat_long['range']


    ################# TWO COLUMNS #################
    Attitude_and_Motivation = ['MOTAI', 'MOTSN', 'MOTNC', 'LEff']
    Knowledge_Sharing = ['ITT']
    Teaming_Approach_and_Skills_II = ['SL']
    Emotional_Intelligence = ['EISE', 'EIOE', 'EIUE', 'EIRE']
    # Belongingness_Uniqueness = ['Bel', 'Uniq']
    Values = ['ALT', 'PAY', 'REL', 'SEC', 'AUTH', 'VAR', 'AUTO', 'PRES']

    for each in Attitude_and_Motivation + Knowledge_Sharing + Teaming_Approach_and_Skills_II + Emotional_Intelligence + Values:
        Functions.create_chart(dat_long, each + f'{s}', 'report_images//', mode=1)

    ################# FOUR COLUMNS #################
    Leadership_Abilities = ['MOTI', 'SI', 'MCON', 'WIT']
    Empowering_Leadership = ['LBE', 'PDM', 'COACH', 'INF', 'SCTI']
    Visionary_Meaning_Based_Leadership = ['VL', 'MBL']
    Knowledge_Sharing_II = ['IE']
    Political_Skills = ['NET', 'II', 'SAS', 'ASN']
    Attitudes_Towards_Others_Cooperation = ['COOP']
    Teaming_Approach_and_Skills = ['TMX', 'CRE']

    for each in Leadership_Abilities + Empowering_Leadership + Visionary_Meaning_Based_Leadership + Knowledge_Sharing_II + Political_Skills + Attitudes_Towards_Others_Cooperation + Teaming_Approach_and_Skills:
        Functions.create_chart(dat_long, each + f'{s}', 'report_images//', mode=2)

    ################# THREE COLUMNS #################
    # Inclusive_Leadership = ['SG', 'EJ', 'SD', 'ED', 'HG']
    Knowledge_Sharing_III = ['SAFE', 'ITT', 'KS']
    Resistance_to_Change_Attitudes = ['RTCRS', 'RTCER', 'PT', 'PP']

    for each in Knowledge_Sharing_III + Resistance_to_Change_Attitudes:
        Functions.create_chart(dat_long, each + f'{s}', 'report_images//', mode=3)

    return Functions.get_name(dat_long, s)