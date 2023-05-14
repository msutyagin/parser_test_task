from parser import Parser, PandasParser
from database import SqliteDatabaseConnector, Saver, SqliteDataSaver, SqliteDataGetter, DataGetter
from result import ResultFormatter, ResultSaver
from config import SL_DB_NAME, RESULT_FILEPATH

if __name__ == '__main__':
    custom_parser = PandasParser()
    parsed_df = Parser.parse(custom_parser)
    engine = SqliteDatabaseConnector.get_connection(SL_DB_NAME)
    custom_saver = SqliteDataSaver(engine=engine)
    Saver.save(custom_saver, parsed_df=parsed_df, table_name='parse_data')
    custom_getter = SqliteDataGetter(engine=engine)
    res = DataGetter.get_data(custom_getter, 'parse_data')

    result_df = ResultFormatter().prepare_result(res)
    ResultSaver().save_result(result_df, RESULT_FILEPATH)






