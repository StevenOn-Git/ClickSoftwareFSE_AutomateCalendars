# ClickSoftwareFSE_AutomateCalendars
For clicksoftware FSE customers, I found a way to automate alternating 9 hour work shifts without having dispatchers and schedulers to manually edit them every 3 to 6 months

The purpose of this library is to automate the need for end users to manually
input calendars for "n" number of years for multiple shifts such as: 9F11, 9F21, 9M11 et cetera.

This product leverages the ClickSoftware FSE APIs
https://wiki.cloud.clicksoftware.com/fsedoc/en/development/service-edge-api-references/rest-api-reference/calendar-services-rest-apis

Three .py files are required to run this script that includes URL, username, and password that is not provided in the files. 

This automation surpasses the limitations of the product's importing functionality of only uploaded 6 month calendars. The max capacity we attempted was a full three years.

In Chronological Order here's how the code executes:
1. Use click object services to get Calendar name and Keys https://wiki.cloud.clicksoftware.com/fsedoc/en/development/service-edge-api-references/rest-api-reference/object-services-rest-apis and create a Calendar object from the ClickCalendarModel.py file.
Note. Only calendars with "9M" or "9F" are causing business pain points. oData filter used to only pull these type of calendars. 
2. Loop through calendars and call GetCalendarInterval https://wiki.cloud.clicksoftware.com/fsedoc/en/development/service-edge-api-references/rest-api-reference/calendar-services-rest-apis for both Work and OptionalTime status to retrive YearlyLevel Intervals.
3. If YearlyLevel time intervals are found, use "biweeklify" function that passes the argument of number of biweeks to produce "n" number of biweeks to be created in Click for each calendar. 
4. Perform a similar new Loop for YearlyShiftInterval using GetCalendarInterval and update the calendar object.
5. Call UpdateCalendarInterval with the Calendar.get_payload() method as the data.

The ongoing use is to manipulate global variables located in the automatecalendars.py file. 
