import os

os.system("clear")

routes = {"WAW-CDG-WAW", "WAW-FRA-WAW", "WAW-LHR-WAW", "WAW-BCN-WAW", "WAW-LIS-WAW", "WAW-VIE-WAW", "WAW-MUC-WAW", "WAW-VNL-WAW", "WAW-ATH-WAW", "WAW-KRK-WAW"}
demand = {"WAW-CDG-WAW": 100, "WAW-FRA-WAW": 90, "WAW-LHR-WAW": 110, "WAW-BCN-WAW": 10, "WAW-LIS-WAW": 100, "WAW-VIE-WAW": 100, "WAW-MUC-WAW": 100, "WAW-VNL-WAW": 100, "WAW-ATH-WAW": 100, "WAW-KRK-WAW": 200}
time = {"WAW-CDG-WAW": 4.5, "WAW-FRA-WAW": 4, "WAW-LHR-WAW": 6, "WAW-BCN-WAW": 8, "WAW-LIS-WAW": 9, "WAW-VIE-WAW": 4, "WAW-MUC-WAW": 4, "WAW-VNL-WAW": 3, "WAW-ATH-WAW": 6, "WAW-KRK-WAW": 2}
aircraft = {"1": 5, "2": 5, "3": 5, "4": 5, "5": 5, "6": 5, "7": 5, "8": 5, "9": 5, "10": 5}

finalDemandOrder = []

aircraftTimeline = {key: [] for key in aircraft.keys()}
aircraftTimeslot = {key: [] for key in aircraft.keys()}

for aircraftId in aircraft.keys():
    aircraftTimeslot[aircraftId] = [0, 30, 100, 130, 200, 230, 300, 330, 400, 430, 500, 530, 600, 630, 700, 730, 800, 830, 900, 930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430, 1500, 1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930, 2000, 2030, 2100, 2130, 2200, 2230, 2300, 2330]

def aircraftLimitations(earlyestTime, latestTime):
    for aircraftId, timeslots in aircraftTimeslot.items():
        aircraftTimeslot[aircraftId] = [time for time in timeslots if time >= earlyestTime]
    
    for aircraftId, timeslots in aircraftTimeslot.items():
        aircraftTimeslot[aircraftId] = [time for time in timeslots if time <= latestTime]


#Change this for first takeoff time, last takeoff time in your hub.
aircraftLimitations(630, 2330)

def add_time(start, duration):
    if start is None or duration is None:
        return None
    startHours = start // 100
    startMinutes = start % 100
    durationHours = duration // 100
    durationMinutes = duration % 100

    totalMinutes = startMinutes + durationMinutes
    totalHours = startHours + durationHours + totalMinutes // 60
    totalMinutes %= 60
    totalHours %= 24 

    return totalHours * 100 + totalMinutes

def checkEarliestTime(duration):
    earliestTime = float('inf')
    earliestAircraft = None

    for aircraftId, timeslots in aircraftTimeslot.items():
        if timeslots != []:
            minTime = min(timeslots)
            if minTime < earliestTime:
                if minTime + duration*100 in timeslots:
                    earliestTime = minTime
    if earliestTime == float('inf'):
        # print("No available timeslots")
        return None
    else:
        # print(f"Earliest available time: {earliestTime} from aircraft {earliestAircraft}")
        return earliestTime
    
# def upgradeCheckEarlyTime(route):
#     earliestTime = float('inf')
#     earliestAircraft = None
#     route_duration = int(time[route] * 100)

#     for aircraftId, timeslots in aircraftTimeslot.items():
#         for startTime in timeslots:
#             if startTime is None:
#                 continue
#             endTime = add_time(startTime, route_duration)
#             if endTime is None:
#                 continue
#             if all(time in timeslots for time in range(startTime, endTime)):
#                 if startTime < earliestTime:
#                     earliestTime = startTime
#                     earliestAircraft = aircraftId

#     if earliestTime == float('inf'):
#         return None
#     else:
#         return earliestTime
    
def checkEarliestAircraft(duration):
    earliestTime = float('inf')
    earliestAircraft = None

    for aircraftId, timeslots in aircraftTimeslot.items():
        if timeslots != []:
            minTime = min(timeslots)
            if minTime < earliestTime:
                if minTime + duration*100 in timeslots:
                    earliestTime = minTime
                    earliestAircraft = aircraftId
                
    if earliestTime == float('inf'):
        # print("No available timeslots")
        return None
    else:
        # print(f"Earliest available time: {earliestTime} from aircraft {earliestAircraft}")
        return earliestAircraft


# def assignRoute(route, aircraftId, startTime):
#     if aircraftId in aircraftTimeline:
#         OverDays = False
#         startTime = datetime.strptime(startTime, '%H%M')
#         endTime = startTime + timedelta(hours=time[route])
#         aircraftTimeline[aircraftId].append((route, startTime.strftime('%H%M'), endTime.strftime('%H%M')))
        
#         endTimeInt = endTime.hour * 100 + endTime.minute
#         startTimeInt = startTime.hour * 100 + startTime.minute
        
#         if time[route] >=24:
#             OverDays = True
        
#         if OverDays:
#             aircraftTimeslot[aircraftId] = []
#         else: 
#             aircraftTimeslot[aircraftId] = [time for time in aircraftTimeslot[aircraftId] if time < startTimeInt or time > endTimeInt]
#         return None
#     else:
#         return None
    
    

# Errors that can't remove the timeslot after time 2000 is fixed by github Copilot editing the assignRoute function.

def assignRoute(route, aircraftId, startTime):
    # Convert to integer HHMM
    startTimeInt = int(startTime)
    # Calculate end time using your add_time logic; assume duration is derived within assignRoute or passed in
    route_duration = int(time[route] * 100)  # e.g., 200 for 2 hours
    endTimeInt = add_time(startTimeInt, route_duration)
    
    # Append assignment to timeline (formatting as needed)
    aircraftTimeline[aircraftId].append((route, startTime, endTimeInt))
    
    # Determine if the event goes over day
    if route_duration >= 2400 or endTimeInt < startTimeInt:
        # Remove all available slots since it overflows into a new day
        aircraftTimeslot[aircraftId] = []
    else:
        # Remove all time slots from startTimeInt up to endTimeInt.
        # Note: using ">= endTimeInt" excludes the ending slot.
        aircraftTimeslot[aircraftId] = [t for t in aircraftTimeslot[aircraftId]
                                        if t < startTimeInt or t >= endTimeInt]
    return None
    
# assignRoute("WAW-CDG-WAW", "E195-1", "0700")




# Organizing the route with demand order
restRoute = dict(demand)
finalDemandOrder = []
while restRoute:
    highest = max(restRoute, key=restRoute.get)
    finalDemandOrder.append(highest)
    del restRoute[highest]

while True:
    assigned = False
    for route in finalDemandOrder:
        aircraftId = checkEarliestAircraft(time[route])
        startTime = checkEarliestTime(time[route])
        if aircraftId is None or startTime is None:
            continue
        assignRoute(str(route), str(aircraftId), str(startTime))
        assigned = True

    if assigned == False:
        break



for aircraftId, timeline in aircraftTimeline.items():
    print(f"--------------------------")
    print(f"Aircraft {aircraftId}:")
    print(f"--------------------------")
    print(f"    Route   | Start | End")
    print(f"--------------------------")
    for route, start, end in timeline:
        print(f"{route} | {start} | {end}")

# print(assignRoute("WAW-FRA-WAW", str(checkEarliestAircraft()), str(checkEarliestTime())))
