# merged_academic = merged DataFrame
# description = label for the independent variable
# selection_column = column where the labels of the independent variables are
# selection_column = values for the independent variable

def analysis(df, ind_label,ind_value):
    # import the dependencies
    import matplotlib.pyplot as plt
    from scipy import stats

    # build df based on school district code and independent variable label
    grouped = df.groupby(['School District Code', ind_label]).mean().reset_index()
    # create list of indepenent variables
    ind_var_list = grouped[ind_label].unique()
    # start for loop for each independent variable
    for ind_var in ind_var_list:
        ind_df = grouped.loc[grouped[ind_label] == ind_var]
        # check to see if there are actually data
        if ind_df[ind_value].mean()==0:
            continue
        ind_df = ind_df.assign(z_score = stats.zscore(ind_df[ind_value]))
        ind_df = ind_df.loc[(ind_df['z_score']<3) & (ind_df['z_score']>-3)]
        # build the regression function
        x_values = ind_df[ind_value]
        y_values = ind_df['Percent']
        (slope, intercept, rvalue, pvalue, stderr) = stats.linregress(x_values, y_values)
        regress_values = x_values * slope + intercept
        # print analysis
        print(f'regression function = f(x) = x*{slope.round(2)} + {intercept.round(2)}')
        print(f'p-value: {pvalue}')
        print(f'std error: {stderr}')
        ind_df.plot.scatter(x = ind_value, y = 'Percent', figsize = (8,8))
        plt.plot(x_values, regress_values, color = 'red')
        plt.title(f'{ind_var} vs college enrollment')
        plt.xlabel(ind_var)
        plt.ylabel('College Enrollment Percentage')
        ind_var = ind_var.replace("/", "&")
        plt.savefig(f'../images/{ind_var}.png')
        plt.show()
                