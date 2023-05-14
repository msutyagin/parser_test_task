import pytest
from tests.utils import input_df, parsed_df, SystemMessagesErrors


@pytest.mark.parametrize('cell_value, result', [
    (input_df.iloc[0][0], 'id'),
    (input_df.iloc[0][1], 'company'),
    (input_df.iloc[0][2], 'fact'),
    (input_df.iloc[0][6], 'forecast'),
    (input_df.iloc[1][2], 'Qliq'),
    (input_df.iloc[1][4], 'Qoil'),
    (input_df.iloc[1][6], 'Qliq'),
    (input_df.iloc[1][8], 'Qoil'),
    (input_df.iloc[2][2], 'data1'),
    (input_df.iloc[2][3], 'data2'),
    (input_df.iloc[2][4], 'data1'),
    (input_df.iloc[2][5], 'data2'),
    (input_df.iloc[2][6], 'data1'),
    (input_df.iloc[2][7], 'data2'),
    (input_df.iloc[2][8], 'data1'),
    (input_df.iloc[2][9], 'data2'),
])
def test_file_structure(cell_value, result):
    assert cell_value == result, SystemMessagesErrors.FILE_STRUCTURE_ERROR


@pytest.mark.parametrize('len_df, result', [
    (len(parsed_df.columns), 10),
    (len(parsed_df.index), 20)
])
def test_df_len(len_df, result):
    assert len_df == result, SystemMessagesErrors.DATAFRAME_LEN_ERROR


