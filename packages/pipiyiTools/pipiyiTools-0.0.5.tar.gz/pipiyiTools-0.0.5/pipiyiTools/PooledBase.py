import pymysql
from dbutils.pooled_db import PooledDB
from typing import Dict, List, Union, Tuple, Any


class PooledBase:
    def __init__(self, host, user, password, db, log, port=3306, charset="utf8mb4"):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，连接池至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 连接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。
            # 因为pymysql和MySQLdb等模块的 threadsafety都为1，所以可设为0或None；
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            host=host,
            port=port,
            user=user,
            password=password,
            database=db,
            charset=charset,
        )
        self.log = log

    def execute(self, sql, params=None, is_fetch=True):
        """
        执行sql语句
        :param sql:
        :param params:
        :param is_fetch: bool 是否为查询
        :return:
        """
        with self.pool.connection() as conn:
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                try:
                    cursor.execute(sql, params)
                    if is_fetch:
                        return cursor.fetchall()
                    else:
                        conn.commit()
                        return cursor.lastrowid
                except Exception as e:
                    self.log.error(f"Execute error: {e},sql:{sql}.params:{params}")
                    conn.rollback()

    def select(
            self,
            table: str,
            columns: List[str] = None,
            where: Dict[str, Union[str, int]] = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
    ) -> Union[None, Dict, List[Dict]]:
        """
        查询所有数据
        :param table: string 表名
        :param columns: list 值为字符串 字段名 DEMO:
        ["username", "password", "age", "height", "is_active"]
        :param where: dict key：字符串 value: 字符串OR整数 条件 DEMO:
        {"age": 30, "height": 180.5}
        :param limit: 数量
        :param offset: 偏移量
        :param order_by: 排序
        :return: list
        """
        if columns is None:
            columns = ["*"]
        sql = f"SELECT {','.join(columns)} FROM {table}"
        params = None
        if where:
            where_str = " AND ".join([f"{k}=%s" for k in where.keys()])
            sql += f" WHERE {where_str}"
            params = tuple(where.values())

        if order_by:
            sql += f" ORDER BY {order_by}"

        if limit:
            sql += " LIMIT %s"
            params = (limit,) if params is None else params + (limit,)

        if offset:
            sql += " OFFSET %s"
            params = (offset,) if params is None else params + (offset,)

        return self.execute(sql, params)

    def fetch_one(
            self,
            table: str,
            columns: List[str] = None,
            where: Dict[str, Union[str, int]] = None,
    ):
        """
        查询一条
        :param table: string 表名
        :param columns: list 字段名称
        :param where: dict 条件
        :return: dict or None
        """
        result = self.select(table, columns, where, limit=1)
        return result[0] if result else None

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        插入单条
        :param table: string 表名
        :param data: dict 数据 DEMO:
        {"username": "Bob", "password": "password2", "age": 30}
        :return: int 数量
        """
        columns = ", ".join(data.keys())
        placeholders = ",".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params = tuple(data.values())
        return self.execute(sql, params, is_fetch=False)

    def insert_all(self, table: str, data_list: List[Dict[str, Any]]) -> int:
        """
            批量插入
            :param table:string 表名
            :param data_list: 数据 DEMO:
            data_list = [
            {"username": "Alice", "password": "password1", "age": 28},
            {"username": "Bob", "password": "password2", "age": 30},
            {"username": "Charlie", "password": "password3", "age": 25},
        ]
            :return:int 受影响的数目
        """
        if not data_list:
            return 0

        keys = data_list[0].keys()
        placeholders = ",".join(["%s"] * len(keys))
        columns = ",".join(keys)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        params_list = [tuple(data.values()) for data in data_list]

        with self.pool.connection() as conn:
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                affected_rows = 0
                try:
                    affected_rows = cursor.executemany(sql, params_list)
                    conn.commit()
                except Exception as e:
                    self.log.error(f"insert all error: {e}")
                    conn.rollback()
                return affected_rows

    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """
        更新数据
        :param table:string 表名
        :param data: dict 更新的数据
        :param where: dict 条件
        :return: int 受影响的条数
        """
        set_str = " ,".join([f"{key}=%s" for key in data.keys()])
        where_str = " AND ".join([f"{key}=%s" for key in where.keys()])
        sql = f"UPDATE {table} SET {set_str} WHERE {where_str}"
        params = tuple(data.values()) + tuple(where.values())
        return self.execute(sql, params, is_fetch=False)

    def delete(self, table: str, where: Dict[str, Any]) -> int:
        """
        删除
        :param table:string 表名
        :param where: dict 条件
        :return:int 受影响的条数
        """
        where_str = " AND ".join([f"{key}=%s" for key in where.keys()])
        sql = f"DELETE FROM {table} WHERE {where_str}"
        params = tuple(where.values())
        return self.execute(sql, params, is_fetch=False)
