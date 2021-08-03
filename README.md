<h3 align="center">Group (Lorem ipsum dolor sit amet)</h3>

<p align="center">
     College Enrollment from High School
    <br />
    <a href="https://github.com/HsuChe/Project-1"><strong>Project Github URL »</strong></a>
    <br />
    <br />
  </p>
</p>

<!-- ABOUT THE PROJECT -->

## About The Project

![hero image](https://github.com/HsuChe/Project-1/blob/c77948626aef175d2735c6d4783f35d59d35fd1d/image/graduation-995042_1920.jpg)

Graduating from high school can mean different things to different people as graduation criteria can often be different between schools and the standard can be opaque. The overall competitiveness of students graduating from Georgia district highschools can be standardized by their enrollment into college after graduation.

We took graduation data and enrollment data from 2018 and calculated the percent of student enrolling to college after graduation. We will use that metric as the dependent variable and we will test various variables to see what is the best way to improve school performance.

Features of the dependent variable dataset:

* The dependent variable is cleaned and filtered base on the School District Code.
* We will retain the following columns to be analyzed in the dataset.

  * Graduates: **The number of people graduating from the school district in year 2018**
  * Postsecondary Institution: **Number of students that enrolled in post secondary institutions after graduation.**
  * Percent: **The percent of students that went to college after graduation (Dependent Variable)**
* The dataset is in the csv file format with delimiter of comma.
* Download the dependent variable dataset [HERE](https://github.com/HsuChe/Project-1/blob/487dcc90e1735e5e4d304ed3287454154ec8e67b/raw_data/C11_FY2019_HS%20Graduates%202017_Enrolled%20in%20College%20in%2016%20Mos_Redacted%20(2).xlsx)

Features of the independent variables datasets:

* The independent variable is cleaned and filtered base on the School District Code.
* For the independent variable datasets, we will have one column that provides the value for the independent variables and another providing the labels. These columns can vary drastically, but we will always be merging against school district code and these variables.
* Download the dropout rate dataset [HERE](https://github.com/HsuChe/Project-1/blob/487dcc90e1735e5e4d304ed3287454154ec8e67b/raw_data/7-12%20Dropout%20Rate-2018_DEC_10th_2018.csv)
* Download the ACT performance dataset [HERE](https://github.com/HsuChe/Project-1/blob/487dcc90e1735e5e4d304ed3287454154ec8e67b/raw_data/ACT-Score-Data.csv)
* Download the EOC performance rate dataset [HERE](https://github.com/HsuChe/Project-1/blob/487dcc90e1735e5e4d304ed3287454154ec8e67b/raw_data/EOC_2019_By_Grad_FEB_24_2020%20(1).csv)
* Download the graduation rate dataset [HERE](https://github.com/HsuChe/Project-1/blob/487dcc90e1735e5e4d304ed3287454154ec8e67b/raw_data/Graduation_Rate_2019_Dec2nd_2019%20(3).csv)
* Download the revenues and expenditure dataset [HERE](https://github.com/HsuChe/Project-1/blob/487dcc90e1735e5e4d304ed3287454154ec8e67b/raw_data/Revenues_and_Expenditures_2018_DEC_10th_2018.csv)
* Download the SAT performance dataset [HERE](https://github.com/HsuChe/Project-1/blob/487dcc90e1735e5e4d304ed3287454154ec8e67b/raw_data/SAT-score-data.csv)
  *`<!-- GETTING STARTED -->`

## Processing the dependent variable

Isolate the data points that we are interested in.

* For loop to add to list

  ```sh
  # load the excel into pandas
  df_enrollment = pd.read_excel('../../raw_data/C11_FY2019_HS Graduates 2017_Enrolled in College in 16 Mos_Redacted (2).xlsx')
  df_enrollment

  # isolate the datapoints that we are interested in
  all_school = df_enrollment.iloc[:,0:7].iloc[1:,]
  # set new vlaues for columns
  all_school.columns = all_school.iloc[0]
  # remove the duplicate column names and reset the index
  all_school = all_school.loc[2:,:].reset_index(drop = True)
  ```
* We are now ready to remove data from the various school codes. The first thing we need to do is to remove all the school codes that focuses on aggregating all the data.

  ```sh
  # create df for the individual school codes
  school_district = all_school.loc[all_school['School Code'] != 'ALL']
  school_district
  ```
* We can now isolate the performance metrics that we want to use.

  ```sh
  # identify the performance metrics that we want to use for analysis
  performance_metrics = school_all[['School District Code','Total High School Graduates','Number of High School Graduates Enrolled in Postsecondary Institution']]
  performance_metrics
  ```
* The next step is to remove the none integer data points which is TFS or to few students and NaN
  ```sh
  # drop all the rows where there are anhy value "TFS" in the cells
  school_no_TFS = df.replace('TFS', np.nan).dropna()
  school_no_TFS
    ```

* After that, we noticed that the last datapoint is an aggregation row for all the school districts, we removed the last row from the datapoint. 
  ```sh
  # reset the index for the dataframe
  school_no_TFS = school_no_TFS.reset_index(drop=True)
  # remove the aggregate School District Code data at the end of the dataset
  school_no_TFS = school_no_TFS.iloc[:185]
  school_no_TFS
    ```

### Creating a column for the dependent variable we want to test. 

The next step is to generate the percentage of students that graduated that went to post secondary institution. 

* Take the number of students that went on to post secondary institution and divide it by total graduates
  ```sh
  # create a column for the percentage of students that went to college after graduation
  percent = (school_no_TFS['Postsecondary Institution'] / school_no_TFS['Graduates']*100).round(2)
  school_no_TFS['Percent'] = percent
  school_no_TFS
  ```

We now will graph the districts and see if there are any anomolies, we found out that there are charter school districts that are giving us weird results. We decided to remove them.

The charter school districts have digits above 1000, so we removed all the rows with district IDs that are more than 3 digits long. 

* we will reset the index after removing the charter school district codes.
  ```sh
  # remove charter school district codes
  school_no_TFS = school_no_TFS.loc[school_no_TFS['School District Code']<1000]

  # sort the results from the schools by descending order based on Percent of college enrollment
  school_sorted = school_no_TFS.sort_values('Percent', ascending = False)
  ```

## Picking 100 random samples from the dataset. 

We wanted to random sample the data so we can have test data if we wish to build machine learning models in the future. The batch size we chose for this analysis is 100. 

* Avearge change in profit and losses month to month.
  ```sh
  # find 100 random samples of schools to analyze
  import random
  random_list = []
  for index in range(school_sorted['School District Code'].count()):
      random_list.append(random.randrange(school_sorted['School District Code'].count()))
      
  index_list = random_list[:100]
  ```

We can now export our cleaned dependent variable dataset. 

## Cleaning independent variable datasets

We created a function that cleans the independent variable data based upon the column that we want to merge with, the column that lables the independent variable, and the column that has the values we want to test. 

* FIrst thing is to remove all aggregate district codes. merge_column is the column name where school district codes are located. 
  ```sh
  # remove all rows that aggregates data from SCHOOL_DSTRCT_CD
  dataframe = dataframe.loc[dataframe[merge_column] != 'ALL']
  ```

Next we will change the name of the merge column to "school district code" and also make sure that all the data in the series is a int.

* use astype(int) to change the series to integers
  ```sh
  dataframe['School District Code'] = dataframe[merge_column].astype(int)
  ```

Then we can isolate the columns that we want to keep the values of for testing against the dependent variable. In this case, the test_column consists of the list of column names we want to keep. 

* the test columns are a list of columns that we want to keep.
  ```sh
  dataframe = dataframe[test_column]
  ```

Next we drop the NaN from the dataset.

* the test columns are a list of columns that we want to keep.
  ```sh
  clean_data = dataframe.dropna()
  ```

Lastly we sort the database by school district and the lables of the indenpendet variables that we want to test. 

* the average is what we are testing against the dependent variable. 
  ```sh
  clean_data.groupby(['School District Code',selection_column]).mean()
  ```

Now the independent variable data is cleaned. 

## Analysis and graphing the independent variable against the dependent variable. 

To graph the data, we would need the following information: 
1. the merged dataframe.
2. labels for the independent variables.
3. values for the independent variables.

First we create a list of the labels for the independent variables. 

* Use the .unique() to isolate the list of independent variables that we are testing.

  ```sh
  description_list = merged_academic[selection_column].unique()
  merged_academic.loc[:,:] = merged_academic.groupby(['School District Code',selection_column]).mean().reset_index()
  ```

Then we create a for loop for each lables and pulling the values. 
* Be sure to use .drop_duplicates() to remove any duplicate data.
  ```sh
  for description in description_list:
    instruction_df = merged_academic.loc[(merged_academic[selection_column] == description)]
    instruction_df.drop_duplicates()
  ```

Now we will find the z values for each value in the independent variable and we will remove all z values that are over -3 and 3 to remove outliers. 

* z scores will be generated against other values in the independent variable column.
  ```sh
  z = (stats.zscore(instruction_df.loc[:,indepent_var_label]))
  instruction_df.loc[:,(f'{description}_zscore')] = z
  instruction_df = instruction_df.loc[(instruction_df[f'{description}_zscore']<3) & (instruction_df[f'{description}_zscore']>-3)]
  ```

we can now put the x and y values that we want to graph.

* put in the values and generate linear regression variables.
  ```sh
  x_values = instruction_df[indepent_var_label]
  y_values = instruction_df['Percent']
  # fill out the information necessary for linear regression
  (slope, intercept, rvalue, pvalue, stderr) = stats.linregress(x_values, y_values)
  regress_values = x_values * slope + intercept
  line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
  ```

put in the parameters for the graphs that we are generating.

* put in the values and generate linear regression variables.
  ```sh
  plt.figure(figsize=(15,15), dpi=300)
  plt.scatter(x_values,y_values)

  plt.xlabel(f"{description}")
  plt.ylabel('% of Graduates into College')
  plt.title(f"{description} vs. Into College ")
  plt.plot(x_values,regress_values,"r-")
  plt.annotate(line_eq,(20,15),fontsize=15,color="red")
  print(f"The r-value is: {rvalue**2}")
  print(f"The intercept value is: {intercept}")
  print(f"The p-value is: {pvalue}")
  plt.savefig(f'../images/{description}.png',bbox_inches = 'tight')
  plt.show()
  ```

We can now analyze the graphs and export the images. 



# Conclusion

# 1.

## Spend more funds on hiring qualified 9th grade teachers

# 2.

## Emphasize importance of success in 9th grade courses

# 3.

## Implement specific programs to aid homeless students

# 4.

## Offer SAT/ACT prep to all students in schools

