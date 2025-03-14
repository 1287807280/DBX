from methons import read_sql
from config import db_config


task = read_sql("select uri,site from task_d where site = '抖音'",db_config)
print(task)
for t in task.itertuples():
    url = t.uri
    print(url)
    print("*"*200)

