import pandas as pd
import numpy as np
import os
import re
import warnings
from pandas.errors import PerformanceWarning

# ignore all PerformanceWarning coming from pandas
warnings.filterwarnings("ignore", category=PerformanceWarning)
 
# --- Configuration ---
OUTPUT_DIR = '.'
SELF_DAT_PATH = "primary_script\\2025\\SelfDat.xlsx"
MASTER_RATER_FILE_PATH = "primary_script\\2025\\PeerDat.xlsx"
os.makedirs(OUTPUT_DIR, exist_ok=True)

self_reverse_coded_map = {
    'LEff3T': 'LEff3', 'LEff5T': 'LEff5', 'wit1T': 'wit1', 'si4T': 'si4',
    'si5T': 'si5', 'mcon4T': 'mcon4', 'mcon5T': 'mcon5', 'wit5T': 'wit5',
    'wit6T': 'wit6', 'mot4T': 'mot4', 'rtcrs4T': 'rtcrs4', 'safe1T': 'safe1',
    'safe3T': 'safe3', 'safe5T': 'safe5', 'ks3T': 'ks3'
}
self_scales_def = {
    'aLEffx': ['LEff1', 'LEff2', 'LEff3T', 'LEff4', 'LEff5T'], 'aPPx': ['ProPer1', 'ProPer4', 'ProPer5', 'ProPer6', 'ProPer8'],
    'aEISEx': ['EI_SE2', 'EI_SE3'], 'aEIOEx': ['EI_OE1', 'EI_OE2', 'EI_OE3'], 'aEIUEx': ['EI_UE1', 'EI_UE3'],
    'aEIREx': ['EI_RE1', 'EI_RE2', 'EI_RE3'], 'aMOTIx': ['mot1', 'mot2', 'mot3', 'mot4T'],
    'aSIx': ['si1', 'si2', 'si3', 'si4T', 'si5T'], 'aMCONx': ['mcon1', 'mcon2', 'mcon3', 'mcon4T', 'mcon5T'],
    'aWITx': ['wit1T', 'wit2', 'wit3', 'wit4', 'wit5T', 'wit6T'], 'aLBEx': ['lbe1', 'lbe2', 'lbe3'],
    'aPDMx': ['pdm1', 'pdm2', 'pdm3'], 'aCOACHx': ['coach1', 'coach2', 'coach3'], 'aINFx': ['inf1', 'inf2', 'inf3'],
    'aSCTIx': ['scti1', 'scti2', 'scti3'], 'aRTCRSx': ['rtcrs1', 'rtcrs2', 'rtcrs3', 'rtcrs4T', 'rtcrs5'],
    'aRTCERx': ['rtcer1', 'rtcer2', 'rtcer3', 'rtcer4'], 'aNETx': ['net1', 'net2', 'net3', 'net4', 'net5', 'net6'],
    'aIIx': ['ii1', 'ii2', 'ii3', 'ii4'], 'aSASx': ['sa1', 'sa2', 'sa3', 'sa4', 'sa5'], 'aASNx': ['asin1', 'asin2', 'asin3'],
    'aMOTAIx': ['motai1', 'motai2', 'motai3'], 'aMOTSNx': ['motsn1', 'motsn2', 'motsn3'],
    'aMOTNCx': ['motnc1', 'motnc2', 'motnc3'], 'aCREx': ['cre1', 'cre2', 'cre3', 'cre4', 'cre5', 'cre6'],
    'aPTx': ['pt1', 'pt2', 'pt3', 'pt4'], 'aSAFEx': ['safe1T', 'safe2', 'safe3T', 'safe4', 'safe5T', 'safe6', 'safe7'],
    'aIEx': ['ie1', 'ie2', 'ie3', 'ie4', 'ie5'], 'aKSx': ['ks1', 'ks2', 'ks3T', 'ks4'],
    'aCOOPx': ['coop1', 'coop2', 'coop3'], 'aTMXx': ['tmx1', 'tmx2', 'tmx3', 'tmx4', 'tmx5', 'tmx6'],
    'aSLx': ['SL1s', 'SL2s', 'SL3s'], 'aITTx': ['itt1', 'itt2', 'itt3', 'itt4'],
    'aALTx': ['ALT1s', 'ALT9s', 'ALT17s'], 'aRELx': ['REL2s', 'REL10s', 'REL18s'],
    'aPAYx': ['PAY3s', 'PAY11s', 'PAY19s'], 'aPRESx': ['PRES4s', 'PRES12s', 'PRES20s'],
    'aSECx': ['SEC5s', 'SEC13s', 'SEC21s'], 'aAUTHx': ['AUTH6s', 'AUTH14s', 'AUTH22s'],
    'aVARx': ['VAR7s', 'VAR15s', 'VAR23s'], 'aAUTOx': ['AUTO8s', 'AUTO16s', 'AUTO24s'],
    'aMBLx': ['MBL1s', 'MBL2s', 'MBL3s', 'MBL4s', 'MBL5s', 'MBL6s', 'MBL7s', 'MBL8s', 'MBL9s'],
    'aVLx': ['VSL1s', 'VSL2s', 'VSL3s', 'VSL4s', 'VSL5s', 'VSL6s', 'VSL7s', 'VSL8s'],
    'aBelx': ['b1', 'b2', 'b3', 'b4'], 'aUniqx': ['u1', 'u2', 'u3']
}
rater_reverse_coded_map = {
    'wit1pT': 'wit1p', 'si4pT': 'si4p', 'si5pT': 'si5p', 'mcon4pT': 'mcon4p',
    'mcon5pT': 'mcon5p', 'wit5pT': 'wit5p', 'wit6pT': 'wit6p', 'mot4pT': 'mot4p'
}
rater_scales_def = {
    'WIT': ['wit1pT', 'wit2p', 'wit3p', 'wit4p', 'wit5pT', 'wit6pT'], 'MOTI': ['mot1p', 'mot2p', 'mot3p', 'mot4pT'],
    'SI': ['si1p', 'si2p', 'si3p', 'si4pT', 'si5pT'], 'MCON': ['mcon1p', 'mcon2p', 'mcon3p', 'mcon4pT', 'mcon5pT'],
    'LBE': ['lbe1p', 'lbe2p', 'lbe3p'], 'PDM': ['pdm1p', 'pdm2p', 'pdm3p'],
    'COACH': ['coach1p', 'coach2p', 'coach3p'], 'INF': ['inf1p', 'inf2p', 'inf3p'],
    'SCTI': ['scti1p', 'scti2p', 'scti3p'], 'SG': ['sg1p', 'sg2p', 'sg6p'], 'EJ': ['ej2p', 'ej3p', 'ej5p'],
    'SD': ['sd1p', 'sd3p', 'sd7p'], 'ED': ['ed3p', 'ed6p', 'ed8p'], 'HG': ['hg1p', 'hg3p', 'hg4p'],
    'MBL': ['MBL1p', 'MBL2p', 'MBL3p', 'MBL4p', 'MBL5p', 'MBL6p', 'MBL7p', 'MBL8p', 'MBL9p'],
    'VL': ['VSL1p', 'VSL2p', 'VSL3p', 'VSL4p', 'VSL5p', 'VSL6p', 'VSL7p', 'VSL8p'],
    'IE': ['ie1p', 'ie2p', 'ie3p'], 'TMX': ['tmx1p', 'tmx2p', 'tmx3p', 'tmx4p', 'tmx5p'],
    'CRE': ['cre1p', 'cre2p', 'cre3p', 'cre4p', 'cre5p', 'cre6p'],
    'NET': ['net1p', 'net2p', 'net3p', 'net4p', 'net5p', 'net6p'], 'II': ['ii1p', 'ii2p', 'ii3p', 'ii4p'],
    'SAS': ['sa1p', 'sa2p', 'sa3p', 'sa4p', 'sa5p'], 'ASN': ['asin1p', 'asin2p', 'asin3p'],
    'COOP': ['coop1p', 'coop2p', 'coop3p']
}
ordered_scale_checks = [
    'ASN', 'COACH', 'COOP', 'CRE', 'EIOE', 'EIRE', 'EISE', 'EIUE', 'IE', 'II', 'INF', 'ITT', 'KS',
    'LBE', 'LEff', 'MCON', 'MOTI', 'MOTAI', 'MOTNC', 'MOTSN', 'NET', 'PDM', 'PP', 'PT', 'RTCRS',
    'RTCER', 'SAS', 'SAFE', 'SCTI', 'SI', 'SL', 'TMX', 'WIT', 'ALT', 'AUTO', 'AUTH', 'PAY',
    'REL', 'PRES', 'SEC', 'VAR', 'VL', 'MBL', 'Bel', 'Uniq', 'SG', 'EJ', 'SD', 'ED', 'HG'
]
rater_group_definitions = [
    {'name': 'GeneralPeers', 'q34_value': None,  'prefix': 'cX', 'suffix': 'p'},
    {'name': 'Supervisors',  'q34_value': '1',   'prefix': 'eX', 'suffix': 'sup'},
    {'name': 'TeamSameDept', 'q34_value': '2',   'prefix': 'fX', 'suffix': 'p2'},
    {'name': 'TeamDiffDept', 'q34_value': '3',   'prefix': 'gX', 'suffix': 'p3'},
    {'name': 'DirectReports','q34_value': '4',   'prefix': 'hX', 'suffix': 'p4'},
    {'name': 'Partners',     'q34_value': '5',   'prefix': 'jX', 'suffix': 'p5'},
    {'name': 'Suppliers',    'q34_value': '6',   'prefix': 'kX', 'suffix': 'p6'},
]

