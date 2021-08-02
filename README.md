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

![hero image](https://github.com/HsuChe/matplotlib_challenge/blob/a25ee9a2ca6e4f6dd4c99a6167490a08182b8bba/Images/mouse-1708347_1920.jpg)

Graduating from high school can mean different things to different people as graduation criteria can often be different between schools and the standard can be opaque. The overall competitiveness of students graduating from Georgia district highschools can be standardized by their enrollment into college after graduation. 

We took graduation data and enrollment data from 2018 and calculated the percent of student enrolling to college after graduation. We will use that metric as the dependent variable and we will test various variables to see what is the best way to improve school performance.

Features of the dataset:

* The dependent variable is cleaned and filtered base on the School District Code.
* We will retain the following columns to be analyzed in the dataset.

  * Graduates: **The number of people graduating from the school district in year 2018**
  * Postsecondary Institution: **Number of students that enrolled in post secondary institutions after graduation.**
  * Percent: **The percent of students that went to college after graduation (Dependent Variable)**
* The dataset is in the csv file format with delimiter of comma.
* Download the dataset [HERE](https://github.com/HsuChe/matplotlib_challenge/blob/a25ee9a2ca6e4f6dd4c99a6167490a08182b8bba/Pymaceuticals/data/Mouse_metadata.csv)
* Download 1st half of Dataset click [HERE](https://github.com/HsuChe/matplotlib_challenge/blob/a25ee9a2ca6e4f6dd4c99a6167490a08182b8bba/Pymaceuticals/data/Study_results.csv)

The homework is interested generating a few specific items for the summary table for changes in tumor growth over various timepoints.

<!-- GETTING STARTED -->

## Processing the csv and make it into a easier to use dataset.

Import the dependencies for the dataset

* For loop to add to list
  ```sh
  import metplotlib.pyplot as plt
  import pandas as pd
  ```

After importing the dependencies, go ahead and merge the first and the second half the of the data.

* Merge the data
  ```sh
  mouse_metadata_path = "data/Mouse_metadata.csv"
  study_results_path = "data/Study_results.csv"
  mouse_metadata = pd.read_csv(mouse_metadata_path)
  study_results = pd.read_csv(study_results_path)
  mouse_metadata.head(),study_results.head()
  merge_df = pd.merge(mouse_metadata,study_results, how = 'inner', on = 'Mouse ID')
  ```

### finding specific information about mouse IDs to know how to clean the data.

We can begin analyzing various aspects of mouse ID. First we tried to find the exact number of unique mice in the dataset.
The two most important information for this dataset is the timepoint.

* See if there are any mouse with duplicate mouse ID and timepoint
  ```sh
  df.loc[df.duplicated(subset = ['Mouse ID', 'Timepoint'], keep='last')]
  ```

This will help us find out that specifically mouse ID g989 has duplicate mouse ID and timepoint.

Next we will remove the specific mouse ID from the dataset

* Removing the g989 Mouse ID
  ```sh
  df_989_drop = df.loc[df['Mouse ID'] != need_to_drop['Mouse ID'].unique()[0]]
  df_989_drop.reset_index(drop = True)
  len(df_989_drop['Mouse ID'].unique())
  ```

## Generating a DataFrame without the duplicates

The next goal is to generate the dataframe without all the duplicated mouse ID and take the latest iteration of Timepoint from them.

This dataset is ordered from least to greatest so we can keep the higher Timepoint by taking the last iteration of the duplicate.

* Avearge change in profit and losses month to month.
  ```sh
  df_dup_drop = df_989_drop.drop_duplicates('Mouse ID', keep = 'last')
  df_dup_drop
  ```

## Generating Summary Statistics

The great increase and decrease is calculated by calculating the max and min of the change list and while referencing their index location to find the months that these changes happened.

* Generating the summary statistics the conventional way, by creating the DataFrame from scratch.
  ```sh
  group_drug = df.groupby('Drug Regimen')
  summary_mean = group_drug['Tumor Volume (mm3)'].mean().round(2)
  summary_med = group_drug['Tumor Volume (mm3)'].median().round(2)
  summary_var = group_drug['Tumor Volume (mm3)'].var().round(2)
  summary_std = group_drug['Tumor Volume (mm3)'].std().round(2)
  summary_sem = group_drug['Tumor Volume (mm3)'].sem().round(2)

  summary_table = pd.DataFrame()
  summary_table['Mean'] = summary_mean
  summary_table['Med'] = summary_med
  summary_table['Var'] = summary_var
  summary_table['St Dev'] = summary_std
  summary_table['St Err'] = summary_sem
  ```

Another way to generate the summary table is using the aggregate method.

* Store Yearly Change and Yearly Percent Change to memory
  ```sh
  summary_table = group_drug.agg({'Tumor Volume (mm3)':['mean','median','var','std','sem']})
  summary_table.columns = ['Mean', 'Med', 'Var', 'St Dev', 'St Err']
  summary_table
  ```

## Generating Bar and Pie Chart

We for variables for each of the information we calculated before and map them into a string.

* Create the bar chart showing the distribution of Regiment

  ```sh
  drug_id = df_dup_drop.groupby('Drug Regimen')['Mouse ID'].count()
  drug_id.plot.bar(color = 'green', figsize=(15,5))
  plt.xlabel('Drug Regiment')
  plt.ylabel('Mouse Count')
  plt.title('Mouse Count vs Regiment')
  plt.show()
  ```
* Creating the chart with plt instead of pandas

  ```sh
  gender_spread = df_dup_drop.groupby('Sex')['Mouse ID'].count()
  gender_spread.plot.pie(figsize = (8,8),labels = ['Male','Female'],autopct='%1.1f%%', shadow = True, startangle = 90)
  plt.xlabel('Mice Count')
  plt.ylabel('Gender')
  plt.title('Gender Mice Count')
  plt.show()
  ```

```

* Creating the chart with plt instead of pandas
  ```sh
  gender_spread = df_dup_drop.groupby('Sex')['Mouse ID'].count()
  gender_spread.plot.pie(figsize = (8,8),labels = ['Male','Female'],autopct='%1.1f%%', shadow = True, startangle = 90)
  plt.xlabel('Mice Count')
  plt.ylabel('Gender')
  plt.title('Gender Mice Count')
  plt.show()
```

* Creating the chart with plt instead of pandas
  ```sh
  plt.figure(figsize = (8,8))
  plt.pie(gender_spread, labels = gender_spread.index, autopct = "%1.1f%%", shadow= True, startangle = 90)
  plt.xlabel('Mice Count')
  plt.ylabel('Gender')
  plt.title('Gender Mice Count')
  plt.show()

  ```

```

## Quartiles, Outliers, and Boxplots

<br>
<br>
<br>

We want a dataframe that has the tumor volume for the last iteration of timepoint. 

* For loop to add to list
```sh
df_max_time = pd.DataFrame(df_dup_drop.groupby('Mouse ID')['Timepoint'].max()).reset_index()

df_time = pd.merge(df_max_time,df_dup_drop,on=['Mouse ID','Timepoint'])]
```

After generating the csvlist, find the total number of votes being accounted for. To do this, we will find the index of the rows.

* Function to find the box and whiskers graph and outliers
  ```sh
  def boxplot_drugs(drug_list):
    drug_df = pd.DataFrame()
    for drugs in drug_list:
        tumor_vol = df_time.loc[df_time['Drug Regimen'] == drugs]['Tumor Volume (mm3)']
        drug_df[drugs] = tumor_vol.reset_index(drop=True)

        # Calculate the IQR and quantitatively determine if there are any potential outliers. 

        # Locate the rows which contain mice on each drug and get the tumor volumes
        quartiles = tumor_vol.reset_index(drop=True).quantile([.25,.5,.75])
        # add subset 
        lowerq = quartiles[0.25]
        upperq = quartiles[0.75]
        iqr = upperq-lowerq
        # Determine outliers using upper and lower bounds
        lower_bound = quartiles[0.25] - (1.5*iqr)
        upper_bound = quartiles[0.75] + (1.5*iqr)
        print(f"Upper/Lower Bound: {drugs}")
        print(f"Values below {lower_bound.round(2)} could be outliers.")
        print(f"Values above {upper_bound.round(2)} could be outliers.")

    return drug_df


  drug_df = boxplot_drugs(drug_list)
  ```

## Line and Scatter Plots

To plot effectiveness for each regiment and its effect on the weight of the mouse.

* plotting a line graph for changes in tumor size over Time Point:
  ```sh
  mouse_name = df_time.loc[df_time['Drug Regimen'] == 'Capomulin']['Mouse ID'].iloc[0]
  mouse_info = merge_df.loc[merge_df['Mouse ID'] == mouse_name][['Timepoint','Tumor Volume (mm3)']]
  mouse_info.index = mouse_info['Timepoint']
  mouse_info['Tumor Volume (mm3)'].plot.line(figsize = (10,6))
  plt.xlabel('Time Point (Days)')
  plt.ylabel('Tumor Size (mm^3)')
  plt.title(f'My Mouse "{mouse_name}" Will Live')
  ```

## Regression and Correlation

Finding the information on the effectiveness of regimen against size.

* Scatter plot for Timepoint against Tumor Size:
  ```sh
  from scipy.stats import linregress

  x_axis = mouse_vol_weight['Weight (g)']
  y_axis = mouse_vol_weight['Tumor Volume (mm3)']
  (slope, intercept, rvalue, pvalue, stderr) = linregress(x_axis, y_axis)
  y_values = slope*x_axis+intercept
  print(f"regression function: f(x) = {slope.round(2)}x + {intercept.round(2)}")
  plt.figure(figsize=(10,7))
  plt.plot(x_axis, y_values)
  plt.scatter(x_axis, y_axis)
  plt.xlabel('Weight (g)')
  plt.ylabel('Tumor Size (mm^3)')
  plt.title('Effect of Capomulin on Weight')
  plt.show()
  ```

## Conclusion

### 1.

#### The dataset has a nice spread in terms of giving an even amount of regiment to each mouse. There are no real statistical bias in terms of the distribution of regiments

### 2.

#### The dataset has a nice spread for gender of the mouse, there are no significant bias between the male and female population in the data.

### 3.

#### Based on the bar and whisker graph, the regiment Capomulin and Ramicane seems to be the more effective regiment as the tumor volume seems to be the lowest on the last time point. However, the drugs Infubinol and Ceftamin are more consistant as their outliers are closer to the lower and higher quantiles.

#### Infubinol and Ceftamin should yield more consistant results and if those drugs are more effective past 45 time point, then they might be better drugs than Capomulin and Ramicane.
