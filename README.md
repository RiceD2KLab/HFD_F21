# Houston Fire Department - Fall 2021
#### Members: Hannah Lei, Mingzhao Liu, Yikun Li, Sacheth Reddy Mamidi, Parth Parulekar

This is our repository that contains the code for our capstone project: <br /> **Analyzing Fire Inspections for the Houston Fire Department**

### NOTE: Since we do not have admin permissions on this repository, we are unable to change the default branch to "master" which is the branch we are working on.

DISCLAIMER: The Houston Fire Department data is private and cannot be posted to a public repository. In order to run our files and generate diagrams based on the dataset we were given, please locate and download the files `Address_&_Violation_Records_data 2020.csv` and `Address_&_Violation_Records_data 2021.csv`.

## Steps to Run our Python Code

1. Clone repository to your local machine
2. Install dependencies with the following commands:

```
pip install seaborn
pip install pandas
pip install numpy
pip install matplotlib
pip install geopandas
pip install plotly 
```

3. Open terminal and run `python HFD_Data_Cleaning_till_VIOLATIONDESCRIPT.py`
4. Diagrams and graphs should pop up in a Matplotlib window. These windows 
   can be closed and Python should generate the next graph, which will open
   in a new window promptly.
5. Alternatively, you may open HFD_Data_Cleaning_till_VIOLATIONDESCRIPT.py in an IDE 
   such as Visual Studio Code and run each of the code blocks to generate visuals based on    the dataset in a readable format.


### For the interactive maps
1. Run the create shape file to get a silhouette of Houston in .shp

2. Run the create cav to get the required data to create the interactive map

3. Run the testGeoPy file to get the HTML outputs 

4. Run the Integrate.html file to see the website where the interactive maps of each team can be selected 


### For the word clouds
Go into wordcloud directory:

* To see results, go into directories:
   - violation_word_clouds_by_inspector
   - violation_word_clouds_by_teamcode

* To recreate word clouds: 
   1. Run printViolationComment.py 
   2. Run wordFrequencyGenerator.py using the output from (1)
   3. Run wordCloudfromFreqGenerator.py to generate word cloud from the frequency csv file made from (2)


