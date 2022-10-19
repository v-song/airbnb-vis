

"""
The goal is to look at the Airbnb
    data of dfferent cities in different years and determine whether there is correlation between the price of a
    listing and overall satisfaction, if hosts have multiple listings at the same time, how the prices of rentals
    change over time, and how the prices of listings are different in different neighborhoods.
"""

from scipy.stats.stats import spearmanr
import matplotlib.pyplot as plt

# PART 1
def price_satisfaction(filename):
    """
    This function takes a string that is a filename as a parameter and returns a list of lists. Each list has two elements,
    price of listing and overall satisfaction with listing.

    :param filename: a string that is a file name (str)
    :return: list of lists, and each list has two floats (list)
    """
    # opens the file for reading
    file_in = open(filename, "r")
    # reads the first line of the file
    first_line = file_in.readline()
    # reads every line after the first of the file
    lines = file_in.readlines()
    # makes a list from the first line of the file, splitting after each comma
    first_split = first_line.split(",")

    outer_list = []
    inner_list = []

    # loops over the words in each line and puts them into a list
    for words in lines:
        split = words.split(",")

        # for loop iterates over the number of columns (the number of entries in the first line)
        for k in range(len(first_split)):
            # if the number of reviews is greater than 0, runs the rest of the code
            if first_split[k] == "reviews":
                if int(split[k]) > 0:

                    for i in range(len(first_split)):
                        for j in range(len(first_split)):

                            # adds the values in the price column and the overall satisfaction column as a tuple into
                            # a new list
                            if first_split[i] == "price":
                                if first_split[j] == "overall_satisfaction":
                                    inner_list = [float(split[i]), float(split[j])]

                    # appends the inner list to an outer list and resets the inner list
                    outer_list.append(inner_list)
                    inner_list = []

    # returns the outer list
    return outer_list

def correlation(l):
    """
    This function uses a list of lists that consists of price and overall satisfaction (both floats). It uses a
    Spearman's rank correlation to return the correlation and pvalue between the price and overall satisfaction.

    :param l: a list of lists consisting of floats: price and overall satisfaction (list)
    :return: a tuple consisting of correlation (float) and overall satisfaction (float), (tuple)
    """
    price_list = []
    rating_list = []

    # for loop loops over the number of lists in the list in the parameter
    for i in range(len(l)):
        # adds the first element in each sublist to the list of prices
        price_list.append(l[i][0])
        # adds the second element in each sublist to the list of ratings
        rating_list.append(l[i][1])
    # calls spearmanr to compute the correlation between the list of prices and list of ratings
    result = spearmanr(price_list, rating_list)
    correlation = result.correlation
    pvalue = result.pvalue
    # sets tuple as a tuple consisting of the correlation and pvalue from spearmanr
    tuple = (float(correlation), float(pvalue))
    # returns the tuple
    return tuple

# PART 2
def host_listings(filename):
    """
    This function takes a string that is a file name and uses it to create a dictionary. The dictionary's keys are host ids
    and the associated values are the room ids that belong to that host

    :param filename: a string that is a file name (str)
    :return: a dictionary with host ids as keys (int) and room ids (int) in a list as values, (dict)
    """
    dict = {}
    # opens filename to read
    file_in = open(filename, "r")
    # reads the first line of the file
    first_line = file_in.readline()
    # reads the lines after the first line of the file
    lines = file_in.readlines()
    # splits the first line of the file into a list, separating by commas
    first_split = first_line.split(",")
    values_list = []

    # loops over the words in each line and puts them into a list
    for words in lines:
        split = words.split(",")

        # for loops loop over the elements in the columns containing host id and room id
        for i in range(len(first_split)):
            for j in range(len(first_split)):
                if first_split[i] == "host_id":
                    if first_split[j] == "room_id":

                        # if host id is already in dictionary, adds additional room ids to the list that is the value
                        if int(split[i]) in dict.keys():
                            dict[int(split[i])].append(int(split[j]))
                        # if the host id isn't already in  dictionary, adds new item with room id (list) as the value
                        else:
                            dict[int(split[i])] = [int(split[j])]
    return dict

