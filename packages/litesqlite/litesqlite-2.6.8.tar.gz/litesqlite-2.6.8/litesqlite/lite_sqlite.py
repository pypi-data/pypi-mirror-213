import aiosqlite
import sqlite3
from typing import Dict, Union, Tuple, List
from .datatypes import DataTypes


class Sqlite:

    def __init__(self,
                 db_name: str) -> None:
        self.__db_name = db_name
        self.__conn = None
        self.__cursor = None

    def open_conn(self) -> None:
        self.__conn = sqlite3.connect(self.__db_name)
        self.__cursor = self.__conn.cursor()

    def __enter__(self) -> 'Sqlite':
        self.open_conn()
        return self

    def create_table(self,
                     table_name: str,
                     columns: Dict[str, Union[DataTypes, str]]) -> None:
        columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        self.__cursor.execute(query)
        self.__conn.commit()

    def insert_data(self,
                    table_name: str,
                    data: Dict[str, Union[str, int, float]]) -> None:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.__cursor.execute(query, values)
        self.__conn.commit()

    def select_data(self,
                    table_name: str,
                    columns: Union[List[str], str] = '*',
                    where: Union[List[Dict[str, Union[str, int, float]]], None] = None,
                    limit: Union[int, None] = None,
                    offset: Union[int, None] = None,
                    fetch: DataTypes.Fetch = DataTypes.Fetch.FETCHONE) -> Union[Tuple, List[Tuple]]:
        if columns != '*':
            columns = ', '.join(columns)
        if where:
            where_clause = 'WHERE ' + ' OR '.join([' AND '.join([f'{col}=?' for col in d.keys()]) for d in where])
            values = tuple(value for d in where for value in d.values())
        else:
            where_clause = ''
            values = ()
        if limit:
            limit_clause = f"LIMIT {limit}"
        else:
            limit_clause = ""
        if offset:
            offset_clause = f'OFFSET {offset}'
        else:
            offset_clause = ""
        query = f"SELECT {columns} FROM {table_name} {where_clause} {limit_clause} {offset_clause}"
        self.__cursor.execute(query, values)
        if fetch == DataTypes.Fetch.FETCHONE:
            result = self.__cursor.fetchone()
        elif fetch == DataTypes.Fetch.FETCHALL:
            result = self.__cursor.fetchall()
        return result

    def update_data(self,
                    table_name: str,
                    set_data: Dict[str, Union[str, int, float]],
                    where: Union[Dict[str, Union[str, int, float]], None] = None,
                    sign: Union[str, None] = None) -> None:
        if sign:
            set_clause = ', '.join([f'{col}={col}{sign}?' for col in set_data.keys()])
        else:
            set_clause = ', '.join([f'{col}=?' for col in set_data.keys()])
        if where:
            where_clause = 'WHERE' + ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(set_data.values()) + tuple(where.values())
        else:
            where_clause = ''
            values = tuple(set_data.values())
        query = f"UPDATE {table_name} SET {set_clause} {where_clause}"
        self.__cursor.execute(query, values)
        self.__conn.commit()

    def delete_data(self,
                    table_name: str,
                    where: Union[Dict[str, Union[str, int, float]], None] = None) -> None:
        if where:
            where_clause = 'WHERE' + ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(where.values())
        else:
            where_clause = ''
            values = ()
        query = f"DELETE FROM {table_name} {where_clause}"
        self.__cursor.execute(query, values)
        self.__conn.commit()

    def close_conn(self) -> None:
        self.__conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.open_conn()


class AioSqlite:

    def __init__(self,
                 db_name: str) -> None:
        self.__db_name = db_name
        self.__conn = None
        self.__cursor = None

    async def open_conn(self) -> None:
        self.__conn = await aiosqlite.connect(self.__db_name)
        self.__cursor = await self.__conn.cursor()

    async def __aenter__(self) -> 'AioSqlite':
        await self.open_conn()
        return self

    async def create_table(self,
                           table_name: str,
                           columns: Dict[str, Union[DataTypes, str]]) -> None:
        columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        await self.__cursor.execute(query)
        await self.__conn.commit()

    async def insert_data(self,
                          table_name: str,
                          data: Dict[str, Union[str, int, float]]) -> None:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        await self.__cursor.execute(query, values)
        await self.__conn.commit()

    async def select_data(self,
                          table_name: str,
                          columns: Union[List[str], str] = '*',
                          where: Union[List[Dict[str, Union[str, int, float]]], None] = None,
                          limit: Union[int, None] = None,
                          offset: Union[int, None] = None,
                          fetch: DataTypes.Fetch = DataTypes.Fetch.FETCHONE) -> Union[Tuple, List[Tuple]]:
        if columns != '*':
            columns = ', '.join(columns)
        if where:
            where_clause = 'WHERE ' + ' OR '.join([' AND '.join([f'{col}=?' for col in d.keys()]) for d in where])
            values = tuple(value for d in where for value in d.values())
        else:
            where_clause = ''
            values = ()
        if limit:
            limit_clause = f"LIMIT {limit}"
        else:
            limit_clause = ""
        if offset:
            offset_clause = f'OFFSET {offset}'
        else:
            offset_clause = ""
        query = f"SELECT {columns} FROM {table_name} {where_clause} {limit_clause} {offset_clause}"
        await self.__cursor.execute(query, values)

        if fetch == DataTypes.Fetch.FETCHONE:
            result = await self.__cursor.fetchone()
        elif fetch == DataTypes.Fetch.FETCHALL:
            result = await self.__cursor.fetchall()
        return result

    async def update_data(self,
                          table_name: str,
                          set_data: Dict[str, Union[str, int, float]],
                          where: Union[Dict[str, Union[str, int, float]], None] = None,
                          sign: Union[str, None] = None) -> None:
        if sign:
            set_clause = ', '.join([f'{col}={col}{sign}?' for col in set_data.keys()])
        else:
            set_clause = ', '.join([f'{col}=?' for col in set_data.keys()])
        if where:
            where_clause = 'WHERE' + ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(set_data.values()) + tuple(where.values())
        else:
            where_clause = ''
            values = tuple(set_data.values())
        query = f"UPDATE {table_name} SET {set_clause} {where_clause}"
        await self.__cursor.execute(query, values)
        await self.__conn.commit()

    async def delete_data(self,
                          table_name: str,
                          where: Union[Dict[str, Union[str, int, float]], None] = None) -> None:
        if where:
            where_clause = 'WHERE' + ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(where.values())
        else:
            where_clause = ''
            values = ()
        query = f"DELETE FROM {table_name} {where_clause}"
        await self.__cursor.execute(query, values)
        await self.__conn.commit()

    async def close_conn(self) -> None:
        await self.__conn.close()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_conn()