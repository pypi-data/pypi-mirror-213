from typing import Union


class DataTypes:

    class Fetch:
        FETCHONE = 'fetchone'
        FETCHALL = 'fetchall'

    class Collation:
        BINARY = 'BINARY'
        NOCASE = 'NOCASE'
        RTRIM = 'RTRIM'
        UTF16 = 'UTF16'
        UTF16CI = 'UTF16CI'

    @staticmethod
    def INTEGER(not_null: bool = False,
                primary_key: bool = False,
                autoincrement: bool = False,
                unique: bool = False,
                default: Union[str, int, float] = None,
                check: Union[str, int, float] = None,
                collation: Union[Collation, str] = None) -> str:
        type_str = 'INTEGER'
        if primary_key:
            type_str += ' PRIMARY KEY'
            if autoincrement:
                type_str += ' AUTOINCREMENT'
        if not_null:
            type_str += ' NOT NULL'
        if unique:
            type_str += ' UNIQUE'
        if default is not None:
            type_str += f" DEFAULT {default}"
        if check is not None:
            type_str += f" CHECK ({check})"
        if collation is not None:
            type_str += f" COLLATE {collation}"
        return type_str

    @staticmethod
    def REAL(not_null: bool = False,
             primary_key: bool = False,
             unique: bool = False,
             default: Union[str, int, float] = None,
             check: Union[str, int, float] = None,
             collation: Union[Collation, str] = None) -> str:
        type_str = 'REAL'
        if primary_key:
            type_str += ' PRIMARY KEY'
        if not_null:
            type_str += ' NOT NULL'
        if unique:
            type_str += ' UNIQUE'
        if default is not None:
            type_str += f" DEFAULT {default}"
        if check is not None:
            type_str += f" CHECK ({check})"
        if collation is not None:
            type_str += f" COLLATE {collation}"
        return type_str

    @staticmethod
    def TEXT(not_null: bool = False,
             primary_key: bool = False,
             unique: bool = False,
             default: Union[str, int, float] = None,
             check: Union[str, int, float] = None,
             collation: Union[Collation, str] = None) -> str:
        type_str = 'TEXT'
        if primary_key:
            type_str += ' PRIMARY KEY'
        if not_null:
            type_str += ' NOT NULL'
        if unique:
            type_str += ' UNIQUE'
        if default is not None:
            type_str += f" DEFAULT {default}"
        if check is not None:
            type_str += f" CHECK ({check})"
        if collation is not None:
            type_str += f" COLLATE {collation}"
        return type_str

    @staticmethod
    def BLOB(not_null: bool = False,
             primary_key: bool = False,
             unique: bool = False,
             default: Union[str, int, float] = None,
             check: Union[str, int, float] = None,
             collation: Union[Collation, str] = None) -> str:
        type_str = 'BLOB'
        if primary_key:
            type_str += ' PRIMARY KEY'
        if not_null:
            type_str += ' NOT NULL'
        if unique:
            type_str += ' UNIQUE'
        if default is not None:
            type_str += f" DEFAULT {default}"
        if check is not None:
            type_str += f" CHECK ({check})"
        if collation is not None:
            type_str += f" COLLATE {collation}"
        return type_str

    @staticmethod
    def NUMERIC(not_null: bool = False,
                primary_key: bool = False,
                unique: bool = False,
                default: Union[str, int, float] = None,
                check: Union[str, int, float] = None,
                collation: Union[Collation, str] = None) -> str:
        type_str = 'NUMERIC'
        if primary_key:
            type_str += ' PRIMARY KEY'
        if not_null:
            type_str += ' NOT NULL'
        if unique:
            type_str += ' UNIQUE'
        if default is not None:
            type_str += f" DEFAULT {default}"
        if check is not None:
            type_str += f" CHECK ({check})"
        if collation is not None:
            type_str += f" COLLATE {collation}"
        return type_str