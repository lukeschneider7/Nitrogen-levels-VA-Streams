# Nitrogen-levels-VA-Streams
ENGR_265  Final project analysing VA USGS water data to look for patterns in Nitrogen Data

This code was written to evaluate USGS water data to see how high Nitrogen levels are in Virgina stream as well as how they 
have change over time and how they relate to other water quality metrics

This program required Daily data sets from the 10 USGS monitoring locations in VA that track nitrogen levels in water.
I realized only 5 of these locations actually had compiled the nitrogen level data into downloadable files.
I aslo learned that the locations only had downloadable files for annual discharge and it was daily data only on nitrogen levels so I would have to work with that and evaluate nitrogen level changes over days instead of years.

usgs_water_data.py was written to parse the USGS and then ask a user which stream they wanted information for.
-numpy, pandas, csv, tkinter, datetime and matplotlib were modules that were used.

The main part of the file asks for user input on which stream they would like to see data for.
The parsing data function is then called and the selected file is opened in tab seperated format.
The user is then asked which water quality characteristic they would like to see compared to nitrogen levels between discharge, temp and dissolved oxygen.
Empty entries of the data are ignored and the others are compiled along with time data and nitrogen and either dishcarge, temp or dissolved oxygen are both plotted over time. Nitrogen and the selected second characteristic are also paramters for the compare_data function. This function takes the change each day in nitrogen levels and the other statistic and then sees how often they either both increase/decrease, don't change, or move in the opposite direction
The percentage of changes that fit with the most common trend between the two datasets is then printed along with the max nitrogen level for the stream.

Results:
- Image of Dissolved oxygen next to Nitrogen plot for stream and comparison data
- Dissolved oxygen seems to be the only parameter related to Nitrogen levels although this could only be seen graphically and not through the daily changes
- Plots support the notion that an increase in Nitrogen will lead to a decrease in Dissolved oxygen a month or two later
<img width="1440" alt="Screenshot 2023-05-08 at 9 44 19 AM" src="https://user-images.githubusercontent.com/100543430/236840257-b9278631-ef01-4042-89df-cb7b8587693e.png">

![image](https://user-images.githubusercontent.com/100543430/236840465-4ae1e126-8f5e-412a-ba68-eefb2704c168.png)



Limitations:
- Only 5 datasets for VA and only have daily not annual data for nitrogen Levels
- Don't have option to plot more multiple parameters or creaks at the same time
- Only max and daily changes were calculated from nitrogen data
- compare_data function not a good indicator of relationship between nitrogen and dissolved_oxygen


Future results:
- Look at nitrogen levels based on how far up/downstream they are, land use in drainage area and if any local wastewater plants
- make function to look at 1) How long change in Nitrogen levels takes to impact dissolve oxygen levels, and 2) how strong this relationship is.
- Plot nitrogen levels at each stream on the same plot to compare how they change seasonally
- Use data from monitoring stations in other regions and compare data to VA stations
