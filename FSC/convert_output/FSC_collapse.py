#!/usr/bin/env python3

# python3 -m pip install pandas

import pandas as pd
import glob
import os

#  Will need to get os.path for file location...

cwd = os.getcwd()
print(cwd)
base = f"{cwd}/outputs/"
# base = "/Users/travishartman/Desktop/Working/supermaas_models/FSC/jupyter/outputs/"

### BASED ON THE FILES FROM DR. PUMA

# Two column output file names:
two_col_files = ["Export_FinalTotalByCountry.csv",
                 "Export_InitialTotalByCountry.csv",
                 "Import_FinalTotalByCountry.csv",
                 "Import_InitialTotalByCountry.csv",
                 "NumberExportTradePartners_FinalTotalByCountry.csv",
                 "NumberExportTradePartners_InitialTotalByCountry.csv",
                 "NumberImportTradePartners_FinalTotalByCountry.csv",
                 "NumberImportTradePartners_InitialTotalByCountry.csv"
                ]
# Four column output file names:
four_col_files = ["ConsumptiontoC0_TimeSeries.csv",
                 "Production_TimeSeries.csv",
                 "Reserve_TimeSeries.csv",
                 "ReserveChangetoC0_TimeSeries.csv",
                 "Shortage_TimeSeries.csv"
                ]

# ADD YEAR 0 to the files listed below to match shape of other output files
add_year_0_list = ["ConsumptiontoC0_TimeSeries.csv",
                 "ReserveChangetoC0_TimeSeries.csv",
                 "Shortage_TimeSeries.csv"
                ]

# function to take in all FSC 2 column output files and build a single csv file
def two_col_to_many(base, two_col_files):
    
    # Directory control to grab ALL output files
    path = rf'{base}'
    all_files = glob.glob(path + "*.csv")

    df = pd.DataFrame()
    for filename in all_files:
        
        fn = filename.split("/")[-1]
        
        # Parse out 2 column files and build df to write to .csv
        if fn in two_col_files:
            df_temp = pd.read_csv(filename, index_col=None, header=0)
            
            # initial build to grab country column
            if df.shape[0] == 0:
                df = df_temp
            
            # build additional columns with variable name and data (sans country column)
            else:
                col_name = df_temp.columns[1]
                df[col_name] = df_temp[col_name]
    
    # Rename originally unnammed country column to iso3
    df = df.rename(columns={'Unnamed: 0': 'iso3'})

    return df

# copy year one data and change to year 0 with NaN as Value; used as filler to match shape of other files with Year=0
def add_year_0(df):

    df_0 = df[df["Year"]==1]
    df_0 = df_0.assign(Year=0)
    df_0 = df_0.assign(Value="NaN")
    
    return df_0

# Read in all four column FSC files, add year 0 (if needed), and combine into single dataframe that is written to working directory
def four_col_to_many(base, four_col_files, add_year_0_list):
    
    # Directory control to grab ALL output files
    path = rf'{base}'
    all_files = glob.glob(path + "*.csv")

    df = pd.DataFrame()
    for filename in all_files:
        
        fn = filename.split("/")[-1]
        
        # Parse out 4-column files and build df to write to .csv
        if fn in four_col_files:

        	# Check to see if Year 0 needed...and add if so
            if fn in add_year_0_list:
                    
                df_raw = pd.read_csv(filename, index_col=None, header=0)
                
                # Function call from above
                df_0 = add_year_0(df_raw)

                # add "Year=0" to top of original FSC output and reindex to avoid issues with non-add_year_0 dfs
                df_temp = df_0.append(df_raw)
                df_temp = df_temp.reset_index(drop=True)
            
            # No Year 0 required
            else:
                df_temp = pd.read_csv(filename, index_col=None, header=0)             
            
            # initial build to grab first 3 columns
            if df.shape[0] == 0:
                
                df = df_temp
                
                #rename "Value" column with specific "Value_<filename>"
                col_name = fn.split(".")[0]
                df = df.rename(columns={'Value': f'Value_{col_name}'})

            # Already have base, so add "Value" data only to the df    
            else:
                col_name = fn.split(".")[0]
                df[f'Value_{col_name}'] = df_temp["Value"] 

    return df            

## Execute 
if __name__ == "__main__":

    print("Converting Files...")

    # Call functions to return dfs
    df_two = two_col_to_many(base, two_col_files)
    df_four = four_col_to_many(base, four_col_files, add_year_0_list)

    # Convert dfs to csv and write to working directory
    df_two.to_csv(rf'{base}two_col.csv', index=False, na_rep='NA')
    df_four.to_csv(rf'{base}four_col.csv', index=False, na_rep='NA')

    print("Check your directory for your new files")