def clean_ascii_names(df):
    for col in ['FName', 'LName']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: re.sub(r'[^\x00-\x7F]', '', str(x)) if pd.notna(x) else x)
    return df

def read_data_file(path, **kwargs):
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.xlsx', '.xls']:
        df = pd.read_excel(path, **kwargs)
    elif ext == '.csv':
        df = pd.read_csv(path, encoding="utf-8", **kwargs)
    else:
        raise ValueError(f"Unsupported file extension for {path}")
    df = clean_ascii_names(df)
    return df

def get_all_item_cols(scales_definition, reverse_map=None):
    all_cols = set()
    if scales_definition:
        for items in scales_definition.values():
            for item in items:
                all_cols.add(item)
    if reverse_map:
        for rc_item, orig_item in reverse_map.items():
            all_cols.add(rc_item)
            all_cols.add(orig_item)
    return list(all_cols)

print("Processing Self-rating data...")
try:
    self_dat = read_data_file(SELF_DAT_PATH, header=0, dtype=str)
except FileNotFoundError:
    print(f"FATAL ERROR: Self-rating file not found at {SELF_DAT_PATH}. Exiting.")
    exit()
if self_dat.empty:
    print(f"FATAL ERROR: Self-rating file {SELF_DAT_PATH} is empty. Exiting.")
    exit()
