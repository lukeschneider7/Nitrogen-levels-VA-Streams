import tkinter as tk
from tkinter import simpledialog
import csv
# Plotting was done inspired from https://stackoverflow.com/questions/19079143/how-to-plot-time-series-in-python
# GUI code modified from https://djangocentral.com/creating-user-input-dialog/
# Parsing data inspired from https://evanhahn.com/how-to-read-tsv-files-in-python/
def compare_data(nitrogen_data, second_parameter, file_path, second_stat = ''):
    import numpy as np
    """
    :param nitrogen_data: daily nitrogen data
    :param second_parameter: temp, discharge or pH data
    :param file_path: path to data file
    :param second_stat: name of second statistic being comapared to nitrogen
    :return trend_strength: % of days that follow most common trend between two parameters
    """
    both_stat_same = 0
    stat_oppo_direction = 0
    no_change = 0
    # Take daily changes in Nitrogen and second parameter being measured
    for entry in nitrogen_data:
        nitrogen_deltas = np.diff(nitrogen_data)
    for entry in second_parameter:
        parameter_deltas = np.diff(second_parameter)
    trend_counter = 0
    # Count how often nitrogen and second stat have the same change behavior
    for diff1 in nitrogen_deltas:
        if diff1 > 0 and parameter_deltas[trend_counter] > 0:
            both_stat_same += 1
        elif diff1 <0 and parameter_deltas[trend_counter] < 0:
            both_stat_same += 1
        elif diff1 == 0 or parameter_deltas[trend_counter] == 0:
            no_change += 1
        else:
            stat_oppo_direction += 1
        trend_counter += 1
    # Info for site and chosen stats, trend strenghpercent of days that obey most popoular trend between nitrogen and chosen stat
    trend_strength = (max(both_stat_same, stat_oppo_direction, no_change))/(both_stat_same + stat_oppo_direction + no_change)
    print("Nitrogen and", second_stat, "daily changes 2022-23")
    print(".........................................................")
    print(("stream|\t\tsame_direction|\t\topp_direction|\t\tno_change|"))
    print(file_path[:(len(file_path) - 4)],"|\t",both_stat_same,"|\t",stat_oppo_direction,"|\t", no_change,)
    print(".........................................................")
    print("Highest 2022-23 nitrogen level:", max(nitrogen_data), "mg/L for", file_path[:(len(file_path) - 4)])
    return trend_strength