def num_listings(d):
    """
    This function takes d, a parameter that's a dictionary consisting of keys that are host ids and values that are lists
    of room ids. The function returns a list consisting of the number of hosts with i amount of listings.

    :param d: a dictionary of keys that are host ids (int) and values that are lists of room ids (int), (dict)
    :return: a list where where l[i] is the number of hosts with i listings (list)
    """
    num_list = []
    frequency_list = []
    max_listing = 0
    list_d = list(d)
    count = 0

    # compares the number of values/listings associated with host ids to identify the greatest number of listings for any one host
    for i in range(len(d)):
        if (len(d[list_d[i]]) > max_listing):
            max_listing = len(d[list_d[i]])

    # counts how many hosts have listings that are equal to i
    for i in range(max_listing+1):
        for host in d.keys():
            # if the number of listings a host has is equal to i, adds one to the count
            if len(d[host]) == i:
                count += 1
        # appends the frequency of hosts with i number of listings to a list
        num_list.append(count)
        # resets the count to zero
        count = 0
    # returns a list with the number of hosts with exactly i listings
    return num_list

# PART 3
def room_prices(filename_list, roomtype):
    """
    This function takes a list of filenames and the room type as parameters. It organizes the filenames by date and
    creates a dictionary mapping room ids for a certain roomtype to the change in the room id's price over the years
    :param filename_list: a list of filenames that are strings (list)
    :param roomtype: a room type (string)
    :return: a dictionary with room ids (int) as keys and a list of prices (float) over time as values
    """
    file_list = filename_list
    d = {}
    new_d = {}

    # creates dictionary mapping dates to file names (not in order)
    for elem in filename_list:
        # strips the file name of ".csv"
        stripped = elem.strip(".csv")
        # separates the file name into a list of strings based on "_"
        elem_split = stripped.split("_")
        # maps the last element of the list (the date) to the file name
        d[elem_split[-1]] = (elem)

    # turns the keys in the dictionary into a list
    list_d = list(d)

    # uses insertion sort to sort the list of dates and list of filenames in chronological order
    for i in range(1, len(list_d)):
        value = list_d[i]
        value2 = file_list[i]
        pos = i
        while pos>0 and list_d[pos-1]>value:
            list_d[pos]=list_d[pos-1]
            file_list[pos] = file_list[pos-1]
            pos = pos-1
        list_d[pos]=value
        file_list[pos]=value2

    # creates an ordered dictionary mapping the reorganized dates to their corresponding file names
    for elem in file_list:
        stripped = elem.strip(".csv")
        elem_split = stripped.split("_")
        new_d[elem_split[-1]] = (elem)

    id_list = []
    price_list_1 = []
    price_list_2 = []
    price_list_3 = []
    output_dict = {}

    # opens the first, second, and third files in the ordered list for reading
    file_in_1 = open(file_list[0], "r")
    file_in_2 = open(file_list[1], "r")
    file_in_3 = open(file_list[2], "r")

    # reads the first line in the first file
    first_line_1 = file_in_1.readline()
    # reads the following lines in the first file
    lines_1 = file_in_1.readlines()
    # splits the first line of the first file into a list based on commas
    first_split_1 = first_line_1.split(",")

    # reads the first line in the second file
    first_line_2 = file_in_2.readline()
    # reads the following lines in the second file
    lines_2 = file_in_2.readlines()
    # splits the first line of the second file into a list based on commas
    first_split_2 = first_line_2.split(",")

    # reads the first line in the third file
    first_line_3 = file_in_3.readline()
    # reads the following lines in the third file
    lines_3 = file_in_3.readlines()
    # splits the first line of the third file into a list based on commas
    first_split_3 = first_line_3.split(",")

    # loops over the words in each line in the first file and puts them into a list
    for words_1 in lines_1:
        split_1 = words_1.split(",")
        # loops over the elements in the columns for room id and the rows containing shared room
        for i in range(len(first_split_1)):
            for j in range(len(first_split_1)):
                if first_split_1[i] == "room_id":
                    if split_1[j] == "Shared room":

                        # loops over the columns under price
                        for k in range(len(first_split_1)):
                            if first_split_1[k] == "price":

                                # creates a dictionary mapping room id to corresponding price (list)
                                output_dict[int(split_1[i])] = [float(split_1[k])]

    # loops over the words in each line in the second file and puts them into a list
    for words_2 in lines_2:
        split_2 = words_2.split(",")

        # loops over the elements in the column for room id and the rows containing shared room
        for i in range(len(first_split_2)):
            for j in range(len(first_split_2)):
                if first_split_2[i] == "room_id":
                        if split_2[j] == "Shared room":

                            # loops over the columns under price
                            for k in range(len(first_split_2)):
                                if first_split_2[k] == "price":

                                    # if the room id is already in the keys of the dictionary, appends price to the list of values
                                    if int(split_2[i]) in list(output_dict):
                                        output_dict[int(split_2[i])].append(float(split_2[k]))
                                    # if room id isn't in keys of dictionary, adds it and maps it to price
                                    else:
                                        output_dict[int(split_2[i])] = [float(split_2[k])]


    # loops over the words in each line in the third file and puts them into a list
    for words_3 in lines_3:
        split_3 = words_3.split(",")

        # loops over the elements in the column for room id and the rows containing shared room
        for i in range(len(first_split_3)):
            for j in range(len(first_split_3)):
                if first_split_3[i] == "room_id":
                        if split_3[j] == "Shared room":

                            # loops over the columns under price
                            for k in range(len(first_split_3)):
                                if first_split_3[k] == "price":

                                    # if the room id is already in the keys of the dictionary, appends price to the list of values
                                    if int(split_3[i]) in list(output_dict):
                                        output_dict[int(split_3[i])].append(float(split_3[k]))
                                    # if room id isn't in keys of dictionary, adds it and maps it to price
                                    else:
                                        output_dict[int(split_3[i])] = [float(split_3[k])]


    # returns a dictionary where keys are room ids and values are list of prices
    return (output_dict)

