import pandas as pd
import pymysql
from datetime import datetime


def dt_s(timestamp):
    ym = datetime.fromtimestamp(timestamp)
    # 格式化成标准日期时间
    formatted_date = ym.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def read_sql(sql, db_config):
    db = pymysql.connect(host=db_config.get('host'), user=db_config.get('user'), password=db_config.get('password'),
                         port=db_config.get('port'), db=db_config.get('db'))
    df = pd.read_sql(sql, db)
    return df