import os


def test_env_file_exists():
    assert os.path.exists("./.env")


def test_source_file_exists():
    assert os.path.exists("./files/source.xlsx")



