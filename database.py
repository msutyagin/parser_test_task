from abc import ABC, abstractmethod
import sqlite3
import pandas as pd


class SqliteDatabaseConnector:
    """Интерфейс подключения к SQLite"""

    @staticmethod
    def get_connection(db_file_path: str = None) -> sqlite3.Connection:
        connection = sqlite3.connect(f'{db_file_path}')
        print(connection)
        return connection


class ISqliteDataSaver(ABC):
    """Абстрактный класс-интерфейс, шаблон для классов парсеров, в конструкторе инициализируем файл для парсинга.
     Строго говоря, например, в Java такой класс не мог бы считаться интерфейсом, посколько в нем должны быть обозначены
     только методы класса без реализации. Но в python нет сущности интерфейс, он позволяет нам собрать и методы
     для реализации и переменные объектов в одном классе.
     """

    def __init__(self, engine: sqlite3.Connection):
        self._engine = engine

    @abstractmethod
    def save_data(self, parsed_df: pd.DataFrame, table_name: str):
        raise NotImplementedError("Пожалуйста реализуйте этот метод в дочернем классе")


class SqliteDataSaver(ISqliteDataSaver):
    """
    В классе реализован метод сохранения данных в таблицу Sqlite БД
    """

    def save_data(self, parsed_df: pd.DataFrame, table_name: str) -> None:
        """
        Метод реализует сохранение данных в таблицу, название которой передается в параметрах.
        Предварительно, если таблица с таким названием существует, она удаляется.
        :param parsed_df: Датафрейм с данными для сохранение в таблицу
        :param table_name: Имя таблицы
        """
        try:
            with self._engine:
                cursor = self._engine.cursor()
                cursor.execute(f"DROP TABLE {table_name}")
        except sqlite3.OperationalError:
            pass
        parsed_df.to_sql(table_name, con=self._engine)


class Saver:
    """Абстрактный класс для независимого использования возможностей конкретных парсеров.
    Демонстрация Dependency inversion и Barbara Liskov Substitution"""

    @staticmethod
    def save(saver: ISqliteDataSaver, parsed_df: pd.DataFrame, table_name: str) -> None:
        """
        Запускает абстрактный объект, сохраняющий данные в БД
        :param saver: Абстрактный объект сохраняющий данные в БД
        :param parsed_df: Датафрейм с данными для сохранение
        :param table_name: Имя таблицы
        """
        saver.save_data(parsed_df, table_name)


class ISqliteDataGetter(ABC):
    """Абстрактный класс-интерфейс, шаблон для классов парсеров, в конструкторе инициализируем файл для парсинга.
     Строго говоря, например, в Java такой класс не мог бы считаться интерфейсом, посколько в нем должны быть обозначены
     только методы класса без реализации. Но в python нет сущности интерфейс, он позволяет нам собрать и методы
     для реализации и переменные объектов в одном классе.
     """

    def __init__(self, engine: sqlite3.Connection):
        self._engine = engine

    @abstractmethod
    def get_data_from_table(self, table_name: str) -> list:
        raise NotImplementedError("Пожалуйста реализуйте этот метод в дочернем классе")


class SqliteDataGetter(ISqliteDataGetter):
    """
    В классе реализован метод получения данных из таблицы Sqlite БД
    """

    def get_data_from_table(self, table_name: str) -> list:
        """
        Метод возвращает данные из таблицы, имя которой передается в параметрах
        :param table_name: Имя таблицы
        :return: Список строк таблицы
        """
        with self._engine:
            cursor = self._engine.cursor()
            result = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
        return result


class DataGetter:
    """Абстрактный класс для независимого использования возможностей конкретных парсеров.
    Демонстрация Dependency inversion и Barbara Liskov Substitution"""

    @staticmethod
    def get_data(getter: ISqliteDataGetter, table_name: str) -> list:
        """
        Метод запускает процесс получения данных из таблицы, имя которой передается в параметрах
        :param getter: Абстрактный объект получающий данные из БД
        :param table_name: Имя таблицы
        :return: Результат работы метода get_data_from_table объекта ISqliteDataGetter
        """
        return getter.get_data_from_table(table_name)
