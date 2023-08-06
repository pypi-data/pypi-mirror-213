import MySQLdb
from dbutils.pooled_db import PooledDB
from MySQLdb.cursors import DictCursor
from sometools.sync_tools.base import Base


# pip install mysqlclient -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install DBUtils -i https://pypi.tuna.tsinghua.edu.cn/simple
# 使用dbutils的PooledDB连接池，操作数据库。
# 这样就不需要每次执行sql后都关闭数据库连接，频繁的创建连接，消耗时间
# PooledDB 提供线程间可共享的数据库连接，并自动管理连接。一般来说，PooledDB 的数据库连接耗时更稳定，大多数情况下都推荐使用。
# import sys
# from MySQLdb.converters import conversions
# def mysqlclient_converters():
#     from MySQLdb.constants import FIELD_TYPE
#     conversions[FIELD_TYPE.BIT] = lambda x: 1 if int.from_bytes(x, byteorder=sys.byteorder, signed=False) else 0
#     return conversions


class MysqlPoolMixIn(Base):
    def __init__(self, *args, **kwargs):
        super(MysqlPoolMixIn, self).__init__(*args, **kwargs)

    def get_sync_mysql_conn(self, **kwargs):
        # MySQLdb连接池
        pool = PooledDB(
            mincached=10,  # 连接池初始化的总连接数，默认值为 0，不初始化任何连接，推荐使用 10。
            maxcached=20,  # 连接池中最大的空闲连接数量，默认值为 0，无限制，推荐使用 20。
            maxshared=20,  # 最大的共享连接数，默认值为 0，所有连接都为独占，推荐使用 20。
            maxconnections=40,  # 连接池的最大连接数，硬性限制，默认值为0，无限制，推荐使用 40。
            blocking=False,  # 决定连接数达到上限时的行为。设置为 True 时会进入等待状态知道连接数降低；设置为 False 时会直接报错，默认值为 False，推荐使用默认值。
            maxusage=0,  # 单个连接被复用的次数，达到次数之后会关闭并重新打开连接，默认值为 0，无限制，推荐使用默认值。
            setsession=None,  # 连接使用前自动执行的 SQL 语句。默认值为 NULL，推荐使用默认值。
            ping=1,
            # ping: 控制使用 ping() 方法检测连接的方式，（0 = 不检查；1 = 默认，从连接池获取的时候进行检查；2 = 创建游标时检查；4 = 执行查询时检查； 7 = 全部检查，包含 1，2，4 的所有场景），推荐使用默认值。
            creator=MySQLdb,
            host='localhost',
            port=3306,
            user='root',
            passwd='zk199245',
            db='my_site',
            charset='utf8mb4',
            cursorclass=DictCursor,
            # conv=mysqlclient_converters()
        )
        return pool
