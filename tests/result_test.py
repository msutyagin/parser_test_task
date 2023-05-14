import os
from database import SqliteDataGetter, DataGetter
from result import ResultFormatter, ResultSaver
from tests.utils import SystemMessagesErrors


def test_result(setup_db):
    engine = setup_db
    custom_getter = SqliteDataGetter(engine=engine)
    res = DataGetter.get_data(custom_getter, 'test')
    result_df = ResultFormatter().prepare_result(res)
    result_file = './files/test_result.xlsx'
    ResultSaver().save_result(result_df, result_file)
    assert result_df.loc['Total', 'fact-Qliq-data'] == 980, SystemMessagesErrors.RESULT_TOTAL_ERROR
    assert result_df.loc['Total', 'fact-Qoil-data'] == 1780, SystemMessagesErrors.RESULT_TOTAL_ERROR
    assert result_df.loc['Total', 'forecast-Qliq-data'] == 1060, SystemMessagesErrors.RESULT_TOTAL_ERROR
    assert result_df.loc['Total', 'forecast-Qoil-data'] == 2700, SystemMessagesErrors.RESULT_TOTAL_ERROR
    assert len(result_df.columns) == 4
    assert len(result_df.index) == 11
    assert os.path.exists("./files/test_result.xlsx")
    os.remove(result_file)


