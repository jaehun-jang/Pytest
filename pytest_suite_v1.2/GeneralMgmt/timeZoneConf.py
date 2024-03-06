# funBaConf.py

# $language = "python"
# $interface = "1.0"

from datetime import datetime, timedelta
from netmiko import ConnectHandler
import pandas as pd
import time , re

# ###  TEST MODULE ###  
import basic.basicConf as bc


def timeZone(dut): 
    timeZone_src = './GeneralMgmt/time_zone.csv'
    timeZone_df = pd.read_csv(timeZone_src, encoding='utf-8')
    rows, cols = timeZone_df.shape  # Get the number of rows
    result = []
    failed_City = []
    with bc.connect(dut) as child:  
        for row in range(rows):
            
            # Get Time Zone Offset   
            timezoneoffset = timeZone_df.loc[row, "Time_Zone"] 
            timezoneoffset = timezoneoffset.split('GMT')[1]
            # GMT 이후 문자열을 리스트로 변환
            list_timezone_str = list(timezoneoffset)
            # 필요한 부분 추출
            timezone_offset_list = list_timezone_str[:-1]
            # 리스트를 문자열로 변환
            timezone_offset_str = ''.join(timezone_offset_list)
            
            # Set Local Time  
            setclock = child.send_command("clock set 00:00:00 1 1 2024") 
            
            # Change timezone and Get local Time  
            timeZone_config = [
                f'time-zone {timeZone_df.loc[row, "Continent"]} {timeZone_df.loc[row, "City"]}'
            ]
            child.send_config_set(timeZone_config) 
            time.sleep(0.5) 
            time_str1 = child.send_command('show clock | exclude ^ *%')
            match = re.search(r'(\d{2}:\d{2}:\d{2})', time_str1)
            local_time_str = match.group(1) if match else "N/A"
            time.sleep(2) 
            
            # Get GMT Time 
            timeZone_config = ('time-zone europe london')
            child.send_config_set(timeZone_config) 
            time.sleep(0.5) 
            time_str2 = child.send_command('show clock | exclude ^ *%')
            match = re.search(r'(\d{2}:\d{2}:\d{2})', time_str2)
            gmt_time_str = match.group(1) if match else "N/A"
              
            # print(local_time_str, gmt_time_str, timezone_offset_str)
            
            # 문자열을 datetime 객체로 변환
            local_time = datetime.strptime(local_time_str, "%H:%M:%S")
            gmt_time = datetime.strptime(gmt_time_str, "%H:%M:%S")

            # 시간대 오프셋 파싱 및 음수 값 처리 (stjohns: -03:00 처리를 위하여 사용)
            if timezone_offset_str.startswith('-'):
                sign = -1
                timezone_offset_str = timezone_offset_str[1:]
            else:
                sign = 1

            hours_offset, minutes_offset = map(int, timezone_offset_str.split(':'))
            timezone_offset = sign * timedelta(hours=hours_offset, minutes=minutes_offset)
            local_time_with_offset = local_time - timezone_offset

            # 결과가 GMT 시간과 일치하는지 확인 (분 단위로 비교)
            is_matching = local_time_with_offset.replace(second=0, microsecond=0).time() == gmt_time.replace(second=0, microsecond=0).time()

            # 결과 출력
            print(f"{timeZone_df.loc[row, 'City']} 시간: {local_time_str}, GMT 시간: {gmt_time_str}, 시간대 오프셋: {timezone_offset_str}")
            print(f"적용된 지역 시간: {local_time_with_offset.strftime('%H:%M')}, GMT 시간과 일치: {is_matching}")      
            if is_matching == True:
                result.append('True')
            else:
                failed_City.append(timeZone_df.loc[row, 'City'])
                result.append('False')
        if 'False' in result:
            print('The falure count is :',result.count('False'), 'And the City is : ', failed_City )
            return False
        else:
            return True



