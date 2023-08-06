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
        with self:
            columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
            self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})")
            self.__conn.commit()

    def insert_data(self,
                    table_name: str,
                    data: Dict[str, Union[str, int, float]]) -> None:
        with self:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in range(len(data))])
            values = tuple(data.values())
            self.__cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
            self.__conn.commit()

    def select_data(self,
                    table_name: str,
                    columns: Union[List[str], None] = None,
                    where: Union[Dict[str, Union[str, int, float]], None] = None,
                    limit: Union[int, None] = None,
                    offset: Union[int, None] = None,
                    fetch: DataTypes.Fetch = DataTypes.Fetch.FETCHONE) -> Union[Tuple, List[Tuple]]:
        with self:
            if columns:
                columns = ', '.join(columns)
            else:
                columns = '*'
            if where:
                where_clause = 'WHERE ' + ' AND '.join([f'{col}=?' for col in where.keys()])
                values = tuple(where.values())
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
            self.__cursor.execute(f"SELECT {columns} FROM {table_name} {where_clause} {limit_clause} {offset_clause}",
                                  values)

            if fetch == DataTypes.Fetch.FETCHONE:
                result = self.__cursor.fetchone()
            elif fetch == DataTypes.Fetch.FETCHALL:
                result = self.__cursor.fetchall()
            return result

    def update_data(self,
                    table_name: str,
                    set_data: Dict[str, Union[str, int, float]],
                    where: Dict[str, Union[str, int, float]],
                    sign: Union[str, None] = None) -> None:
        with self:
            if sign:
                set_clause = ', '.join([f'{col}={col}{sign}?' for col in set_data.keys()])
            else:
                set_clause = ', '.join([f'{col}=?' for col in set_data.keys()])
            where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(set_data.values()) + tuple(where.values())
            self.__cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", values)
            self.__conn.commit()

    def delete_data(self,
                    table_name: str,
                    where: Dict[str, Union[str, int, float]]) -> None:
        with self:
            where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(where.values())
            self.__cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause}", values)
            self.__conn.commit()

    def close_conn(self) -> None:
        self.__conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_conn()


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
        async with self:
            columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
            await self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})")
            await self.__conn.commit()

    async def insert_data(self,
                          table_name: str,
                          data: Dict[str, Union[str, int, float]]) -> None:
        async with self:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in range(len(data))])
            values = tuple(data.values())
            await self.__cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
            await self.__conn.commit()

    async def select_data(self,
                          table_name: str,
                          columns: Union[List[str], None] = None,
                          where: Union[Dict[str, Union[str, int, float]], None] = None,
                          limit: Union[int, None] = None,
                          offset: Union[int, None] = None,
                          fetch: DataTypes.Fetch = DataTypes.Fetch.FETCHONE) -> Union[Tuple, List[Tuple]]:
        async with self:
            if columns:
                columns = ', '.join(columns)
            else:
                columns = '*'
            if where:
                where_clause = 'WHERE ' + ' AND '.join([f'{col}=?' for col in where.keys()])
                values = tuple(where.values())
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
            await self.__cursor.execute(f"SELECT {columns} FROM {table_name} {where_clause} {limit_clause} {offset_clause}",
                                        values)

            if fetch == DataTypes.Fetch.FETCHONE:
                result = self.__cursor.fetchone()
            elif fetch == DataTypes.Fetch.FETCHALL:
                result = self.__cursor.fetchall()
            return result

    async def update_data(self,
                          table_name: str,
                          set_data: Dict[str, Union[str, int, float]],
                          where: Dict[str, Union[str, int, float]],
                          sign: Union[str, None] = None) -> None:
        with self:
            if sign:
                set_clause = ', '.join([f'{col}={col}{sign}?' for col in set_data.keys()])
            else:
                set_clause = ', '.join([f'{col}=?' for col in set_data.keys()])
            where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(set_data.values()) + tuple(where.values())
            await self.__cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", values)
            await self.__cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", values)
            await self.__conn.commit()

    async def delete_data(self,
                          table_name: str,
                          where: Dict[str, Union[str, int, float]]) -> None:
        with self:
            where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
            values = tuple(where.values())
            await self.__cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause}", values)
            await self.__conn.commit()

    async def close_conn(self) -> None:
        await self.__conn.close()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_conn()

