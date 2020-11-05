#!/usr/bin/env python3

# python3 -m pip install pandas

import pandas as pd
import glob
import os


# Define where results will be sent
cwd = os.getcwd()
res_dir = f"{cwd}/results/"
in_dir = f"{cwd}/fsc_output_files/"

#Read in all csv files
def get_all_csv(in_dir):
    # Directory control to grab ALL output files
    path = rf'{in_dir}'
    all_files = glob.glob(path + "*.csv")

    print(path)

    return all_files

# function to take in all FSC 2 column output files and build a single csv file
def two_col_to_many(all_files):

    df = pd.DataFrame()
    for filename in all_files:
        
        # Parse out 2 column files and build df to write to .csv
        df_temp = pd.read_csv(filename, index_col=None, header=0)
        num_cols = df_temp.shape
        num_cols = num_cols[1]

        # Parse out 2-column files and build df to write to .csv
        if num_cols == 2:
    
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
def four_col_to_many(all_files):

    df = pd.DataFrame()
    for filename in all_files:
        
        fn = filename.split("/")[-1]
        
        # Parse out 4 column files and build df to write to .csv
        df_temp = pd.read_csv(filename, index_col=None, header=0)
        
        num_cols = df_temp.shape
        num_cols = num_cols[1]

        # Parse out 4-column files and build df to write to .csv
        if num_cols == 4:
            
            start_year = df_temp.get("Year", "X")[0]

        	# Check to see if Year 0 needed...and add if so
            if start_year == 1:
                # Function call from above
                df_0 = add_year_0(df_temp)

                # add "Year=0" to top of original FSC output and reindex to avoid issues with non-add_year_0 dfs
                df_temp = df_0.append(df_temp).reset_index(drop=True)

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
    all_files = get_all_csv(in_dir)
    # Call functions to return dfs
    df_two = two_col_to_many(all_files)
    df_four = four_col_to_many(all_files)

    # Convert dfs to csv and write to working directory
    df_two.to_csv(rf'{res_dir}two_col.csv', index=False, na_rep='NA')
    df_four.to_csv(rf'{res_dir}four_col.csv', index=False, na_rep='NA')

    print(f"New csv files written to: {res_dir}")