self_dat = self_dat.sort_values(by='LName').reset_index(drop=True)
self_dat['FName'] = self_dat['FName'].astype(str).str.upper().str.replace(" ", "", regex=False)
self_dat['LName'] = self_dat['LName'].astype(str).str.upper().str.replace(" ", "", regex=False)
self_item_cols_to_convert = get_all_item_cols(self_scales_def, self_reverse_coded_map)
for col in self_item_cols_to_convert:
    if col in self_dat.columns:
        self_dat[col] = pd.to_numeric(self_dat[col], errors='coerce')
for new_col, original_col in self_reverse_coded_map.items():
    if original_col in self_dat.columns and pd.api.types.is_numeric_dtype(self_dat[original_col]):
        self_dat[new_col] = 8 - self_dat[original_col]
    elif new_col not in self_dat.columns and original_col in self_dat.columns:
        self_dat[new_col] = np.nan
for scale_col, item_cols in self_scales_def.items():
    existing_item_cols = [col for col in item_cols if col in self_dat.columns and pd.api.types.is_numeric_dtype(self_dat[col])]
    if existing_item_cols:
        self_dat[scale_col] = self_dat[existing_item_cols].mean(axis=1).round(2)
    else:
        self_dat[scale_col] = np.nan
cohort_means_self = {}
for scale_col_self_avg in self_scales_def.keys():
    cohort_col_name = 'bX' + scale_col_self_avg[1:-1]
    if scale_col_self_avg in self_dat.columns and pd.api.types.is_numeric_dtype(self_dat[scale_col_self_avg]):
        cohort_means_self[cohort_col_name] = self_dat[scale_col_self_avg].mean(skipna=True).round(2)
    else:
         cohort_means_self[cohort_col_name] = np.nan
