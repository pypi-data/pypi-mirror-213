import datatime

"""
방법1
from datetime import datetime
dt = datetime.now()
dt.microsecond
방법2
from datetime import datetime
dt = datetime.now()
print dt.microsecond/1000 + dt.second*1000

밀리 초 단위로 현재 UTC 시간을 얻는 가장 간단한 방법
# timeutil.py
import datetime
def get_epochtime_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)
    
# sample.py
import timeutil
timeutil.get_epochtime_ms()
"""
def get_epochtime_ms():
    # dt = datetime.now()
    # print(f'dt:{dt}')
    return round(datatime.datetime.utcnow().timestamp() * 1000)