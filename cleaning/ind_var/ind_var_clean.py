
def ind_var_clean(dataframe,merge_column,test_column,selection_column,output_name):
    # remove all rows that aggregates data from SCHOOL_DSTRCT_CD
    dataframe = dataframe.loc[dataframe[merge_column] != 'ALL']
    dataframe['School District Code'] = dataframe[merge_column].astype(int)
    dataframe = dataframe[test_column]
    # remove all the rows with NaN
    clean_data = dataframe.dropna()
    # isolate the two columns that we want to test with group by
    clean_data.groupby(['School District Code',selection_column]).mean()
    clean_data = clean_data.reset_index(drop='True')
    clean_data.to_csv(f'../../merge_ready_data/{output_name}.csv')