for col_name, mean_val in cohort_means_self.items():
    self_dat[col_name] = mean_val
for scale_avg_col, item_cols in self_scales_def.items():
    existing_item_cols = [col for col in item_cols if col in self_dat.columns and pd.api.types.is_numeric_dtype(self_dat[col])]
    if not existing_item_cols : continue
    min_vals_series = self_dat[existing_item_cols].min(axis=1, skipna=True)
    max_vals_series = self_dat[existing_item_cols].max(axis=1, skipna=True)
    formatted_scores = []
    for i in range(len(self_dat)):
        mean_score_val = self_dat.loc[i, scale_avg_col]
        min_v = min_vals_series.iloc[i]
        max_v = max_vals_series.iloc[i]
        min_str = f"{int(min_v)}" if pd.notna(min_v) and np.isfinite(min_v) else "NA"
        max_str = f"{int(max_v)}" if pd.notna(max_v) and np.isfinite(max_v) else "NA"
        if pd.isna(mean_score_val):
            formatted_scores.append(f"NA [{min_str}-{max_str}]")
        else:
            formatted_scores.append(f"{mean_score_val:.2f} [{min_str}-{max_str}]")
    self_dat[scale_avg_col] = formatted_scores

print("\nProcessing Rater data from ALLpeersMerk2024.csv...")
all_rater_base_item_cols = get_all_item_cols(rater_scales_def, rater_reverse_coded_map)
try:
    master_rater_dat = read_data_file(MASTER_RATER_FILE_PATH, header=0, dtype={'Q34': str}, keep_default_na=False, na_values=[''])
    if master_rater_dat.empty:
        raise FileNotFoundError("Master rater file is empty.")
except FileNotFoundError:
    print(f"ERROR: Master rater file not found or empty at {MASTER_RATER_FILE_PATH}. Rater scores will be missing.")
    master_rater_dat = pd.DataFrame()
if not master_rater_dat.empty:
    if 'Q34' not in master_rater_dat.columns:
        print(f"ERROR: Column 'Q34' not found in {MASTER_RATER_FILE_PATH}. Cannot filter rater groups. Rater scores will be missing.")
        master_rater_dat = pd.DataFrame()
