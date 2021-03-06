import csv
from functools import reduce
import json

# Part 1: Model the Detroit Police Population
# Read in the data from the Detroit Police Reports file using the CSVREADER and translate this into a list of dictionaries..

data = []

with open('911_Calls.csv', newline='') as csvFile:
    reader = csv.DictReader(csvFile, delimiter=',')
    for row in reader:
        data.append(row)

# Using Filter with lambda functions to exclude dictionaries (rows of the CSV) that have missing data in the Zip, or Neighborhood columns.

data_clean_1 = list(filter(lambda x: (x['zip_code'] != '0' and x['neighborhood'] != '' and x['totalresponsetime'] != '' and x['dispatchtime'] != '' and x['totaltime'] != ''), data))

# Using lambda functions and Reduce, calculate the average total response time, the average dispatch time, 
# and average total time for the Detroit Police force.

total_response_time = reduce(lambda x, y: x + float(y['totalresponsetime']), data_clean_1, 0)
avg_response_time = total_response_time/len(data_clean_1)

total_dispatch_time = reduce(lambda x, y: x + float(y['dispatchtime']), data_clean_1, 0)
avg_dispatch_time = total_dispatch_time/len(data_clean_1)

total_total_time = reduce(lambda x, y: x + float(y['totaltime']), data_clean_1, 0)
avg_total_time = total_total_time/len(data_clean_1)


print(f"Average responce time: {avg_response_time}")
print(f"Average dispatch time: {avg_dispatch_time}")
print(f"Average total time: {avg_total_time}")

# Part 2: Model the Neighborhood Samples
# Using lambda and Map functions, or lambda and Filter, 
# divide the list of dictionaries into smaller lists of dictionaries separated by neighborhood. 
# 


neighborhoods = list(set([row['neighborhood'] for row in data_clean_1]))

neighborhoodsDict = {}

for n in neighborhoods:
    neighborhoodsDict[n] = list(filter(lambda row: row['neighborhood'] == n, data_clean_1))

# Using lambda and Reduce, find the average total response time for each neighborhood, the average dispatch time for each neighborhood, 
# and the average total time for each neighborhood and store this into a list of dictionaries. 
# Add a dictionary item to include the population data for all of Detroit in your combined list.

averageByNeighborhood = []

for neighborhood in neighborhoodsDict:

    # print(neighborhood)
 
    total_response_time = reduce(lambda x, y: x + float(y['totalresponsetime']), neighborhoodsDict[neighborhood], 0)
    avg_response_time = total_response_time/len(neighborhoodsDict[neighborhood])
    # print(f"Average responce time: {avg_response_time}")

    total_dispatch_time = reduce(lambda x, y: x + float(y['dispatchtime']), neighborhoodsDict[neighborhood], 0)
    avg_dispatch_time = total_dispatch_time/len(neighborhoodsDict[neighborhood])
    # print(f"Average dispatch time: {avg_dispatch_time}")

    total_total_time = reduce(lambda x, y: x + float(y['totaltime']), neighborhoodsDict[neighborhood], 0)
    avg_total_time = total_total_time/len(neighborhoodsDict[neighborhood])
    # print(f"Average total time: {avg_total_time}\n")

    averageByNeighborhood.append({neighborhood: {'average_responce_time': avg_response_time, 'average_dispatch_time': avg_dispatch_time, 'average_total_time': avg_total_time}}) 


# Part 3: Create an Output JSON file
# Using the JSON module, format your list of dictionaries as a JSON and
#  test the output with the JSON lint website (https://jsonlint.com/) Write the tested JSON to a file.

averageByNeighborhood_json = json.dumps(averageByNeighborhood)

with open('averageByNeighborhood.json', 'w') as j_file:
    j_file.write(averageByNeighborhood_json)

