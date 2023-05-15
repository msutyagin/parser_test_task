from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import pandas as pd
from config import FILEPATH
from logger import logger


class IParser(ABC):
    """Абстрактный класс-интерфейс, шаблон для классов парсеров, в конструкторе инициализируем файл для парсинга.
    Строго говоря, например, в Java такой класс не мог бы считаться интерфейсом, посколько в нем должны быть обозначены
    только методы класса без реализации. Но в python нет сущности интерфейс, он позволяет нам собрать и методы
    для реализации и переменные объектов в одном классе.
    """
    def __init__(self) -> None:
        self._file_path = FILEPATH

    @abstractmethod
    def get_file_path(self) -> str:
        raise NotImplementedError("Пожалуйста реализуйте этот метод в дочернем классе")

    @abstractmethod
    def parse_file(self) -> pd.DataFrame:
        raise NotImplementedError("Пожалуйста реализуйте этот метод в дочернем классе")


class PandasParser(IParser):
    """Класс конкретного парсера. В нем реализованы методы осуществляющие парсинг файла,
     структура котрого дана в задании"""

    def __init__(self):
        super().__init__()

    def get_file_path(self) -> str:
        """
        Инкапсуляция
        :return: Путь до файла для парсинга
        """
        return self._file_path

    def parse_file(self) -> pd.DataFrame:
        """
        Парсит передаваемый файл
        :return: Результирующий датафрейм
        """
        df = pd.read_excel(self.get_file_path(), header=None)
        df.ffill(axis=1, inplace=True)
        df.ffill(axis=0, inplace=True)

        header_df_p1 = df.loc[:2, :1]
        header_df_p1 = header_df_p1.drop([0, 1])
        header_df_p2 = df.loc[:2, 2:]
        df = df.loc[3 :]

        header_df_p2 = header_df_p2.transpose()
        header_df_p2 = header_df_p2.apply(lambda rows: '-'.join(rows.values.astype(str)), axis=1)
        header_df_p2 = pd.DataFrame(header_df_p2, columns=['0'])
        header_df_p2 = header_df_p2.transpose()
        header_df_p2.drop(['0'])
        header_df = pd.concat([header_df_p1, header_df_p2], ignore_index=True)
        header_df.ffill(axis=0, inplace=True)
        header_df = header_df.loc[1:]

        df = pd.concat([header_df, df], ignore_index=True)
        df.columns = df.loc[0, :]
        df = df.loc[1:, 'company':]

        start_date = datetime(2023, 5, 1).date()
        dates = [start_date + timedelta(days=_ // 2) for _ in range(len(df))]
        df['date'] = dates

        return df


class Parser:
    """Абстрактный класс для независимого использования возможностей конкретных парсеров.
    Демонстрация Dependency inversion и Barbara Liskov Substitution"""

    @staticmethod
    def parse(parser: IParser) -> pd.DataFrame:
        """
        Запускакт абстрактный парсера
        :param parser: Абстрактный парсер
        :return: Результат работы метода parse_file объекта IParser
        """
        return parser.parse_file()


class PandasParserAnotherFile(IParser):
    """Класс для демонстрации open-close принципа парадигмы SOLID. Расширяем функционал за счет
     реализации парсера для файла другой структуры"""

    def __init__(self) :
        super().__init__()
        self._file_path = './files/source2.xlsx'

    def get_file_path(self) -> str:
        """
        Инкапсуляция
        :return: Путь до файла для парсинга
        """
        return self._file_path

    def parse_file(self) -> pd.DataFrame:
        """
        Парсит передаваемый файл
        :return: Результирующий датафрейм
        """
        df = pd.read_excel(self.get_file_path(), header=None)
        logger.info(f'df = \n {df}')
        return df