if not master_rater_dat.empty:
    master_rater_dat['FName'] = master_rater_dat['FName'].astype(str).str.upper().str.replace(" ", "", regex=False)
    master_rater_dat['LName'] = master_rater_dat['LName'].astype(str).str.upper().str.replace(" ", "", regex=False)
    for col in all_rater_base_item_cols:
        if col in master_rater_dat.columns:
            master_rater_dat[col] = pd.to_numeric(master_rater_dat[col], errors='coerce')
    for new_col, original_col in rater_reverse_coded_map.items():
        if original_col in master_rater_dat.columns and pd.api.types.is_numeric_dtype(master_rater_dat[original_col]):
            master_rater_dat[new_col] = 8 - master_rater_dat[original_col]
        elif new_col not in master_rater_dat.columns and original_col in master_rater_dat.columns :
             master_rater_dat[new_col] = np.nan
    for scale_base_name, item_cols_list in rater_scales_def.items():
        actual_item_cols = [col for col in item_cols_list if col in master_rater_dat.columns and pd.api.types.is_numeric_dtype(master_rater_dat[col])]
        temp_mean_col = f"_temp_{scale_base_name}_mean"
        temp_min_items_col = f"_temp_{scale_base_name}_min_items"
        temp_max_items_col = f"_temp_{scale_base_name}_max_items"
        if actual_item_cols:
            master_rater_dat[temp_mean_col] = master_rater_dat[actual_item_cols].mean(axis=1)
            master_rater_dat[temp_min_items_col] = master_rater_dat[actual_item_cols].min(axis=1, skipna=True)
            master_rater_dat[temp_max_items_col] = master_rater_dat[actual_item_cols].max(axis=1, skipna=True)
        else:
            master_rater_dat[temp_mean_col] = np.nan
            master_rater_dat[temp_min_items_col] = np.nan
            master_rater_dat[temp_max_items_col] = np.nan
    id_cols_for_snapshot = ['LName', 'FName']
    if 'FName_Rater' in master_rater_dat.columns: id_cols_for_snapshot.append('FName_Rater')
    if 'LName_Rater' in master_rater_dat.columns: id_cols_for_snapshot.append('LName_Rater')
    peer_snapshot_dat = master_rater_dat[id_cols_for_snapshot].copy()
    for item_col_snap in all_rater_base_item_cols:
        if item_col_snap in master_rater_dat.columns:
            peer_snapshot_dat[item_col_snap] = master_rater_dat[item_col_snap]
    for scale_base_name in rater_scales_def.keys():
        snapshot_scale_col = f"{scale_base_name}p"
        temp_mean_col_for_snapshot = f"_temp_{scale_base_name}_mean"
        if temp_mean_col_for_snapshot in master_rater_dat:
            peer_snapshot_dat[snapshot_scale_col] = master_rater_dat[temp_mean_col_for_snapshot].round(2)
        else:
            peer_snapshot_dat[snapshot_scale_col] = np.nan
    if not peer_snapshot_dat.empty:
        peer_snapshot_dat.to_csv(os.path.join(OUTPUT_DIR, 'peerRatingsRange_py.csv'), index=False)
        print(f"Saved peerRatingsRange_py.csv with {len(peer_snapshot_dat.columns)} columns.")
    else:
        print("Warning: peer_snapshot_dat for peerRatingsRange_py.csv was empty.")
    for group_def in rater_group_definitions:
        group_name = group_def['name']
        q34_val = group_def['q34_value']
        agg_prefix = group_def['prefix']
        output_suffix = group_def['suffix']
        print(f"  Processing rater group: {group_name}")
        if q34_val is not None:
            group_specific_dat = master_rater_dat[master_rater_dat['Q34'].astype(str) == str(q34_val)].copy()
        else:
            group_specific_dat = master_rater_dat.copy()
        if group_specific_dat.empty or 'LName' not in group_specific_dat.columns or not group_specific_dat['LName'].notna().any():
            print(f"    No data or no valid LNames for group {group_name}. Adding NaN columns to self_dat.")
            for scale_base_name in rater_scales_def.keys():
                col_to_add_nan = f"{agg_prefix}{scale_base_name}{output_suffix}"
                if col_to_add_nan not in self_dat.columns:
                    self_dat[col_to_add_nan] = "NA [NA-NA]"
            continue
        agg_ops_group = {}
        for scale_base_name in rater_scales_def.keys():
            final_col_name_group = f"{agg_prefix}{scale_base_name}{output_suffix}"
            temp_mean_col_group = f"_temp_{scale_base_name}_mean"
            temp_min_items_col_group = f"_temp_{scale_base_name}_min_items"
            temp_max_items_col_group = f"_temp_{scale_base_name}_max_items"
            agg_ops_group[final_col_name_group] = pd.NamedAgg(column=temp_mean_col_group, aggfunc='mean')
            agg_ops_group[f"_overall_min_for_{scale_base_name}"] = pd.NamedAgg(column=temp_min_items_col_group, aggfunc='min')
            agg_ops_group[f"_overall_max_for_{scale_base_name}"] = pd.NamedAgg(column=temp_max_items_col_group, aggfunc='max')
        group_specific_dat_filtered = group_specific_dat[group_specific_dat['LName'].notna()]
        if not group_specific_dat_filtered.empty:
            missing_agg_cols = False
            for key_agg_op, named_agg_op in agg_ops_group.items():
                if named_agg_op.column not in group_specific_dat_filtered.columns:
                    print(f"    Warning: Column '{named_agg_op.column}' for aggregation key '{key_agg_op}' not found in data for group {group_name}. Score will be NaN.")
                    missing_agg_cols = True
                    group_specific_dat_filtered[named_agg_op.column] = np.nan
            aggregated_df = group_specific_dat_filtered.groupby('LName', as_index=False).agg(**agg_ops_group)
        else:
            aggregated_df = pd.DataFrame(columns=['LName'] + list(agg_ops_group.keys()))
        for scale_base_name in rater_scales_def.keys():
            mean_col_fmt_group = f"{agg_prefix}{scale_base_name}{output_suffix}"
            overall_min_col_fmt_group = f"_overall_min_for_{scale_base_name}"
            overall_max_col_fmt_group = f"_overall_max_for_{scale_base_name}"
            if mean_col_fmt_group not in aggregated_df.columns: continue
            aggregated_df[mean_col_fmt_group] = aggregated_df[mean_col_fmt_group].round(2)
            fmt_scores_list = []
            for _, row_agg in aggregated_df.iterrows():
                mean_val_agg = row_agg[mean_col_fmt_group]
                min_val_agg = row_agg.get(overall_min_col_fmt_group, np.nan)
                max_val_agg = row_agg.get(overall_max_col_fmt_group, np.nan)
                min_str_agg = f"{int(min_val_agg)}" if pd.notna(min_val_agg) and np.isfinite(min_val_agg) else "NA"
                max_str_agg = f"{int(max_val_agg)}" if pd.notna(max_val_agg) and np.isfinite(max_val_agg) else "NA"
                if pd.isna(mean_val_agg):
                    fmt_scores_list.append(f"NA [{min_str_agg}-{max_str_agg}]")
                else:
                    fmt_scores_list.append(f"{mean_val_agg:.2f} [{min_str_agg}-{max_str_agg}]")
            aggregated_df[mean_col_fmt_group] = fmt_scores_list
            if overall_min_col_fmt_group in aggregated_df.columns: aggregated_df.drop(columns=[overall_min_col_fmt_group], inplace=True)
            if overall_max_col_fmt_group in aggregated_df.columns: aggregated_df.drop(columns=[overall_max_col_fmt_group], inplace=True)
        if not aggregated_df.empty:
            self_dat = pd.merge(self_dat, aggregated_df, on='LName', how='left')
        for scale_base_name in rater_scales_def.keys():
            expected_col_name = f"{agg_prefix}{scale_base_name}{output_suffix}"
            if expected_col_name not in self_dat.columns:
                self_dat[expected_col_name] = "NA [NA-NA]"