def price_change(d):
    """
    This function takes a dictionary with keys as room ids (int) and values as list of prices (float) for the parameter.
    The function returns a tuple with the max percentage change, starting price for listing with max percent change, and
    ending price for listing with max percentage change

    :param d: a dictionary with keys as room ids (int) and values as list of prices (float), (dict)
    :return: a tuple with three elements: max percent change, starting price for listing with max change, and ending price
    for listing with max percent change, (tuple)
    """

    list_d = list(d)
    max = 0
    starting = 0
    ending = 0

    # for loop iterates over the number of items in the dictionary
    for i in range(len(d)):
        # calculates percent change by subtracting the last price from the first price, all divided by the first price
        percent_change = ((float(d[list_d[i]][-1])) - (float(d[list_d[i]][0]))) / float((d[list_d[i]][0]))
        # sets the starting price as the first element from the list of values associated with each key
        starting = float(d[list_d[i]][0])
        # sets the ending price as the last element from the list of values associated with each key
        ending = float(d[list_d[i]][-1])
        # if the percent change is negative, makes it positive and converts it from decimal to percentage
        if percent_change < 0:
            percent_change = (percent_change * -1) * 100
        # if percent change is positive, converts it from decimal to percentage
        else:
            percent_change = percent_change * 100

        # identifies the max percent change by comparing it with previous max values
        if percent_change > max:
            max = percent_change
            # sets max_ending as the ending price associated with the max percent change
            max_ending = ending
            # sets max_starting as the ending price associated with the max percent change
            max_starting = starting

    # returns a tuple with the max percent change, max starting price, and max ending price
    return (max, max_starting, max_ending)

