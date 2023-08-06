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

    def __init2(self) -> None:
        self.__conn = sqlite3.connect(self.__db_name)
        self.__cursor = self.__conn.cursor()

    def create_table(self,
                     table_name: str,
                     columns: Dict[str, Union[DataTypes, str]]) -> None:
        self.__init2()
        columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})")
        self.__conn.commit()
        self.__close_conn()

    def insert_data(self,
                    table_name: str,
                    data: Dict[str, Union[str, int, float]]) -> None:
        self.__init2()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])
        values = tuple(data.values())
        self.__cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.__conn.commit()
        self.__close_conn()

    def select_data(self,
                    table_name: str,
                    columns: Union[List[str], None] = None,
                    where: Union[Dict[str, Union[str, int, float]], None] = None,
                    limit: Union[int, None] = None,
                    offset: Union[int, None] = None,
                    fetchall: bool = False) -> Union[Tuple, List[Tuple]]:
        self.__init2()
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

        if fetchall:
            result = self.__cursor.fetchall()
        else:
            result = self.__cursor.fetchone()
        self.__close_conn()
        return result

    def update_data(self,
                    table_name: str,
                    set_data: Dict[str, Union[str, int, float]],
                    where: Dict[str, Union[str, int, float]],
                    sign: Union[str, None] = None) -> None:
        self.__init2()
        if sign:
            set_clause = ', '.join([f'{col}={col}{sign}?' for col in set_data.keys()])
        else:
            set_clause = ', '.join([f'{col}=?' for col in set_data.keys()])
        where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
        values = tuple(set_data.values()) + tuple(where.values())
        self.__cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", values)
        self.__conn.commit()
        self.__close_conn()

    def delete_data(self,
                    table_name: str,
                    where: Dict[str, Union[str, int, float]]) -> None:
        self.__init2()
        where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
        values = tuple(where.values())
        self.__cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause}", values)
        self.__conn.commit()
        self.__close_conn()

    def __close_conn(self) -> None:
        self.__init2()
        self.__conn.close()


class AioSqlite:

    def __init__(self,
                 db_name: str) -> None:
        self.__db_name = db_name
        self.__conn = None
        self.__cursor = None

    async def __init2(self) -> None:
        self.__conn = await aiosqlite.connect(self.__db_name)
        self.__cursor = await self.__conn.cursor()

    async def create_table(self,
                           table_name: str,
                           columns: Dict[str, Union[DataTypes, str]]) -> None:
        await self.__init2()
        columns_def = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns.items()])
        await self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})")
        await self.__conn.commit()
        await self.__close_conn()

    async def insert_data(self,
                          table_name: str,
                          data: Dict[str, Union[str, int, float]]) -> None:
        await self.__init2()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])
        values = tuple(data.values())
        await self.__cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        await self.__conn.commit()
        await self.__close_conn()

    async def select_data(self,
                          table_name: str,
                          columns: Union[List[str], None] = None,
                          where: Union[Dict[str, Union[str, int, float]], None] = None,
                          limit: Union[int, None] = None,
                          offset: Union[int, None] = None,
                          fetchall: bool = False) -> Union[Tuple, List[Tuple]]:
        await self.__init2()
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

        if fetchall:
            result = await self.__cursor.fetchall()
        else:
            result = await self.__cursor.fetchone()
        await self.__close_conn()
        return result

    async def update_data(self,
                          table_name: str,
                          set_data: Dict[str, Union[str, int, float]],
                          where: Dict[str, Union[str, int, float]],
                          sign: Union[str, None] = None) -> None:
        await self.__init2()
        if sign:
            set_clause = ', '.join([f'{col}={col}{sign}?' for col in set_data.keys()])
        else:
            set_clause = ', '.join([f'{col}=?' for col in set_data.keys()])
        where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
        values = tuple(set_data.values()) + tuple(where.values())
        await self.__cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", values)
        await self.__cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", values)
        await self.__conn.commit()
        await self.__close_conn()

    async def delete_data(self,
                          table_name: str,
                          where: Dict[str, Union[str, int, float]]) -> None:
        await self.__init2()
        where_clause = ' AND '.join([f'{col}=?' for col in where.keys()])
        values = tuple(where.values())
        await self.__cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause}", values)
        await self.__conn.commit()
        await self.__close_conn()

    async def __close_conn(self) -> None:
        await self.__init2()
        await self.__conn.close()