else:
    print("Skipping rater group processing loop as master_rater_dat is empty or invalid.")
    for group_def in rater_group_definitions:
        agg_prefix = group_def['prefix']
        output_suffix = group_def['suffix']
        for scale_base_name in rater_scales_def.keys():
            col_to_add_nan = f"{agg_prefix}{scale_base_name}{output_suffix}"
            if col_to_add_nan not in self_dat.columns:
                self_dat[col_to_add_nan] = "NA [NA-NA]"

if not self_dat.empty:
    id_numbers_str = (pd.Series(np.arange(len(self_dat)) + 1, index=self_dat.index)).astype(str)
    self_dat['ID'] = 'MTI' + id_numbers_str
    self_dat['ScaleID_NumPart_Temp'] = np.arange(len(self_dat)) + 1
else:
    self_dat['ID'] = pd.Series(dtype=str)
    self_dat['ScaleID_NumPart_Temp'] = pd.Series(dtype=int)

codebook = self_dat[['FName', 'LName', 'ID']].copy() if 'ID' in self_dat.columns else pd.DataFrame(columns=['FName', 'LName', 'ID'])
id_vars_for_melt = ['FName', 'LName', 'ID', 'ScaleID_NumPart_Temp']
measure_vars_for_melt = list(self_scales_def.keys()) + \
                        list(cohort_means_self.keys()) + \
                        [f"{g['prefix']}{scale_base}{g['suffix']}"
                         for g in rater_group_definitions
                         for scale_base in rater_scales_def.keys()]