# PART 4
def price_by_neighborhood(filename):
    """
    This function takes the name of a file (str) and creates a dictionary mapping a neighborhood to its average price
    for an entire home/apt listing

    :param filename: the name of a file (string)
    :return: a dictionary where neighborhoods are the keys (str) and the neighborhood's average price for an Entire home/apt
    listing is the value (float), (dict)
    """
    # opens filename to read
    file_in = open(filename, "r")
    # reads through the first line of the file
    first_line = file_in.readline()
    # reads through the folloiwng lines of the file
    lines = file_in.readlines()
    # splits the first line of the file into words in a list based on commas
    first_split = first_line.split(",")

    list_prices = []
    list_neighborhood = []
    d = {}
    counter = 0
    total = 0

    # loops over the words in each line and puts them into a list
    for words in lines:
        split = words.split(",")

        # loops over the elements in the columns for price and neighbordhood and the rows containing Entire home/apt
        for i in range(len(first_split)):
            for j in range(len(first_split)):
                for k in range(len(first_split)):
                    if split[j] == "Entire home/apt":
                        if first_split[k] == "price":
                            if first_split[i] == "neighborhood":

                                # if the listed neighborhood is already a key in the dictionary, appends price of another
                                # listing in the neighborhood to the list of existing values
                                if split[i] in d.keys():
                                    d[split[i]].append(split[k])
                                # otherwise, maps listed neighborhood to the price of listing in the neighborhood (list)
                                else:
                                    d[split[i]] = [split[k]]
    print(d)
    # loops over each neighborhood listed in the dictionary
    for key in d.keys():
        # loops over all the prices associated with a neighborhood
        for value in d.values():
            for i in range(len(value)):
                # adds up all the prices associated with a neighborhood
                total += float((d[key])[i])
                # counts the number of prices values associated with a neighborhood
                counter += 1
        # calculates the average price of a listing in the neighborhood
        avg = total / counter
        # maps a neighborhood to the average price of a listing in that neighborhood
        d[key] = avg
    # returns the dictionary with neighborhood:average price of listing as key:value pairs
    return d

def plot_data(data, format, filename, done):
    """
    This function creates a scatter plot that plots correlation of price and satisfaction against pvalues for the specified file.
    :param data: a tuple consisting of correlation and pvalue (both floats), (tuple)
    :param format: a string that specifies the color and markers of a plot (str)
    :param name: a string that specifies the file name (str)
    :param done: Boolean that is only True when it is the last plot (bool)
    """
    # sets x coordinate as the first element in the tuple in the data set
    x = data[0]
    # sets y coordinate as the second element in the tuple in the data set
    y = data[1]
    # plots (x, y) coordinate pairs on the scattergram and uses the label name (from parameters) in the legend
    plt.plot(x, y, format, label=filename)
    # labels the x axis
    plt.xlabel("correlation between price and overall satisfaction (x-axis) ")
    # labels the y axis
    plt.ylabel("p-value determining if result is statistically significant (y-axis")
    # labels the scattergram's title
    plt.title("scattergram of correlation vs p-value for price and overall satisfaction")
    # only shows legend and scattergram if done is True
    if done:
        plt.legend()
        plt.show()


def main():
    # asks user to input first file name
    filename_1 = input("input the first file name")
    # asks user to input second file name
    filename_2 = input("input the second file name")
    # asks user to input third file name
    filename_3 = input("input the third file name")
    # calls price_satisfaction on the first file to return a list of lists
    l_1 = price_satisfaction(filename_1)
    # calls correlation to return a tuple with correlation and pvalue for price data and rating
    data_1 = correlation(l_1)
    # calls price_satisfaction on the second file to return a list of lists
    l_2 = price_satisfaction(filename_2)
    # calls correlation to return a tuple with correlation and pvalue for price data and rating
    data_2 = correlation(l_2)
    # calls price_satisfaction on the third file to return a list of lists
    l_3 = price_satisfaction(filename_3)
    # calls correlation to return a tuple with correlation and pvalue for price data and rating
    data_3 = correlation(l_3)

    # creates but doesn't show a scattergram with blue circles plotting the first file's correlation against pvalue
    plot_data(data_1, "bo", filename_1, False)
    # creates but doesn't show a scattergram with red circles plotting the second file's correlation against pvalue
    plot_data(data_2, "ro", filename_2, False)
    # creates a scattergram with green circles plotting the third file's correlation against pvalue, shows all scattergrams
    plot_data(data_3, "go", filename_3, True)


if __name__ == '__main__':
    main()