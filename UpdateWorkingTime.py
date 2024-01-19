from datetime import timedelta, datetime
import pandas as pd
import ClickCalendarModel as ccModel
from AllThingsClick import UpdateCalendarIntervals, prodUpdateCalendarCheck, environmentUsr, environmentPwd

"""
.Title
Update Work time calendar

.Description
The purpose of this library is to automate the need for end users to manually
input calendars for the next three years for multiple shifts such as: 9F11, 9F21, 9M11 et cetera.

.History
Original Release - MZubair - 7/28/2022
Code Review - SON - 08/31/2022
Refactoring last version - SON - 09/02/2022
Altering new edition to mainly find workshifts in one function using pandas - SON - 10/26/2023
"""

environment = "TEST"
prodCheck = True if environment == "PROD" else False

def get_date(year, week, day_of_week):
    """Gets the date of the first day in the calendar year by iso day of week Monday=1 Sunday= 7"""
    d = datetime(year, 1, 1)
    delta_days = d.isoweekday() - day_of_week
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= day_of_week
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta


def get_work_offset(dates, start_time, td_hours):
    result = []
    for date in dates:
        start_date = datetime.strptime(str(date) + start_time, '%Y-%m-%d%H:%M:%S')
        td = timedelta(hours=td_hours)
        end_date = start_date + td
        result.append({"TimeInterval": {"Start": start_date.isoformat(),
                                        "Finish": end_date.isoformat()}})
    return result


def add_weekly_level(click_cal_obj, start_time, day_name, status, td_hours):
    st = datetime.strptime(start_time, '%H:%M:%S')
    td = timedelta(hours=td_hours)
    et = st + td

    click_cal_obj.add_weekly_lvl(ccModel.WeeklyLevel(
        start_day=day_name,
        start_time=str(start_time),
        end_day=day_name,
        end_time=str(et.time()),
        status=status
    ))


def get_work_schedule_plus_optional(click_calendar_key, day_off, short_day, start_time, schedule_type, length,
                                    ENV=environment, PROD_CHECK=prodCheck):
    week_num = 1
    freq = "2W-MON"
    calObj = ccModel.Calendar(click_calendar_key)
    is_monday = True
    td_hours = 8
    st = datetime.strptime(start_time, '%H:%M:%S')

    first_week_list = ["9M11", "9F11"]
    if schedule_type[:4] in first_week_list:
        week_num = 2
    if schedule_type[1] == "F":
        freq = "2W-FRI"
        is_monday = False
        td_hours = 7

    # use pandas to get schedule
    first_day = get_date(2023, week_num, day_off).date()
    idx = pd.date_range(first_day, periods=length, freq=freq)

    # get working date and short date
    working_date = [datetime.date(idx[i]) for i in range(length)]
    working_datetime = get_work_offset(working_date, start_time, td_hours)
    for ti in working_datetime:
        start_date = datetime.fromisoformat(ti['TimeInterval']['Start'])
        minus_hour = timedelta(hours=1)
        b_start_date = start_date - minus_hour

        calObj.add_yearly_lvl(ccModel.YearlyLevel(
            start_date=b_start_date.isoformat(),
            end_date=ti['TimeInterval']['Start'],
            status="OptionalWork"
        ))
        calObj.add_yearly_lvl(ccModel.YearlyLevel(
            start_date=ti['TimeInterval']['Start'],
            end_date=ti['TimeInterval']['Finish'],
            status="Work"
        ))
        finish_date = datetime.fromisoformat(ti['TimeInterval']['Finish'])
        add_minutes = timedelta(minutes=30)
        e_finish_date = finish_date + add_minutes
        calObj.add_yearly_lvl(ccModel.YearlyLevel(
            start_date=ti['TimeInterval']['Finish'],
            end_date=e_finish_date.isoformat(),
            status="OptionalWork"
        ))
    # get weekly interval
    working_date_week = datetime.strptime(working_datetime[0]['TimeInterval']['Start'],
                                          '%Y-%m-%dT%H:%M:%S').isoweekday()

    # beginning shift optional time code interval
    bs_td = timedelta(hours=1)
    b_opt_st = st - bs_td
    b_start_time = str(b_opt_st.time())

    if is_monday:
        long_date = [get_date(workday.year, workday.isocalendar().week + 1, short_day).date() for workday in
                     working_date]
        long_datetime = get_work_offset(long_date, start_time, td_hours)
        for ti in long_datetime:
            start_date = datetime.fromisoformat(ti['TimeInterval']['Start'])
            minus_hour = timedelta(hours=1)
            b_start_date = start_date - minus_hour

            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=b_start_date.isoformat(),
                end_date=ti['TimeInterval']['Start'],
                status="OptionalWork"
            ))
            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=ti['TimeInterval']['Start'],
                end_date=ti['TimeInterval']['Finish'],
                status="Work"
            ))
            finish_date = datetime.fromisoformat(ti['TimeInterval']['Finish'])
            add_minutes = timedelta(minutes=30)
            e_finish_date = finish_date + add_minutes
            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=ti['TimeInterval']['Finish'],
                end_date=e_finish_date.isoformat(),
                status="OptionalWork"
            ))

        short_date = [get_date(workday.year, workday.isocalendar().week, short_day).date() for workday in
                      working_date]
        short_datetime = get_work_offset(short_date, start_time, td_hours - 1)
        for ti in short_datetime:
            start_date = datetime.fromisoformat(ti['TimeInterval']['Start'])
            minus_hour = timedelta(hours=1)
            b_start_date = start_date - minus_hour

            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=b_start_date.isoformat(),
                end_date=ti['TimeInterval']['Start'],
                status="OptionalWork"
            ))
            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=ti['TimeInterval']['Start'],
                end_date=ti['TimeInterval']['Finish'],
                status="Work"
            ))
            finish_date = datetime.fromisoformat(ti['TimeInterval']['Finish'])
            add_minutes = timedelta(minutes=30)
            e_finish_date = finish_date + add_minutes
            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=ti['TimeInterval']['Finish'],
                end_date=e_finish_date.isoformat(),
                status="OptionalWork"
            ))

        short_date_week = datetime.strptime(short_datetime[0]['TimeInterval']['Start'],
                                            '%Y-%m-%dT%H:%M:%S').isoweekday()
        if working_date_week == 1 and short_date_week == 5:
            for i in range(2, 5):
                day_name = "Tuesday"
                if i == 3:
                    day_name = "Wednesday"
                if i == 4:
                    day_name = "Thursday"

                add_weekly_level(calObj, b_start_time, day_name, "OptionalWork", 1)
                add_weekly_level(calObj, start_time, day_name, "Work", 8)

                # end shift optional time code interval
                es_td = timedelta(hours=td_hours)
                e_opt_st = st + es_td
                e_start_time = str(e_opt_st.time())

                add_weekly_level(calObj, e_start_time, day_name, "OptionalWork", 0.5)

    if working_date_week == 5 and short_day == 5:
        for i in range(1, 6):
            day_name = "Monday"
            if i == 2:
                day_name = "Tuesday"
            if i == 3:
                day_name = "Wednesday"
            if i == 4:
                day_name = "Thursday"
            add_weekly_level(calObj, b_start_time, day_name, "OptionalWork", 1)
            add_weekly_level(calObj, start_time, day_name, "Work", 8)

            # end shift optional time code interval
            es_td = timedelta(hours=td_hours+1)
            e_opt_st = st + es_td
            e_start_time = str(e_opt_st.time())

            add_weekly_level(calObj, e_start_time, day_name, "OptionalWork", 0.5)

    UpdateCalendarIntervals(prodUpdateCalendarCheck(PROD_CHECK), calObj.get_payload(), environmentUsr(ENV),
                            environmentPwd(ENV))
    # print(calObj.get_payload())
    return