def parse_usgs(file_path = ''):
    import matplotlib.pyplot as plt
    from datetime import datetime
    import pandas as pd
    """
    Parse the USGS data and return appropriate data
    :param file_path: Path to data file
    :return water_data:
    """
    #Open file and set variables to hold time, Nitrogen, and compared parameter values
    with open(file_path, "r", encoding="utf8") as stream_file:
        tsv_reader = csv.reader(stream_file, delimiter="\t")
        measured_daily_data = []
        dates = []
        dates2 = []
        measured_daily_data2 = []

        #Ask User which water quality metric they want to see compared to Nitrogen for chosen stream
        USER_INP2 = simpledialog.askstring(title="USGS Water Monitoring Stations",
                                           prompt="Which parameter do you want to compare to Nitrogen ? \n A) Discharge"
                                                 "\n B) Temperature \n C) Dissolved Oxygen")
        if USER_INP2 == "A":
            # skip over data explanation to get to row of data parameters
            for row in tsv_reader:
                if row[0] != 'agency_cd':
                    continue
                # Look for column index with qualification codes (cd) for daily data on mean discharge and mean Nitrogen
                else:
                    column_index_of_nit_cd = 0
                    column_index_of_flow_cd = 0
                    #Search for location of desired parameter_statistic_cd to work for any file
                    for element in row:
                        if '99133_00008_cd' in element:
                            break
                        else:
                            column_index_of_nit_cd += 1
                    for element in row:
                        if '00060_00003_cd' in element:
                            break
                        else:
                            column_index_of_flow_cd += 1
                    # Go back a column to get from qualification code to actual data
                    column_index_of_nit = (column_index_of_nit_cd - 1)
                    column_index_of_flow = (column_index_of_flow_cd - 1)
                    # skip over data explanations and headers this time
                    for line in tsv_reader:
                        if line[0] != 'USGS':
                            next(tsv_reader)
                        # Ignore the junk entries for when data wasn't recorded
                        elif line[column_index_of_nit] == '' or line[column_index_of_nit] == 'Bkw' or line[column_index_of_nit] == 'Eqp' or line[column_index_of_flow] == 'Bkw' or line[column_index_of_flow] =='':
                            next(tsv_reader)
                        # Add time, Nitrogen, and discharge data for each 'good' line to variables
                        else:
                            measured_daily_data.append(float(line[column_index_of_nit]))
                            measured_daily_data2.append(float(line[column_index_of_flow]))
                            dates.append(line[2])
                            dates2.append(line[2])
                    # Compare relationship between Nitrogen and Temperature
                    comparison = compare_data(measured_daily_data, measured_daily_data2, file_path, 'Discharge')
                    print("Percent of days experiencing trend :", comparison*100)

                    # Plot 1 for Nitrogen over time
                    dates = [datetime.strptime(x, '%Y-%m-%d') for x in dates]
                    df = pd.DataFrame({'date': dates, 'nitrogen': measured_daily_data})
                    df['date'] = pd.to_datetime(df['date'])
                    xs, ys, = zip(*sorted(zip(dates, measured_daily_data)))  # sort by date
                    plt.subplot(1, 2, 1)
                    plt.plot(xs, ys)
                    plt.xlabel('Time (year-month)')
                    plt.ylabel('Nitrogen median amount (mg/L)')
                    usgs_location = file_path[:(len(file_path) - 4)]
                    plt.title('Daily median Nitrate + Nitrite data for ' + usgs_location)

                    # Plot 2 for compared parameter (discharge) over time
                    dates2 = [datetime.strptime(d, '%Y-%m-%d') for d in dates2]
                    df = pd.DataFrame({'date2': dates2, 'flow': measured_daily_data2})
                    df['date2'] = pd.to_datetime(df['date2'])
                    xs, zs, = zip(*sorted(zip(dates, measured_daily_data2)))  # sort by date
                    plt.subplot(1, 2, 2)
                    plt.plot(xs, zs)
                    plt.xlabel('Time (year-month)')
                    plt.ylabel('Volumetric discharge (cfs) ')
                    usgs_location = file_path[:(len(file_path) - 4)]
                    plt.title('Daily mean Discharge data for: ' + usgs_location)
                    plt.show()

        elif USER_INP2 == "B":
            for row in tsv_reader:
                if row[0] != 'agency_cd':
                    continue
                else:
                    column_index_of_nit_cd = 0
                    column_index_of_temp_cd = 0
                    for element in row:
                        if '99133_00008_cd' in element:
                            break
                        else:
                            column_index_of_nit_cd += 1
                    for element in row:
                        if '00010_00008_cd' in element:
                            break
                        else:
                            column_index_of_temp_cd += 1
                    column_index_of_nit = (column_index_of_nit_cd - 1)
                    column_index_of_temp = (column_index_of_temp_cd - 1)
                    for line in tsv_reader:
                        if line[0] != 'USGS':
                            next(tsv_reader)
                        elif line[column_index_of_nit] == '' or line[column_index_of_nit] == 'Bkw' or line[column_index_of_nit] == 'Eqp' or line[column_index_of_temp] == '':
                            next(tsv_reader)
                        else:
                            measured_daily_data.append(float(line[column_index_of_nit]))
                            measured_daily_data2.append(float(line[column_index_of_temp]))
                            dates.append(line[2])
                            dates2.append(line[2])
                    comparison = compare_data(measured_daily_data, measured_daily_data2, file_path, 'Temp')
                    print("Percent of days experiencing trend :", comparison * 100)

                    dates = [datetime.strptime(x, '%Y-%m-%d') for x in dates]
                    df = pd.DataFrame({'date': dates, 'nitrogen': measured_daily_data})
                    df['date'] = pd.to_datetime(df['date'])
                    xs, ys, = zip(*sorted(zip(dates, measured_daily_data)))  # sort by date
                    plt.subplot(1, 2, 1)
                    plt.plot(xs, ys)
                    plt.xlabel('Time (year-month)')
                    plt.ylabel('Nitrogen median amount (mg/L)')
                    usgs_location = file_path[:(len(file_path) - 4)]
                    plt.title('Daily median Nitrate + Nitrite data for ' + usgs_location)

                    dates2 = [datetime.strptime(d, '%Y-%m-%d') for d in dates2]
                    df = pd.DataFrame({'date2': dates2, 'temp': measured_daily_data2})
                    df['date2'] = pd.to_datetime(df['date2'])
                    xs, zs, = zip(*sorted(zip(dates, measured_daily_data2)))  # sort by date
                    plt.subplot(1, 2, 2)
                    plt.plot(xs, zs)
                    plt.xlabel('Time (year-month)')
                    plt.ylabel('Temperature Mean (celsius) ')
                    usgs_location = file_path[:(len(file_path) - 4)]
                    plt.title('Daily mean temp data for: ' + usgs_location)
                    plt.show()

        elif USER_INP2 == 'C':
            for row in tsv_reader:
                if row[0] != 'agency_cd':
                    continue
                else:
                    column_index_of_nit_cd = 0
                    column_index_of_do_cd= 0
                    for element in row:
                        if '99133_00008_cd' in element:
                            break
                        else:
                            column_index_of_nit_cd += 1
                    for element in row:
                        if '00300_00008_cd' in element:
                            break
                        else:
                            column_index_of_do_cd +=1
                    column_index_of_nit = (column_index_of_nit_cd -1)
                    column_index_of_do = (column_index_of_do_cd - 1)
                    for line in tsv_reader:
                        if line[0] != 'USGS':
                            next(tsv_reader)
                        elif line[column_index_of_nit] == '' or line[column_index_of_nit] == 'Bkw' or line[column_index_of_nit] == 'Eqp' or line[column_index_of_do] == '':
                            next(tsv_reader)
                        else:
                            measured_daily_data.append(float(line[column_index_of_nit]))
                            measured_daily_data2.append(float(line[column_index_of_do]))
                            dates.append(line[2])
                            dates2.append(line[2])
                    comparison = compare_data(measured_daily_data, measured_daily_data2, file_path, 'Dissolved Oxygen')
                    print("Percent of days experiencing trend :", comparison * 100)

                    dates = [datetime.strptime(x, '%Y-%m-%d') for x in dates]
                    df = pd.DataFrame({'date': dates, 'nitrogen': measured_daily_data})
                    df['date'] = pd.to_datetime(df['date'])
                    xs, ys, = zip(*sorted(zip(dates, measured_daily_data)))  # sort by date
                    plt.subplot(1, 2, 1)
                    plt.plot(xs, ys)
                    plt.xlabel('Time (year-month)')
                    plt.ylabel('Nitrogen median amount (mg/L)')
                    usgs_location = file_path[:(len(file_path) - 4)]
                    plt.title('Daily median Nitrate + Nitrite data for ' + usgs_location)

                    dates2 = [datetime.strptime(d, '%Y-%m-%d') for d in dates2]
                    df = pd.DataFrame({'date2': dates2, 'pH': measured_daily_data2 })
                    df['date2'] = pd.to_datetime(df['date2'])
                    xs, zs, = zip(*sorted(zip(dates, measured_daily_data2)))  # sort by date
                    plt.subplot(1, 2, 2)
                    plt.plot(xs, zs)
                    plt.xlabel('Time (year-month)')
                    plt.ylabel('Dissolved Oxygen median amount (mg/L) ')
                    usgs_location = file_path[:(len(file_path) - 4)]
                    plt.title('Daily median Dissolved Oxygen data for: ' + usgs_location)
                    plt.show()
    return measured_daily_data
# Main function for asking user which VA stream they want to see data for
if __name__ == "__main__":
    ROOT = tk.Tk()
    ROOT.withdraw()
    USER_INP = simpledialog.askstring(title="USGS Water Monitoring Stations",
                                      prompt="Which stream do you want to see data for? \n A) Difficult Run \n " 
                                              "B) James River \n C) Smith Creek \n D) Snakeden Branch \n ""E) The Glade")
    if USER_INP == "A":
        parse_usgs('difficult_run.csv')
    elif USER_INP == "B":
        parse_usgs('james_river.csv')
    elif USER_INP == "C":
        parse_usgs('smith_creek.csv')
    elif USER_INP == "D":
        parse_usgs('snakeden_branch.csv')
    elif USER_INP == "E":
        parse_usgs('the_glade.csv')