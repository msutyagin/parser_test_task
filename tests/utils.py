from enum import Enum
from parser import Parser, PandasParser
from config import FILEPATH
import pandas as pd


class SystemMessagesErrors(Enum):
    FILE_STRUCTURE_ERROR = 'Структура входящего файла не соответствует заданной'
    DATAFRAME_LEN_ERROR = 'Кол-во колонок(столбцов) датафрейма парсинга не соответствует заданным'
    DATABASE_DATA_ERROR = 'Данные в базе данных не соответствуют ожидаемым'
    RESULT_TOTAL_ERROR = 'Ошибка в расчете итогового результата'


parsed_df = Parser.parse(PandasParser())
input_df = pd.read_excel(FILEPATH, header=None)