def get_work_schedule(click_calendar_key, day_off, short_day, start_time, schedule_type, length,
                      ENV=environment, PROD_CHECK=prodCheck):
    week_num = 1
    freq = "2W-MON"
    calObj = ccModel.Calendar(click_calendar_key)
    is_monday = True
    td_hours = 8
    st = datetime.strptime(start_time, '%H:%M:%S')

    first_week_list = ["9M11", "9F11"]
    if schedule_type[:4] in first_week_list:
        week_num = 2
    if schedule_type[1] == "F":
        freq = "2W-FRI"
        is_monday = False
        td_hours = 7

    # use pandas to get schedule
    first_day = get_date(2023, week_num, day_off).date()
    idx = pd.date_range(first_day, periods=length, freq=freq)

    # get working date and short date
    working_date = [datetime.date(idx[i]) for i in range(length)]
    working_datetime = get_work_offset(working_date, start_time, td_hours)
    for ti in working_datetime:
        calObj.add_yearly_lvl(ccModel.YearlyLevel(
            start_date=ti['TimeInterval']['Start'],
            end_date=ti['TimeInterval']['Finish'],
            status="Work"
        ))

    # get weekly interval
    working_date_week = datetime.strptime(working_datetime[0]['TimeInterval']['Start'],
                                          '%Y-%m-%dT%H:%M:%S').isoweekday()

    if is_monday:
        long_date = [get_date(workday.year, workday.isocalendar().week + 1, short_day).date() for workday in
                     working_date]
        long_datetime = get_work_offset(long_date, start_time, td_hours)
        for ti in long_datetime:
            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=ti['TimeInterval']['Start'],
                end_date=ti['TimeInterval']['Finish'],
                status="Work"
            ))

        short_date = [get_date(workday.year, workday.isocalendar().week, short_day).date() for workday in
                      working_date]
        short_datetime = get_work_offset(short_date, start_time, td_hours - 1)
        for ti in short_datetime:
            calObj.add_yearly_lvl(ccModel.YearlyLevel(
                start_date=ti['TimeInterval']['Start'],
                end_date=ti['TimeInterval']['Finish'],
                status="Work"
            ))

        short_date_week = datetime.strptime(short_datetime[0]['TimeInterval']['Start'],
                                            '%Y-%m-%dT%H:%M:%S').isoweekday()
        if working_date_week == 1 and short_date_week == 5:
            for i in range(2, 5):
                day_name = "Tuesday"
                if i == 3:
                    day_name = "Wednesday"
                if i == 4:
                    day_name = "Thursday"

                add_weekly_level(calObj, start_time, day_name, "Work", 8)

    if working_date_week == 5 and short_day == 5:
        for i in range(1, 6):
            day_name = "Monday"
            if i == 2:
                day_name = "Tuesday"
            if i == 3:
                day_name = "Wednesday"
            if i == 4:
                day_name = "Thursday"
            add_weekly_level(calObj, start_time, day_name, "Work", 8)

    UpdateCalendarIntervals(prodUpdateCalendarCheck(PROD_CHECK), calObj.get_payload(), environmentUsr(ENV),
                            environmentPwd(ENV))
    return


# MAIN
print("Let's Get Click Calendar Info!")
print("")

# weekday (Monday =1 Sunday=7)
# get_work_schedule(442712064, 5, 5, "06:30:00", "9F21", 50)
# get_work_schedule(384163840, 1, 5, "07:30:00", "9M21", 50)
# get_work_schedule(383942656, 5, 5, "07:30:00", "9F11", 50)
# get_work_schedule(383959040, 5, 5, "07:30:00", "9F21", 50)
