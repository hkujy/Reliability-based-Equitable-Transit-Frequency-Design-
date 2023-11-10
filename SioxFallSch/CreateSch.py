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
fixed_dwell_time = 1  # it seems i have to use fixed dewll time, otherwise, it might become difficult to create a time-space network


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
        dep_stop = int(ttdf["From"][row])
        arr_top = int(ttdf["To"][row])
        travel_time[dep_stop][arr_top] = int(ttdf["Time"][row])
    # print(travel_time)
    
    #TODO: next step: based on travel time create the trajectory time for each bus line
    # print(_buslines)
    # exit()
    duration = end_time - start_time    

    with open ("BusLineTrips.csv","w+") as f:
        print("line_id,trip_id,arrival_time,departure_time,stop_id,stop_sequence",file=f)
        for l in range(0,num_lines):
            num_trips = int(duration/headway[l])
            num_stops = len(_buslines[l])
            for t in range(0,num_trips):
                # the first two lines are the time at the terminal
                arr = int(start_time + t*headway[l])
                dep = arr + fixed_dwell_time
                stop_id = _buslines[l][0]
                print("{0},{1},{2},{3},{4},{5}".format(
                   l,t,arr,dep,stop_id,0
                ),file = f)
                # the follwong loop from the second stop to the last
                for s in range(0, num_stops-1):
                    dep_stop = _buslines[l][s]
                    arr_stop = _buslines[l][s+1]
                    tt = travel_time[dep_stop][arr_stop]
                    # print(tt)
                    arr = dep + tt
                    dep = arr + fixed_dwell_time     
                    print("{0},{1},{2},{3},{4},{5}".format(
                       l,t,arr,dep,arr_stop,s+1
                    ),file = f)
 




    # for one bus line
    # for each departure time 
    # for each bue line












