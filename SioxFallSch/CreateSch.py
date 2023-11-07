__author__ = 'Yu Jiang'
__version__ = '6-Nov-2023'
__email__ = 'yujiang@lancaster.ac.uk'
__status__ = 'complete, paper under second round review'
""" 
    code for create schedule for the arbitary lines
"""
import pandas as pd

# the following two set the start and end time for bus lines
start_time = 0
end_time = 120
num_lines = 20


def get_headway():
    """
        generate the number of trips for each bus line
    """
    trips = [6]*20
    headway = []
    # trips = [4]*20
    for t in trips:
        headway.append(60/t)

    return headway

def create_dep_time(_buslines):
    """
        Create the departure time for each bus line
    """
    print(_buslines)
    headway = get_headway()
    print(headway)
    ttdf = pd.read_csv(".\\LinkData.csv")
    # header = ttdf.head() 
    # print(header)
    # exit()
    # print(ttdf)
    travel_time = [[0]*25 for i in range(25)]
    for row in range(0, ttdf.shape[0]):
        i = int(ttdf["From"][row])
        j = int(ttdf["To"][row])
        travel_time[i][j] = int(ttdf["Time"][row])
    print(travel_time)
    
    #TODO: next step: based on travel time create the trajectory time for each bus line
    duration = end_time - start_time    
    for l in range(0,num_lines):
        num_trips = duration/headway[l]
        for t in range(0,num_trips):
            dep_from_terminal = int(start_time + (t-1)*headway[l])
            for



    # for one bus line
    # for each departure time 
    # for each bue line












