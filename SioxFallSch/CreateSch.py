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
target_folder = "./JND - ISTTT Sioux Fall/"


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
    _start_times = [] 
    _end_times = [] 
    _line_times = []  # travel time between stops
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
            lt = [] 
            for t in range(0,num_trips):
                # the first two lines are the time at the terminal
                arr = int(start_time + t*headway[l])
                if t == 0:
                    _start_times.append(arr)
                if t == num_trips-1:
                    _end_times.append(arr)
                # dep = arr + fixed_dwell_time
                dep = arr   # at departing terminal is not neccessar to add the depart time
                stop_id = _buslines[l][0]
                print("{0},{1},{2},{3},{4},{5}".format(
                   l,t,arr,dep,stop_id,0
                ),file = f)
                # the follwong loop from the second stop to the last
                for s in range(0, num_stops-1):
                    dep_stop = _buslines[l][s]
                    arr_stop = _buslines[l][s+1]
                    tt = travel_time[dep_stop][arr_stop]
                    if (t == 0):
                        lt.append(tt)
                    # print(tt)
                    arr = dep + tt
                    dep = arr + fixed_dwell_time     
                    print("{0},{1},{2},{3},{4},{5}".format(
                       l,t,arr,dep,arr_stop,s+1
                    ),file = f)
                if (t == 0):
                    _line_times.append(lt)
    return (headway,_start_times,_end_times,_line_times)

# TODO: print file list for the ISTTT JND paper input

def print_lines(_buses,_headways,_start_time,_end_time):
    """
        file: lines.csv
        id,Name,SerType,HeadWay,StartTime,EndTime,VehType,Doors 
    """
    file_name = "./JND - ISTTT Sioux Fall/lines.csv"
    with open(file_name,"w+") as f:
        print("id,Name,SerType,HeadWay,StartTime,EndTime,VehType,Doors",file=f)
        for l in range(0, len(_buses)):
            print("{0},{1},{2},{3},{4},{5},{6},{7}".format(
                l,
                str(l),
                "Schedule",
                _headways[l],
                _start_time[l],
                _end_time[l],
                "Buses",
                2
            ),file = f)

def print_linestop(_buses):
    """
        lines stops /without header file
    """
    file_name= target_folder + "LineStop.csv"
    with open(file_name,"w+") as f:
        for l in range(0,len(_buses)):
            print("{0},".format(l),file=f,end="")
            print(','.join(str(x) for x in list(_buses[l])),file=f,)

def print_linetimes(_lt):
    """
        lines stops /without header file
    """
    file_name= target_folder + "LineTime.csv"
    with open(file_name,"w+") as f:
        for l in range(0,len(_lt)):
            print("{0},".format(l),file=f,end="")
            print(','.join(str(x) for x in list(_lt[l])),file=f)


def print_node():
    """
        id,Name,Type
    """
    print("---remarks: print 24 nodes for the SiouxFall Network---")
    file_name = target_folder + "Node.csv" 
    with open(file_name,"w+") as f:
        print("id,Name,Type",file=f)
        for i in range(0,24):
            print("{0},{1},{2}".format(i,i+1,"Stop"),file=f)

def print_SchDep(_headway):
    """
        print the scheduled departure time for each bus line
    """
    file_name = target_folder + "SchDep.csv" 
    duration = end_time - start_time    
    with open(file_name,"w+") as f:
        for l in range(0, len(_headway)): # loop every bus lines
            num_trips = int(duration/_headway[l])
            for t in range(0,num_trips):
                # the first two lines are the time at the terminal
                arr = int(start_time + t*_headway[l])
                dep = arr  # not neccessar to add the depart time
                print("{0},{1},{2}".format(l,t,dep),file = f)


def print_trips():
    """
        print the OD pairs for the sioux fall network 
        id,Origin,Dest,TargetDepTime,TargetArrTime,DepMaxEarly,DepMaxLate,ArrMaxEarly,ArrMaxLate,Demand,MinPie,MaxPie
        0,0,5,0,30,0,5,20,30,50,1,30
        1,0,5,5,35,5,10,25,35,50,1,30
    """
    file_name = target_folder + "Trips.csv" 
    with open(file_name,"w+") as f:
        print("id,Origin,Dest,TargetDepTime,TargetArrTime,DepMaxEarly,DepMaxLate,ArrMaxEarly,ArrMaxLate,Demand,MinPie,MaxPie",file=f)
        print("0,0,23,0,60,0,5,20,30,50,1,30",file=f)
        print("1,0,5,5,35,5,10,25,35,50,1,30",file=f)
         

def create_and_print_sch_file(_buses):
    """
        create and print schedule files
    """
    # the buses only contain the bus lines 
    (headway,start_time,end_time,line_time) = create_dep_time(_buses)
    print(line_time)
    print_linetimes(line_time)
    print_node()
    print_SchDep(headway)
    print_trips()
    print_lines(_buses,headway,start_time,end_time)
    print_linestop(_buses)





