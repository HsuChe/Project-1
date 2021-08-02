# merged_academic = merged DataFrame
# description = label for the independent variable
# selection_column = column where the labels of the independent variables are
# selection_column = values for the independent variable

def bar_graph(merged_academic,selection_column,indepent_var_label):
    import matplotlib.pyplot as plt
    from scipy import stats
    description_list = merged_academic[selection_column].unique()
    merged_academic.loc[:,:] = merged_academic.groupby(['School District Code',selection_column]).mean().reset_index()
    for description in description_list:
        instruction_df = merged_academic.loc[(merged_academic[selection_column] == description)]
        instruction_df.drop_duplicates()
        z = (stats.zscore(instruction_df.loc[:,indepent_var_label]))
        instruction_df.loc[:,(f'{description}_zscore')] = z
        instruction_df = instruction_df.loc[(instruction_df[f'{description}_zscore']<3) & (instruction_df[f'{description}_zscore']>-3)]
        x_values = instruction_df[indepent_var_label]
        y_values = instruction_df['Percent']
        plt.figure(figsize=(4,4), dpi=300)
        plt.scatter(x_values,y_values)
        (slope, intercept, rvalue, pvalue, stderr) = stats.linregress(x_values, y_values)
        print(intercept)
        regress_values = x_values * slope + intercept
        line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
        plt.xlabel(f"{description}")
        plt.ylabel('% of Graduates into College')
        plt.title(f"{description} vs. Into College ")
        plt.plot(x_values,regress_values,"r-")
        plt.annotate(line_eq,(20,15),fontsize=15,color="red")
        print(f"The r-value is: {rvalue**2}")
        print(f"The intercept value is: {intercept}")
        print(f"The p-value is: {pvalue}")
        plt.savefig(f'../images/{description}.jpg')
        plt.show()
        
    