from datetime import datetime as dt

def get_time(launch_datetime_str):
    launch = dt.strptime(launch_datetime_str,'%Y-%m-%d %H:%M')
    date = launch.strftime('%d/%m/%Y')
    hour = launch.strftime('%H:%M')
    res_seconds = (launch - dt.utcnow()).seconds
    return {'hour':hour,'date':date,'res_seconds':res_seconds}
    
