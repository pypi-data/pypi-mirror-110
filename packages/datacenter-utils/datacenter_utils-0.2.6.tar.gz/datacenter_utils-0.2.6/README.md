# datacenter_utils

### install

```
pip install datacenter-utils
```

### module

_usage_
```
from datacenter_utils.redis_common import RedisObject, ET, BJ, UTC
from datacenter_utils.mongo_common import MongoObject
from datacenter_utils.aws_s3 import download_s3, run_unzip_file, s3_list
from datacenter_utils.pgsql_common import Postgres
```

_info_

|  module   | class  | func | info |
|  ----  | ----  |---- |---- |
| redis_common  | RedisObject | get_dataframe_from_redis | get dataframe object from redis |
| mongo_common  | MongoObject | upsert_many_df | upsert dataframe to mongodb on specify key fields
| mongo_common  | MongoObject | remove | remove collections match the filter dict
| mongo_common  | MongoObject | insert_one | insert one dict 
| mongo_common  | MongoObject | insert_many | insert list of dict
| mongo_common  | MongoObject | update_one | update one collection with the condition by the data
| mongo_common  | MongoObject | find_many_df | find dataframe match the filter dict
| aws_s3  | - | download_s3 | download file from s3
| aws_s3  | - | run_unzip_file | unzip the zipped file from the path
| aws_s3  | - | s3_list | show the file list in the path
| pgsql_common  | Postgres | update_insert_df | upsert dataframe to postgresql by creating CONSTRAINT on constraint_columns 
| pgsql_common  | Postgres | find | find all rows match the filter dict
| pgsql_common  | Postgres | find_one | find one row match the filter dict
| pgsql_common  | Postgres | find_by_sql | find all rows by SQL
