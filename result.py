from abc import ABC, abstractmethod
import pandas as pd
from logger import logger


class IResultFormatter(ABC):
    """Абстрактный интерфейс, шаблон для классов обратного парсинга.
    """

    @abstractmethod
    def prepare_result(self, result_list: list) -> pd.DataFrame:
        raise NotImplementedError("Пожалуйста реализуйте этот метод в дочернем классе")


class IResultSaver(ABC):
    """Интерфейс, шаблон для классов сохранения результата."""

    @abstractmethod
    def save_result(self, df: pd.DataFrame, file_path: str) -> None:
        raise NotImplementedError("Пожалуйста реализуйте этот метод в дочернем классе")


class ResultFormatter(IResultFormatter):
    """Класс для поддготовки датафрейма результата"""

    def prepare_result(self, data: list) -> pd.DataFrame:
        """
        Метод формирует результирующий датафрейм
        :param data: Результат select запроса из БД
        :return: результирующий датафрейм
        """
        df = pd.DataFrame(data, columns=[
            'id',
            'company',
            'fact-Qliq-data1',
            'fact-Qliq-data2',
            'fact-Qoil-data1',
            'fact-Qoil-data2',
            'forecast-Qliq-data1',
            'forecast-Qliq-data2',
            'forecast-Qoil-data1',
            'forecast-Qoil-data2',
            'date'
        ])
        df['fact-Qliq-data'] = df['fact-Qliq-data1'] + df['fact-Qliq-data2']
        df['fact-Qoil-data'] = df['fact-Qoil-data1'] + df['fact-Qoil-data2']
        df['forecast-Qliq-data'] = df['forecast-Qliq-data1'] + df['forecast-Qliq-data2']
        df['forecast-Qoil-data'] = df['forecast-Qoil-data1'] + df['forecast-Qoil-data2']
        total_fact_qliq = df.groupby('date')['fact-Qliq-data'].sum()
        total_fact_qoil = df.groupby('date')['fact-Qoil-data'].sum()
        total_forecast_qliq = df.groupby('date')['forecast-Qliq-data'].sum()
        total_forecast_qoil = df.groupby('date')['forecast-Qoil-data'].sum()
        dates = df.drop_duplicates(subset=["date"], ignore_index=True)['date']
        result_df = pd.DataFrame({
            'fact-Qliq-data': total_fact_qliq,
            'fact-Qoil-data': total_fact_qoil,
            'forecast-Qliq-data': total_forecast_qliq,
            'forecast-Qoil-data': total_forecast_qoil,
        }, index=dates)
        result_df.loc['Total', :] = result_df.sum(numeric_only=True, axis=0)
        logger.info(f'result_df =  \n {result_df}')

        return result_df


class ResultSaver(IResultSaver):
    """Класс для сохранения результата в файл"""

    def save_result(self, df: pd.DataFrame, file_path: str) -> None:
        """
        Метод сохраняет передаваемый датафрейм в файл
        :param df: датафрейм результата
        :param file_path: Путь для файла сохранения результат
        """
        df.to_excel(file_path)