measure_vars_for_melt = [col for col in measure_vars_for_melt if col in self_dat.columns]
if not measure_vars_for_melt or self_dat.empty:
    print("Warning: No measure_vars identified or self_dat is empty. Final long data will be empty or incomplete.")
    dat_long = pd.DataFrame(columns=id_vars_for_melt + ['Scale', 'Score', 'ScaleID'])
else:
    dat_long = pd.melt(self_dat,
                       id_vars=id_vars_for_melt,
                       value_vars=measure_vars_for_melt,
                       var_name='Scale',
                       value_name='Score')
    def get_scale_prefix_from_col_name(scale_col_name_str):
        for check_key in ordered_scale_checks:
            if check_key in scale_col_name_str:
                return check_key
        match = re.match(r"^[a-zA-Z]+X?([A-Z_]+[A-Za-z0-9]*)(?:x|p|sup|p[2-6])?$", str(scale_col_name_str))
        if match and match.group(1):
            return match.group(1)
        return "UNKNOWN"
    if not dat_long.empty:
        dat_long['ScaleID_Prefix_Temp'] = dat_long['Scale'].apply(get_scale_prefix_from_col_name)
        dat_long['ScaleID'] = dat_long['ScaleID_Prefix_Temp'] + dat_long['ScaleID_NumPart_Temp'].astype(str)
        dat_long.drop(columns=['ScaleID_NumPart_Temp', 'ScaleID_Prefix_Temp'], inplace=True, errors='ignore')
    else:
        dat_long['ScaleID'] = pd.Series(dtype=str)


# Order columns: FName, LName, ID, ScaleID, Scale, Score
col_order = ['FName', 'LName', 'ID', 'ScaleID', 'Scale', 'Score']
for col in col_order:
    if col not in dat_long.columns:
        dat_long[col] = np.nan
dat_long = dat_long[col_order + [c for c in dat_long.columns if c not in col_order]]
# Replace missing Score values (NaN or empty string) with 'missing'
dat_long['Score'] = dat_long['Score'].where(dat_long['Score'].notnull(), 'NaN [Inf--Inf]')
dat_long['Score'] = dat_long['Score'].replace('', 'NaN [Inf--Inf]')
dat_long['Score'] = dat_long['Score'].replace('NA [NA-NA]', 'NaN [Inf--Inf]')


# --- 4. Save Output Files ---
if not self_dat.empty:
    # self_dat.to_csv(os.path.join(OUTPUT_DIR, 'selfRatingsRange_py.csv'), index=False, encoding="utf-8")
    pass
else:
    print("Warning: self_dat was empty, not saving selfRatingsRange_py.csv.")

if not dat_long.empty:
    dat_long.to_csv(os.path.join(OUTPUT_DIR, 'CombinedDataNational_py.csv'), index=False, encoding="utf-8")
    # dat_long.to_csv(os.path.join(OUTPUT_DIR, 'MerckCombined_py.csv'), index=False, encoding="utf-8") # R script saves identical file
else:
    print("Warning: dat_long was empty, not saving CombinedDataNational_py.csv or MerckCombined_py.csv.")

if not codebook.empty:
    # codebook.to_csv(os.path.join(OUTPUT_DIR, 'codebook_py.csv'), index=False, encoding="utf-8")
    pass
else:
    print("Warning: codebook was empty, not saving codebook_py.csv.")
