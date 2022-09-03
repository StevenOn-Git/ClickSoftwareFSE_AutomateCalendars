'''
.Description
Master Click API Functions

.Version
Steven On - Original Release - 20200425
Steven On - Removed UserNames, Passwords, and URLs - 20220903
'''

from datetime import timedelta
import requests
import json


def prodObjectCheck(prod):
    # api-endpoint
    URL_Objects = "https://{cloud_tenant-sb}-int01.cloud.clicksoftware.com/so/api/objects/"
    PRODURL_Objects = "https://{cloud_tenant}-int01.cloud.clicksoftware.com/so/api/objects/"
    if prod == 'True':
        return PRODURL_Objects
    else:
        return URL_Objects

      
def prodGetCalendarCheck(prod):
    # api-endpoint
    url_objects = "https://{cloud_tenant-sb}-int01.cloud.clicksoftware.com/so/api/Services/Calendar/GetCalendarIntervals"
    produrl_objects = "https://{cloud_tenant}-int01.cloud.clicksoftware.com/so/api/Services/Calendar/GetCalendarIntervals"
    if prod == 'True':
        return produrl_objects
    else:
        return url_objects

      
def prodUpdateCalendarCheck(prod):
    # api-endpoint
    url_objects = "https://{cloud_tenant-sb}-int01.cloud.clicksoftware.com/so/api/Services/Calendar/UpdateCalendarIntervals"
    produrl_objects = "https://{cloud_tenant}-int01.cloud.clicksoftware.com/so/api/Services/Calendar/UpdateCalendarIntervals"
    if prod == 'True':
        return produrl_objects
    else:
        return url_objects
      
      
def environmentUsr(environment):
    devUsr = "devUser@devpod"
    qaUsr = "devUser@qapod"
    testUsr = "devUser@testpod"
    prodUsr = "devUser@prodpod"
    if environment == "PROD":
        return prodUsr
    elif environment == "QA":
        return qaUsr
    elif environment == 'DEV':
        return devUsr
    else:
        return testUsr

      
def environmentPwd(environment):
    devPwd = "dev_P@$$w0rD"
    qaPwd = "qa_P@$$w0rD"
    testPwd = "test_P@$$w0rD"
    prodPwd = "prod_P@$$w0rD"
    if environment == "PROD":
        return prodPwd
    elif environment == "QA":
        return qaPwd
    elif environment == "DEV":
        return devPwd
    else:
        return testPwd
      
      
def GetClickObject(obj, PARAMS, url, username, password):
    print(url + obj + "?" + PARAMS)
    ObjList = []
    #Get REST Call
    try:
        from requests.auth import HTTPBasicAuth
        r = requests.get(url=url + obj + "?" + PARAMS,
                         auth=(username, password))
        print(r.status_code)
        if (r.status_code == 200 or r.status_code == 500):
            #convert string response to Python JSON
            data = r.json()
            # print(data)
            # print('object Size: ' + str(len(data)))
            # loop through objects and create an object List
            for item in data:
                ObjList.append(item)
            '''
            # Get object properties
            for item in data[0]:
                print(item)
            '''
            return ObjList
    except Exception as e:
        print(e)      
      
      
def cal_interval_payload(key, start_date, status):
    end_date = start_date + timedelta(days=+14)
    return {
        "Calendar": key,
        "IncludeBase": True,
        "RequestedYearlyLevel": {
            "UseCalendarTimeZone": True,
            "TimeInterval": {
                "Start": start_date.isoformat(),
                "Finish": end_date.isoformat()
            },
            "Status": status
        },
        "RequestedWeeklyLevel": {
            "Status": status
        },
        "RequestedTimePhasedWeeklyLevel": {
            "TimeInterval": {
                "Start": start_date.isoformat(),
                "Finish": end_date.isoformat()
            },
            "Status": status
        }
    }


def GetCalendarIntervals(url, cal_key, start_date, shift_status, username, password):
    data = cal_interval_payload(cal_key, start_date, shift_status)
    try:
        from requests.auth import HTTPBasicAuth
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers, auth=(username, password))
        print(r.status_code)
        if r.status_code == 200 or r.status_code == 500:
            #print(r.text)
            return r.json()
        else:
            print(r.text)

        return None
    except Exception as e:
        print(e)


def cal_shifts_payload(key, start_date, shift_name):
    end_date = start_date + timedelta(days=+14)
    return {
        "Calendar": key,
        "IncludeBase": True,
        "RequestedYearlyShiftLevel": {
            "TimeInterval": {
                "Start": start_date.isoformat(),
                "Finish": end_date.isoformat()
            },
            "Shift": {
                "@objectType": "Group",
                "Name": shift_name
            }
        },
        "RequestedWeeklyShiftLevel": {
            "Shift": {
                "@objectType": "Group",
                "Name": shift_name
            }
        }
    }


def GetCalendarShiftIntervals(url, cal_key, start_date, shift_name, username, password):
    data = cal_shifts_payload(cal_key, start_date, shift_name)
    try:
        from requests.auth import HTTPBasicAuth
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers, auth=(username, password))
        print(r.status_code)
        if r.status_code == 200 or r.status_code == 500:
            #print(r.text)
            return r.json()
        else:
            print(r.text)

        return None
    except Exception as e:
        print(e)


def UpdateCalendarIntervals(url, data, username, password):
    try:
        from requests.auth import HTTPBasicAuth
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers, auth=(username, password))
        print(r.status_code)
        if r.status_code == 200 or r.status_code == 500:
            print(r.text)
        else:
            print(r.text)

        return None
    except Exception as e:
        print(e)
