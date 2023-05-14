from tests.utils import parsed_df, SystemMessagesErrors
from database import SqliteDataSaver, Saver, SqliteDataGetter, DataGetter


def test_data_in_db(setup_db):
    engine = setup_db
    custom_saver = SqliteDataSaver(engine=engine)
    Saver.save(saver=custom_saver, parsed_df=parsed_df, table_name='test')
    custom_getter = SqliteDataGetter(engine=engine)
    db_data = DataGetter.get_data(getter=custom_getter, table_name='test')
    assert db_data[0] == (1, 'company1', 10, 20, 30, 40, 12, 22, 15, 25, '2023-05-01'), \
        SystemMessagesErrors.DATABASE_DATA_ERROR
    assert db_data[19] == (20, 'company2', 29, 39, 49, 59, 31, 41, 110, 120, '2023-05-10'), \
        SystemMessagesErrors.DATABASE_DATA_ERROR
