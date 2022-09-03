def YearlyLevel(start_date, end_date, status):
    """Capture Yearly Time Intervals"""
    obj = {
        "TimeInterval": {
            "Start": start_date,
            "Finish": end_date
        },
        "Status": status
    }
    return obj


def YearlyShiftLevel(start_date, end_date, shift_key):
    """Capture Yearly Shift Time Intervals"""
    obj = {
        "TimeInterval": {
            "Start": start_date,
            "Finish": end_date
        },
        "Shift": shift_key
    }
    return obj


def WeeklyLevel(start_day, start_time, end_day, end_time, status):
    """Capture Weekly Time Intervals"""
    obj = {
        "WeeklyIntervalStart": {
            "Day": start_day,
            "Time": start_time
        },
        "WeeklyIntervalFinish": {
            "Day": end_day,
            "Time": end_time
        },
        "Status": status
    }
    return obj


def WeeklyShiftLevel(start_day, start_time, end_day, end_time, shift_key):
    """Capture Weekly Shift Time Intervals"""
    obj = {
        "WeeklyIntervalStart": {
            "Day": start_day,
            "Time": start_time
        },
        "WeeklyIntervalFinish": {
            "Day": end_day,
            "Time": end_time
        },
        "Shift": shift_key
    }
    return obj


def TimePhasedWeeklyLevel(start_datetime, end_datetime, start_day, start_time, end_day, end_time, status):
    """Capture Time Phased Weekly Time Intervals"""
    obj = {
        "WeeklyIntervalStart": {
            "Day": start_day,
            "Time": start_time
        },
        "WeeklyIntervalFinish": {
            "Day": end_day,
            "Time": end_time
        },
        "Start": start_datetime,
        "Finish": end_datetime,
        "Status": status
    }
    return obj


class Calendar:
    """Capture entire Calendar"""
    def __init__(self, key):
        self.CalendarKey = key
        self.YearlyLevel = []
        self.YearlyShiftLevel = []
        self.WeeklyLevel = []
        self.WeeklyShiftLevel = []
        self.TimePhasedWeeklyLevel = []

    def add_yearly_lvl(self, item):
        self.YearlyLevel.append(item)

    def add_yearly_shift_lvl(self, item):
        self.YearlyShiftLevel.append(item)

    def add_weekly_lvl(self, item):
        self.WeeklyLevel.append(item)

    def add_weekly_shift_lvl(self, item):
        self.WeeklyShiftLevel.append(item)

    def add_time_phased_lvl(self, item):
        self.TimePhasedWeeklyLevel.append(item)

    def get_payload(self):
        return {
            "CalendarKey": self.CalendarKey,
            "CalendarIntervals": {
                "YearlyLevel": self.YearlyLevel,
                "YearlyShiftLevel": self.YearlyShiftLevel,
                "WeeklyLevel": self.WeeklyLevel,
                "WeeklyShiftLevel": self.WeeklyShiftLevel,
                "TimePhasedWeeklyLevel": self.TimePhasedWeeklyLevel
            },
            "OverwriteExisting": False
        }
