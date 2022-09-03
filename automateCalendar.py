"""
.Title
Automating Click Calendars

.Description
The purpose of this library is to automate the need for end users to manually
input calendars for the next three years for multiple shifts such as: 9F11, 9F21, 9M11 et cetera.

.History
Original Release - MZubair - 7/28/2022
Code Review - SON - 08/31/2022
Refactoring last version - SON - 09/02/2022
"""
from datetime import timedelta, datetime
from AllThingsClick import GetCalendarIntervals
from AllThingsClick import GetCalendarShiftIntervals
from AllThingsClick import prodGetCalendarCheck
from AllThingsClick import environmentUsr
from AllThingsClick import environmentPwd
import ClickCalendarModel as ccModel
from AllThingsClick import GetClickObject
from AllThingsClick import prodObjectCheck
from AllThingsClick import UpdateCalendarIntervals
from AllThingsClick import prodUpdateCalendarCheck

PRODCHECK = False
ENV = 'DEV'
CURRENT_DATE = datetime.now()
ARB_DATE = datetime(year=2022, month=7, day=30)
CAL_STATUS_LIST = ["Work", "OptionalWork"]
SHIFT_STATUS_LIST = ["SMUD - Svc Crews Appointment", "SMUD - Svc Crews Routine"]
NUM_OF_BIWEEKS = 78
filter1 = "$filter=Name%20eq%20'9F21-UC5:630-1600'"
filter2 = "$filter=(contains(Name,'9M')%20or%20contains(Name,'9F'))"


def biweeklify_single_date(iso_str_date, num_of_biweeks):
    biweekly_list = []
    for i in range(0, num_of_biweeks * 14, 14):
        biweekly_list.append((datetime.fromisoformat(iso_str_date) + timedelta(days=+i)).isoformat())
    return biweekly_list


############## MAIN #################
print("Let's Update Some Click Calendars!")
print("")

# Get All Click Calendars
objs = GetClickObject("Calendar", filter2,
                      prodObjectCheck(PRODCHECK), environmentUsr(ENV), environmentPwd(ENV))
for ob in objs:
    # Create Calendar Object
    print(f"Creating Calendar {ob['Name']}")
    calObj = ccModel.Calendar(ob['Key'])

    # find two week "Work" and "OptionalTime" shifts
    for i in range(len(CAL_STATUS_LIST)):
        obj = GetCalendarIntervals(
            prodGetCalendarCheck(PRODCHECK), ob['Key'],
            ARB_DATE, CAL_STATUS_LIST[i], environmentUsr(ENV), environmentPwd(ENV)
        )
        # Check to see if there are any YearlyLevel Time Intervals
        if len(obj["YearlyLevel"]) > 0:
            time_interval = obj["YearlyLevel"][0]

            # biweeklify to multiply the number of dates to create in Click
            time_interval_start_date_list = biweeklify_single_date(
                time_interval['TimeInterval']['Start'], NUM_OF_BIWEEKS)
            time_interval_finish_date_list = biweeklify_single_date(
                time_interval['TimeInterval']['Finish'], NUM_OF_BIWEEKS)

            # Append YearlyIntervals to Calendar Object
            for j in range(len(time_interval_start_date_list)):
                calObj.add_yearly_lvl(ccModel.YearlyLevel(
                    time_interval_start_date_list[j],
                    time_interval_finish_date_list[j],
                    time_interval['Status']
                ))

    # find two week Svc Crew shift intervals
    for i in range(len(SHIFT_STATUS_LIST)):
        obj = GetCalendarShiftIntervals(
            prodGetCalendarCheck(PRODCHECK), ob['Key'],
            ARB_DATE, SHIFT_STATUS_LIST[i], environmentUsr(ENV), environmentPwd(ENV)
        )
        # Check to see if there are any YearlyShiftLevel Time Intervals
        if len(obj["YearlyShiftInterval"]) > 0:
            time_interval = obj["YearlyShiftInterval"][0]

            # biweeklify to multiply the number of dates to create in Click
            time_interval_start_date_list = biweeklify_single_date(
                time_interval['TimeInterval']['Start'], NUM_OF_BIWEEKS)
            time_interval_finish_date_list = biweeklify_single_date(
                time_interval['TimeInterval']['Finish'], NUM_OF_BIWEEKS)

            # Append YearlyShiftIntervals to Calendar Object
            for j in range(len(time_interval_start_date_list)):
                calObj.add_yearly_shift_lvl(ccModel.YearlyShiftLevel(
                    time_interval_start_date_list[j],
                    time_interval_finish_date_list[j],
                    time_interval['Shift']['Key']
                ))

    # Update Calendars
    UpdateCalendarIntervals(prodUpdateCalendarCheck(PRODCHECK), calObj.get_payload(),
                            environmentUsr(ENV), environmentPwd(ENV))

print('done done')
